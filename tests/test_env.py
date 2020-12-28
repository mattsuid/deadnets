import unittest
import os
from aws_cdk.core import Environment
from app import ENV


class TestEnvironmentVariables(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_account(self):
        self.assertIsNotNone(os.environ.get('CDK_DEFAULT_ACCOUNT'))

    def test_region(self):
        self.assertIsNotNone(os.environ.get('CDK_DEFAULT_REGION'))

    def test_iam_key_id(self):
        self.assertIsNotNone(os.environ.get('AWS_ACCESS_KEY_ID'))

    def test_iam_secret_access_key(self):
        self.assertIsNotNone(os.environ.get('AWS_SECRET_ACCESS_KEY'))

    def test_iam_default_region(self):
        self.assertIsNotNone(os.environ.get('AWS_DEFAULT_REGION'))


class TestCDKEnv(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_app_env(self):
        self.assertIsInstance(ENV, Environment)

    def test_app_env_account(self):
        self.assertEqual(ENV.account, os.environ.get('CDK_DEFAULT_ACCOUNT'))

    def test_app_env_region(self):
        self.assertEqual(ENV.region, os.environ.get('CDK_DEFAULT_REGION'))



