from django.test import TransactionTestCase, Client
from .models import Product

class ProductsTestCase(TransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUp(self):
        self.client = Client()

        self.product_1 = Product(
            name='Cerebro',
            category='Cosmetics',
            price=1749.99,
            num_stocks=3,
            short_description='Read minds across the globe!',
            full_description='Cerebro is a fictional device appearing in American comic books published by Marvel Comics. The device is used by the X-Men (in particular, their leader, Professor Charles Xavier) to detect humans, specifically mutants.',
            image='http://localhost:8000/images/cerebro.jpg',
            seller=None
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
            seller=None
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
            seller=None
        )
        self.product_3.save()

    def test_all_products_should_be_present_when_retrieved(self):
        response = self.client.get('/products/')

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

    def test_server_should_return_405_with_wrong_HTTP_methods_for_retrieving_all_products(self):
        first_response = self.client.post('/products/')
        second_response = self.client.put('/products/')
        third_response = self.client.patch('/products/')
        fourth_response = self.client.delete('/products/')

        self.assertEqual(first_response.status_code, 405)
        self.assertEqual(second_response.status_code, 405)
        self.assertEqual(third_response.status_code, 405)
        self.assertEqual(fourth_response.status_code, 405)
