import json

from django.test import TestCase, Client

from .models import User

class SignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="doboblock@google.com",
            name="bodoblock",
            password="0694",
        )

    def tearDown(self):
        User.objects.all().delete()
        
    def test_signup_success(self):
        client = Client()
        user = {
            "email": "bodoblock2@google.com",
            "name": "보도블록",
            "password": "0694",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_duplication_user(self):
        client = Client()
        user = {
            "email": "loveim0112@gmail.com",
            "name": "임예진",
            "password": "yejin0694",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "ALREADY_EXISTED_EMAIL"})

    def test_email_format_error(self):
        client = Client()
        user = {
            "email": "sumin@gmail.com",
            "name": "이수민",
            "password": "sumin12",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "EMAIL_ERROR"})
    
    def test_password_format_error(self):
        client = Client()
        user = {
            "email": "jeongyoon@gmail.com",
            "name": "신정윤",
            "password": "jy0776",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "PASSWORD_ERROR"})
    
    def test_key_error(self):
        client = Client()
        user = {
            "email": "sooin@gmail.com",
            "name": "조수인",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})