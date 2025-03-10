# Dinamik E-Ticaret Veri Analizi ve Öneri Sistemi

## 📌 Proje Açıklaması
Bu proje, bir e-ticaret firmasının müşteri satın alma davranışlarını analiz ederek **dinamik fiyatlandırma** ve **ürün öneri sistemi** geliştirmesini amaçlamaktadır. Veriler, **oluşturulan API'den** çekilecek ve **Pandas, NumPy** gibi kütüphaneler kullanılarak analiz edilecektir.

## Gereksinimler
Projeyi çalıştırmadan önce aşağıdaki gereksinimlerin sisteminizde yüklü olduğundan emin olun:

- [Node.js](https://nodejs.org/) (LTS sürümü önerilir)
- npm (Node.js ile birlikte gelir)


## Kurulum

1. **Depoyu klonlayın** (veya kendi JSON dosyanızı oluşturun):

   ```sh
   git clone <repo-link>
   cd <repo-name>
   ```

2. **Gerekli bağımlılıkları yükleyin:**

   ```sh
   npm install -g json-server
   ```

## API'yi Çalıştırma

Aşağıdaki komut ile `api.json` dosyanızı bir REST API olarak çalıştırabilirsiniz:

```sh
json-server --watch api.json
```

Bu komut, varsayılan olarak `http://localhost:3000` adresinde bir API sunucusu başlatacaktır.

## `api.json` İçeriği ve Yapısı

Bu API, çeşitli varlıkları içeren bir JSON veri tabanı simülasyonu sağlar. `api.json` dosyası aşağıdaki yapıyı içermektedir:

### 1. **Tablolar ve İçerikleri**
`api.json` toplam **7 tablo (koleksiyon)** içermektedir:

- **categories**: Ürün kategorilerini içerir.
- **suppliers**: Tedarikçileri içerir.
- **products**: Ürünlerin detaylarını içerir.
- **productSuppliers**: Ürün ve tedarikçilerin eşleşmelerini içerir.
- **customers**: Müşteri bilgilerini içerir.
- **carts**: Müşterilerin alışveriş sepetlerini içerir.
- **cartItems**: Sepete eklenen ürünleri içerir.

### 2. **Örnek İçerik**

#### **categories (Kategoriler)**
```json
{
  "categoryId": 1,
  "categoryName": "Electronics",
  "description": "Devices and gadgets"
}
```

#### **products (Ürünler)**
```json
{
  "id": "1",
  "categoryId": 1,
  "productName": "Smartphone",
  "description": "Latest model smartphone",
  "price": 7800,
  "stockQuantity": 50
}
```

#### **customers (Müşteriler)**
```json
{
    "customerId": 2,
    "customerName": "Aysenur Yorur",
    "customerEmail": "aysenuryorur0@gmail.com",
    "customerPhone": "+1234567890",
    "address": "123 Main St, City, Country",
    "createdAt": "2025-03-08T12:00:00Z"
}
```

## API Kullanımı

- **Tüm ürünleri listeleme:**
  ```sh
  GET http://localhost:3000/products
  ```

- **Belirli bir ürünü getirme:**
  ```sh
  GET http://localhost:3000/products/1
  ```

- **Yeni bir ürün ekleme:**
  ```sh
  POST http://localhost:3000/products
  Content-Type: application/json

  {
    "categoryId": 1,
    "productName": "Tablet",
    "description": "High-performance tablet",
    "price": 5000,
    "stockQuantity": 25
  }
  ```

- **Bir ürünü güncelleme:**
  ```sh
  PUT http://localhost:3000/products/1
  Content-Type: application/json

  {
    "productName": "Updated Smartphone"
  }
  ```

- **Bir ürünü silme:**
  ```sh
  DELETE http://localhost:3000/products/1
  ```

## JSON Server'ı Durdurma

JSON Server'ı durdurmak için terminalde `Ctrl + C` tuş kombinasyonunu kullanabilirsiniz.

Daha fazla bilgi için [JSON Server Dokümantasyonu](https://github.com/typicode/json-server) sayfasını ziyaret edebilirsiniz.

## 🚀 Proje İçeriği

### 1️⃣ API’den Veri Çekme
API’den aşağıdaki veriler alınacaktır:
- **Müşteri ID**
- **Ürün Adı**
- **Kategori**
- **Fiyat**
- **Satın Alma Tarihi**
- **Satın Alınan Miktar**
- **Müşteri Memnuniyeti Skoru**

### 2️⃣ Veri Manipülasyonu
- Eksik verilerin tespiti ve doldurulması
- Tarih formatlarının düzeltilmesi
- Belirli kategorilerde fiyat güncelleme
- Müşteri memnuniyetine göre en popüler ürünleri belirleme

### 3️⃣ Veri Analizi
- En çok satın alınan ürünleri belirleme
- Fiyat ve satış miktarı arasındaki korelasyonu inceleme
- Kategorilere göre ortalama fiyat hesaplama
- Belirli bir zaman diliminde en çok satılan ürünleri bulma
- Müşteri harcama seviyelerine göre gruplama yapma

### 4️⃣ Dinamik Fiyatlandırma
- Ürünlerin ortalama fiyatlarını hesaplayarak aşırı pahalı veya ucuz ürünleri belirleme
- Piyasadan belirli bir oranda düşük fiyatlı ürünlerin fiyatlarını güncelleme

### 5️⃣ Ürün Öneri Sistemi
- Müşterilere satın aldıkları ürünlere benzer en popüler ürünleri önerme
- Kategori bazlı ürün öneri sistemi geliştirme

## 📂 İçerikler
- [ ] API’den verileri çeken Python kodu
- [ ] Pandas ile veri manipülasyonu ve temizleme
- [ ] NumPy ile dinamik fiyatlandırma
- [ ] Veri analizi ve raporlama
- [ ] Ürün öneri sistemi

- json-server --watch api.json