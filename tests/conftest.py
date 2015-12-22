# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import sys
from os import path

PROJECT_DIR = path.join(
    path.dirname(path.dirname(path.realpath(__file__))), 'src')
sys.path.insert(0, PROJECT_DIR)

import pytest

from server import make_application


@pytest.fixture
def app():
    application = make_application()

    return application
