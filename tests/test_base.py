import unittest
from app import create_app
from flask import json


class TestBase(unittest.TestCase):
    app = create_app('TESTING')
    app.app_context().push()
    client = app.test_client()
