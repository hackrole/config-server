# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import threading

# import requests


class ConfigClient(object):
    _instance_lock = threading.Lock()

    @staticmethod
    def instance(cls, **kw):
        if not hasattr(ConfigClient, "_instance"):
            with ConfigClient._instance_lock:
                if not hasattr(ConfigClient, "_instance"):
                    ConfigClient._instance = ConfigClient(**kw)
                    ConfigClient._instance._connect(**kw)

        return ConfigClient._instance

    def _connect(self, **kw):
        pass

    def get_msg(namespace, key):
        pass
