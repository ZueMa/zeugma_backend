from django.test import TransactionTestCase, Client
from .models import Seller
from src.products.models import Product

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

        self.product_1 = Product(
            name='Cerebro',
            category='Cosmetics',
            price=1749.99,
            num_stocks=3,
            short_description='Read minds across the globe!',
            full_description='Cerebro is a fictional device appearing in American comic books published by Marvel Comics. The device is used by the X-Men (in particular, their leader, Professor Charles Xavier) to detect humans, specifically mutants.',
            image='http://localhost:8000/images/cerebro.jpg',
            seller=self.seller
        )
        self.product_1.save()

        self.product_2 = Product(
            name='Invisibility Cloak',
            category='Clothes',
            price=799.99,
            num_stocks=3,
            short_description='Hide from anything, even death!',
            full_description='An invisibility cloak is a magical garment which renders whomever or whatever it covers unseeable. These are common items that are massed produced in the wizarding world. The first known cloak was made by Death for Ignotus Peverell in the 13th century and it is one of a kind.',
            image='http://localhost:8000/images/invisibility_cloak.jpg',
            seller=self.seller
        )
        self.product_2.save()

        self.product_3 = Product(
            name='Mjolnir',
            category='Sports',
            price=2499.99,
            num_stocks=3,
            short_description='Weight-lifting like never before!',
            full_description='In Norse mythology, Mjolnir is the hammer of Thor, a major Norse god associated with thunder. Mjolnir is depicted in Norse mythology as one of the most fearsome and powerful weapons in existence, capable of leveling mountains.',
            image='http://localhost:8000/images/mjolnir.jpg',
            seller=self.seller
        )
        self.product_3.save()

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

    def test_seller_should_retrieve_their_prodcuts(self):
        response = self.client.get('/sellers/1/products/')

        self.assertIsNotNone(response.json()['products'])
        self.assertEqual(len(response.json()['products']), 3)
        self.assertEqual(response.json()['products'][0]['product_id'], 1)
        self.assertEqual(response.json()['products'][0]['name'], 'Cerebro')
        self.assertEqual(response.json()['products'][0]['category'], 'Cosmetics')
        self.assertEqual(response.json()['products'][0]['price'], 1749.99)
        self.assertEqual(response.json()['products'][0]['short_description'], 'Read minds across the globe!')
        self.assertEqual(response.json()['products'][0]['image'], 'http://localhost:8000/images/cerebro.jpg')
        self.assertEqual(response.json()['products'][1]['product_id'], 2)
        self.assertEqual(response.json()['products'][1]['name'], 'Invisibility Cloak')
        self.assertEqual(response.json()['products'][1]['category'], 'Clothes')
        self.assertEqual(response.json()['products'][1]['price'], 799.99)
        self.assertEqual(response.json()['products'][1]['short_description'], 'Hide from anything, even death!')
        self.assertEqual(response.json()['products'][1]['image'], 'http://localhost:8000/images/invisibility_cloak.jpg')
        self.assertEqual(response.json()['products'][2]['product_id'], 3)
        self.assertEqual(response.json()['products'][2]['name'], 'Mjolnir')
        self.assertEqual(response.json()['products'][2]['category'], 'Sports')
        self.assertEqual(response.json()['products'][2]['price'], 2499.99)
        self.assertEqual(response.json()['products'][2]['short_description'], 'Weight-lifting like never before!')
        self.assertEqual(response.json()['products'][2]['image'], 'http://localhost:8000/images/mjolnir.jpg')
        self.assertEqual(response.status_code, 200)

    def test_seller_should_create_new_product(self):
        response = self.client.post(
            '/sellers/1/products/',
            json.dumps({
                'name': 'Web Shooters',
                'category': 'Kids',
                'price': 299.99,
                'num_stocks': 220,
                'short_description': 'Shoot webs everywhere to satisfy your childish dreams!',
                'full_description': 'Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special \'web fluid\' (the chemical composition of which is not known) at high pressure.',
                'image': 'web_shooters.jpg'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.json()['product_id'], 4)
        self.assertEqual(response.status_code, 201)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_retrieving_and_creating_products(self):
        first_response = self.client.put('/sellers/1/products/')
        second_response = self.client.patch('/sellers/1/products/')
        third_response = self.client.delete('/sellers/1/products/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)

    def test_seller_should_update_product(self):
        product = Product(
            name='Web Shooters',
            category='Kids',
            price=299.99,
            num_stocks=220,
            short_description='Shoot webs everywhere to satisfy your childish dreams!',
            full_description='Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special \'web fluid\' (the chemical composition of which is not known) at high pressure.',
            image='web_shooters.jpg'
        )
        product.save()
        response = self.client.put(
            '/sellers/1/products/4/',
            json.dumps({
                'name': 'Web Shooters',
                'category': 'Kids',
                'price': 249.99,
                'num_stocks': 320,
                'short_description': 'Shoot webs everywhere to accomplish your dreams!',
                'full_description': 'Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special \'web fluid\' (the chemical composition of which is not known) at high pressure.',
                'image': 'web_shooters.jpg'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 204)

    def test_seller_should_delete_product(self):
        product = Product(
            name='Web Shooters',
            category='Kids',
            price=299.99,
            num_stocks=220,
            short_description='Shoot webs everywhere to satisfy your childish dreams!',
            full_description='Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special \'web fluid\' (the chemical composition of which is not known) at high pressure.',
            image='web_shooters.jpg'
        )
        product.save()
        response = self.client.delete('/sellers/1/products/4/')

        self.assertEqual(response.status_code, 204)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_updating_and_deleting_products(self):
        first_response = self.client.get('/sellers/1/products/4/')
        second_response = self.client.post('/sellers/1/products/4/')
        third_response = self.client.patch('/sellers/1/products/4/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
