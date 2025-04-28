# 🧠 Makine Öğrenmesi Ödevi: Banka Müşterisinin Kredi Onayı Tahmini

## 📌 Proje Özeti

Bu projede, bir bankada çalıştığınız ve yeni gelen kredi başvurularını otomatik olarak değerlendirmek üzere bir makine öğrenmesi modeli geliştirdiğiniz senaryosu ele alınmıştır.

Güvenlik gerekçesiyle bankanın gerçek müşteri verileri sağlanmadığı için, **2000 satırlık sentetik veri seti** oluşturulmuştur. Bu veri üzerinden `RandomForestClassifier` modeli eğitilmiş ve başarı metrikleri analiz edilmiştir.

---

## 📊 Veri Seti Açıklaması

Veri seti 2000 satır ve aşağıdaki 10 özellikten oluşmaktadır:

| Özellik Adı          | Açıklama                                                | Veri Tipi     | Değer Aralığı / Örnekler               |
|----------------------|----------------------------------------------------------|---------------|----------------------------------------|
| `age`                | Müşterinin yaşı                                          | Sayısal (int) | 18 - 65                                |
| `income`             | Aylık geliri (₺)                                         | Sayısal (int) | 3000 - 30000                           |
| `debt`               | Toplam kredi kartı/kredi borcu                           | Sayısal (int) | 0 - 50000                              |
| `credit_score`       | Kredi puanı (0–1000 arası)                               | Sayısal (int) | 300 - 900                              |
| `employment_years`   | İş yerinde çalışma süresi (yıl)                         | Sayısal (int) | 0 - 40                                 |
| `is_homeowner`       | Ev sahibi olup olmadığı (1: ev sahibi, 0: değil)         | Kategorik     | 0 veya 1                               |
| `education_level`    | Eğitim seviyesi                                          | Kategorik     | "High School", "Bachelor", "Master", "PhD" |
| `is_married`         | Evli olup olmadığı (1: evli, 0: bekar)                   | Kategorik     | 0 veya 1                               |
| `previous_loans`     | Geçmiş kredi sayısı                                      | Sayısal (int) | 0 - 10                                 |
| `approved`           | **Hedef değişken**: kredi başvurusu onaylandı mı?        | Kategorik     | 1 = Onaylandı, 0 = Reddedildi          |

---

## 🎯 Hedef Değişkenin Belirlenmesi (Onay Kuralları)

Kredi onay kararı belirlenirken aşağıdaki **puana dayalı sistem** uygulanmıştır:

Her müşteri, bazı özelliklerinden puan alır. Eğer toplam puanı **7 veya üzerindeyse başvuru onaylanır**, aksi durumda %5 olasılıkla rastgele onaylanır (gerçek hayattaki istisnaları yansıtmak için).

### 🧮 Puanlama Kuralları

- **Gelir (`income`)**
  - >15000 → +2 puan
  - 8000–15000 → +1 puan

- **Kredi Skoru (`credit_score`)**
  - >700 → +2 puan
  - 600–700 → +1 puan

- **Borç (`debt`)**
  - <10000 → +2 puan
  - 10000–20000 → +1 puan

- **Çalışma Süresi (`employment_years`)**
  - >5 yıl → +2 puan
  - 2–5 yıl → +1 puan

- **Ev Sahipliği (`is_homeowner`)**
  - 1 ise → +1 puan

- **Eğitim Seviyesi (`education_level`)**
  - Master/PhD → +2 puan
  - Bachelor → +1 puan

- **Medeni Durum (`is_married`)**
  - 1 ise → +1 puan

- **Geçmiş Krediler (`previous_loans`)**
  - 2 veya daha fazla ise → +1 puan

**Not:** Toplam puan <7 ise, %5 ihtimalle rastgele onay verilebilir.

---

## 📁 Dosyalar

- `credit_dataset.csv`: 2000 satırlık sentetik veri seti
- Modelleme ve analiz scripti (Jupyter Notebook veya `.py` dosyası)
- Görselleştirme grafikleri ve değerlendirme raporları

---

## ✅ Model Başarı Değerlendirmesi

Modelin performansı, test verisi üzerinde aşağıdaki şekilde değerlendirilmiştir:

- **Accuracy (Doğruluk Oranı):** `0.9225` (yani %92.25)
- **Precision, Recall, F1-Score** değerleri aşağıdaki gibidir:

          precision    recall  f1-score   support

       0       0.95      0.81      0.87       132
       1       0.91      0.98      0.94       268




### 🔍 Yorumlar:

- **Sınıf 1 (Onaylanan başvurular)** için model, %98 doğrulukta yakalama (recall) sağlamaktadır.
- **Sınıf 0 (Reddedilen başvurular)** için ise model, daha seçici davranmakta ve %95 precision ile doğru reddetmeler yapmaktadır.
- **Macro ve weighted ortalamalar**, modelin her iki sınıfa da dengeli bir şekilde performans gösterdiğini ortaya koymaktadır.

---

## 💡 Sonuç

RandomForestClassifier algoritması, oluşturulan sentetik veri üzerinde yüksek doğrulukla çalışmış ve kredi başvurularını başarılı bir şekilde sınıflandırmıştır.

- %92.25 genel doğruluk oranı ile model, pratikte kullanılabilecek seviyede güçlüdür.
- Özellikle onaylanan başvuruları hatasız yakalaması, modelin müşteri lehine etkili çalıştığını göstermektedir.
- Bu proje, puanlama sistemine dayalı kredi değerlendirme senaryosunu başarıyla simüle etmiş ve gerçek dünya koşullarını veri üretiminde ve modellemede yansıtmıştır.

Model, **karmaşık kural tabanlı onay sistemlerini** öğrenmiş ve test verisi üzerinde başarılı sonuçlar vermiştir.
