# 📙 Proje Kapsamı ve Yapılan Problemler

## 🎢 Problem 2: Ürün Kümeleme (Benzer Ürünler)

**Tablolar:** Products, OrderDetails

**Soru:**

> "Benzer sipariş geçmişine sahip ürünleri DBSCAN ile gruplandırın. Az satılan ya da alışılmadık kombinasyonlarda geçen ürünleri belirleyin."

**Çıkartılan Özellikler:**
- Ortalama satış fiyatı (`avg_price`)
- Satış sıklığı (`sales_count`)
- Sipariş başına ortalama miktar (`avg_quantity_per_order`)
- Kaç farklı müşteriye satıldı (`customer_count`)

**Amaç:**
- Benzer ürünlerin segmentasyonu.
- DBSCAN ile -1 kümesinde kalan ürünler → **niche ürünler** veya **özel kullanım ürünleri** olarak değerlendirildi.

---

## 🏢 Problem 3: Tedarikçi Segmentasyonu

**Tablolar:** Suppliers, Products, OrderDetails

**Soru:**

> "Tedarikçileri sağladıkları ürünlerin satış performansına göre gruplandırın. Az katkı sağlayan veya sıra dışı tedarikçileri bulun."

**Çıkartılan Özellikler:**
- Tedarik ettiği ürün sayısı (`product_count`)
- Toplam satış miktarı (`total_sales_quantity`)
- Ortalama satış fiyatı (`avg_price`)
- Ortalama müşteri sayısı (`avg_customer_count`)

**Amaç:**
- Tedarikçilerin performansa göre segmentasyonu.
- -1 kümesine düşen tedarikçiler → **düşük katkı sağlayan** veya **farklı davranış sergileyen** tedarikçiler olarak raporlandı.

---

## 🌎 Problem 4: Ülkelere Göre Satış Deseni Analizi

**Tablolar:** Customers, Orders, OrderDetails

**Soru:**

> "Farklı ülkelerden gelen siparişleri DBSCAN ile kümeleyin. Sıra dışı sipariş alışkanlığı olan ülkeleri tespit edin."

**Çıkartılan Özellikler:**
- Toplam sipariş sayısı (`total_orders`)
- Ortalama sipariş tutarı (`avg_order_value`)
- Sipariş başına ürün sayısı (`avg_products_per_order`)

**Amaç:**
- Ülkeleri sipariş davranışlarına göre gruplamak.
- Outlier çıkan ülkeler → **alışılmışın dışında tüketim alışkanlığına** sahip ülkeler olarak değerlendirildi.

---

## ⚙️ Yöntem ve İş Akışı

### 1. Veri Çekme
- SQL sorguları ile PostgreSQL veritabanından tablolar okunur.

### 2. Özellik Çıkarımı
- Sorulara uygun istatistiksel öznitelikler hesaplanır.

### 3. Ölçeklendirme
- `StandardScaler` ile tüm öznitelikler normalize edilir.

### 4. Optimal eps Bulma
- `FindOptimalEPS` fonksiyonu ile k-distance grafiği çizilir ve KneeLocator ile optimal eps belirlenir.

### 5. min_samples Seçimi
- `GridSearch` modülü kullanılarak farklı `min_samples` değerleri denenir.
- En iyi **Silhouette Score**'a sahip değer seçilir.

### 6. DBSCAN ile Kümeleme
- Optimal eps ve min_samples ile DBSCAN uygulanır.
  - -1 olanlar: **Outlier**
  - >=0 olanlar: **Cluster üyeleri**

### 7. PCA ile Görselleştirme
- Veriler 2 boyuta indirgenir ve matplotlib ile görünür hale getirilir.

### 8. API Üzerinden Sonuç Yayını
- FastAPI ile /cluster/products, /cluster/suppliers, /cluster/countries endpoint'leri sunulur.

---

## 🚀 API Endpointleri

| Yöntem | URL | Açıklama |
|:-------|:----|:---------|
| GET | `/` | API durum kontrolü |
| GET | `/cluster/products` | Ürün kümeleme sonuçları |
| GET | `/cluster/suppliers` | Tedarikçi kümeleme sonuçları |
| GET | `/cluster/countries` | Ülke bazlı sipariş kümeleme sonuçları |

---

## 📈 Başarım Ölçümü

- **Silhouette Score:** Küme ayrım kalitesi değerlendirmesi yapıldı.
- **Outlier Sayısı:** DBSCAN tarafından -1 olarak atanan veriler izlendi.

---

## 🧑‍💻 Geliştiriciler

- [Siladurtas](https://github.com/siladurtas)
- [Ucarrukiye](https://github.com/ucarrukiye)
- [AysenurYrr](https://github.com/AysenurYrr)
- [TulinBabalikKopmaz](https://github.com/TulinBabalikKopmaz)

---

