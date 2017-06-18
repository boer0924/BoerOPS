import os
bashdir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(bashdir, 'BoerOPS.db')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/boerops_dev'

class ProductionConfig(Config):
    pass

config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,

    'default': DevelopmentConfig
}
