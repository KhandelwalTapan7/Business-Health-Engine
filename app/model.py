"""
Model module for health analysis, risk detection, and insight generation
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

class HealthAnalyzer:
    """Analyzes business health based on multiple metrics"""
    
    def __init__(self):
        self.health_categories = ['financial_health', 'operational_health', 
                                   'client_health', 'project_health']
        self.thresholds = {
            'profit_margin': {'warning': 0.10, 'critical': 0.05},
            'late_payment_ratio': {'warning': 0.15, 'critical': 0.25},
            'project_success_rate': {'warning': 0.70, 'critical': 0.50},
            'client_retention_rate': {'warning': 0.75, 'critical': 0.60}
        }
        
    def calculate_health_scores(self, df):
        """
        Calculate overall health scores and individual category scores
        
        Args:
            df: Processed DataFrame with business metrics
        
        Returns:
            dict: Health scores for different categories
        """
        # Get most recent data point
        if 'date' in df.columns:
            latest = df.sort_values('date', ascending=False).iloc[0]
        else:
            latest = df.iloc[-1]
        
        # Calculate individual health scores
        scores = {
            'financial_health': self._calculate_financial_health(latest),
            'operational_health': self._calculate_operational_health(latest),
            'client_health': self._calculate_client_health(latest),
            'project_health': self._calculate_project_health(latest),
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate overall health (weighted average)
        weights = {'financial_health': 0.35, 'operational_health': 0.25,
                  'client_health': 0.25, 'project_health': 0.15}
        
        scores['overall_health'] = sum(
            scores[category] * weights[category] 
            for category in self.health_categories
        )
        
        # Add health status text
        scores['health_status'] = self._get_health_status(scores['overall_health'])
        
        return scores
    
    def _calculate_financial_health(self, data):
        """Calculate financial health score (0-100)"""
        score = 70  # Base score
        
        # Profit margin contribution
        if 'profit_margin' in data and not pd.isna(data['profit_margin']):
            margin_score = min(100, data['profit_margin'] * 500)  # 20% margin = 100
            score = 0.6 * score + 0.4 * margin_score
        
        # Revenue trend contribution
        if 'revenue_mom_change' in data:
            if data['revenue_mom_change'] > 0.05:  # 5% growth
                score += 10
            elif data['revenue_mom_change'] < 0:
                score -= 15
        
        # Late payment impact
        if 'late_payment_ratio' in data:
            if data['late_payment_ratio'] > 0.2:
                score -= 20
            elif data['late_payment_ratio'] > 0.1:
                score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_operational_health(self, data):
        """Calculate operational health score (0-100)"""
        score = 75  # Base score
        
        # Project success rate
        if 'project_success_rate' in data:
            success_score = data['project_success_rate'] * 100
            score = 0.5 * score + 0.5 * success_score
        
        # Employee satisfaction
        if 'employee_satisfaction' in data:
            satisfaction_score = (data['employee_satisfaction'] / 5) * 100
            score = 0.7 * score + 0.3 * satisfaction_score
        
        # Cost efficiency
        if 'cost_per_project' in data and 'revenue_per_client' in data:
            if data['cost_per_project'] > data['revenue_per_client'] * 0.8:
                score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_client_health(self, data):
        """Calculate client health score (0-100)"""
        score = 70  # Base score
        
        # Client retention
        if 'client_retention_rate' in data:
            retention_score = data['client_retention_rate'] * 100
            score = 0.6 * score + 0.4 * retention_score
        
        # Customer satisfaction
        if 'customer_satisfaction' in data:
            csat_score = (data['customer_satisfaction'] / 5) * 100
            score = 0.5 * score + 0.5 * csat_score
        
        # New vs churned clients
        if 'new_clients' in data and 'churned_clients' in data:
            net_growth = data['new_clients'] - data['churned_clients']
            if net_growth > 2:
                score += 10
            elif net_growth < 0:
                score -= 15
        
        return max(0, min(100, score))
    
    def _calculate_project_health(self, data):
        """Calculate project health score (0-100)"""
        score = 75  # Base score
        
        # Delay impact
        if 'projects_delayed' in data and 'projects_completed' in data:
            delay_ratio = data['projects_delayed'] / (data['projects_completed'] + 1)
            if delay_ratio < 0.1:
                score += 10
            elif delay_ratio > 0.3:
                score -= 20
            elif delay_ratio > 0.2:
                score -= 10
        
        # Project volume trend
        if 'projects_completed' in data and len(data) > 1:
            if data.get('projects_completed_mom_change', 0) > 0.1:
                score += 10
        
        return max(0, min(100, score))
    
    def _get_health_status(self, score):
        """Convert numerical score to health status"""
        if score >= 80:
            return 'Excellent'
        elif score >= 60:
            return 'Good'
        elif score >= 40:
            return 'Fair'
        elif score >= 20:
            return 'Poor'
        else:
            return 'Critical'
    
    def detect_risks(self, df):
        """
        Detect various business risks from the data
        
        Args:
            df: Processed DataFrame
        
        Returns:
            list: Detected risks with severity and description
        """
        risks = []
        
        # Get latest data point
        if 'date' in df.columns:
            latest = df.sort_values('date', ascending=False).iloc[0]
        else:
            latest = df.iloc[-1]
        
        # Financial risks
        if 'profit_margin' in latest:
            if latest['profit_margin'] < self.thresholds['profit_margin']['critical']:
                risks.append({
                    'category': 'financial',
                    'severity': 'high',
                    'title': 'Critical Profit Margin',
                    'description': f"Profit margin is critically low at {latest['profit_margin']:.1%}",
                    'recommendation': 'Review pricing strategy and reduce unnecessary expenses'
                })
            elif latest['profit_margin'] < self.thresholds['profit_margin']['warning']:
                risks.append({
                    'category': 'financial',
                    'severity': 'medium',
                    'title': 'Low Profit Margin',
                    'description': f"Profit margin is below target at {latest['profit_margin']:.1%}",
                    'recommendation': 'Monitor expenses and consider price adjustments'
                })
        
        # Cash flow risks
        if 'late_payment_ratio' in latest:
            if latest['late_payment_ratio'] > self.thresholds['late_payment_ratio']['critical']:
                risks.append({
                    'category': 'financial',
                    'severity': 'high',
                    'title': 'Severe Late Payment Issue',
                    'description': f"{latest['late_payment_ratio']:.1%} of payments are late",
                    'recommendation': 'Implement stricter payment terms and follow-up process'
                })
            elif latest['late_payment_ratio'] > self.thresholds['late_payment_ratio']['warning']:
                risks.append({
                    'category': 'financial',
                    'severity': 'medium',
                    'title': 'Late Payment Concerns',
                    'description': f"{latest['late_payment_ratio']:.1%} of payments are late",
                    'recommendation': 'Send reminders and review client payment behavior'
                })
        
        # Operational risks
        if 'project_success_rate' in latest:
            if latest['project_success_rate'] < self.thresholds['project_success_rate']['critical']:
                risks.append({
                    'category': 'operational',
                    'severity': 'high',
                    'title': 'Project Success Crisis',
                    'description': f"Only {latest['project_success_rate']:.1%} of projects are on time",
                    'recommendation': 'Audit project management processes and resource allocation'
                })
            elif latest['project_success_rate'] < self.thresholds['project_success_rate']['warning']:
                risks.append({
                    'category': 'operational',
                    'severity': 'medium',
                    'title': 'Project Delays Increasing',
                    'description': f"{latest['project_success_rate']:.1%} of projects are on time",
                    'recommendation': 'Review project timelines and resource planning'
                })
        
        # Client risks
        if 'client_retention_rate' in latest:
            if latest['client_retention_rate'] < self.thresholds['client_retention_rate']['critical']:
                risks.append({
                    'category': 'client',
                    'severity': 'high',
                    'title': 'Client Churn Crisis',
                    'description': f"Client retention rate is critically low at {latest['client_retention_rate']:.1%}",
                    'recommendation': 'Conduct exit interviews and improve client service'
                })
            elif latest['client_retention_rate'] < self.thresholds['client_retention_rate']['warning']:
                risks.append({
                    'category': 'client',
                    'severity': 'medium',
                    'title': 'Client Retention Warning',
                    'description': f"Client retention rate is {latest['client_retention_rate']:.1%}",
                    'recommendation': 'Reach out to at-risk clients and address concerns'
                })
        
        # Check for negative trends
        if len(df) >= 3:
            recent_profit = df['profit'].tail(3).values
            if all(recent_profit[i] < recent_profit[i-1] for i in range(1, 3)):
                risks.append({
                    'category': 'financial',
                    'severity': 'medium',
                    'title': 'Declining Profit Trend',
                    'description': 'Profit has decreased for 3 consecutive periods',
                    'recommendation': 'Analyze cost structure and revenue sources'
                })
        
        return risks

class InsightGenerator:
    """Generates plain-language insights from business data"""
    
    def __init__(self):
        self.insight_templates = {
            'positive': [
                "Great news! Your {metric} has improved by {change:.1f}% compared to last period.",
                "You're doing well in {area}. {metric} is {value} which is above industry average.",
                "Your business is showing strong {metric} performance. Keep up the good work!"
            ],
            'warning': [
                "Warning: {metric} has decreased. This could impact your {impact_area} if not addressed.",
                "Keep an eye on {metric}. It's showing signs of {trend}.",
                "There's room for improvement in {area}. Current {metric} is below target."
            ],
            'action': [
                "Consider {action} to improve your {metric}. This could increase {benefit}.",
                "Based on your data, focusing on {focus_area} could help address {issue}.",
                "We recommend {recommendation} to optimize your business performance."
            ]
        }
        
    def generate_insights(self, df, health_scores, risks):
        """
        Generate comprehensive insights based on data analysis
        
        Args:
            df: Processed DataFrame
            health_scores: Health scores dictionary
            risks: Detected risks list
        
        Returns:
            dict: Organized insights by category
        """
        insights = {
            'summary': [],
            'warnings': [],
            'opportunities': [],
            'recommendations': []
        }
        
        # Generate summary insights
        insights['summary'].append({
            'type': 'summary',
            'message': f"Overall business health is {health_scores['health_status'].lower()} "
                      f"with a score of {health_scores['overall_health']:.1f}/100"
        })
        
        # Convert risks to insights
        for risk in risks:
            if risk['severity'] == 'high':
                insights['warnings'].append({
                    'type': 'warning',
                    'severity': 'high',
                    'message': risk['description'],
                    'recommendation': risk['recommendation']
                })
            else:
                insights['opportunities'].append({
                    'type': 'opportunity',
                    'severity': risk['severity'],
                    'message': risk['description'],
                    'recommendation': risk['recommendation']
                })
        
        # Generate trend-based insights
        if len(df) >= 2:
            trend_insights = self._analyze_trends(df)
            insights['opportunities'].extend(trend_insights['opportunities'])
            insights['recommendations'].extend(trend_insights['recommendations'])
        
        # Generate area-specific insights
        area_insights = self._analyze_business_areas(df, health_scores)
        for key in insights:
            if key in area_insights:
                insights[key].extend(area_insights[key])
        
        return insights
    
    def _analyze_trends(self, df):
        """Analyze trends in the data"""
        insights = {'opportunities': [], 'recommendations': []}
        
        # Sort by date
        if 'date' in df.columns:
            df = df.sort_values('date')
        
        # Check revenue trend
        if 'revenue' in df.columns and len(df) >= 3:
            recent_revenue = df['revenue'].tail(3).values
            if recent_revenue[-1] > recent_revenue[0] * 1.1:
                insights['opportunities'].append({
                    'type': 'opportunity',
                    'message': f"Revenue has grown by {((recent_revenue[-1]/recent_revenue[0])-1)*100:.1f}% "
                              "over the last 3 periods. This strong growth could be leveraged for expansion.",
                    'recommendation': "Consider reinvesting some profits into marketing or new hires."
                })
        
        # Check profit margin trend
        if 'profit_margin' in df.columns and len(df) >= 3:
            recent_margins = df['profit_margin'].tail(3).values
            if recent_margins[-1] < recent_margins[0] * 0.9:
                insights['recommendations'].append({
                    'type': 'recommendation',
                    'message': "Profit margins are declining despite revenue trends. "
                              "This suggests rising costs.",
                    'recommendation': "Review supplier contracts and operational expenses."
                })
        
        return insights
    
    def _analyze_business_areas(self, df, health_scores):
        """Generate insights for specific business areas"""
        insights = {'opportunities': [], 'recommendations': []}
        
        latest = df.iloc[-1] if len(df) > 0 else None
        
        if latest is not None:
            # Financial insights
            if health_scores['financial_health'] < 50:
                insights['recommendations'].append({
                    'type': 'recommendation',
                    'message': "Financial health needs immediate attention.",
                    'recommendation': "Schedule a financial review meeting and consider consulting "
                                     "with an accountant to identify improvement areas."
                })
            
            # Client insights
            if health_scores['client_health'] > 80:
                insights['opportunities'].append({
                    'type': 'opportunity',
                    'message': "Your client relationships are strong! This is a great foundation "
                              "for growth.",
                    'recommendation': "Consider implementing a referral program to leverage "
                                     "your happy clients for new business."
                })
            
            # Operational insights
            if health_scores['operational_health'] < 60:
                if 'employee_satisfaction' in latest:
                    if latest['employee_satisfaction'] < 3.5:
                        insights['recommendations'].append({
                            'type': 'recommendation',
                            'message': "Low employee satisfaction may be impacting operations.",
                            'recommendation': "Conduct anonymous employee surveys to identify "
                                             "and address workplace issues."
                        })
        
        return insights