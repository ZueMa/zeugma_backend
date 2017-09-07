from django.test import TransactionTestCase, Client
from .models import Seller

import json

class SellersTestCase(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUp(self):
        self.client = Client()

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

    def test_seller_should_register_with_the_right_credentials(self):
        response = self.client.post(
            '/sellers/',
            json.dumps({
                'username': 'fat_benders52',
                'password': '12345678',
                'first_name': 'Michael',
                'last_name': 'Fassbender',
                'company_name': 'The Brother',
                'address': '900 Exposition Boulevard, Los Angeles',
                'description': 'The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers.'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 204)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_seller_registration(self):
        first_response = self.client.get('/sellers/')
        second_response = self.client.put('/sellers/')
        third_response = self.client.patch('/sellers/')
        fourth_response = self.client.delete('/sellers/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
    
    def test_seller_should_retrieve_their_information(self):
        response = self.client.get('/sellers/1/')

        self.assertEqual(response.json()['seller_id'], 1)
        self.assertEqual(response.json()['username'], 'fat_bender52')
        self.assertEqual(response.json()['first_name'], 'Michael')
        self.assertEqual(response.json()['last_name'], 'Fassbender')
        self.assertEqual(response.json()['company_name'], 'The Brotherhood')
        self.assertEqual(response.json()['address'], '900 Exposition Boulevard, Los Angeles')
        self.assertEqual(response.json()['description'], 'The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers.')
        self.assertEqual(response.status_code, 200)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_seller_information(self):
        first_response = self.client.post('/sellers/1/')
        second_response = self.client.put('/sellers/1/')
        third_response = self.client.patch('/sellers/1/')
        fourth_response = self.client.delete('/sellers/1/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
