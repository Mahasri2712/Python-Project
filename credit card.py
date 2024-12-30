import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from imblearn.over_sampling import SMOTE

data = pd.read_csv("creditcard.csv")

# Step 2: Explore the data
print("Dataset Shape:", data.shape)
print("\nFirst 5 rows:\n", data.head())
print("\nSummary Statistics:\n", data.describe())
print("\nChecking for missing values:\n", data.isnull().sum())

# Step 3: Check class distribution
print("\nClass Distribution:\n", data['Class'].value_counts())
sns.countplot(x='Class', data=data)
plt.title("Class Distribution")
plt.show()

# Step 4: Data preprocessing
# Check for correlations using a heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(data.corr(), cmap='coolwarm', annot=False)
plt.title("Correlation Heatmap")
plt.show()

# Step 5: Split features and target variable
X = data.drop('Class', axis=1)  # Features
y = data['Class']  # Target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# Step 6: Handle class imbalance using SMOTE
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("\nClass distribution after SMOTE:\n", pd.Series(y_train_smote).value_counts())

# Step 7: Train a Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_smote, y_train_smote)

# Step 8: Make predictions
y_pred = model.predict(X_test)

# Step 9: Evaluate the model
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nAccuracy Score:", accuracy_score(y_test, y_pred))

# Step 10: Visualize feature importance
importances = model.feature_importances_
features = X.columns
plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=features)
plt.title("Feature Importance")
plt.show()

# Step 11: Save the model
import joblib
joblib.dump(model, "fraud_detection_model.pkl")
print("\nModel saved as 'fraud_detection_model.pkl'")
