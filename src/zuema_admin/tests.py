import json

from django.test import Client, TransactionTestCase
from django.shortcuts import get_object_or_404

from .models import Admin
from src.buyers.models import Buyer, Cart, ProductCart, Purchase
from src.products.models import Product
from src.sellers.models import Seller

class AdminTestCase(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUp(self):
        self.client = Client()

class AuthenticationTestCase(AdminTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        Admin(
            username='Admin',
            password='ZueMaAdmin'
        ).save()

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
    
class AdminWithProductsTestCase(AdminTestCase):

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
            is_confirmed=True,
            image='http://localhost:8000/images/mjolnir.jpg',
            seller=self.seller
        )
        self.product_3.save()

class AdminWithPurchasesTestCase(AdminWithProductsTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        self.buyer = Buyer(
            username='jimmyXavier',
            password='12345678',
            first_name='James',
            last_name='McAvoy',
            address='100 Universal City Plaza, Universal City, Los Angeles'
        )
        self.buyer.save()

        self.cart_1 = Cart(buyer=self.buyer)
        self.cart_1.save()
        ProductCart(
            cart=self.cart_1,
            product=self.product_1
        ).save()
        Purchase(
            cart=self.cart_1,
            buyer=self.buyer,
            is_shipped=True
        ).save()

        self.cart_2 = Cart(buyer=self.buyer)
        self.cart_2.save()
        ProductCart(
            cart=self.cart_2,
            product=self.product_2
        ).save()
        Purchase(
            cart=self.cart_2,
            buyer=self.buyer
        ).save()

        self.cart_3 = Cart(buyer=self.buyer)
        self.cart_3.save()
        ProductCart(
            cart=self.cart_3,
            product=self.product_3
        ).save()
        Purchase(
            cart=self.cart_3,
            buyer=self.buyer
        ).save()

class RetrievePurchasesTestCase(AdminWithPurchasesTestCase):
    
    def test_should_retrieve_all_purchases_when_requested(self):
        response = self.client.get('/admin/purchases/')

        response_body = response.json()
        self.assertIsNotNone(response_body['purchases'])
        self.assertEqual(len(response_body['purchases']), 2)
        self.assertEqual(response_body['purchases'][0]['purchase_id'], 3)
        self.assertEqual(response_body['purchases'][0]['total_price'], 2499.99)
        self.assertEqual(response_body['purchases'][0]['buyer_username'], 'jimmyXavier')
        self.assertEqual(response_body['purchases'][1]['purchase_id'], 2)
        self.assertEqual(response_body['purchases'][1]['total_price'], 799.99)
        self.assertEqual(response_body['purchases'][1]['buyer_username'], 'jimmyXavier')

class ConfirmProductTestCase(AdminWithProductsTestCase):

    def test_should_confirm_specified_products(self):
        response = self.client.patch('/admin/purchases/2/')

        purchase = Purchase.objects.filter(id=2)
        self.assertTrue(purchase[0].is_shipped)
        self.assertEquals(response.status_code, 204)

class RetrieveUnconfirmedProductsTestCase(AdminWithProductsTestCase):
    
    def test_should_retrieve_all_products_when_requested(self):
        response = self.client.get('/admin/products/')

        response_body = response.json()
        self.assertIsNotNone(response_body['products'])
        self.assertEqual(len(response_body['products']), 2)
        self.assertEqual(response_body['products'][0]['product_id'], 2)
        self.assertEqual(response_body['products'][0]['name'], 'Invisibility Cloak')
        self.assertEqual(response_body['products'][0]['price'], 799.99)
        self.assertEqual(response_body['products'][0]['short_description'], 'Hide from anything, even death!')
        self.assertEqual(response_body['products'][1]['product_id'], 1)
        self.assertEqual(response_body['products'][1]['name'], 'Cerebro')
        self.assertEqual(response_body['products'][1]['price'], 1749.99)
        self.assertEqual(response_body['products'][1]['short_description'], 'Read minds across the globe!')

class ConfirmProductTestCase(AdminWithProductsTestCase):

    def test_should_confirm_specified_products(self):
        response = self.client.patch('/admin/products/1/')

        product = Product.objects.filter(id=1)
        self.assertTrue(product[0].is_confirmed)
        self.assertEquals(response.status_code, 204)

class HttpMethodNotAllowedTestCase(AdminTestCase):

    def test_should_return_405_code_when_http_method_is_not_allowed_in_authentication(self):
        first_response = self.client.get('/admin/')
        second_response = self.client.put('/admin/')
        third_response = self.client.patch('/admin/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_retrieve_unconfirmed_products(self):
        first_response = self.client.post('/admin/products/')
        second_response = self.client.put('/admin/products/')
        third_response = self.client.patch('/admin/products/')
        fourth_response = self.client.delete('/admin/products/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_confirm_product(self):
        first_response = self.client.post('/admin/products/')
        second_response = self.client.put('/admin/products/')
        third_response = self.client.patch('/admin/products/')
        fourth_response = self.client.delete('/admin/products/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
