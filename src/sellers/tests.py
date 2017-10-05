import json

from datetime import date

from django.test import Client, TransactionTestCase
from django.shortcuts import get_object_or_404

from .models import Order, Seller
from src.products.models import Product

class SellersTestCase(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUp(self):
        self.client = Client()

class RegisteredSellersTestCase(SellersTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

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

class RegisteredSellersWithProductsTestCase(RegisteredSellersTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

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

class RegisteredSellersWithMoreProductsTestCase(RegisteredSellersWithProductsTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        self.product_4 = Product(
            name='Web Shooters',
            category='Kids',
            price=299.99,
            num_stocks=220,
            short_description='Shoot webs everywhere to satisfy your childish dreams!',
            full_description='Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special \'web fluid\' (the chemical composition of which is not known) at high pressure.',
            image='web_shooters.jpg',
            seller=self.seller
        )
        self.product_4.save()

class RegisterSellerTestCase(SellersTestCase):

    def test_should_register_seller_when_credentials_are_valid(self):
        response = self.client.post(
            '/sellers/',
            json.dumps({
                'username': 'fat_bender52',
                'password': '12345678',
                'first_name': 'Michael',
                'last_name': 'Fassbender',
                'company_name': 'The Brother',
                'address': '900 Exposition Boulevard, Los Angeles',
                'description': 'The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers.'
            }),
            content_type='application/json'
        )

        seller = Seller.objects.filter(id=1)
        self.assertTrue(seller.exists())
        self.assertEqual(seller[0].username, 'fat_bender52')
        self.assertEqual(seller[0].password, '12345678')
        self.assertEqual(seller[0].first_name, 'Michael')
        self.assertEqual(seller[0].last_name, 'Fassbender')
        self.assertEqual(seller[0].company_name, 'The Brother')
        self.assertEqual(seller[0].address, '900 Exposition Boulevard, Los Angeles')
        self.assertEqual(seller[0].description, 'The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers.')
        self.assertEqual(response.status_code, 204)

class RetrieveSellerInformationTestCase(RegisteredSellersTestCase):
    
    def test_should_retrieve_seller_information_when_requested(self):
        response = self.client.get('/sellers/1/')

        response_body = response.json()
        self.assertEqual(response_body['seller_id'], 1)
        self.assertEqual(response_body['username'], 'fat_bender52')
        self.assertEqual(response_body['first_name'], 'Michael')
        self.assertEqual(response_body['last_name'], 'Fassbender')
        self.assertEqual(response_body['company_name'], 'The Brotherhood')
        self.assertEqual(response_body['address'], '900 Exposition Boulevard, Los Angeles')
        self.assertEqual(response_body['description'], 'The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers.')
        self.assertEqual(response.status_code, 200)

class RetrieveSellerProductsTestCase(RegisteredSellersWithProductsTestCase):

    def test_should_retrieve_seller_products_when_requested(self):
        response = self.client.get('/sellers/1/products/')

        response_body = response.json()
        self.assertIsNotNone(response_body['products'])
        self.assertEqual(len(response_body['products']), 3)
        self.assertEqual(response_body['products'][0]['product_id'], 1)
        self.assertEqual(response_body['products'][0]['name'], 'Cerebro')
        self.assertEqual(response_body['products'][0]['category'], 'Cosmetics')
        self.assertEqual(response_body['products'][0]['price'], 1749.99)
        self.assertEqual(response_body['products'][0]['short_description'], 'Read minds across the globe!')
        self.assertEqual(response_body['products'][0]['image'], 'http://localhost:8000/images/cerebro.jpg')
        self.assertEqual(response_body['products'][1]['product_id'], 2)
        self.assertEqual(response_body['products'][1]['name'], 'Invisibility Cloak')
        self.assertEqual(response_body['products'][1]['category'], 'Clothes')
        self.assertEqual(response_body['products'][1]['price'], 799.99)
        self.assertEqual(response_body['products'][1]['short_description'], 'Hide from anything, even death!')
        self.assertEqual(response_body['products'][1]['image'], 'http://localhost:8000/images/invisibility_cloak.jpg')
        self.assertEqual(response_body['products'][2]['product_id'], 3)
        self.assertEqual(response_body['products'][2]['name'], 'Mjolnir')
        self.assertEqual(response_body['products'][2]['category'], 'Sports')
        self.assertEqual(response_body['products'][2]['price'], 2499.99)
        self.assertEqual(response_body['products'][2]['short_description'], 'Weight-lifting like never before!')
        self.assertEqual(response_body['products'][2]['image'], 'http://localhost:8000/images/mjolnir.jpg')
        self.assertEqual(response.status_code, 200)

class CreateNewProductTestCase(RegisteredSellersWithProductsTestCase):

    def test_should_create_new_product_when_details_are_valid(self):
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

        product = Product.objects.filter(id=4)
        self.assertTrue(product.exists())
        self.assertEqual(product[0].name, 'Web Shooters')
        self.assertEqual(product[0].category, 'Kids')
        self.assertEqual(product[0].price, 299.99)
        self.assertEqual(product[0].num_stocks, 220)
        self.assertEqual(product[0].short_description, 'Shoot webs everywhere to satisfy your childish dreams!')
        self.assertEqual(product[0].full_description, 'Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special \'web fluid\' (the chemical composition of which is not known) at high pressure.')
        self.assertEqual(product[0].image, '/images/web_shooters.jpg')
        self.assertEqual(response.json()['product_id'], 4)
        self.assertEqual(response.status_code, 201)

class UpdateProductTestCase(RegisteredSellersWithMoreProductsTestCase):

    def test_should_update_product_when_details_are_valid(self):
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

        product = get_object_or_404(Product, id=4)
        self.assertEqual(product.name, 'Web Shooters')
        self.assertEqual(product.category, 'Kids')
        self.assertEqual(product.price, 249.99)
        self.assertEqual(product.num_stocks, 320)
        self.assertEqual(product.short_description, 'Shoot webs everywhere to accomplish your dreams!')
        self.assertEqual(product.full_description, 'Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special \'web fluid\' (the chemical composition of which is not known) at high pressure.')
        self.assertEqual(product.image, '/images/web_shooters.jpg')
        self.assertEqual(response.status_code, 204)

class DeleteProductTestCase(RegisteredSellersWithMoreProductsTestCase):

    def test_should_delete_product_when_requested(self):
        response = self.client.delete('/sellers/1/products/4/')

        product = Product.objects.filter(id=4)
        self.assertTrue(product.exists())
        self.assertIsNone(product[0].seller)
        self.assertEqual(product[0].num_stocks, 0)
        self.assertEqual(response.status_code, 204)

class RetrieveOrderHistoryTestCase(RegisteredSellersWithProductsTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        Order(
            product=self.product_1,
            seller=self.seller,
            num_items=1,
            revenue=self.product_1.price
        ).save()
        Order(
            product=self.product_2,
            seller=self.seller,
            num_items=2,
            revenue=self.product_2.price * 2
        ).save()
        Order(
            product=self.product_3,
            seller=self.seller,
            num_items=3,
            revenue=self.product_3.price * 3
        ).save()

    def test_should_retrieve_order_history_when_requested(self):
        response = self.client.get('/sellers/1/orders/')

        response_body = response.json()
        self.assertIsNotNone(response_body['orders'])
        self.assertEqual(len(response_body['orders']), 3)
        self.assertEqual(response_body['orders'][0]['order_id'], 3)
        self.assertEqual(response_body['orders'][0]['product_id'], 3)
        self.assertEqual(response_body['orders'][0]['name'], 'Mjolnir')
        self.assertEqual(response_body['orders'][0]['short_description'], 'Weight-lifting like never before!')
        self.assertEqual(response_body['orders'][0]['image'], 'http://localhost:8000/images/mjolnir.jpg')
        self.assertEqual(response_body['orders'][0]['num_items'], 3)
        self.assertEqual(response_body['orders'][0]['revenue'], 7499.97)
        self.assertEqual(response_body['orders'][0]['timestamp'], str(date.today()))
        self.assertEqual(response_body['orders'][1]['order_id'], 2)
        self.assertEqual(response_body['orders'][1]['product_id'], 2)
        self.assertEqual(response_body['orders'][1]['name'], 'Invisibility Cloak')
        self.assertEqual(response_body['orders'][1]['short_description'], 'Hide from anything, even death!')
        self.assertEqual(response_body['orders'][1]['image'], 'http://localhost:8000/images/invisibility_cloak.jpg')
        self.assertEqual(response_body['orders'][1]['num_items'], 2)
        self.assertEqual(response_body['orders'][1]['revenue'], 1599.98)
        self.assertEqual(response_body['orders'][1]['timestamp'], str(date.today()))
        self.assertEqual(response_body['orders'][2]['order_id'], 1)
        self.assertEqual(response_body['orders'][2]['product_id'], 1)
        self.assertEqual(response_body['orders'][2]['name'], 'Cerebro')
        self.assertEqual(response_body['orders'][2]['short_description'], 'Read minds across the globe!')
        self.assertEqual(response_body['orders'][2]['image'], 'http://localhost:8000/images/cerebro.jpg')
        self.assertEqual(response_body['orders'][2]['num_items'], 1)
        self.assertEqual(response_body['orders'][2]['revenue'], 1749.99)
        self.assertEqual(response_body['orders'][2]['timestamp'], str(date.today()))
        self.assertEqual(response.status_code, 200)

class HttpMethodNotAllowedTestCase(SellersTestCase):

    def test_should_return_405_code_when_http_method_is_not_allowed_in_register_seller(self):
        first_response = self.client.get('/sellers/')
        second_response = self.client.put('/sellers/')
        third_response = self.client.patch('/sellers/')
        fourth_response = self.client.delete('/sellers/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_retrieve_seller_information(self):
        first_response = self.client.post('/sellers/1/')
        second_response = self.client.put('/sellers/1/')
        third_response = self.client.patch('/sellers/1/')
        fourth_response = self.client.delete('/sellers/1/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_retrieve_and_create_products(self):
        first_response = self.client.put('/sellers/1/products/')
        second_response = self.client.patch('/sellers/1/products/')
        third_response = self.client.delete('/sellers/1/products/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_update_and_delete_products(self):
        first_response = self.client.get('/sellers/1/products/4/')
        second_response = self.client.post('/sellers/1/products/4/')
        third_response = self.client.patch('/sellers/1/products/4/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_retrieve_order_history(self):
        first_response = self.client.post('/sellers/1/orders/')
        second_response = self.client.put('/sellers/1/orders/')
        third_response = self.client.patch('/sellers/1/orders/')
        fourth_response = self.client.delete('/sellers/1/orders/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
