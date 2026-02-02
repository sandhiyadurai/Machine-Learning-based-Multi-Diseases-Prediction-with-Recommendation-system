import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("dataset/Heart_Disease_Prediction.csv")

# Encode categorical target variable
le = LabelEncoder()
df['Heart Disease'] = le.fit_transform(df['Heart Disease'])

# Split features and target
X = df.drop("Heart Disease", axis=1)
y = df["Heart Disease"]

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

print("Heart Disease Model Accuracy:", accuracy)

# Save model
with open("model/heart_disease_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save label encoder
with open("model/heart_disease_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("Heart Disease Model saved successfully!")