import json

from django.test import Client, TransactionTestCase
from django.shortcuts import get_object_or_404

class AdminTestCase(TransactionTestCase):
    reset_sequence = True

    @classmethod
    def setUp(self):
        self.client = Client()

class AuthenticationTestCase(AdminTestCase):

    def sign_in(self, username, password):
        return self.client.post(
            '/admin/',
            json.dumps({
                'username': username,
                'password': password
            }),
            content_type='application/json'
        )
    
    def test_should_sign_in_as_admin_when_credentials_are_valid(self):
        response = self.sign_in('Admin', "ZueMaAdmin")

        self.assertEqual(response.status_code, 204)
    
    def test_should_fail_to_sign_in_as_admin_when_credentials_are_invalid(self):
        response = self.sign_in('admin', 'zuemaadmin')

        self.assertEqual(response.status_code, 404)
    
    def test_should_sign_out_when_requested(self):
        response = self.client.delete('/admin/')

        self.assertEqual(response.status_code, 204)

class HttpMethodNotAllowedTestCase(AdminTestCase):

    def test_should_return_405_code_when_http_method_is_not_allowed_in_authentication(self):
        first_response = self.client.get('/admin/')
        second_response = self.client.put('/admin/')
        third_response = self.client.patch('/admin/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
