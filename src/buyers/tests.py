from django.test import TransactionTestCase, Client
from django.shortcuts import get_object_or_404
from .models import Buyer, Cart, ProductCart, Purchase
from datetime import date
from src.products.models import Product
from src.sellers.models import Seller

import json

class BuyersTestCase(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUp(self):
        self.client = Client()

class RegisteredBuyersTestCase(BuyersTestCase):

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

class RegisteredBuyersWithCartsTestCase(RegisteredBuyersTestCase):

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

        self.product = Product(
            name='Cerebro',
            category='Cosmetics',
            price=1749.99,
            num_stocks=3,
            short_description='Read minds across the globe!',
            full_description='Cerebro is a fictional device appearing in American comic books published by Marvel Comics. The device is used by the X-Men (in particular, their leader, Professor Charles Xavier) to detect humans, specifically mutants.',
            image='http://localhost:8000/images/cerebro.jpg',
            seller=self.seller
        )
        self.product.save()

        self.cart = Cart(buyer=self.buyer)
        self.cart.save()

    def add_item_to_cart(self, product_id):
        return self.client.post(
            '/buyers/1/cart/items/',
            json.dumps({
                'product_id': product_id
            }),
            content_type='application/json'
        )

    def update_item_quantity(self, action):
        return self.client.post(
            '/buyers/1/cart/items/1/',
            json.dumps({
                'action': action
            }),
            content_type='application/json'
        )

class RegisterBuyerTestCase(BuyersTestCase):

    def test_should_register_buyer_when_credentials_are_valid(self):
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

        buyer = Buyer.objects.filter(id=1)
        self.assertTrue(buyer.exists())
        self.assertEqual(buyer[0].username, 'jimmyXavier')
        self.assertEqual(buyer[0].password, '12345678')
        self.assertEqual(buyer[0].first_name, 'James')
        self.assertEqual(buyer[0].last_name, 'McAvoy')
        self.assertEqual(buyer[0].address, '100 Universal City Plaza, Universal City, Los Angeles')
        self.assertEqual(response.status_code, 204)

class RetrieveBuyerInformationTestCase(RegisteredBuyersTestCase):

    def test_should_retrieve_buyer_information_when_requested(self):
        response = self.client.get('/buyers/1/')

        response_body = response.json()
        self.assertEqual(response_body['buyer_id'], 1)
        self.assertEqual(response_body['username'], 'jimmyXavier')
        self.assertEqual(response_body['first_name'], 'James')
        self.assertEqual(response_body['last_name'], 'McAvoy')
        self.assertEqual(response_body['address'], '100 Universal City Plaza, Universal City, Los Angeles')
        self.assertEqual(response.status_code, 200)

class RetrieveCurrentCartTestCase(RegisteredBuyersWithCartsTestCase):

    def text_should_retrieve_current_cart_and_its_items_when_they_both_exist(self):
        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        response = self.client.get('/buyers/1/cart/')

        response_body = response.json()
        self.assertEqual(response_body['cart_id'], 1)
        self.assertEqual(response_body['total_price'], 0)
        self.assertIsNotNone(response_body['items'])
        self.assertEqual(len(response_body['items']), 1)
        self.assertEqual(response_body['items'][0]['product_id'], 1)
        self.assertEqual(response_body['items'][0]['name'], 'Cerebro')
        self.assertEqual(response_body['items'][0]['price'], 1749.99)
        self.assertEqual(response_body['items'][0]['num_stocks'], 3)
        self.assertEqual(response_body['items'][0]['short_description'], 'Read minds across the globe!')
        self.assertEqual(response_body['items'][0]['image'], 'http://localhost:8000/images/cerebro.jpg')
        self.assertEqual(response_body['items'][0]['num_items'], 1)
        self.assertEqual(response.status_code, 200)

    def text_should_retrieve_current_cart_when_an_unpurchased_cart_exists(self):
        response = self.client.get('/buyers/1/cart/')

        response_body = response.json()
        self.assertEqual(response_body['cart_id'], 1)
        self.assertEqual(response_body['total_price'], 0)
        self.assertIsNotNone(response_body['items'])
        self.assertEqual(response.status_code, 200)

    def test_should_create_and_retrieve_new_cart_when_an_unpurchased_cart_does_not_exist(self):
        self.cart.is_purchased = True
        self.cart.save(update_fields=['is_purchased'])
        response = self.client.get('/buyers/1/cart/')

        response_body = response.json()
        self.assertEqual(response_body['cart_id'], 2)
        self.assertEqual(response_body['total_price'], 0)
        self.assertIsNotNone(response_body['items'])
        self.assertEqual(response.status_code, 200)

class AddItemToCartTestCase(RegisteredBuyersWithCartsTestCase):

    def test_should_add_item_to_cart_when_it_is_not_already_in_cart(self):
        response = self.add_item_to_cart(1)

        product_cart = ProductCart.objects.filter(id=1)
        self.assertTrue(product_cart.exists())
        self.assertEqual(product_cart[0].num_items, 1)
        self.assertEqual(response.status_code, 204)

    def test_should_fail_to_add_item_to_cart_when_it_is_already_in_cart(self):
        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        response = self.add_item_to_cart(1)

        product_cart = ProductCart.objects.filter(id=2)
        self.assertFalse(product_cart.exists())
        self.assertEqual(response.status_code, 304)

class UpdateItemQuantityTestCase(RegisteredBuyersWithCartsTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        self.product_cart = ProductCart(
            cart=self.cart,
            product=self.product
        )
        self.product_cart.save()

    def test_should_increase_item_quantity_in_cart_when_number_of_items_is_less_than_number_of_in_stock_items(self):
        response = self.update_item_quantity('increase')

        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)
        self.assertEqual(product_cart.num_items, 2)
        self.assertEqual(response.status_code, 204)

    def test_should_fail_to_increase_item_quantity_in_cart_when_number_of_items_is_equal_to_number_of_in_stock_items(self):
        self.product_cart.num_items = 3
        self.product_cart.save(update_fields=['num_items'])
        response = self.update_item_quantity('increase')

        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)
        self.assertEqual(product_cart.num_items, 3)
        self.assertEqual(response.status_code, 304)

    def test_should_decrease_item_quantity_in_cart_when_number_of_items_is_more_than_one(self):
        self.product_cart.num_items = 3
        self.product_cart.save(update_fields=['num_items'])
        response = self.update_item_quantity('decrease')

        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)
        self.assertEqual(product_cart.num_items, 2)
        self.assertEqual(response.status_code, 204)

    def test_should_fail_to_decrease_item_quantity_in_cart_when_number_of_items_is_equal_to_one(self):
        response = self.update_item_quantity('decrease')

        product_cart = get_object_or_404(ProductCart, cart_id=self.cart.id, product_id=self.product.id)
        self.assertEqual(product_cart.num_items, 1)
        self.assertEqual(response.status_code, 304)

class DeleteItemFromCartTestCase(RegisteredBuyersWithCartsTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()

    def test_should_delete_item_from_cart_when_it_exists(self):
        response = self.client.delete('/buyers/1/cart/items/1/')

        self.assertFalse(ProductCart.objects.filter(id=1).exists())
        self.assertEqual(response.status_code, 204)

class PurchaseCartTestCase(RegisteredBuyersWithCartsTestCase):

    def test_should_purchase_cart_when_cart_is_not_empty(self):
        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        response = self.client.post('/buyers/1/cart/purchase/')

        purchase = Purchase.objects.filter(id=1)
        self.assertTrue(purchase.exists())
        self.assertEqual(purchase[0].buyer.id, 1)
        self.assertEqual(purchase[0].cart.id, 1)
        self.assertTrue(purchase[0].cart.is_purchased)
        self.assertFalse(purchase[0].is_shipped)
        self.assertEqual(purchase[0].timestamp, date.today())
        self.assertEqual(response.json()['purchase_id'], 1)
        self.assertEqual(response.status_code, 201)

    def test_should_fail_to_purchase_cart_when_cart_is_empty(self):
        response = self.client.post('/buyers/1/cart/purchase/')

        purchase = Purchase.objects.filter(id=1)
        self.assertFalse(purchase.exists())
        self.assertEqual(response.status_code, 304)

class RetrievePurchaseHistoryTestCase(RegisteredBuyersWithCartsTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        Purchase(
            cart=self.cart,
            buyer=self.buyer
        ).save()
        Purchase(
            cart=self.cart,
            buyer=self.buyer
        ).save()
        Purchase(
            cart=self.cart,
            buyer=self.buyer
        ).save()
        self.cart.is_purchased = True
        self.cart.save(update_fields=['is_purchased'])

    def test_should_retrieve_purchase_history_when_requested(self):
        response = self.client.get('/buyers/1/purchases/')

        response_body = response.json()
        self.assertIsNotNone(response_body['purchases'])
        self.assertEqual(len(response_body['purchases']), 3)
        self.assertEqual(response_body['purchases'][0]['purchase_id'], 3)
        self.assertEqual(response_body['purchases'][0]['cart_id'], 1)
        self.assertEqual(response_body['purchases'][0]['total_items'], 1)
        self.assertEqual(response_body['purchases'][0]['total_price'], 1749.99)
        self.assertEqual(response_body['purchases'][0]['is_shipped'], True)
        self.assertEqual(response_body['purchases'][0]['timestamp'], str(date.today()))
        self.assertEqual(response_body['purchases'][1]['purchase_id'], 2)
        self.assertEqual(response_body['purchases'][1]['cart_id'], 1)
        self.assertEqual(response_body['purchases'][1]['total_items'], 1)
        self.assertEqual(response_body['purchases'][1]['total_price'], 1749.99)
        self.assertEqual(response_body['purchases'][1]['is_shipped'], True)
        self.assertEqual(response_body['purchases'][1]['timestamp'], str(date.today()))
        self.assertEqual(response_body['purchases'][2]['purchase_id'], 1)
        self.assertEqual(response_body['purchases'][2]['cart_id'], 1)
        self.assertEqual(response_body['purchases'][2]['total_items'], 1)
        self.assertEqual(response_body['purchases'][2]['total_price'], 1749.99)
        self.assertEqual(response_body['purchases'][2]['is_shipped'], True)
        self.assertEqual(response_body['purchases'][2]['timestamp'], str(date.today()))
        self.assertEqual(response.status_code, 200)

class RetrievePurchaseHistoryTestCase(RegisteredBuyersWithCartsTestCase):

    @classmethod
    def setUp(self):
        super().setUp()

        ProductCart(
            cart=self.cart,
            product=self.product
        ).save()
        Purchase(
            cart=self.cart,
            buyer=self.buyer
        ).save()
        self.cart.is_purchased = True
        self.cart.save(update_fields=['is_purchased'])

    def test_should_retrieve_purchased_cart_when_requested(self):
        response = self.client.get('/buyers/1/purchases/1/')

        response_body = response.json()
        self.assertEqual(response_body['purchase_id'], 1)
        self.assertEqual(response_body['cart_id'], 1)
        self.assertEqual(response_body['total_price'], 1749.99)
        self.assertIsNotNone(response_body['items'])
        self.assertEqual(len(response_body['items']), 1)
        self.assertEqual(response_body['items'][0]['product_id'], 1)
        self.assertEqual(response_body['items'][0]['name'], 'Cerebro')
        self.assertEqual(response_body['items'][0]['price'], 1749.99)
        self.assertEqual(response_body['items'][0]['short_description'], 'Read minds across the globe!')
        self.assertEqual(response_body['items'][0]['image'], 'http://localhost:8000/images/cerebro.jpg')
        self.assertEqual(response_body['items'][0]['num_items'], 1)
        self.assertEqual(response.status_code, 200)

class HttpMethodNotAllowedTestCase(BuyersTestCase):

    def test_should_return_405_code_when_http_method_is_not_allowed_in_register_buyer(self):
        first_response = self.client.get('/buyers/')
        second_response = self.client.put('/buyers/')
        third_response = self.client.patch('/buyers/')
        fourth_response = self.client.delete('/buyers/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_retrieve_buyer_information(self):
        first_response = self.client.post('/buyers/1/')
        second_response = self.client.put('/buyers/1/')
        third_response = self.client.patch('/buyers/1/')
        fourth_response = self.client.delete('/buyers/1/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_retrieve_cart(self):
        first_response = self.client.post('/buyers/1/cart/')
        second_response = self.client.put('/buyers/1/cart/')
        third_response = self.client.patch('/buyers/1/cart/')
        fourth_response = self.client.delete('/buyers/1/cart/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_add_item_to_cart(self):
        first_response = self.client.get('/buyers/1/cart/items/')
        second_response = self.client.put('/buyers/1/cart/items/')
        third_response = self.client.patch('/buyers/1/cart/items/')
        fourth_response = self.client.delete('/buyers/1/cart/items/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_update_and_delete_item_from_cart(self):
        first_response = self.client.get('/buyers/1/cart/items/1/')
        second_response = self.client.put('/buyers/1/cart/items/1/')
        third_response = self.client.patch('/buyers/1/cart/items/1/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_purchase_cart(self):
        first_response = self.client.get('/buyers/1/cart/purchase/')
        second_response = self.client.put('/buyers/1/cart/purchase/')
        third_response = self.client.patch('/buyers/1/cart/purchase/')
        fourth_response = self.client.delete('/buyers/1/cart/purchase/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)

    def test_should_return_405_code_when_http_method_is_not_allowed_in_retrieve_purchased_cart(self):
        first_response = self.client.post('/buyers/1/purchases/1/')
        second_response = self.client.put('/buyers/1/purchases/1/')
        third_response = self.client.patch('/buyers/1/purchases/1/')
        fourth_response = self.client.delete('/buyers/1/purchases/1/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
