# -*- coding:utf-8 -*-
__author__ = 'duwen'

from flask_login import UserMixin
from lightbbs import db
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'lb_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    group_id = db.Column(db.Integer, db.ForeignKey('lb_groups.id'))
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    open_id = db.Column(db.Integer)
    avatar = db.Column(db.String(64))
    homepage = db.Column(db.String(64))
    money = db.Column(db.Integer)
    cred_it = db.Column(db.Integer)
    about_me = db.Column(db.Text)
    topics = db.Column(db.Integer)
    replies = db.Column(db.Integer)
    notices = db.Column(db.Integer)
    follows = db.Column(db.Integer)
    faorites = db.Column(db.Integer)
    messages_unread = db.Column(db.Integer)
    regtime = db.Column(db.DateTime, default=datetime.utcnow())
    lastlogin = db.Column(db.DateTime, default=datetime.utcnow())
    lastpost = db.Column(db.DateTime,default=datetime.utcnow())
    qq = db.Column(db.Integer)
    group_type = db.Column(db.String)
    gid = db.Column(db.Integer)
    ip = db.Column(db.String)
    location = db.Column(db.String)
    introduction = db.Column(db.Text)
    is_active = db.Column(db.Boolean)
