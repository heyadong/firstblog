import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hardtoguess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


# 开发配置
class DevelopmentConfig(Config):
    DEBUG = True
    UPLOAD_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app\\static\\uploads\\')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/mytest?charset=utf8'


# 单元测试配置
class TestingConfig(Config):
    TESTING = True

    SQLAlCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')


config = {'development': DevelopmentConfig, 'testing': TestingConfig, }
