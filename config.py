# config.py
import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')  # Default to 'localhost' if not set
    MYSQL_USER = os.getenv('MYSQL_USER', 'annlita')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'aadannia@DB')
    MYSQL_DB = os.getenv('MYSQL_DB', 'NetGuardDB')
