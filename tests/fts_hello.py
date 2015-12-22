# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import pytest


@pytest.mark.gen_test
def test_hello(http_client, base_url):
    response = yield http_client.fetch(base_url)

    assert response.code == 200
    assert response.body == 'Hello world'
