class AppConfig(object):
    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # app configuration
    DEBUG = True
    SECRET_KEY = 'secret key' #絶対にこのdefalut値を使わないでください。