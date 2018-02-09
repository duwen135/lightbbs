#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'duwen'

import os
from lightbbs import create_app, db
from lightbbs.models.user import User
from lightbbs.models.role import Role
from lightbbs.models.node import Node
from lightbbs.models.topic import Topic
from lightbbs.models.tag import Tag
from lightbbs.models.tags_relation import Tags_relation
from lightbbs.models.comment import Comment
from lightbbs.models.message import Message
from lightbbs.models.message_dialog import Message_dialog
from lightbbs.models.page import Page
from lightbbs.models.favorite import Favorite
from lightbbs.models.follow import Follow
from lightbbs.models.notification import Notification
from lightbbs.models.link import Link
from lightbbs.models.setting import Setting
from .lightbbs.models.site_stat import Stat
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Node=Node, Topic=Topic, \
                Tag=Tag, Tags_relation=Tags_relation, Comment=Comment, Message= Message, \
                Message_dialog=Message_dialog, Page=Page, Favorite=Favorite, Follow=Follow, \
                Notification=Notification, Link=Link, Setting=Setting, Stat=Stat)
manager.add_command('shell', Shell(make_shell_context()))
manager.add_command('db', MigrateCommand)

if __name__ == '__mai__':
    manager.run()