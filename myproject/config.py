from os import environ as env

IMAGES_FOLDER = 'app/static/images'
IMAGES_DEFAULT_NAME = 'default.jpg'

class Config:
    TESTING = False
    DEVELOPMENT = False
    FLASK_DEBUG = False
    APP_SECRET_KEY = b"pleasedosha512fiwkeokweowoefkm3r8j"
    IMAGES_FOLDER = IMAGES_FOLDER
    IMAGES_DEFAULT_NAME = IMAGES_DEFAULT_NAME
    POST_PAGINATION_SIZE = 2

    def get_secret_key(self):
        return self.APP_SECRET_KEY

    @staticmethod
    def get_profile():
        config = {
            DevProfile.ENV_NAME: DevProfile(),
            TestProfile.ENV_NAME: TestProfile(),
            ProdProfile.ENV_NAME: ProdProfile()
        }
        default_config = 'development'
        return config.get(env.get('APP_CONFIG') or default_config)


class DevProfile(Config):
    DEVELOPMENT = True
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    ENV_NAME = 'development'


class TestProfile(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    ENV_NAME = 'test'
    DEBUG = True


class ProdProfile(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' 
    ENV_NAME = 'prod'