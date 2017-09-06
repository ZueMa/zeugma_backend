from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from .models import Buyer, Cart, ProductCart, Purchase
from src.products.models import Product
from src.sellers.models import Seller

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

        self.product = Product(
            name='Cerebro',
            category='Cosmetics',
            price=1749.99,
            num_stocks=3,
            short_description='Read minds across the globe!',
            full_description='Cerebro is a fictional device appearing in American comic books published by Marvel Comics. The device is used by the X-Men (in particular, their leader, Professor Charles Xavier) to detect humans, specifically mutants.',
            image='cerebro.jpg',
            seller=self.seller
        )
        self.product.save()

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

    def test_buyer_should_add_item_to_cart(self):
        response = self.client.post(
            '/buyers/1/cart/items/',
            json.dumps({
                'product_id': 1
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 204)

    def test_server_should_return_304_if_product_already_exists(self):
        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        response = self.client.post(
            '/buyers/1/cart/items/',
            json.dumps({
                'product_id': 1
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 304)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_adding_item_to_cart(self):
        first_response = self.client.get('/buyers/1/cart/items/')
        second_response = self.client.put('/buyers/1/cart/items/')
        third_response = self.client.patch('/buyers/1/cart/items/')
        fourth_response = self.client.delete('/buyers/1/cart/items/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_buyer_should_increase_item_quantity_in_cart(self):
        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        response = self.client.post(
            '/buyers/1/cart/items/1/',
            json.dumps({
                'action': 'increase'
            }),
            content_type='application/json'
        )
        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)

        self.assertEqual(product_cart.num_items, 2)
        self.assertEqual(response.status_code, 204)

    def test_server_should_return_304_if_num_items_will_exceed_num_stocks(self):
        product_cart = ProductCart(
            cart=self.cart,
            product=self.product
        )
        product_cart.num_items = 3
        product_cart.save()
        response = self.client.post(
            '/buyers/1/cart/items/1/',
            json.dumps({
                'action': 'increase'
            }),
            content_type='application/json'
        )
        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)

        self.assertEqual(product_cart.num_items, 3)
        self.assertEqual(response.status_code, 304)

    def test_buyer_should_decrease_item_quantity_in_cart(self):
        product_cart = ProductCart(
            cart=self.cart,
            product=self.product
        )
        product_cart.num_items = 3
        product_cart.save()
        response = self.client.post(
            '/buyers/1/cart/items/1/',
            json.dumps({
                'action': 'decrease'
            }),
            content_type='application/json'
        )
        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)

        self.assertEqual(product_cart.num_items, 2)
        self.assertEqual(response.status_code, 204)

    def test_server_should_return_304_if_num_items_will_be_zero(self):
        product_cart = ProductCart(
            cart=self.cart,
            product=self.product
        )
        product_cart.num_items = 1
        product_cart.save()
        response = self.client.post(
            '/buyers/1/cart/items/1/',
            json.dumps({
                'action': 'decrease'
            }),
            content_type='application/json'
        )
        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)

        self.assertEqual(product_cart.num_items, 1)
        self.assertEqual(response.status_code, 304)

    def test_buyer_should_delete_item_from_cart(self):
        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        response = self.client.delete('/buyers/1/cart/items/1/')

        self.assertFalse(ProductCart.objects.filter(cart_id=self.cart.id, product_id=self.product.id).exists())
        self.assertEqual(response.status_code, 204)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_updating_and_deleting_item_in_cart(self):
        first_response = self.client.get('/buyers/1/cart/items/1/')
        second_response = self.client.put('/buyers/1/cart/items/1/')
        third_response = self.client.patch('/buyers/1/cart/items/1/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)

    def test_buyer_should_purchase_their_cart(self):
        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        response = self.client.post('/buyers/1/cart/purchase/')

        self.assertEqual(response.json()['purchase_id'], 1)
        self.assertEqual(response.status_code, 201)

    def test_buyer_should_fail_to_purchase_empty_cart(self):
        response = self.client.post('/buyers/1/cart/purchase/')

        self.assertEqual(response.status_code, 304)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_purchasing_cart(self):
        first_response = self.client.get('/buyers/1/cart/purchase/')
        second_response = self.client.put('/buyers/1/cart/purchase/')
        third_response = self.client.patch('/buyers/1/cart/purchase/')
        fourth_response = self.client.delete('/buyers/1/cart/purchase/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_buyer_should_retrieve_their_purchase_history(self):
        for x in range(0, 3):
            ProductCart(
                cart=self.cart,
                product=self.product
            ).save()
            purchase = Purchase(
                cart=self.cart,
                buyer=self.buyer
            )
            purchase.save()
            self.cart.is_purchased = True
            self.cart.save(update_fields=['is_purchased'])
        response = self.client.get('/buyers/1/purchases/')

        self.assertIsNotNone(response.json()['purchases'])
        self.assertEqual(response.status_code, 200)

    def test_server_should_return_405_with_wrong_HTTP_methods_for_purchase_history(self):
        first_response = self.client.post('/buyers/1/purchases/')
        second_response = self.client.put('/buyers/1/purchases/')
        third_response = self.client.patch('/buyers/1/purchases/')
        fourth_response = self.client.delete('/buyers/1/purchases/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
