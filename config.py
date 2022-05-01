import secrets
import os

class Config(object):
    DEBUG = False
    TESTING = False
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_urlsafe(255)
    SESSION_COOKIE_SECURE = True
    MAIL_SERVER = os.environ.get("MAIL_SERVER", 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SENDER = os.environ.get("MAIL_SENDER", "pepelope8@gmail.com")
    SECURITY_PASSWORD_SALT="verify"

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = ""
    DB_NAME = ""
    DB_USER = ""
    DB_PASSWORD = ""
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    SESSION_COOKIE_SECURE = False


config = {
    'development':DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}