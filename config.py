import os


class Config(object):
    SECRET_KEY = "ohflkfjenfoiehfoiwehjpj"
    UPLOADED_PHOTOS_DEST = '/var/www/tour/build/static/image/find'  # 文件储存地址
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}