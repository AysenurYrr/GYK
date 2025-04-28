import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# CSV'yi oku
df = pd.read_csv("credit_dataset.csv")

# 1. Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop("approved", axis=1)
y = df["approved"]

# 2. Kategorik ve sayısal sütunları ayır
categorical_cols = ["education_level"]
numeric_cols = X.drop(columns=categorical_cols).columns.tolist()

# 3. OneHotEncoder'ı ColumnTransformer içine yerleştir
preprocessor = ColumnTransformer(
    transformers=[
        ("onehot", OneHotEncoder(drop="first"), categorical_cols)
    ],
    remainder="passthrough"  # Sayısal sütunları olduğu gibi geçir
)

# 4. Veriyi eğitim/test olarak ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Pipeline oluşturarak tüm ön işleme ve modeli bağla
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline(steps=[
    ("preprocessing", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# 6. Modeli eğit
pipeline.fit(X_train, y_train)

# 7. Test verisiyle tahmin
y_pred = pipeline.predict(X_test)

# Accuracy
acc = accuracy_score(y_test, y_pred)
print("Accuracy:", acc)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

plt.figure(figsize=(8,5))
sns.histplot(y_test, color="blue", label="Actual", kde=False, bins=2)
sns.histplot(y_pred, color="orange", label="Predicted", kde=False, bins=2)
plt.title("Actual vs Predicted Approvals")
plt.legend()
plt.xticks([0,1])
plt.show()
