import os
from flask import Flask

# # 使用工厂模式创建app
# db = SQLAlchemy()
# def create_app(config_name):
#     app = Flask(__name__)
#     app.config.from_object(config[config_name])
#     config[config_name].init_app(app)
#     db.init_app(app)
#
#     # 错误路由定义
#     from app.blog import blog as blog_blueprint
#     app.register_blueprint(blog_blueprint)
#     return app



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/mytest?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config["UPLOAD_FILE"] = os.path.join(os.path.abspath(os.path.dirname(__file__)),'static\\uploads\\')
app.config['SECRET_KEY'] = 'hardtoguss'
app.config['WTF_CSRF_ENABLED'] = False  # 测试禁用
app.debug = True
from app.blog import blog as blog_blueprint   # 导入蓝图
app.register_blueprint(blog_blueprint)




