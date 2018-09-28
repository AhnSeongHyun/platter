
class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_MAX_OVERFLOW = -1
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_RECYCLE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    AES256_KEY = "X" * 32
    AES256_IV = "X" * 16


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{{db_user}}:{{db_password}}@{{db_host}}/{{db_scheme}}'
    SENTRY_DSN = ''


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{{db_user}}:{{db_password}}@{{db_host}}/{{db_scheme}}'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{{db_user}}:{{db_password}}@{{db_host}}/{{db_scheme}}'
