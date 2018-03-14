# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models.role import Role
from ..models.user import User
