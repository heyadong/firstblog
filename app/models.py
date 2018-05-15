# encoding: utf-8
from app import app
from datetime import datetime
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


"""数据库初始化"""


class Safe(db.Model):
    __tablename__ = 'safe'
    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(64), unique=True)
    main_num = db.Column(db.String(64), unique=True)
    sec_num = db.Column(db.String(64), unique=True)
    control_num = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Safe %r>' % self.order_num


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    tel = db.Column(db.String(11),nullable=False)
    password1 = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return '<%r>' % self.username

    def check_password(self, pw):
        return check_password_hash(self.password1,pw)


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article = db.relationship('Users',backref=db.backref('article'))


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    comment_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    article = db.relationship('Articles',backref=db.backref('comment'))


class Photos(db.Model):
    __tablename__ = "photos"
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))  # 定义外键引用关系
    photo_name = db.Column(db.String(200),nullable=False)
    create_time = db.Column(db.DateTime(),default=datetime.now())
    db.relationship('User',backref=db.backref('photos'))  # 添加lazy='dynamic'，调用引用查询（返回Users.photosjian是

#    定义引用关系，不用重复查询数据库：
#    在Comments 表中定义 article = db.relationship('Articles',backref = db.backref('comment'))
#    可以通过my_articles.comment 访问 Comments 模型
#    也可以通过my_comments.artile 访问 Article 模型
#    default 设值该列的默认值，datatime.now()返回当前时间
