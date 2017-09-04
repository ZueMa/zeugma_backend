# ZueMa API

ZueMa API is an API for amazon-like website.

## Authentication [/authentication]

### Sign in to the site [POST]

User can sign in to ZueMa site using username and password

+ Request (application/json)

        {
            "username": "jimmyXavier",
            "password": "12345678",
            "user_type": "buyer"
        }

+ Request (application/json)

        {
            "username": "fat_bender52",
            "password": "12345678",
            "user_type": "seller"
        }

+ Response 201 (application/json)

    + Body
            
            {
                "user_id": 1,
                "user_type": "buyer / seller"
            }

### Sign out from the site [DELETE]

User can sign out from ZueMa site

+ Response 204

## Buyers [/buyers]

### Register buyer [POST]

Buyer can register a new account to ZueMa site by filling the required information

+ Request (application/json)

        {
            "username": "jimmyXavier",
            "password": "12345678",
            "first_name": "James",
            "last_name": "McAvoy",
            "address": "100 Universal City Plaza, Universal City, Los Angeles"
        }

+ Response 204

## Current Buyer [/buyers/{buyer_id}]

### Retrieve current buyer [GET]

Buyer can request their own information

+ Response 200 (application/json)

    + Body
            
            {
                "buyer_id": 1,
                "username": "jimmyXavier",
                "first_name": "James",
                "last_name": "McAvoy",
                "address": "100 Universal City Plaza, Universal City, Los Angeles"
            }

## Buyer's Cart [/buyers/{buyer_id}/cart]

### Retrieve buyer's shopping cart [GET]

Buyer can request to view his/her shopping cart

+ Response 200 (application/json)

    + Body
            
            {
                "cart_id": 1,
                "total_items": 5,
                "total_price": 40499.95,
                "items": [
                    {
                        "product_id": 1,
                        "name": "Cerebro",
                        "price": 1749.99,
                        "num_stocks": 30,
                        "short_description": "Read minds across the globe!",
                        "image": "http://localhost:8000/images/cerebro.jpg",
                        "num_items": 3
                    },
                    {
                        "product_id": 3,
                        "name": "Web Shooters",
                        "price": 249.99,
                        "num_stocks": 320,
                        "short_description": "Shoot webs everywhere to accomplish your dreams!!",
                        "image": "http://localhost:8000/images/web_shooters.jpg",
                        "num_items": 1
                    },
                    {
                        "product_id": 5,
                        "name": "Waverider",
                        "price": 34999.99,
                        "num_stocks": 2,
                        "short_description": "Time-travel like a pro!",
                        "image": "http://localhost:8000/images/waverider.jpg",
                        "num_items": 1
                    }
                ]
            }

## Cart's Items [/buyers/{buyer_id}/cart/items]

### Add item to cart [POST]

Buyer can add item to his/her cart

+ Request (application/json)

        {
            "product_id": 1
        }

+ Response 204

+ Response 304

## Cart's Item Interaction [/buyer/{buyer_id}/cart/items/{item_id}]

### Update number of items in the cart [POST]

Buyer can update the number of items his/her cart

+ Request (application/json)

        {
            "action": "increase"
        }

+ Request (application/json)

        {
            "action": "decrease"
        }
    
+ Response 204

+ Response 304

### Delete cart's items [DELETE]

Buyer can delete an item from the cart

+ Response 204

## Buyer's Purchase Confirmation [/buyers/{buyer_id}/cart/purchase]

### Purchase shopping cart [POST]

Buyer can purchase the products in the shopping cart

+ Response 201 (application/json)

    + Body
            
            {
                "purchase_id": 1
            }

## Buyer's Purchase History [/buyers/{buyer_id}/purchases]

### Retrieve buyer's purchase history [GET]

Buyer can request his/her purchase history

+ Response 200 (application/json)

    + Body
            
            {
                "purchases": [
                    {
                        "purchase_id": 1,
                        "cart_id": 1,
                        "total_items": 5,
                        "total_price": 40499.95,
                        "is_shipped": true,
                        "timestamp": "2017-04-25"
                    },
                    {
                        "purchase_id": 2,
                        "cart_id": 2,
                        "total_items": 1,
                        "total_price": 2499.99,
                        "is_shipped": false,
                        "timestamp": "2017-05-14"
                    }
                ]
            }

## Buyer's Purchased Cart [/buyer/{buyer_id}/purchases/{purchase_id}]

### Retrieve buyer's purchased cart [GET]

Buyer can request a specific purchased cart

+ Response 200 (application/json)

    + Body
            
            {
                "purchase_id": 1,
                "cart_id": 1,
                "items": [
                    {
                        "product_id": 1,
                        "name": "Cerebro",
                        "price": 1749.99,
                        "short_description": "Read minds across the globe!",
                        "image": "http://localhost:8000/images/cerebro.jpg",
                        "num_items": 3
                    },
                    {
                        "product_id": 3,
                        "name": "Web Shooters",
                        "price": 249.99,
                        "short_description": "Shoot webs everywhere to accomplish your dreams!!",
                        "image": "http://localhost:8000/images/web_shooters.jpg",
                        "num_items": 1
                    },
                    {
                        "product_id": 5,
                        "name": "Waverider",
                        "price": 34999.99,
                        "short_description": "Time-travel like a pro!",
                        "image": "http://localhost:8000/images/waverider.jpg",
                        "num_items": 1
                    }
                ]
            }

## Sellers [/sellers]

### Register seller [POST]

Seller can register a new account to ZueMa site by filling the required information

+ Request 200 (application/json)

        {
            "username": "fat_bender52",
            "password": "12345678",
            "first_name": "Michael",
            "last_name": "Fassbender",
            "company_name": "The Brotherhood",
            "address": "900 Exposition Boulevard, Los Angeles",
            "description": "The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers."
        }
        
+ Response 204

## Current Seller [/sellers/{seller_id}]

### Retrieve current seller [GET]

Seller can request their own information

+ Response 200 (application/json)

    + Body
            
            {
                "seller_id": 1,
                "username": "fat_bender52",
                "first_name": "Michael",
                "last_name": "Fassbender",
                "company_name": "The Brotherhood",
                "address": "900 Exposition Boulevard, Los Angeles",
                "description": "The Brotherhood was founded by Magneto and its members were his primary allies in his early battles with the X-Men during the 1960s. The original Brotherhood ultimately disbanded, with Quicksilver and Scarlet Witch going on to become members of the Avengers."
            }

## Seller's Products [/sellers/{seller_id}/products]

### Retrieve seller's available products [GET]

Seller can request his/her products

+ Response 200 (application/json)

    + Body
            
            {
                "products": [
                    {
                        "product_id": 1,
                        "name": "Cerebro",
                        "category": "Cosmetics",
                        "price": 1749.99,
                        "short_description": "Read minds across the globe!",
                        "image": "http://localhost:8000/images/cerebro.jpg"
                    },
                    {
                        "product_id": 2,
                        "name": "Invisibility Cloak",
                        "category": "Clothes",
                        "price": 799.99,
                        "short_description": "Hide from anything, even death!",
                        "image": "http://localhost:8000/images/invisibility_cloak.jpg"
                    },
                    {
                        "product_id": 4,
                        "name": "Mjolnir",
                        "category": "Sports",
                        "price": 2499.99,
                        "short_description": "Weight-lifting like never before!",
                        "image": "http://localhost:8000/images/mjolnir.jpg"
                    }
                ]
            }

### Create new product [POST]

Seller can create new product

+ Request (application/json)

        {
            "name": "Web Shooters",
            "category": "Kids",
            "price": 299.99,
            "num_stocks": 220,
            "short_description": "Shoot webs everywhere to satisfy your childish dreams!",
            "full_description": "Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special 'web fluid' (the chemical composition of which is not known) at high pressure.",
            "image": "web_shooters.jpg"
        }

+ Response 201 (application/json)

    + Body
            
            {
                "product_id": 3
            }

## Seller's Product Interaction [/sellers/{seller_id}/products/{product_id}]

### Update Product Information [PUT]

Seller can update his/her product information

+ Request (application/json)

        {
            "name": "Web Shooters",
            "category": "Kids",
            "price": 249.99,
            "num_stocks": 320,
            "short_description": "Shoot webs everywhere to accomplish your dreams!",
            "full_description": "Web Shooters are twin devices, worn on your wrists beneath the gauntlets of your costume, that can shoot thin strands of a special 'web fluid' (the chemical composition of which is not known) at high pressure.",
            "image": "web_shooters.jpg"
        }
        
+ Response 204

### Delete Product [DELETE]

Seller can delete his/her product

+ Response 204

## Seller's Order History [/sellers/{seller_id}/orders]

### Retrieve seller's order history [GET]

Seller can request to view his/her order history

+ Response 200 (application/json)

    + Body
            
            {
                "orders": [
                    {
                        "order_id": 1,
                        "product_id": 1,
                        "name": "Cerebro",
                        "short_description": "Read minds across the globe!",
                        "image": "http://localhost:8000/images/cerebro.jpg",
                        "num_items": 3,
                        "revenue": 5249.97,
                        "timestamp": "2017-04-25"
                    },
                    {
                        "order_id": 3,
                        "product_id": 5,
                        "name": "Waverider",
                        "short_description": "Time-travel like a pro!",
                        "image": "http://localhost:8000/images/waverider.jpg",
                        "num_items": 1,
                        "revenue": 34999.99,
                        "timestamp": "2017-04-25"
                    },
                    {
                        "order_id": 4,
                        "product_id": 4,
                        "name": "Mjolnir",
                        "short_description": "Weight-lifting like never before!",
                        "image": "http://localhost:8000/images/mjolnir.jpg",
                        "num_items": 1,
                        "revenue": 2499.99,
                        "timestamp": "2017-05-14"
                    }
                ]
            }

## Products [/products]

### Retrieve all products [GET]

Retrieve all available products

+ Response 200 (application/json)

    + Body
            
            {
                "products": [
                    {
                        "product_id": 1,
                        "name": "Cerebro",
                        "category": "Cosmetics",
                        "price": 1749.99,
                        "short_description": "Read minds across the globe!",
                        "image": "http://localhost:8000/images/cerebro.jpg"
                    },
                    {
                        "product_id": 2,
                        "name": "Invisibility Cloak",
                        "category": "Clothes",
                        "price": 799.99,
                        "short_description": "Hide from anything, even death!",
                        "image": "http://localhost:8000/images/invisibility_cloak.jpg"
                    },
                    {
                        "product_id": 3,
                        "name": "Web Shooters",
                        "category": "Kids",
                        "price": 249.99,
                        "short_description": "Shoot webs everywhere to accomplish your dreams!",
                        "image": "http://localhost:8000/images/web_shooters.jpg"
                    },
                    {
                        "product_id": 4,
                        "name": "Mjolnir",
                        "category": "Sports",
                        "price": 2499.99,
                        "short_description": "Weight-lifting like never before!",
                        "image": "http://localhost:8000/images/mjolnir.jpg"
                    },
                    {
                        "product_id": 5,
                        "name": "Waverider",
                        "category": "Home & Garden",
                        "price": 34999.99,
                        "short_description": "Time-travel like a pro!",
                        "image": "http://localhost:8000/images/waverider.jpg"
                    },
                    {
                        "product_id": 6,
                        "name": "Cerebro",
                        "category": "Electronics",
                        "price": 1749.99,
                        "short_description": "Read minds across the globe!",
                        "image": "http://localhost:8000/images/cerebro.jpg"
                    },
                    {
                        "product_id": 7,
                        "name": "Invisibility Cloak",
                        "category": "Clothes",
                        "price": 799.99,
                        "short_description": "Hide from anything, even death!",
                        "image": "http://localhost:8000/images/invisibility_cloak.jpg"
                    },
                    {
                        "product_id": 8,
                        "name": "Web Shooters",
                        "category": "Kids",
                        "price": 249.99,
                        "short_description": "Shoot webs everywhere to accomplish your dreams!",
                        "image": "http://localhost:8000/images/web_shooters.jpg"
                    },
                    {
                        "product_id": 9,
                        "name": "Mjolnir",
                        "category": "Sports",
                        "price": 2499.99,
                        "short_description": "Weight-lifting like never before!",
                        "image": "http://localhost:8000/images/mjolnir.jpg"
                    },
                    {
                        "product_id": 10,
                        "name": "Waverider",
                        "category": "Home & Garden",
                        "price": 34999.99,
                        "short_description": "Time-travel like a pro!",
                        "image": "http://localhost:8000/images/waverider.jpg"
                    },
                    {
                        "product_id": 11,
                        "name": "Cerebro",
                        "category": "Cosmetics",
                        "price": 1749.99,
                        "short_description": "Read minds across the globe!",
                        "image": "http://localhost:8000/images/cerebro.jpg"
                    },
                    {
                        "product_id": 12,
                        "name": "Invisibility Cloak",
                        "category": "Clothes",
                        "price": 799.99,
                        "short_description": "Hide from anything, even death!",
                        "image": "http://localhost:8000/images/invisibility_cloak.jpg"
                    },
                    {
                        "product_id": 13,
                        "name": "Web Shooters",
                        "category": "Kids",
                        "price": 249.99,
                        "short_description": "Shoot webs everywhere to accomplish your dreams!",
                        "image": "http://localhost:8000/images/web_shooters.jpg"
                    },
                    {
                        "product_id": 14,
                        "name": "Mjolnir",
                        "category": "Sports",
                        "price": 2499.99,
                        "short_description": "Weight-lifting like never before!",
                        "image": "http://localhost:8000/images/mjolnir.jpg"
                    },
                    {
                        "product_id": 15,
                        "name": "Waverider",
                        "category": "Electronics",
                        "price": 34999.99,
                        "short_description": "Time-travel like a pro!",
                        "image": "http://localhost:8000/images/waverider.jpg"
                    }
                ]
            }

## Specific Product [/products/{product_id}]

### Retrieve product's information [GET]

Retrieve product's information (e.g. price, description)

+ Response 200 (application/json)

    + Body
            
            {
                "product_id": 1,
                "name": "Cerebro",
                "category": "Cosmetics",
                "price": 1749.99,
                "num_stocks": 30,
                "short_description": "Read minds across the globe!",
                "full_description": "Cerebro is a fictional device appearing in American comic books published by Marvel Comics. The device is used by the X-Men (in particular, their leader, Professor Charles Xavier) to detect humans, specifically mutants.",
                "image": "http://localhost:8000/images/cerebro.jpg"
            }
