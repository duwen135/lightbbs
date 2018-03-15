# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models.role import Role
from ..models.user import User


class UserEdit(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须一致！')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    homepage = StringField('个人主页')
    location = StringField('所在地', validators=[Length(0, 64)])
    signature = TextAreaField('签名')
    about_me = TextAreaField('个人简介')
    integral = IntegerField('积分')
    confirmed = BooleanField('认证')
    role = SelectField('角色', coerce=int)
    submit = SubmitField('更新用户信息')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')