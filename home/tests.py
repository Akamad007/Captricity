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


class StoragePathTest(TestCase):
    def test_get_photo_storage_path(self):
        from home.models import get_photo_storage_path
        from django.contrib.auth.models import User
        from unittest.mock import patch
        user = User(id=5)

        class Photo:
            def __init__(self, user):
                self.user = user

        with patch('home.models.random.choice', return_value='A'):
            path = get_photo_storage_path(Photo(user), 'example.jpg')

        import hashlib
        expected_hash = hashlib.sha1(str(user.id).encode()).hexdigest()
        self.assertTrue(path.startswith('img/home/'))
        # Ensure the random string length is 10 characters
        random_part = path.split('/')[-1].split('_')[0]
        self.assertEqual(random_part, 'A' * 10)
        self.assertIn('_' + expected_hash + '_example.jpg', path)
