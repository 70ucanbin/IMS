class Config(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@172.22.13.194/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # app configuration
    DEBUG = True
    SECRET_KEY = 'secret key'
    USERNAME = 'yo'
    PASSWORD = 'yoyoyo'