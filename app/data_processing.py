"""
Data processing module for loading, cleaning, and transforming business data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataLoader:
    """Handles loading of business data from various sources"""
    
    def __init__(self):
        self.sample_data_path = None
        
    def load_sample_data(self):
        """
        Generate sample SME business data for demonstration
        Returns a DataFrame with realistic business metrics
        """
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate date range for the last 12 months
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
        
        # Create sample data
        data = {
            'date': dates,
            'revenue': np.random.normal(50000, 10000, len(dates)),
            'expenses': np.random.normal(35000, 8000, len(dates)),
            'profit': np.random.normal(15000, 5000, len(dates)),
            'projects_completed': np.random.randint(5, 15, len(dates)),
            'projects_delayed': np.random.randint(0, 5, len(dates)),
            'new_clients': np.random.randint(2, 8, len(dates)),
            'churned_clients': np.random.randint(0, 3, len(dates)),
            'late_payments': np.random.randint(0, 10, len(dates)),
            'outstanding_invoices': np.random.normal(25000, 5000, len(dates)),
            'employee_satisfaction': np.random.uniform(3, 5, len(dates)),
            'customer_satisfaction': np.random.uniform(3.5, 5, len(dates))
        }
        
        df = pd.DataFrame(data)
        
        # Add some realistic trends and patterns
        df['revenue'] = df['revenue'] * (1 + np.linspace(0, 0.2, len(dates)))  # Growth trend
        df['profit'] = df['revenue'] - df['expenses']
        
        # Ensure non-negative values
        df['profit'] = df['profit'].clip(lower=0)
        df['outstanding_invoices'] = df['outstanding_invoices'].clip(lower=0)
        
        return df
    
    def load_custom_data(self, file_path):
        """
        Load custom CSV data uploaded by user
        
        Args:
            file_path: Path to CSV file or file object
        
        Returns:
            pandas.DataFrame: Loaded data
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise Exception(f"Error loading custom data: {str(e)}")

class DataProcessor:
    """Handles data cleaning, transformation, and feature engineering"""
    
    def __init__(self):
        self.required_columns = ['date', 'revenue', 'expenses', 'profit']
        
    def process_data(self, df):
        """
        Main data processing pipeline
        
        Args:
            df: Raw DataFrame
        
        Returns:
            processed_df: Cleaned and enriched DataFrame
        """
        # Make a copy to avoid modifying original
        processed_df = df.copy()
        
        # Handle missing values
        processed_df = self._handle_missing_values(processed_df)
        
        # Convert date column if present
        if 'date' in processed_df.columns:
            processed_df['date'] = pd.to_datetime(processed_df['date'])
        
        # Calculate derived metrics
        processed_df = self._calculate_derived_metrics(processed_df)
        
        # Add rolling averages for trend detection
        processed_df = self._add_rolling_metrics(processed_df)
        
        # Categorize data points
        processed_df = self._categorize_metrics(processed_df)
        
        return processed_df
    
    def _handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        # Forward fill for time-series data
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        # If still missing, fill with median for numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].median())
        
        return df
    
    def _calculate_derived_metrics(self, df):
        """Calculate additional business metrics from raw data"""
        
        # Profit margin
        if 'revenue' in df.columns and 'profit' in df.columns:
            df['profit_margin'] = (df['profit'] / df['revenue']).clip(upper=1)
        
        # Project success rate
        if 'projects_completed' in df.columns and 'projects_delayed' in df.columns:
            total_projects = df['projects_completed'] + df['projects_delayed']
            df['project_success_rate'] = df['projects_completed'] / total_projects
            df['project_success_rate'] = df['project_success_rate'].fillna(1)
        
        # Client retention rate
        if 'new_clients' in df.columns and 'churned_clients' in df.columns:
            df['client_retention_rate'] = 1 - (df['churned_clients'] / 
                                               (df['new_clients'] + df['churned_clients'] + 1))
        
        # Late payment ratio
        if 'late_payments' in df.columns and 'projects_completed' in df.columns:
            df['late_payment_ratio'] = df['late_payments'] / (df['projects_completed'] + 1)
        
        # Cost per project
        if 'expenses' in df.columns and 'projects_completed' in df.columns:
            df['cost_per_project'] = df['expenses'] / (df['projects_completed'] + 1)
        
        # Revenue per client
        if 'revenue' in df.columns and 'new_clients' in df.columns:
            df['revenue_per_client'] = df['revenue'] / (df['new_clients'] + 5)  # Assuming existing clients
        
        return df
    
    def _add_rolling_metrics(self, df):
        """Add rolling averages for trend analysis"""
        
        # Sort by date if available
        if 'date' in df.columns:
            df = df.sort_values('date')
        
        # 3-month rolling averages for key metrics
        for col in ['revenue', 'profit', 'profit_margin', 'project_success_rate']:
            if col in df.columns:
                df[f'{col}_rolling_3m'] = df[col].rolling(window=3, min_periods=1).mean()
        
        # Month-over-month change
        for col in ['revenue', 'profit', 'expenses']:
            if col in df.columns:
                df[f'{col}_mom_change'] = df[col].pct_change()
        
        return df
    
    def _categorize_metrics(self, df):
        """Categorize metrics into health status categories"""
        
        # Profit margin categories
        if 'profit_margin' in df.columns:
            df['profit_margin_category'] = pd.cut(
                df['profit_margin'],
                bins=[0, 0.05, 0.10, 0.15, 1],
                labels=['Critical', 'Warning', 'Good', 'Excellent']
            )
        
        # Late payment categories
        if 'late_payment_ratio' in df.columns:
            df['late_payment_category'] = pd.cut(
                df['late_payment_ratio'],
                bins=[0, 0.1, 0.2, 0.3, 1],
                labels=['Good', 'Warning', 'Critical', 'Severe']
            )
        
        return df
    
    def get_recent_metrics(self, df, periods=6):
        """Get most recent metrics for dashboard display"""
        if 'date' in df.columns:
            df = df.sort_values('date', ascending=False)
        return df.head(periods).to_dict('records')