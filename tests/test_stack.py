import unittest
from app import app
from aws_cdk.core import App


class TestEnvironmentVariables(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_stack_instantiates(self):
        self.assertIsInstance(app, App)
