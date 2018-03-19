# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models.role import Role
from ..models.user import User
from ..models.node import Node


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

    def __init__(self, user, *args, **kwargs):
        super(UserEdit, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.role_name)
                             for role in Role.query.order_by(Role.role_name).all()]
        self.user = user


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')


class NodeForm(FlaskForm):
    name = StringField('节点名称', validators=[
        DataRequired, Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                            'Usernames must have only letters, '
                                            'numbers, dots or underscores')])
    parent_id = SelectField('父目录', coerce=int)
    keywords = StringField('节点关键词')
    content = TextAreaField('分类简介')
    master_id = StringField('节点版主')

    def __init__(self, *args, **kwargs):
        super(NodeForm, self).__init__(*args, **kwargs)
        self.parent_id.choices = [(node.id, node.name)
                             for node in Node.query.order_by(Node.name).filter_by(parent_id=0).all()]
        #self.node = node

    def validate_name(self, field):
        if Node.query.filter_by(name=field.data).first():
            raise ValidationError('该节点已存在!')


class TopicForm(FlaskForm):
    node = SelectField('请选择节点', choices=[], coerce=int)
    title = StringField('请输入话题标题', validators=[DataRequired()])
    content = TextAreaField('描述您的内容', validators=[DataRequired()])
    keywords = StringField('话题关键词，多个请用逗号隔开')
    submit = SubmitField('提交')

class PageForm(FlaskForm):
    title = StringField('网站名称', validators=[DataRequired])
    go_url = StringField('网址', validators=[DataRequired])
    is_hidden = BooleanField('是否隐藏', validators=[DataRequired])