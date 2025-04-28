
"""
ürün kategori sepet kullanıcı sipariş sipariş detayı
Bir e ticaret sitesi için ilişkili sınıflar oluşturunuz.
Product, Category, Cart, User, Order, OrderDetail
1 siparişte 10 ürün olarbilir OrderDetail budur. 
"""

class User():
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

class Product:
    def __init__(self, product_id, name, price, category):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category

class Category():
    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name

class Cart():
    def __init__(self, products, user):
        self.products = products
        self.user = user

class Order():
    def __init__(self, order_id, user, order_details):
        self.order_id = order_id
        self.user = user
        self.order_details = order_details

class OrderDetail():
    def __init__(self, order_detail_id, order, product, quantity):
        self.order_detail_id = order_detail_id
        self.order = order
        self.product = product
        self.quantity = quantity

category1 = Category(1, "Elektronik")
category2 = Category(2, "Giyim")

product1 = Product(1, "Laptop", 5000, category1)
product2 = Product(2, "Telefon", 3000, category1)
product3 = Product(3, "T-shirt", 50, category2)
product4 = Product(4, "Pantolon", 100, category2)

user1 = User(1, "Ahmet", "ahemt@gmail.com")
user2 = User(2, "Mehmet", "mehmet@gmail.com")

cart1 = Cart([product1, product2], user1)
cart2 = Cart([product3, product4], user2)

order_detail1 = OrderDetail(1, 1, product1, 2)
order_detail2 = OrderDetail(2, 1, product2, 1)
order_detail3 = OrderDetail(3, 2, product3, 3)
order_detail4 = OrderDetail(4, 2, product4, 2)

order1 = Order(1, user1, [order_detail1, order_detail2])
order2 = Order(2, user2, [order_detail3, order_detail4])
order3 = Order(3, user1, [order_detail1, order_detail2, order_detail3, order_detail4])

print(order1.order_details[0].product.name)  # Laptop
print(order2.order_details[0].product.name)  # T-shirt
print(order3.order_details[3].product.name)  # Laptop

print(cart1.products[0].name)  # Laptop
print(cart2.products[0].name)  # T-shirt
print(user1.name)  # Ahmet

print