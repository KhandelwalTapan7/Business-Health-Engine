import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Data settings
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    SAMPLE_DATA_FILE = os.path.join(DATA_DIR, 'sample_data.csv')
    
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    TESTING = False
    
    # Health metrics thresholds
    HEALTH_THRESHOLDS = {
        'profit_margin_warning': 0.10,  # 10% profit margin warning
        'profit_margin_critical': 0.05,   # 5% profit margin critical
        'late_payment_days_warning': 15,
        'late_payment_days_critical': 30,
        'project_delay_days_warning': 5,
        'project_delay_days_critical': 10,
        'client_concentration_warning': 0.30,  # 30% revenue from one client
        'client_concentration_critical': 0.50,  # 50% revenue from one client
    }
    
    # Risk scoring weights
    RISK_WEIGHTS = {
        'financial_risk': 0.35,
        'operational_risk': 0.30,
        'client_risk': 0.25,
        'project_risk': 0.10
    }
    
    # Cache settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}