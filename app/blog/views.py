from ..blog import blog
from flask import render_template, request, session, redirect, jsonify, url_for, flash, send_from_directory,g
from app.models import Articles, Users, Photos
from app.models import db
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from .forms import UploadForm, RegistForm,LoginForm
from app import app
import os
import stat
from functools import wraps

@blog.before_request
def my_before_request():
    user = Users.query.filter_by(id=session.get('user_id')).first()
    g.user = user

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = g.user
        return {'user': user}
    else:
        return {}
#
# 登陆限制
def login_requird(func):
    @wraps(func)
    def warp(*args,**kwargs):
        if g.user is None:
            return redirect(url_for('blog.login'))
        return func(*args,**kwargs)
    return warp



@blog.route('/', methods=["GET", ])
@blog.route('/<int:page>')
def index(page=None):
    if page is None:
        page = 1
    articles = Articles.query.order_by(
        Articles.create_time.desc()
    ).paginate(
        page=page,
        per_page=2
    )
    return render_template('index.html', questions=articles)


# ajax_demo
@blog.route('/add', methods=["GET", 'POST'])
def add():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@blog.route('/ajax_demo')
def demo():
    return render_template('ajax_demo.html')


#  相册列表异步加载
@blog.route('/pics', methods=["GET", "POST"])
def get_pic():
    pics_dict = list()
    count = request.args.get('count', 0, type=int)
    page_nums = 2  # 每次点击异步加载数量，可以用次方法进行分页
    pics = Photos.query.all()[page_nums * (count - 1) + 5:page_nums * (count - 1) + 7]
    for pic in pics:
        a = dict(id=pic.id, photo_name=pic.photo_name)
        pics_dict.append(a)
    return jsonify(pics_dict)


# @blog.route('/')
# def index():
#     page_id = 1
#     page_id = request.args.get('page_id')
#     if session.get('user_id'):
#         users = g.user
#         content = {
#             'questions': users.article,
#             'author': users
#         }
#         return render_template('index.html', **content)
#     else:
#         articles = Articles.query.all()
#         article_num = len(articles)
#         page = int(article_num/5)
#         if page >= 1 and article_num % 5 == 0:
#             pages = page
#         elif page >= 1 and article_num % 5 != 0:
#             pages = page+1
#         else:
#             pages = 1
#         pages_list = range(1, pages+1)
#         page_id = request.args.get('page_id')
#         if page_id:
#             page_slice = slice(0+5*(int(page_id)-1), 5+5*(int(page_id)-1))
#             questions = articles[page_slice]
#         else:
#             questions = articles[slice(0,5)]
#         content = {
#                 'questions': questions,
#                 'article_nums': article_num,
#                 'pages_list': pages_list,
#             }
#         return render_template('index.html', **content)
#
#



#
# 登陆页面视图函数
@blog.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        # 手机号已经放在表单进行验证
        # if Users.query.filter_by(tel=data['tel']).count() == 0:
        #     flash("你输入的手机号不存在")
        user = Users.query.filter_by(tel=data['tel']).first()
        if user.check_password(data['pw']):
            session['user_id'] = user.id
            return redirect(url_for('blog.index'))
        flash('输入密码错误', 'err')
    return render_template('login2.html',form=form)


    # if request.method == 'GET':
    #     return render_template('login2.html')
    # else:
    #     tellphone = request.form.get('tel')
    #     print(tellphone)
    #     password1 = request.form.get('password1')
    #     print(password1)
    #     password = generate_password_hash(password1)
    #     print(password)
    #     user = Users.query.filter_by(tel=tellphone, password1=password).first()
    #     print(user)
    #     if user:
    #         session['user_id'] = user.id
    #         return redirect(url_for('blog.index'))
    #     else:
    #         return "登陆用户或者密码输入错误，请重新输入"

# 注册视图函数
@blog.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        password = generate_password_hash(data['pw1'])
        print(password)
        user = Users(username=data['username'], tel=data['tel'], password1=password, email=data['email'])
        try:
            db.session.add(user)
            db.session.commit()
            flash('注册成功，请登陆','ok')
        except:
            flash('未知错误，注册未成功', 'err')
            return redirect('blog.register')
        return redirect(url_for('blog.login'))
    return render_template('register.html',form=form)



    # if request.method == 'GET':
    #     return render_template('register.html')
    # else:
    #     name = request.form.get('username')
    #     email = request.form.get('email')
    #     password1 = generate_password_hash(request.form.get('password1'))
    #     tel = request.form.get('tel')
    #     user = Users(username=name, tel=tel, password1=password1)
    #     db.session.add(user)
    #     db.session.commit()
    #     return '注册成功'
#
# # 查询页面
# @blog.route('/my_blog/')
# def my_blog():
#     q = request.args.get('q')
#     # articles = Articles.query.filter(Articles.title.ilike('%{}%'.format(q)))
#     articles = Articles.query.filter(or_(Articles.content.contains(q),
#                                          Articles.title.contains(q)))
#     content = {
#         'questions': articles
#     }
#     return render_template('index.html', **content)
#
#
# # 钩子函数（hook) context_processor 装饰器，返回字典，所有页面都可用
# @app.before_request
# def my_before_request():
#     user_id = session.get('user_id')
#     user = Users.query.filter_by(id=user_id).first()
#     g.user = user
#
#
#

#



# 文章发布视图函数
@blog.route('/article/', methods=['GET', 'POST'])
@login_requird
def article():
    if request.method == 'GET':
        return render_template('article.html')
    else:
        a_id = session.get('user_id')
        a_title = request.form.get('theme')
        a_content = request.form.get('content')
        articles = Articles(author_id=a_id, title=a_title, content=a_content)
        db.session.add(articles)
        db.session.commit()
        return '发布成功'


# 注销
@blog.route('/login_out/')
def login_out():
    # session.pop('user_id')
    del session['user_id']
    session.clear()
    print(session.get('user_id'))
    return redirect(url_for('blog.register'))


# 图片下载
@blog.route('/download<path:filename>')
def download(filename):
    return send_from_directory(app.config["UPLOAD_FILE"], filename, as_attachment=True)


# 相册
@blog.route('/photo', methods=["GET", "POST"])
def photo():
    form = UploadForm()
    pics = Photos.query.all()[0:5]
    if form.validate_on_submit():
        pic = form.uploads.data.filename
        photo_name = secure_filename(pic)
        photo = Photos(photo_name=photo_name)
        if not os.path.exists(app.config["UPLOAD_FILE"]):  # 不存在保存穿甲图片的文件夹就创建
            os.mkdir(app.config["UPLOAD_FILE"])
            os.chmod(app.config["UPLOAD_FILE"], stat.S_IRWXU)  # 更改文件夹授权赋予读写模式
        form.uploads.data.save(app.config["UPLOAD_FILE"] + photo_name)  # 保存图片
        db.session.add(photo)
        db.session.commit()
        flash("上传照片成功！")
        return redirect(url_for('blog.photo'))
    return render_template("photos.html", form=form, pics=pics)


# 笔记详情页面
@blog.route('/detail/<int:question_id>', methods=['GET', 'POST'])
def detail(question_id):
    if request.method == 'GET':
        content = Articles.query.filter_by(id=question_id).first()
        user = Users.query.join(
            Articles, Articles.author_id == Users.id
        ).filter(
            Articles.id == question_id
        ).first()
        info = {'article': content,
                'author_name': 'nihao',
                'comments': content.comment,
                'comments_count': len(content.comment)
                }

        return render_template('detail.html', **info)
    # elif session.get('user_id'):
    #     comment = request.form.get('comment')
    #     comments = Comments(comment=comment, articles_id=question_id, author_id=session.get('user_id'))
    #     db.session.add(comments)
    #     db.session.commit()
    #     return redirect(url_for('detail', question_id=question_id))
    # return redirect(url_for('login'))
