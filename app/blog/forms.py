from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField,PasswordField
from wtforms.validators import DataRequired, ValidationError, Length, Email

class UploadForm(FlaskForm):
    # 相册上传表单

    uploads = FileField(
        label="上传",
        validators=[DataRequired("请选择图片")],
        render_kw={
            'id': "exampleInputFile"
        }

    )
    submit = SubmitField(
        '上传',
        render_kw={
            'class': "btn btn-primary"

        }

    )

    def validate_uploads(self, filed):
        '''
        判断上传图片是否为png或者jpg图片
        :param filed:
        :return:
        '''
        url = filed.data.filename
        if url.split('.')[-1] != 'jpg' and url.split('.')[-1] != 'png':
            raise ValidationError('请选择JPG,PNG格式图片上传')


class RegistForm(FlaskForm):
    tel = StringField(
        description="phone number",
        validators=[Length(min=11, max=11, message="请输入正确的手机号码")],
        render_kw={
            'class': "form-control",
            'placeholder': "手机号",

        }
    )

    username = StringField(
        description="user name",
        validators=[DataRequired("请输入正确的手机号码")],
        render_kw={
            'class': "form-control",
            'placeholder': "用户名",

        }
    )
    email = StringField(
        description="email",
        validators=[Email("请输入正确的邮箱地址")],
        render_kw={
            'class': "form-control",
            'placeholder': "邮箱",

        }
    )
    pw1 = PasswordField(
        description="password",
        validators=[DataRequired("请输入密码")],
        render_kw={
            'class': "form-control",
            'placeholder': "密码",
            'id': 'pw1'
        }
    )
    pw2 = PasswordField(
        description="password",
        validators=[DataRequired("请输入密码")],
        render_kw={
            'class': "form-control",
            'placeholder': "重复输入密码",
            'id': 'pw2'

        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            'class': "btn btn-primary btn-block",
        }
    )


# 登陆表单
class LoginForm(FlaskForm):
    tel = StringField(
        description="phone number",
        render_kw={
            'class': "form-control",
            'placeholder': "手机号",

        }
    )
    pw = PasswordField(
        description="password",
        validators=[DataRequired("请输入密码")],
        render_kw={
            'class': "form-control",
            'placeholder': "密码",
            'id': 'pw1'
        }
    )
    submit = SubmitField(
        "登陆",
        render_kw={
            'class': "btn btn-primary btn-block",
        }
    )

    def validate_tel(self,field):
        tel = field.data
        from app.models import Users
        users_count = Users.query.filter_by(tel=tel).count()
        if users_count == 0:
            raise ValidationError('输入的手机号不正确')





