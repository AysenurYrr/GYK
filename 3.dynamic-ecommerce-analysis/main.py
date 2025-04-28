import pandas as pd
import requests

def fetch_data(api_urls):
    """
    Belirtilen API URL'lerinden veri çeker, pandas DataFrame'e dönüştürür
    ve bir sözlükte saklar.

    :param api_urls: API URL'lerini içeren liste (list)
    :return: API isimlerini key olarak kullanarak DataFrame'leri saklayan bir sözlük (dict)
    """
    dataframes = {}
    for url in api_urls:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            api_name = url.split("/")[-1]  # API ismini key olarak kullan
            dataframes[api_name] = df  
            #print(f"{url} adresinden veri başarıyla çekildi!")
        else:
            print(f"HATA: {url} adresinden veri çekilemedi! Status Code: {response.status_code}")
    
    return dataframes

def update_category_prices(dataframes, category_name, percentage, api_base_url):
    """
    Belirtilen kategoriye ait ürünlerin fiyatlarını zam miktarına göre günceller.

    :param dataframes: API'den çekilen verileri içeren DataFrame sözlüğü
    :param category_name: Güncellemek istenen kategori adı (str)
    :param percentage: Zam oranı, indirim oranı (örneğin: 1.1 -> %10 zam) (float)
    :param api_base_url: API'nin ana URL'si (str)
    """
    # **1. Kategori ID'lerini Al**
    category_id = dataframes["categories"].loc[
        dataframes["categories"]["categoryName"] == category_name, "categoryId"
    ].squeeze()  # Tek bir değer almak için squeeze()

    if pd.isna(category_id):  # Eğer kategori bulunamazsa
        print(f"HATA: '{category_name}' kategorisi bulunamadı!")
        return dataframes


    # **2. İlgili Kategorideki Ürünleri Seç**
    category_products = dataframes["products"].loc[
        dataframes["products"]["categoryId"] == category_id
    ]

    if category_products.empty:
        print(f"HATA: '{category_name}' kategorisine ait ürün bulunamadı!")
        return dataframes

    print(f"\nKategori '{category_name}' ID {category_id}, içindeki ürünler:")
    print(category_products[['id', 'productName', 'price']])

    # **3. Fiyatları API üzerinden güncelle**
    for _, row in category_products.iterrows():
        product_id = row["id"]
        new_price = round(row["price"] * percentage, 2)  # Zam oranını uygula

        # API'ye güncelleme isteği gönder
        update_url = f"{api_base_url}/products/{product_id}"
        response = requests.patch(update_url, json={"price": new_price}, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            pass  # Başarılı güncelleme
        else:
            print(f"HATA: Ürün ID {product_id} güncellenemedi! {response.status_code}, {response.text}")
    
    return fetch_data(api_urls)  # Güncellenmiş veriyi tekrar çek

def get_top_products(top_n=5, api_url="http://localhost:3000/products"):
    """
    Müşteri memnuniyeti puanlarına göre en popüler ürünleri belirler.

    :param api_url: Ürünleri çekeceğimiz API'nin URL'si (str)
    :param top_n: Kaç tane en popüler ürünü göstermek istediğimiz (int, default=5)
    :return: En yüksek memnuniyet puanına sahip ürünlerin DataFrame'i
    """
    # API'den ürün verisini çek
    response = requests.get(api_url)
    
    if response.status_code == 200:
        products = response.json()
        df = pd.DataFrame(products)

        # `satisfactionScore` sütununun eksik olmadığı verileri filtrele
        df = df.dropna(subset=["satisfactionScore"])

        # `satisfactionScore` değerine göre azalan sırayla sırala
        top_products = df.sort_values(by="satisfactionScore", ascending=False).head(top_n)

        # En popüler ürünleri göster
        print(f"\nEn Popüler {top_n} Ürün:")
        print(top_products[["id", "productName", "price", "satisfactionScore"]])

        return top_products
    else:
        print(f"HATA: API'den veri çekilemedi! Status Code: {response.status_code}")
        return None

def category_based_recommendation(dataframes, customer_id):
    """
    Generates category-based product recommendations for a given customer based on their purchase history.

    :param dataframes: Dictionary containing the required data tables.
    :param customer_id: The customer ID for whom recommendations are to be generated.
    :return: DataFrame containing the top recommended products.
    """
    # Merge cart items with carts to obtain customer purchases
    customer_cart_items = dataframes["cartItems"].merge(
        dataframes["carts"], left_on="cartId", right_on="cartId"
    )
    
    # Filter purchases for the specified customer
    customer_cart = customer_cart_items[customer_cart_items["customerId"] == customer_id]
    
    # Merge customer cart with products to get categoryId
    customer_cart = customer_cart.merge(
        dataframes["products"][["categoryId"]], left_on="productId", right_on="categoryId", how="left"
    )
    # Drop duplicate category entries
    customer_cart = customer_cart.drop_duplicates()
    
    # Identify the most common category purchased by the customer
    most_common_category_id = customer_cart["categoryId"].mode()[0]
    
    # Filter products within the most common category
    category_products = dataframes["products"][dataframes["products"]["categoryId"] == most_common_category_id]
    
    # Select products with the highest satisfaction score
    recommended_products = category_products.sort_values(by="satisfactionScore", ascending=False)
    
    return recommended_products

def get_top_selling_products(start_date, end_date, dataframes, top_n=5):
    """
    Belirtilen tarih aralığında en çok satılan ürünleri belirler.

    :param start_date: Başlangıç tarihi (str, "YYYY-MM-DD")
    :param end_date: Bitiş tarihi (str, "YYYY-MM-DD")
    :param dataframes: API'den çekilen verileri içeren DataFrame sözlüğü
    :param top_n: En çok satılan kaç ürünü göstermek istediğimiz (int, default=5)
    :return: En çok satılan ürünlerin DataFrame'i
    """
    # Satın alma tarihine göre filtreleme
    filtered_carts = dataframes["carts"][
        (dataframes["carts"]["purchaseDate"] >= start_date) &
        (dataframes["carts"]["purchaseDate"] <= end_date)
    ]

    if filtered_carts.empty:
        print("Belirtilen tarihler arasında satış bulunamadı.")
        return None

    # Geçerli sepet ID'lerini al
    cart_ids = filtered_carts["cartId"]

    # İlgili sepetlerdeki ürünleri çek
    filtered_cart_items = dataframes["cartItems"][dataframes["cartItems"]["cartId"].isin(cart_ids)]

    if filtered_cart_items.empty:
        print("Belirtilen tarihler arasında ürün satışı bulunamadı.")
        return None

    # Ürün bazında toplam satılan miktarı hesapla
    top_selling = (
        filtered_cart_items.groupby("productId")["quantity"]
        .sum()
        .reset_index()
        .sort_values(by="quantity", ascending=False)
        .head(top_n)
    )

    # ** Veri Türlerini Düzeltme ** #
    # productId ve id'nin aynı türde olması gerekiyor
    top_selling["productId"] = top_selling["productId"].astype(str)  # productId'yi string'e çevir
    dataframes["products"]["id"] = dataframes["products"]["id"].astype(str)  # products.id'yi string'e çevir

    # Ürün adlarını `products` tablosundan çek
    products_df = dataframes["products"][["id", "productName"]]
    top_selling = top_selling.merge(products_df, left_on="productId", right_on="id").drop(columns=["id"])

    print(f"\n{start_date} ile {end_date} arasındaki en çok satılan {top_n} ürün:")
    print(top_selling,"\n\n")

    return top_selling

def classify_product_prices(dataframes, threshold=0.1):
    """
    Classifies product prices as "Below Average", "Normal", or "Above Average"
    based on a given threshold percentage.

    :param dataframes: Dictionary containing the "products" DataFrame.
    :param threshold: Percentage threshold for classification (default: 10%).
    :return: Updated products DataFrame with price classification.
    """

    def classify_price(row):
        lower_bound = row["price_mean"] * (1 - threshold)
        upper_bound = row["price_mean"] * (1 + threshold)

        if row["price"] < lower_bound:
            return "Below Average"
        elif row["price"] > upper_bound:
            return "Above Average"
        else:
            return "Normal"

    # Extract the 'products' DataFrame
    products = dataframes["products"].copy()

    # Strip whitespace from product names
    products["productName"] = products["productName"].str.strip()

    # Calculate the mean price for each product by its name
    mean_prices = products.groupby("productName")["price"].mean().reset_index()

    # Merge the mean prices with the original products DataFrame
    products = products.merge(mean_prices, on="productName", suffixes=("", "_mean"))

    # Apply classification
    products["price_comparison"] = products.apply(classify_price, axis=1)

    dataframes["products"] = products

    return dataframes

def update_below_above_average_prices(products, api_base_url):
    """
    "Below Average" olarak sınıflandırılan ürünlerin fiyatlarını %10 artırır
    ve "Above Average" olarak sınıflandırılanların fiyatlarını %10 azaltır.

    :param products: Ürünleri içeren DataFrame.
    :param api_base_url: API'nin temel URL'si.
    :return: None
    """
    
    # "Below Average" kategorisindeki ürünleri seç
    below_average_products = products.loc[products["price_comparison"] == "Below Average"]
    
    # "Above Average" kategorisindeki ürünleri seç
    above_average_products = products.loc[products["price_comparison"] == "Above Average"]

    # "Below Average" ürünlerin fiyatlarını %10 artır
    for _, row in below_average_products.iterrows():
        product_id = row["id"]
        new_price = round(row["price"] * 1.1, 2)  # Fiyatı %10 artır
        
        # API'ye güncelleme isteği gönder
        update_url = f"{api_base_url}/products/{product_id}"
        response = requests.patch(update_url, json={"price": new_price}, headers={"Content-Type": "application/json"})

        # Güncelleme sonucunu kontrol et
        if response.status_code != 200:
            print(f"HATA: Ürün ID {product_id} güncellenemedi! {response.status_code}, {response.text}")
        else:
            print(f"Ürün ID {product_id} fiyatı güncellendi!")

    # "Above Average" ürünlerin fiyatlarını %10 azalt
    for _, row in above_average_products.iterrows():
        product_id = row["id"]
        new_price = round(row["price"] * 0.9, 2)  # Fiyatı %10 azalt
        
        # API'ye güncelleme isteği gönder
        update_url = f"{api_base_url}/products/{product_id}"
        response = requests.patch(update_url, json={"price": new_price}, headers={"Content-Type": "application/json"})

        # Güncelleme sonucunu kontrol et
        if response.status_code != 200:
            print(f"HATA: Ürün ID {product_id} güncellenemedi! {response.status_code}, {response.text}")
        else:
            print(f"Ürün ID {product_id} fiyatı güncellendi!")

    # Güncellenmiş verileri getir
    return fetch_data(api_urls)


# API URL'leri
api_urls = [
    "http://localhost:3000/categories",
    "http://localhost:3000/suppliers",
    "http://localhost:3000/products",
    "http://localhost:3000/productSuppliers",
    "http://localhost:3000/customers",
    "http://localhost:3000/carts",
    "http://localhost:3000/cartItems"
]

# 1: API’den Veri Çekme Öğrenciler, kendi oluşturacakları API’den şu bilgileri almalıdır:
# Müşteri ID, Ürün Adı, Kategori, Fiyat, Satın Alma Tarihi, Satın Alınan Miktar, Müşteri, Memnuniyeti Skoru
# Verileri çek
dataframes = fetch_data(api_urls) # Görev Tamamlandı


# 2: Veri Manipülasyonu ---------------------------------------------------------
# API’den gelen veriyi Pandas kullanarak işleyin ve aşağıdaki işlemleri gerçekleştirin:

## 2.1: Eksik verileri tespit edip doldurma veya kaldırma
#Eksik veri sayısı
print("\nEksik Veri Sayısı:")
print(dataframes['products'].isnull().sum())  # Görev Tamamlandı

## 2.2: Tarih formatlarını uygun hale getirme
# Tarih sütununu dönüştür
print("\n\nTarih formatını düzenlemeden önce:\n",dataframes["carts"])
dataframes["carts"]["purchaseDate"] = pd.to_datetime(dataframes["carts"]["purchaseDate"], errors='coerce') # Görev Tamamlandı
print("Tarih formatını düzenledikten sonra:\n",dataframes["carts"])
## 2.3:Belirli kategorilerde fiyat güncelleme
# Kategorilerde Güncellemeleri yap
print("\nKategori Fiyat Güncelleme Öncesi:")
print(dataframes["products"][["productName","price"]])  # Görev Tamamlandı
dataframes = update_category_prices(dataframes, "Electronics", 1.1, "http://localhost:3000")        # Görev Tamamlandı
dataframes = update_category_prices(dataframes, "Home Appliances", 0.95, "http://localhost:3000")   # Görev Tamamlandı
print("\nKategori Fiyat Güncelleme Sonrası:")
print(dataframes["products"][["productName","price"]])  # Görev Tamamlandı

## 2.4: Müşteri memnuniyeti puanlarını analiz ederek en popüler ürünleri belirleme
# Fonksiyonu çağır ve en popüler 2 ürünü getir
top_products_df = get_top_products(2, "http://localhost:3000/products")    # Görev Tamamlandı

# 3: Veri Analizi ---------------------------------------------------------
# Aşağıdaki analizleri gerçekleştirin:

# 3.1: En çok satın alınan ürünleri belirleyin
cart_items = pd.DataFrame(dataframes["cartItems"])
most_purchased = cart_items.loc[cart_items["quantity"].idxmax()]
print("\nEn Çok Satın Alınan Ürünler:\n{}\n".format(most_purchased))

# 3.2: Fiyat ve satış miktarı arasındaki korelasyonu inceleyin
products = pd.DataFrame(dataframes["products"])
correlation = products["price"].corr(cart_items["quantity"])
print("\nFiyat ve Satış Miktarı Arasındaki Korelasyon: ", correlation) 

# 3.3: Kategorilere göre ortalama fiyat hesaplayın
products = pd.DataFrame(dataframes["products"])
category_prices = products.groupby('categoryId')['price'].mean()
print("\nKategorilere Göre Ortalama Fiyatlar:\n", category_prices)  

# 3.4: Belirli bir zaman diliminde en çok satılan ürünleri bulun
# Örnek kullanım:
top_selling_products = get_top_selling_products("2025-03-08", "2025-12-31", dataframes, top_n=5)

# 3.5: Müşteri harcama seviyelerine göre gruplama yapın
# Gruplama yap
# API URL'leri
carts_url = "http://localhost:3000/carts"
cart_items_url = "http://localhost:3000/cartItems"
products_url = "http://localhost:3000/products"
customers_url = "http://localhost:3000/customers"

# API'den verileri çekme
response_carts = requests.get(carts_url)
carts_data = response_carts.json()

response_cart_items = requests.get(cart_items_url)
cart_items_data = response_cart_items.json()

response_customers = requests.get(customers_url)
customers_data = response_customers.json()

# Verileri pandas DataFrame'e dönüştürme
df_carts = pd.DataFrame(carts_data)
df_cart_items = pd.DataFrame(cart_items_data)
df_customers = pd.DataFrame(customers_data)

# Verileri birleştirme (cartItems ile carts)
df_sales = df_cart_items.merge(df_carts[['cartId', 'customerId', 'totalPrice']], on='cartId')

# Müşterilerin toplam harcamasını hesaplama
df_total_spent = df_sales.groupby('customerId')['totalPrice'].sum().reset_index()

# Müşteri bilgilerini ekleme
df_total_spent = df_total_spent.merge(df_customers[['customerId', 'customerName']], on='customerId')

# Harcama seviyelerini belirleme
def categorize_spending(row):
    if row['totalPrice'] < 500:
        return 'Low'
    elif row['totalPrice'] < 1000:
        return 'Medium'
    else:
        return 'High'

df_total_spent['SpendingLevel'] = df_total_spent.apply(categorize_spending, axis=1)

# Gruplama yapma
df_grouped = df_total_spent.groupby('SpendingLevel').agg(
    total_customers=('customerId', 'count'),
    total_spent=('totalPrice', 'sum')
).reset_index()

# Sonuçları yazdırma
print("\nMüşteri Harcama Seviyelerine Göre Gruplama:")
print(df_grouped)


# 4: Dinamik Fiyatlandırma ---------------------------------------------------------
# 4.1: Ürünlerin ortalama fiyatlarını hesaplayarak aşırı pahalı veya ucuz ürünleri belirleyin

dataframes = classify_product_prices(dataframes, threshold=0.1)
print("\nÜrünlerin Fiyat Karşılaştırması:")
print(dataframes["products"][["productName","price","price_comparison"]])

# 4.2: Piyasadan belirli bir oranda düşük fiyatlı ürünlerin fiyatını güncelleyin
dataframes = update_below_above_average_prices(dataframes["products"], "http://localhost:3000")
print("\nÜrünlerin Fiyat Güncellenme Sonrası:")
print(dataframes["products"][["productName","price"]])

# 5: Ürün Öneri Sistemi
# 5.1: Müşterilere, satın aldıkları ürünlere benzer en popüler ürünleri önerin
#cartItems tablosunu al
cart_items = dataframes["cartItems"]

#Ürünlerin satış miktarlarını hesapla
product_sales = cart_items.groupby('productId').agg({'quantity': 'sum'}).reset_index()

#Popüler ürünleri belirle (en fazla satılan ürünler)
popular_products = product_sales.sort_values(by='quantity', ascending=False)

#İlk 5 en popüler ürünü göster
print("\nEn Popüler Ürünler:")
print(popular_products.head())

# 5.2: Öneri sistemini kategori bazında geliştirin
recommended_products = category_based_recommendation(dataframes, 1)
print("\nKullanıcının satın aldığıklarına göre kategori bazında önerilen ürünler:")
print(recommended_products.head(3))

"""
# Teslim Edilecekler
- API'den verileri çeken Python kodu
- Pandas ile veri manipülasyonu ve temizlemesi
- NumPy ile dinamik fiyatlandırma
- Veri analizi ve raporlama
- Ürün öneri sistemi
"""