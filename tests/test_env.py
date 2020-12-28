import unittest
import os


class TestEnvironmentVariables(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_account(self):
        self.assertIsNotNone(os.environ.get('CDK_DEFAULT_ACCOUNT'))

    def test_region(self):
        self.assertIsNotNone(os.environ.get('CDK_DEFAULT_REGION'))
