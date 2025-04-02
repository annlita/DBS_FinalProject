import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST')  # No default to prevent leaks
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = os.getenv('MYSQL_DB')
