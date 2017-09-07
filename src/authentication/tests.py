from django.test import TestCase, Client
from src.buyers.models import Buyer
from src.sellers.models import Seller

import json

class AuthenticationTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

    def sign_in(self, username, password, user_type):
        return self.client.post(
            '/authentication/',
            json.dumps({
                'username': username,
                'password': password,
                'user_type': user_type
            }),
            content_type='application/json'
        )

class BuyersSignInTestCase(AuthenticationTestCase):

    @classmethod
    def setUpTestData(self):
        self.buyer = Buyer(
            username='jimmyXavier',
            password='12345678',
            first_name='James',
            last_name='McAvoy',
            address='100 Universal City Plaza, Universal City, Los Angeles'
        )
        self.buyer.save()

    def test_should_sign_in_as_buyer_when_credentials_are_valid(self):
        response = self.sign_in('jimmyXavier', '12345678', 'buyer')

        response_body = response.json()
        self.assertEqual(response_body['user_id'], 1)
        self.assertEqual(response_body['user_type'], 'buyer')
        self.assertEqual(response.status_code, 201)

    def test_should_fail_to_sign_in_as_buyer_when_credentials_are_invalid(self):
        first_response = self.sign_in('jimmyXabier', '12345678', 'buyer')
        second_response = self.sign_in('jimmyXavier', 'acbdefgh', 'buyer')
        third_response = self.sign_in('jimmyXavier', '12345678', 'seller')

        self.assertEqual(first_response.status_code, 404)
        self.assertEqual(second_response.status_code, 404)
        self.assertEqual(third_response.status_code, 404)

class SellersSignInTestCase(AuthenticationTestCase):

    @classmethod
    def setUpTestData(self):
        self.seller = Seller(
            username='fat_bender52',
            password='12345678',
            first_name='Michael',
            last_name='Fassbender',
            company_name='The Brotherhood',
            address='900 Exposition Boulevard, Los Angeles',
            description='The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers.'
        )
        self.seller.save()

    def test_should_sign_in_as_seller_when_credentials_are_valid(self):
        response = self.sign_in('fat_bender52', '12345678', 'seller')

        response_body = response.json()
        self.assertEqual(response_body['user_id'], 1)
        self.assertEqual(response_body['user_type'], 'seller')
        self.assertEqual(response.status_code, 201)

    def test_should_fail_to_sign_in_as_seller_when_credentials_are_invalid(self):
        first_response = self.sign_in('fat_bender51', '12345678', 'seller')
        second_response = self.sign_in('fat_bender52', 'abcdefgh', 'seller')
        third_response = self.sign_in('fat_bender52', '12345678', 'buyer')

        self.assertEqual(first_response.status_code, 404)
        self.assertEqual(second_response.status_code, 404)
        self.assertEqual(third_response.status_code, 404)

class SignOutTestCase(AuthenticationTestCase):

    def test_should_sign_out_when_requested(self):
        response = self.client.delete('/authentication/')

        self.assertEqual(response.status_code, 204)

class HttpMethodNotAllowedTestCase(AuthenticationTestCase):

    def test_should_return_405_code_when_http_method_is_not_allowed(self):
        first_response = self.client.get('/authentication/')
        second_response = self.client.put('/authentication/')
        third_response = self.client.patch('/authentication/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
