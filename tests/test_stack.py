import unittest
import os
from app import app


class TestEnvironmentVariables(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_stack_env(self):
        self.assertEqual(app.account, os.environ.get('CDK_DEFAULT_ACCOUNT'))
        self.assertEqual(app.region, os.environ.get('CDK_DEFAULT_REGION'))
