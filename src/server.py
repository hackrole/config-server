# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import time

from tornado import web
from tornado.ioloop import IOLoop
from tornado.options import options, define
from tornado.options import parse_command_line
from mongoengine import connect
from mongoengine import Document
from mongoengine import (IntField, StringField)


define('port', default='8000', help='port to run')
define('debug', default=True, help="if debug mode")
define('mongo_host', default='127.0.0.1', help="mongo host")
define('mongo_port', default=27017,
       type=int, help='mongo port')
define('mongo_db', default='config_db', help='mongo dbname')
define('mongo_user', default=None, help="mongo username")
define('mongo_password', default=None, help='mongo password')


class Admin(Document):
    pass


class Token(Document):
    """ API授权令牌 """
    app_key = StringField(required=True, help_text="public key")
    app_secret = StringField(required=True, help_text="private key")


class BaseConfig(Document):
    """ 配置基类 """
    meta = {
        'allow_inheritance': True
    }

    namespace = StringField(required=True, unique=True, help_text="命名空间")
    key = StringField(required=True, unique_with='namespace', help_text="配置键")
    value = StringField(help_text="配置值")
    create_time = IntField(default=time.time(), help_text="时间")


class MsgConfig(BaseConfig):
    """ 文案配置 """
    pass


class ConfigList(web.RequestHandler):

    def get(self):
        pass

    def post(self):
        pass


class ConfigDetail(web.RequestHandler):

    def get(self):
        pass

    def post(self):
        pass


class MsgList(web.RequestHandler):

    def get(self):
        pass

    def post(self):
        pass


class MsgDetail(web.RequestHandler):

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class CheckConfig(web.RequestHandler):
    """ 校验配置值 """

    def post(self):
        pass


class HelloWorld(web.RequestHandler):

    def get(self):
        self.write("Hello world")


def make_application():
    parse_command_line()

    connect(db=options.mongo_db, host=options.mongo_host, port=options.mongo_port)

    application = web.Application([
        ('/', HelloWorld),
        ('/configs', ConfigList),
        ('/configs/(.+)', ConfigDetail),
        ('/messages', MsgList),
        ('/messages/(.+)', MsgDetail),
        ('/check', CheckConfig),
    ], debug=options.debug)

    return application


def main():
    application = make_application()
    application.listen(options.port)

    IOLoop.instance().start()


if __name__ == "__main__":
    main()
