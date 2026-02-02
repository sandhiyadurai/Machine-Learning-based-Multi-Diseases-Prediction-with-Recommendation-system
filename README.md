# 🏥  Machine-Learning-based-Multi-Diseases-Prediction-with-Recommendation-system


An AI-powered web application that predicts multiple diseases based on user symptoms and medical parameters, and provides personalized health recommendations.  
Built using **Machine Learning**, **Python**, and **Streamlit**.

---

## 📌 Project Overview

The **Multi-Disease Prediction & Recommendation System** helps users identify the possibility of certain diseases by:
- Selecting symptoms
- Entering relevant medical values
- Getting AI-based disease prediction
- Receiving basic health recommendations

⚠️ *This system is for educational purposes only and is not a substitute for professional medical advice.*

---

## 🧠 Diseases Supported

- 🍬 **Diabetes**
- ❤️ **Heart Disease**
- 🫀 **Liver Disease**
- 🧠 **Parkinson’s Disease**

Each disease uses a **separate trained machine learning model** for better accuracy.

---

## 🛠️ Technologies Used

- **Python**
- **Streamlit** – Web application framework
- **Scikit-learn** – Machine learning models
- **Pandas** – Data handling
- **Pickle** – Model serialization
- **HTML & CSS** – UI customization

---

## ⚙️ How the System Works

1. User selects symptoms from the UI
2. System identifies the possible disease
3. User enters medical parameters
4. ML model predicts disease presence
5. Confidence score is displayed
6. Personalized recommendations are shown

---

## 📂 Project Structure
project/
│
├── app.py
├── requirements.txt
│
├── model/
│ ├── diabetes_model.pkl
│ ├── heart_disease_model.pkl
│ ├── liver_disease_model.pkl
│ └── parkinsons_model.pkl
│
├── dataset/
├── train_heart_disease.py
├── train_liver_disease.py
├── train_parkinsons.py

⚠️ Disclaimer

This application is developed for academic and learning purposes only.
It should not be used as a replacement for professional medical diagnosis or treatment.
