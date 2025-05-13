import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ctf.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configurations
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = os.environ.get('REMEMBER_COOKIE_SECURE', 'False').lower() == 'true'
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'ctf.log')
    
    # Flag hashes - in a real-world scenario, these would be in a database
    FLAG_HASHES = {
        'flag1': '5f4dcc3b5aa765d61d8327deb882cf99',  # md5 hash of 'password'
        'flag2': '098f6bcd4621d373cade4e832627b4f6',  # md5 hash of 'test'
        'flag3': '1a1dc91c907325c69271ddf0c944bc72',  # md5 hash of 'pass'
        'flag4': 'c21f969b5f03d33d43e04f8f136e7682',  # md5 hash of 'default'
        'flag5': '5ebe2294ecd0e0f08eab7690d2a6ee69',  # md5 hash of 'secret'
        'flag6': '7110eda4d09e062aa5e4a390b0a572ac',  # md5 hash of '1234'
        'flag7': 'e10adc3949ba59abbe56e057f20f883e',  # md5 hash of '123456'
        'flag8': '25f9e794323b453885f5181f1b624d0b',  # md5 hash of '123456789'
        'flag9': '5d41402abc4b2a76b9719d911017c592',  # md5 hash of 'hello'
        'flag10': 'e99a18c428cb38d5f260853678922e03'  # md5 hash of 'abc123'
    }
    
    # Challenge configuration
    MAX_LOGIN_ATTEMPTS = 5
    
    # Discord community link
    DISCORD_LINK = "https://discord.gg/vuqfzVkzRe"
    
    # Club and author info
    CLUB_NAME = "CyberSentinels"
    AUTHOR_NAME = "Sujal Adhikari"