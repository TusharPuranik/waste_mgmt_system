import os

class Config:
    # Secret key for form & session security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'replace-with-a-secure-key'
    
    # Database: using SQLite for now
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///waste_mgmt.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
