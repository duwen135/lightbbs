# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask_login import UserMixin
from lightbbs import db

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    openid = db.Column(db.Integer, unique=True)
    avatar = db.Column(db.String(64),)
    homepage = db.Column(db.String(64))
    money = db.Column(db.Integer)
    credit = db.Column(db.Integer)
    signature = db.Column(db.Text)
    topics = db.Column(db.Integer)
    replies = db.Column(db.Integer)
    notices = db.Column(db.Integer)
    follows = db.Column(db.Integer)
    faorites = db.Column(db.Integer)
    messages_unread = db.Column(db.Integer)
    regtime = db.Column(db.DateTime)
    lastlogin = db.Column(db.DateTime)
    lastpost = db.Column(db.DateTime)
    qq = db.Column(db.Integer)
    group_type = db.Column(db.String)
    gid = db.Column(db.Integer)
    ip = db.Column(db.String)
    location = db.Column(db.String)
    introduction = db.Column(db.Text)
    is_active = db.Column(db.Boolean)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))