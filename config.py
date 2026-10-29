"""
Configuration settings for Timesheet Validator application
"""
import os

class Config:
    """Application configuration"""
    
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
    RULES_FOLDER = os.path.join(BASE_DIR, 'rules')
    
    # File size limit (100MB)
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(Config.RULES_FOLDER, exist_ok=True)

# Made with Bob
