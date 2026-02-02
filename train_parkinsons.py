import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("dataset/parkinsons.csv")

# Drop the 'name' column as it's not a feature
df = df.drop("name", axis=1)

# Split features and target
X = df.drop("status", axis=1)
y = df["status"]

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

print("Parkinson's Disease Model Accuracy:", accuracy)

# Save model
with open("model/parkinsons_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Parkinson's Disease Model saved successfully!")