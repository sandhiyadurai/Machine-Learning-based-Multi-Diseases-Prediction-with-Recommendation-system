import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("dataset/indian_liver_patient.csv")

# Handle missing values
df = df.dropna()

# Encode Gender column
le_gender = LabelEncoder()
df['Gender'] = le_gender.fit_transform(df['Gender'])

# Convert target: 1 = liver disease, 2 = no disease -> 1 = disease, 0 = no disease
df['Dataset'] = df['Dataset'].map({1: 1, 2: 0})

# Split features and target
X = df.drop("Dataset", axis=1)
y = df["Dataset"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Liver Disease Model Accuracy:", accuracy)

# Save model
with open("model/liver_disease_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save gender encoder
with open("model/liver_gender_encoder.pkl", "wb") as f:
    pickle.dump(le_gender, f)

print("Liver Disease Model saved successfully!")