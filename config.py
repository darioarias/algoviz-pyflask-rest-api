import secrets


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = ""

    DB_NAME = ""
    DB_USERNAME = ""
    DB_PASSWORD = ""
    SECRET_KEY = secrets.token_urlsafe(255)
    SESSION_COOKIE_SECURE = True

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_NAME = "development-db"
    DB_USERNAME = "ozsljqnrzlxusl"
    DB_PASSWORD = "3c4ae5859f9232b04752fc4cad2cc73052a9762c94cb8ecb5f6a1ef67a5045d4"
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    DB_NAME = "development-db"
    DB_USERNAME = "admin"
    DB_PASSWORD = "example"
    SESSION_COOKIE_SECURE = False


config = {
  'testing': TestingConfig,
  'production': ProductionConfig,
  'default': DevelopmentConfig,
}