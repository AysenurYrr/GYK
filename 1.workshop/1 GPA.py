# Mevcut bilgiler
current_gpa = 3.72
total_credits = 137

# Mevcut toplam ağırlıklı not
current_weighted_sum = total_credits * current_gpa

# Değişecek dersin bilgileri
course_credits = 3
cc_grade = 2.5  # CC'nin katsayısı
aa_grade = 4.0  # AA'nın katsayısı

# Yeni ağırlıklı toplamı hesapla
new_weighted_sum = current_weighted_sum - (course_credits * cc_grade) + (course_credits * aa_grade)

# Yeni ortalama
new_gpa = new_weighted_sum / total_credits

print(new_gpa)
