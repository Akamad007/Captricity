from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_redirects_on_success(self):
        response = self.client.post(reverse('login.views.login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/home/')
