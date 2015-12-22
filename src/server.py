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
from mongoengine import DoesNotExist, MultipleObjectsReturned


define('port', default=8000, type=int, help='port to run')
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

    namespace = StringField(required=True, help_text="命名空间")
    key = StringField(required=True, unique_with='namespace', help_text="配置键")
    value = StringField(help_text="配置值")
    create_time = IntField(default=time.time(), help_text="时间")


class MsgConfig(BaseConfig):
    """ 文案配置 """
    pass


class MsgRequire(Document):
    """ 设置必须参数 """
    namespace = StringField(required=True, help_text="namespace")
    key = StringField(required=True, help_text="key")


class BaseHandler(web.RequestHandler):
    def get_object(self, pk):
        try:
            obj = self.model.objects.get(pk=pk)
            return obj
        except DoesNotExist:
            raise Exception('404')
        except MultipleObjectsReturned:
            raise Exception('500')


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
        config_list = MsgConfig.objects

        result = []
        for config in config_list:
            data = {
                'pk': str(config.pk),
                'key': config.key,
                'value': config.value,
                'create_time': config.create_time,
            }
            result.append(data)

        self.write({'data': result})

    def post(self):
        namespace = self.get_argument('namespace')
        key = self.get_argument('key')
        value = self.get_argument('value')

        config = MsgConfig(namespace=namespace,
                           key=key, value=value)
        config.save()

        result = {
            'pk': str(config.pk),
            'namespace': config.namespace,
            'key': config.key,
            'value': config.value,
        }

        self.set_status(201)
        self.write(result)


class MsgDetail(BaseHandler):
    model = MsgConfig

    def get(self, pk):
        config = self.get_object(pk)

        data = {
            'pk': str(config.pk),
            'namespace': config.namespace,
            'key': config.key,
            'value': config.value
        }

        self.write(data)

    def put(self):
        pass

    def delete(self, pk):
        config = self.get_object(pk)

        config.delete()

        self.set_status(204)
        self.finish({'pk': str(config.pk)})


class MsgRequireList(web.RequestHandler):

    def get(self):
        requires = MsgRequire.objects

        result = []
        for item in requires:
            data = {
                'pk': str(item.pk),
                'namespace': item.namespace,
                'key': item.key
            }
            result.append(data)

        self.write({'data': result})

    def post(self):
        namespace = self.get_argument('namespace')
        key = self.get_argument('key')

        obj = MsgRequire(namespace=namespace, key=key)
        obj.save()

        data = {
            'pk': str(obj.pk),
            'namespace': obj.namespace,
            'key': obj.key,
        }

        self.set_status(201)
        self.write(data)


class MsgRequireHandler(BaseHandler):
    model = MsgRequire

    def get(self, pk):
        obj = self.get_object(pk)

        result = {
            'pk': str(obj.pk),
            'namespace': obj.namespace,
            'key': obj.key,
        }

        self.write(result)


class CheckConfig(web.RequestHandler):
    """ 校验配置值 """

    def post(self):
        requires = MsgRequire.objects

        errors = []
        for item in requires:
            try:
                MsgConfig.objects.get(namespace=item.namespace, key=item.key)
            except DoesNotExist:
                error = {
                    'pk': str(item.pk),
                    'namespace': item.namespace,
                    'key': item.key,
                }
                errors.append(error)
            except MultipleObjectsReturned:
                raise Exception(500)

        if errors:
            self.set_status(200)
            self.write({'result': False, 'errors': errors})
            return self.finish()

        self.write({'result': True})


class HelloWorld(web.RequestHandler):

    def get(self):
        self.write("Hello world")


def make_application():
    parse_command_line()

    connect(db=options.mongo_db, host=options.mongo_host,
            port=options.mongo_port)

    application = web.Application([
        ('/', HelloWorld),
        ('/configs', ConfigList),
        ('/configs/(.+)', ConfigDetail),
        ('/messages', MsgList),
        ('/messages/(.+)', MsgDetail),
        ('/msg_requires', MsgRequireList),
        ('/msg_requires/(.+)', MsgRequireHandler),
        ('/check', CheckConfig),
    ], debug=options.debug)

    return application


def main():
    application = make_application()
    application.listen(options.port)

    IOLoop.instance().start()


if __name__ == "__main__":
    main()
