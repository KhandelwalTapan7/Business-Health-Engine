"""
Data processing module for loading, cleaning, and transforming business data
"""

import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading of business data from various sources"""
    
    def __init__(self):
        self.required_columns = ['date', 'revenue', 'expenses', 'profit']
    
    def load_sample_data(self):
        """
        Generate sample SME business data for demonstration
        Returns a DataFrame with realistic business metrics
        """
        try:
            # Set random seed for reproducibility
            np.random.seed(42)

            # Generate date range for the last 12 months
            # Use 'ME' for pandas >=2.2, fallback to 'M' for older versions
            try:
                dates = pd.date_range(
                    start="2023-01-01",
                    end="2023-12-31",
                    freq="ME"
                )
            except Exception:
                dates = pd.date_range(
                    start="2023-01-01",
                    end="2023-12-31",
                    freq="M"
                )

            # Create sample data with realistic business metrics
            data = {
                "date": dates,
                "revenue": np.random.normal(50000, 10000, len(dates)),
                "expenses": np.random.normal(35000, 8000, len(dates)),
                "profit": np.random.normal(15000, 5000, len(dates)),
                "projects_completed": np.random.randint(5, 15, len(dates)),
                "projects_delayed": np.random.randint(0, 5, len(dates)),
                "new_clients": np.random.randint(2, 8, len(dates)),
                "churned_clients": np.random.randint(0, 3, len(dates)),
                "late_payments": np.random.randint(0, 10, len(dates)),
                "outstanding_invoices": np.random.normal(25000, 5000, len(dates)),
                "employee_satisfaction": np.random.uniform(3, 5, len(dates)),
                "customer_satisfaction": np.random.uniform(3.5, 5, len(dates)),
            }

            df = pd.DataFrame(data)

            # Add realistic trends and patterns
            df = self._add_sample_trends(df)

            # Ensure data quality
            df["profit"] = df["profit"].clip(lower=0)
            df["outstanding_invoices"] = df["outstanding_invoices"].clip(lower=0)

            logger.info(f"Sample data generated successfully: {len(df)} rows")
            return df

        except Exception as e:
            logger.error(f"Error generating sample data: {str(e)}")
            return self._fallback_data()
    
    def _add_sample_trends(self, df):
        """Add realistic trends to sample data"""
        # Revenue growth trend (increasing over time)
        growth_factor = 1 + np.linspace(0, 0.2, len(df))
        df["revenue"] *= growth_factor

        # Seasonal pattern - higher in Q4 (last 3 months)
        seasonal_factor = np.ones(len(df))
        seasonal_factor[-3:] = 1.1  # Last 3 months get 10% boost
        df["revenue"] *= seasonal_factor

        # Recalculate profit
        df["profit"] = df["revenue"] - df["expenses"]
        
        return df

    def _fallback_data(self):
        """Generate simple fallback data if main generation fails"""
        logger.info("Using fallback data generation")
        dates = pd.date_range(start="2023-01-01", periods=12, freq="ME")

        return pd.DataFrame({
            "date": dates,
            "revenue": np.linspace(50000, 80000, 12),
            "expenses": np.linspace(35000, 52000, 12),
            "profit": np.linspace(15000, 28000, 12),
            "projects_completed": np.random.randint(5, 15, 12),
            "projects_delayed": np.random.randint(0, 5, 12),
            "new_clients": np.random.randint(2, 8, 12),
            "churned_clients": np.random.randint(0, 3, 12),
            "late_payments": np.random.randint(0, 10, 12),
            "outstanding_invoices": np.linspace(23000, 45000, 12),
            "employee_satisfaction": np.random.uniform(3, 5, 12),
            "customer_satisfaction": np.random.uniform(3.5, 5, 12),
        })

    def load_custom_data(self, file):
        """
        Load custom CSV data uploaded by user
        
        Args:
            file: File object from Flask request
        
        Returns:
            pandas.DataFrame: Loaded data
        """
        try:
            df = pd.read_csv(file)
            logger.info(f"Custom data loaded successfully: {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Error loading custom data: {str(e)}")
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
        df = df.copy()

        # Process dates
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors='coerce')
            df = df.sort_values("date")

        # Handle missing values
        df = self._handle_missing_values(df)

        # Calculate derived metrics
        df = self._calculate_derived_metrics(df)

        # Add rolling averages for trend detection
        df = self._add_rolling_metrics(df)

        logger.info(f"Data processed successfully: {len(df)} rows, {len(df.columns)} columns")
        return df
    
    def _handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        # Forward fill then backward fill for time-series data
        df = df.fillna(method="ffill").fillna(method="bfill")

        # Fill any remaining missing values with median for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isnull().any():
                df[col] = df[col].fillna(df[col].median())

        return df
    
    def _calculate_derived_metrics(self, df):
        """Calculate additional business metrics from raw data"""
        
        # Profit margin
        if "revenue" in df.columns and "profit" in df.columns:
            # Avoid division by zero
            revenue_safe = df["revenue"].replace(0, np.nan)
            df["profit_margin"] = (df["profit"] / revenue_safe).clip(upper=1)
            df["profit_margin"] = df["profit_margin"].fillna(0)

        # Project success rate
        if "projects_completed" in df.columns and "projects_delayed" in df.columns:
            total = df["projects_completed"] + df["projects_delayed"]
            # Avoid division by zero
            total_safe = total.replace(0, 1)
            df["project_success_rate"] = df["projects_completed"] / total_safe
            df["project_success_rate"] = df["project_success_rate"].clip(upper=1)

        # Client retention rate
        if "new_clients" in df.columns and "churned_clients" in df.columns:
            total_clients = df["new_clients"] + df["churned_clients"].abs()
            df["client_retention_rate"] = 1 - (
                df["churned_clients"].abs() / (total_clients + 1)
            )
            df["client_retention_rate"] = df["client_retention_rate"].clip(0, 1)

        # Late payment ratio
        if "late_payments" in df.columns and "projects_completed" in df.columns:
            projects_safe = df["projects_completed"].replace(0, 1)
            df["late_payment_ratio"] = df["late_payments"] / projects_safe
            df["late_payment_ratio"] = df["late_payment_ratio"].clip(upper=1)

        return df
    
    def _add_rolling_metrics(self, df):
        """Add rolling averages for trend analysis"""
        
        # Only add rolling metrics if we have enough data
        if len(df) >= 3:
            for col in ["revenue", "profit", "profit_margin"]:
                if col in df.columns:
                    df[f"{col}_rolling_3m"] = df[col].rolling(
                        window=3,
                        min_periods=1
                    ).mean()

        return df
    
    def get_recent_metrics(self, df, periods=6):
        """
        Get most recent metrics for dashboard display
        
        Args:
            df: Processed DataFrame
            periods: Number of periods to return
        
        Returns:
            list: List of dictionaries with recent metrics
        """
        if df is None or df.empty:
            return []

        # Sort by date if available
        if "date" in df.columns:
            df = df.sort_values("date", ascending=False)

        # Get recent records
        records = df.head(periods).to_dict(orient="records")

        # Convert Timestamp objects to string format for JSON serialization
        for record in records:
            if "date" in record:
                if hasattr(record["date"], "strftime"):
                    record["date"] = record["date"].strftime("%Y-%m-%d")
                elif isinstance(record["date"], pd.Timestamp):
                    record["date"] = record["date"].strftime("%Y-%m-%d")
                
            # Round numeric values for cleaner display
            for key, value in record.items():
                if isinstance(value, float):
                    record[key] = round(value, 3)

        return records
    
    def get_data_summary(self, df):
        """
        Generate summary statistics for the dataset
        
        Args:
            df: Processed DataFrame
        
        Returns:
            dict: Summary statistics
        """
        summary = {
            'total_rows': len(df),
            'columns': list(df.columns),
            'date_range': {},
            'averages': {},
            'totals': {}
        }
        
        # Date range
        if 'date' in df.columns and len(df) > 0:
            summary['date_range']['start'] = df['date'].min()
            summary['date_range']['end'] = df['date'].max()
        
        # Key averages
        avg_metrics = ['revenue', 'profit', 'profit_margin', 'project_success_rate']
        for metric in avg_metrics:
            if metric in df.columns:
                summary['averages'][metric] = round(df[metric].mean(), 2)
        
        # Key totals
        total_metrics = ['revenue', 'profit', 'projects_completed', 'new_clients']
        for metric in total_metrics:
            if metric in df.columns:
                summary['totals'][metric] = round(df[metric].sum(), 2)
        
        return summary