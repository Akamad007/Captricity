"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ApiUtilsTest(TestCase):
    def test_get_random_batch_name(self):
        from api.views import get_random_batch_name
        from unittest.mock import patch

        with patch('api.views.random.choice', return_value='B'):
            name = get_random_batch_name('PREFIX')

        self.assertTrue(name.startswith('PREFIX'))
        self.assertEqual(name, 'PREFIX' + 'B' * 10)

    def test_status_errors_raise(self):
        from api.views import status

        class DummyClient:
            def read_batch_readiness(self, batch_id):
                return {'errors': ['boom'], 'status': 'bad'}

        with self.assertRaises(Exception):
            status(DummyClient(), 1)

    def test_status_ok(self):
        from api.views import status

        class DummyClient:
            def read_batch_readiness(self, batch_id):
                return {'errors': [], 'status': 'ready'}

        self.assertEqual(status(DummyClient(), 1), 'ready')
