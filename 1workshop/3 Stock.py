stock = [
{"category": "Meyve", "items": [{"name": "Elma", "price": 10, "quantity": 50}, {"name": "Muz", "price": 15, "quantity": 30}]},
{"category": "Sebze", "items": [{"name": "Domates", "price": 8, "quantity": 60}, {"name": "Patates", "price": 5, "quantity": 100}]},
{"category": "İçecek", "items": [{"name": "Maden Suyu", "price": 3, "quantity": 150}, {"name": "Kola", "price": 12, "quantity": 80}]}
]

#4 Stok miktarı en düşük olan ürünü bulun.
def min_stock():
    min_quantity = stock[0]["items"][0]["quantity"]
    min_item = stock[0]["items"][0]
    for category in stock:
        for item in category["items"]:
            if item["quantity"] < min_quantity:
                min_quantity = item["quantity"]
                min_item = item
    return min_item

print(min_stock())

 # {'name': 'Muz', 'price': 15, 'quantity': 30}
