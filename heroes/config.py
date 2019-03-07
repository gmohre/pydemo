import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'heroesandvillains'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MARVEL_BASE_URL = "https://gateway.marvel.com"
    PRIVATE_API_KEY = "82792e50dbaaac893d8f71991715f346542ef02c"
    PUBLIC_API_KEY = "cb70ad466366b1ddfdbdf18bda853d8a"


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