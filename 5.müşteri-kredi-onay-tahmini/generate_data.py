import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

num_samples = 2000

# Temel sayısal özellikler
age = np.random.randint(18, 66, num_samples)
income = np.random.randint(3000, 30001, num_samples)
debt = np.random.randint(0, 50001, num_samples)
credit_score = np.random.randint(300, 901, num_samples)
employment_years = np.random.randint(0, 41, num_samples)

# Yeni özellikler
is_homeowner = np.random.choice([0, 1], num_samples, p=[0.4, 0.6])
education_level = np.random.choice(["High School", "Bachelor", "Master", "PhD"], num_samples, p=[0.5, 0.3, 0.15, 0.05])
is_married = np.random.choice([0, 1], num_samples, p=[0.5, 0.5])
previous_loans = np.random.randint(0, 11, num_samples)

# Onay kurallarına göre hedef değişken
approved = []
approved = []

for i in range(num_samples):
    score = 0

    # Income
    if income[i] > 15000:
        score += 2
    elif income[i] > 8000:
        score += 1

    # Credit score
    if credit_score[i] > 700:
        score += 2
    elif credit_score[i] > 600:
        score += 1

    # Debt
    if debt[i] < 10000:
        score += 2
    elif debt[i] < 20000:
        score += 1

    # Employment years
    if employment_years[i] > 5:
        score += 2
    elif employment_years[i] > 2:
        score += 1

    # Homeowner
    if is_homeowner[i] == 1:
        score += 1

    # Education
    if education_level[i] in ["Master", "PhD"]:
        score += 2
    elif education_level[i] == "Bachelor":
        score += 1

    # Marital status
    if is_married[i] == 1:
        score += 1

    # Previous loans
    if previous_loans[i] >= 2:
        score += 1

    # Final decision
    if score >= 7:
        approved.append(1)
    else:
        approved.append(1 if random.random() < 0.05 else 0)

# DataFrame oluştur
df = pd.DataFrame({
    "age": age,
    "income": income,
    "debt": debt,
    "credit_score": credit_score,
    "employment_years": employment_years,
    "is_homeowner": is_homeowner,
    "education_level": education_level,
    "is_married": is_married,
    "previous_loans": previous_loans,
    "approved": approved
})

# Veri örneği
print(df.head())
print("\nSınıf Dağılımı:\n", df['approved'].value_counts())

# CSV'ye kaydetmek istersen:
df.to_csv("credit_dataset.csv.csv", index=False)
