# -*- coding:utf-8 -*-
__author__ = 'duwen'


from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models.role import Role
from ..models.user import User


class TopicForm(FlaskForm):
    node = SelectField('请选择节点', choices=[], coerce=int)
    title = StringField('请输入话题标题', validators=[DataRequired()])
    content = TextAreaField('描述您的内容', validators=[DataRequired()])
    keywords = StringField('话题关键词，多个请用逗号隔开')
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    username = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.role_name)
                             for role in Role.query.order_by(Role.role_name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class CommentForm(FlaskForm):
    content = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')