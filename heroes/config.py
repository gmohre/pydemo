import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['FLASK_KEY']
    
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MARVEL_BASE_URL = "https://gateway.marvel.com"
    PRIVATE_API_KEY = os.environ['MARVEL_PRIVATE_KEY']
    PUBLIC_API_KEY = os.environ['MARVEL_PUBLIC_KEY']
    


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

configs = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY