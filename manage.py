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
from lightbbs.models.comment import Comment
from lightbbs.models.message import Message
from lightbbs.models.message_dialog import Message_dialog
from lightbbs.models.page import Page
from lightbbs.models.favorite import Favorite
from lightbbs.models.follow import Follow
from lightbbs.models.notification import Notification
from lightbbs.models.link import Link
from lightbbs.models.setting import Setting
from lightbbs.models.site_stat import Stat
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('LIGHTBBS_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Node=Node, Topic=Topic,
                Tag=Tag, Comment=Comment, Message= Message,
                Message_dialog=Message_dialog, Page=Page, Favorite=Favorite, Follow=Follow,
                Notification=Notification, Link=Link, Setting=Setting, Stat=Stat)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def deploy():
    """Run deployment tasks."""
    #from flask.ext.migrate import upgrade
    from lightbbs import create_app, db
    from lightbbs.models.user import User
    from lightbbs.models.role import Role
    from lightbbs.models.node import Node
    from lightbbs.models.topic import Topic
    from lightbbs.models.tag import Tag
    from lightbbs.models.comment import Comment
    # 把数据库迁移到最新修订版本
    #upgrade()
    db.create_all()
    # 创建用户角色
    Role.insert_roles()
    # 让所有用户都关注此用户
    User.add_self_follows()
    #生成虚拟数据
    User.generate_fake()
    Node.generate_fake()
    Topic.generate_fake()
    Comment.generate_fake()
    Tag.generate_fake()

if __name__ == '__main__':
    manager.run()