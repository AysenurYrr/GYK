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

    print(f"\nKategori '{category_name}' için Kategori ID'leri: {category_id}")

    # **2. İlgili Kategorideki Ürünleri Seç**
    category_products = dataframes["products"].loc[
        dataframes["products"]["categoryId"] == category_id
    ]

    if category_products.empty:
        print(f"HATA: '{category_name}' kategorisine ait ürün bulunamadı!")
        return dataframes

    print(f"\nKategori '{category_name}' ID {category_id} içindeki ürünler:")
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

## 2.2: Tarih formatlarını uygun hale getirme
# Tarih sütununu dönüştür
dataframes["carts"]["purchaseDate"] = pd.to_datetime(dataframes["carts"]["purchaseDate"], errors='coerce') # Görev Tamamlandı

## 2.3:Belirli kategorilerde fiyat güncelleme
# Kategorilerde Güncellemeleri yap
dataframes = update_category_prices(dataframes, "Electronics", 1.1, "http://localhost:3000")        # Görev Tamamlandı
dataframes = update_category_prices(dataframes, "Home Appliances", 0.95, "http://localhost:3000")   # Görev Tamamlandı

## 2.4: Müşteri memnuniyeti puanlarını analiz ederek en popüler ürünleri belirleme
# Fonksiyonu çağır ve en popüler 5 ürünü getir
top_products_df = get_top_products(2, "http://localhost:3000/products")    # Görev Tamamlandı


# 3: Veri Analizi ---------------------------------------------------------
# Aşağıdaki analizleri gerçekleştirin:
# 3.1: En çok satın alınan ürünleri belirleyin
# 3.2: Fiyat ve satış miktarı arasındaki korelasyonu inceleyin
# 3.3: Kategorilere göre ortalama fiyat hesaplayın
# 3.3: Belirli bir zaman diliminde en çok satılan ürünleri bulun
# 3.4: Müşteri harcama seviyelerine göre gruplama yapın

# 4: Dinamik Fiyatlandırma ---------------------------------------------------------
# 4.1: Ürünlerin ortalama fiyatlarını hesaplayarak aşırı pahalı veya ucuz ürünleri belirleyin
# 4.2: Piyasadan belirli bir oranda düşük fiyatlı ürünlerin fiyatını güncelleyin

# 5: Ürün Öneri Sistemi
# 5.1: Müşterilere, satın aldıkları ürünlere benzer en popüler ürünleri önerin
# 5.2: Öneri sistemini kategori bazında geliştirin


""" 
# Teslim Edilecekler
- API'den verileri çeken Python kodu
- Pandas ile veri manipülasyonu ve temizlemesi
- NumPy ile dinamik fiyatlandırma
- Veri analizi ve raporlama
- Ürün öneri sistemi
"""