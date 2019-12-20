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
from ..models.link import Link


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
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                            'Usernames must have only letters, '
                                            'numbers, dots or underscores')])
    parent_id = SelectField('父目录', coerce=int)
    keywords = StringField('节点关键词')
    content = TextAreaField('分类简介')
    master_id = StringField('节点版主')
    submit = SubmitField('提交')

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

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.node.choices = [(node.id, node.name)
                             for node in Node.query.order_by(Node.name).all()]
        #self.node = node

class PageForm(FlaskForm):
    title = StringField('网页名称', validators=[DataRequired()])
    keywords = StringField('关键词')
    content = TextAreaField('页面内容')
    go_url = StringField('网址')
    is_hidden = BooleanField('是否隐藏')
    submit = SubmitField('提交')

class LinkForm(FlaskForm):
    name = StringField('网站名称', validators=[DataRequired()])
    url = StringField('网址')
    logo = StringField('LOGO')
    is_hidden = BooleanField('是否隐藏')
    submit = SubmitField('提交')

class SettingForm(FlaskForm):
    site_name = StringField('网站名称')
    welcome_tip = StringField('欢迎信息')
    short_intro = StringField('简短介绍')
    maketing_str = StringField('关键词')
    site_style = SelectField('网站风格')
    themes = StringField('模版目录')
    site_logo = StringField('网站Logo')
    is_rewrite = BooleanField('开启伪静态')
    auth_code = BooleanField('开启验证码')
    auto_tag = BooleanField('标签开关')
    on_or_off = BooleanField('网站运行状态')
    close_msg = TextAreaField('站点关闭公告')
    custom_head_tags = TextAreaField('第三方统计代码')
    seo_description = TextAreaField('SEO描述')
    reward_title = StringField('奖励名称')
    encryption_key = StringField('安全密匙')
    save = SubmitField('保存')

    comment_order = BooleanField('回复列表顺序')
    is_approve = BooleanField('话题（回复）审核开关')
    pagination_comments = StringField('首页每页条数')
    timespan = StringField('发帖时间间隔')
    words_limit = StringField('发帖字数限制')
    save = SubmitField('保存')

    start_gold = StringField('注册初始积分')
    login_gold = StringField('登录积分')
    topic_gold = StringField('发帖积分')
    reply_gold = StringField('回复积分')
    reply_by_gold = StringField('被回复积分')
    delete_by_gold = StringField('被删除积分')
    follow_by_gold = StringField('被关注积分')
    stop_username = StringField('禁止注册的用户名')
    save = SubmitField('保存')

    send_by_email = BooleanField('邮件发送方式')
    smpt_host = StringField('SMPT服务器')
    smpt_port = StringField('SMPT端口')
    smpt_user = StringField('发信人邮件地址')
    smpt_pass = StringField('邮箱密码')
    is_send_email = BooleanField('发送注册邮件')
    save = SubmitField('保存')

