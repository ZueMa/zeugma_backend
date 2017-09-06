from django.test import TestCase, Client
from .models import Buyer, Cart

import json

class BuyersTestCase(TestCase):

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

        self.cart = Cart(buyer=self.buyer)
        self.cart.save()

    def test_buyer_should_register_with_the_right_credentials(self):
        response = self.client.post(
            '/buyers/',
            json.dumps({
                'username': 'jimmyXavier',
                'password': '12345678',
                'first_name': 'James',
                'last_name': 'McAvoy',
                'address': '100 Universal City Plaza, Universal City, Los Angeles'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 204)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_buyer_registration(self):
        first_response = self.client.get('/buyers/')
        second_response = self.client.put('/buyers/')
        third_response = self.client.patch('/buyers/')
        fourth_response = self.client.delete('/buyers/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_buyer_should_retrieve_their_information(self):
        response = self.client.get('/buyers/1/')

        self.assertEqual(response.json()['buyer_id'], 1)
        self.assertEqual(response.json()['username'], 'jimmyXavier')
        self.assertEqual(response.json()['first_name'], 'James')
        self.assertEqual(response.json()['last_name'], 'McAvoy')
        self.assertEqual(response.json()['address'], '100 Universal City Plaza, Universal City, Los Angeles')
        self.assertEqual(response.status_code, 200)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_buyer_information(self):
        first_response = self.client.post('/buyers/1/')
        second_response = self.client.put('/buyers/1/')
        third_response = self.client.patch('/buyers/1/')
        fourth_response = self.client.delete('/buyers/1/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def text_buyer_should_retrieve_their_cart(self):
        response = self.client.get('/buyers/1/cart/')

        self.assertEqual(response.json()['cart_id'], 1)
        self.assertEqual(response.json()['total_price'], 0)
        self.assertIsNotNone(response.json()['items'])
        self.assertEqual(response.status_code, 200)

    def test_buyer_should_create_new_cart_if_unpurchased_cart_does_not_exist(self):
        self.cart.is_purchased = True
        self.cart.save(update_fields=['is_purchased'])
        response = self.client.get('/buyers/1/cart/')

        self.assertEqual(response.json()['cart_id'], 2)
        self.assertEqual(response.json()['total_price'], 0)
        self.assertIsNotNone(response.json()['items'])
        self.assertEqual(response.status_code, 200)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_buyer_cart(self):
        first_response = self.client.post('/buyers/1/cart/')
        second_response = self.client.put('/buyers/1/cart/')
        third_response = self.client.patch('/buyers/1/cart/')
        fourth_response = self.client.delete('/buyers/1/cart/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
