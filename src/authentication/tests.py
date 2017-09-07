from django.test import TestCase, Client
from src.buyers.models import Buyer
from src.sellers.models import Seller

import json

class AuthenticationTestCase(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

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

    def test_buyer_should_sign_in_with_the_right_credentials(self):
        response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'jimmyXavier',
                'password': '12345678',
                'user_type': 'buyer'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.json()['user_id'], 1)
        self.assertEqual(response.json()['user_type'], 'buyer')
        self.assertEqual(response.status_code, 201)

    def test_buyer_should_fail_to_sign_in_with_the_wrong_credentials(self):
        first_response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'jimmyXabier',
                'password': '12345678',
                'user_type': 'buyer'
            }),
            content_type='application/json'
        )
        second_response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'jimmyXavier',
                'password': 'abcdefgh',
                'user_type': 'buyer'
            }),
            content_type='application/json'
        )
        third_response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'jimmyXavier',
                'password': '12345678',
                'user_type': 'seller'
            }),
            content_type='application/json'
        )

        self.assertEqual(first_response.status_code, 404)
        self.assertEqual(second_response.status_code, 404)
        self.assertEqual(third_response.status_code, 404)

    def test_seller_should_sign_in_with_the_right_credentials(self):
        response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'fat_bender52',
                'password': '12345678',
                'user_type': 'seller'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.json()['user_id'], 1)
        self.assertEqual(response.json()['user_type'], 'seller')
        self.assertEqual(response.status_code, 201)

    def test_seller_should_fail_to_sign_in_with_the_wrong_credentials(self):
        first_response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'fat_bender51',
                'password': '12345678',
                'user_type': 'seller'
            }),
            content_type='application/json'
        )
        second_response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'fat_bender52',
                'password': 'abcdefgh',
                'user_type': 'seller'
            }),
            content_type='application/json'
        )
        third_response = self.client.post(
            '/authentication/',
            json.dumps({
                'username': 'fat_bender52',
                'password': '12345678',
                'user_type': 'buyer'
            }),
            content_type='application/json'
        )

        self.assertEqual(first_response.status_code, 404)
        self.assertEqual(second_response.status_code, 404)
        self.assertEqual(third_response.status_code, 404)

    def test_user_should_sign_out(self):
        response = self.client.delete('/authentication/')

        self.assertEqual(response.status_code, 204)

    def test_server_should_return_405_with_wrong_HTTP_methods(self):
        first_response = self.client.get('/authentication/')
        second_response = self.client.put('/authentication/')
        third_response = self.client.patch('/authentication/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
