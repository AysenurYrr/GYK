# Dinamik E-Ticaret Veri Analizi ve Öneri Sistemi

## 📌 Proje Açıklaması
Bu proje, bir e-ticaret firmasının müşteri satın alma davranışlarını analiz ederek **dinamik fiyatlandırma** ve **ürün öneri sistemi** geliştirmesini amaçlamaktadır. Veriler, **oluşturulan API'den** çekilecek ve **Pandas, NumPy** gibi kütüphaneler kullanılarak analiz edilecektir.

## 🚀 Adımlar

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
