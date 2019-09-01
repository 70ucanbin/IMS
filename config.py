class Config(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://test:test@192.168.1.7/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = 'secret key'
    USERNAME = 'yo'
    PASSWORD = 'yoyoyo'