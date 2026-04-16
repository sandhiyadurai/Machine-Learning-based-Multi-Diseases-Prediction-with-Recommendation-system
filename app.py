import os
import json
import csv
import hashlib
import pickle
from datetime import datetime

import streamlit as st
import pandas as pd
import numpy as np

# Paths for storage and models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "users.json")
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.csv")
MODEL_DIR = os.path.join(BASE_DIR, "model")
DIABETES_MODEL_PATH = os.path.join(MODEL_DIR, "diabetes_model.pkl")
HEART_MODEL_PATH = os.path.join(MODEL_DIR, "heart_disease_model.pkl")
HEART_ENCODER_PATH = os.path.join(MODEL_DIR, "heart_disease_encoder.pkl")
LIVER_MODEL_PATH = os.path.join(MODEL_DIR, "liver_disease_model.pkl")
LIVER_GENDER_ENCODER_PATH = os.path.join(MODEL_DIR, "liver_gender_encoder.pkl")
PARKINSONS_MODEL_PATH = os.path.join(MODEL_DIR, "parkinsons_model.pkl")

# utilities

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def init_storage_files():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": []}, f, indent=2)

    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "name", "feedback", "timestamp"])
            writer.writeheader()


def load_users():
    init_storage_files()
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("users", [])


def save_users(users):
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump({"users": users}, f, indent=2)
def load_history():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_prediction_to_history(username, disease, inputs, result, confidence):
    history = load_history()
    if username not in history:
        history[username] = []
    history[username].append({
        "disease": disease,
        "inputs": inputs,
        "result": result,
        "confidence": f"{confidence:.1%}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def authenticate(username: str, password: str) -> bool:
    users = load_users()
    hashed = hash_password(password)
    return any(u["username"] == username and u["password"] == hashed for u in users)


def register_user(username: str, password: str) -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password cannot be empty."
    users = load_users()
    if any(u["username"] == username for u in users):
        return False, "Username already exists. Please choose a different one."
    users.append({"username": username, "password": hash_password(password)})
    save_users(users)
    return True, "Signup successful! You can now login."


def save_feedback(username: str, name: str, feedback: str):
    init_storage_files()
    with open(FEEDBACK_FILE, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "name", "feedback", "timestamp"])
        writer.writerow({
            "username": username,
            "name": name,
            "feedback": feedback,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })


@st.cache_resource
def load_models():
    models = {}
    try:
        with open(DIABETES_MODEL_PATH, "rb") as f:
            models["diabetes"] = pickle.load(f)
    except FileNotFoundError:
        models["diabetes"] = None

    try:
        with open(HEART_MODEL_PATH, "rb") as f:
            models["heart"] = pickle.load(f)
    except FileNotFoundError:
        models["heart"] = None

    try:
        with open(HEART_ENCODER_PATH, "rb") as f:
            models["heart_encoder"] = pickle.load(f)
    except FileNotFoundError:
        models["heart_encoder"] = None

    try:
        with open(LIVER_MODEL_PATH, "rb") as f:
            models["liver"] = pickle.load(f)
    except FileNotFoundError:
        models["liver"] = None

    try:
        with open(LIVER_GENDER_ENCODER_PATH, "rb") as f:
            models["liver_gender_encoder"] = pickle.load(f)
    except FileNotFoundError:
        models["liver_gender_encoder"] = None

    try:
        with open(PARKINSONS_MODEL_PATH, "rb") as f:
            models["parkinsons"] = pickle.load(f)
    except FileNotFoundError:
        models["parkinsons"] = None

    return models


def get_doctor_platforms():
    return {
        "Diabetes": [
            {"name": "Practo", "url": "https://www.practo.com/consult/endocrinologist", "description": "Trusted endocrinologists for diabetes management."},
            {"name": "Apollo 24/7", "url": "https://apollo247.com/specialties/endocrinology", "description": "24/7 diabetes care from top specialists."},
            {"name": "mfine", "url": "https://www.mfine.co", "description": "Online endocrine consultations with certified doctors."},
        ],
        "Heart Disease": [
            {"name": "Practo", "url": "https://www.practo.com/consult/cardiologist", "description": "Instant appointments with cardiologists."},
            {"name": "Apollo 24/7", "url": "https://apollo247.com/specialties/cardiology", "description": "Trusted cardiac specialists available online."},
            {"name": "Lybrate", "url": "https://www.lybrate.com/cardiology-specialist", "description": "Chat and video consults with heart experts."},
        ],
        "Liver Disease": [
            {"name": "Practo", "url": "https://www.practo.com/consult/gastroenterologist", "description": "Hepatologists and gastroenterologists on demand."},
            {"name": "Apollo 24/7", "url": "https://apollo247.com/specialties/gastroenterology", "description": "Online liver care from experienced specialists."},
            {"name": "mfine", "url": "https://www.mfine.co", "description": "Teleconsultations for liver health."},
        ],
        "Parkinson's Disease": [
            {"name": "Practo", "url": "https://www.practo.com/consult/neurologist", "description": "Neurologists experienced in movement disorders."},
            {"name": "Apollo 24/7", "url": "https://apollo247.com/specialties/neurology", "description": "Online neurology consultations available 24/7."},
            {"name": "Lybrate", "url": "https://www.lybrate.com/neurologist", "description": "Speak to Parkinson's specialists from home."},
        ],
    }


def render_doctor_cards(platforms):
    for platform in platforms:
        st.markdown(
            f"""
            <div style='border:1px solid #d3d3d3; border-radius:12px; padding:16px; margin-bottom:12px; background:#f7f9ff;'>
                <h4 style='margin-bottom:6px;'>{platform['name']}</h4>
                <p style='margin:0 0 10px 0; color:#333;'>{platform['description']}</p>
                <a href='{platform['url']}' target='_blank' style='color:#1f77b4; font-weight:600;'>Visit platform →</a>
            </div>
            """,
            unsafe_allow_html=True,
        )


SYMPTOMS_DATA = {
    "Diabetes": [
        "Fatigue", "Frequent urination", "High glucose", "Excessive thirst",
        "Blurred vision", "Slow-healing wounds", "Unexplained weight loss",
        "Tingling in hands/feet", "Frequent infections", "Dry skin",
        "Increased hunger", "Darkened skin patches", "Fruity breath odor"
    ],
    "Heart Disease": [
        "Chest pain", "Shortness of breath", "High cholesterol", "Palpitations",
        "Swollen ankles/feet", "Dizziness or lightheadedness", "Persistent cough",
        "Fatigue during activity", "Irregular heartbeat", "Pain in arm/shoulder",
        "Cold sweats", "Nausea with chest discomfort", "Jaw or neck pain"
    ],
    "Liver Disease": [
        "Jaundice", "Nausea", "Abdominal pain", "Dark urine",
        "Pale stool color", "Loss of appetite", "Easy bruising",
        "Spider-like blood vessels", "Itchy skin", "Leg swelling",
        "Confusion or forgetfulness", "Vomiting blood", "Abdominal swelling (ascites)"
    ],
    "Parkinson's Disease": [
        "Tremors", "Voice changes", "Stiffness", "Loss of balance",
        "Slow movement (bradykinesia)", "Mask-like facial expression",
        "Micrographia (small handwriting)", "Sleep disturbances",
        "Reduced arm swing while walking", "Constipation",
        "Loss of smell", "Depression or anxiety", "Drooling"
    ]
}


def predict_from_symptoms(selected_symptoms):
    if not selected_symptoms:
        return None, 0, 0, 0.0
    counts = {
        disease: sum(1 for symptom in selected_symptoms if symptom in symptoms)
        for disease, symptoms in SYMPTOMS_DATA.items()
    }
    predicted = max(counts, key=counts.get)
    best_count = counts[predicted]
    total = len(SYMPTOMS_DATA[predicted])
    confidence = min(0.95, 0.2 + (best_count / total) * 0.75)
    return predicted if best_count > 0 else None, best_count, total, confidence


def show_recommendations(disease):
    recommendations = {
        "Diabetes": [
            "Follow a balanced diet and monitor sugar intake.",
            "Maintain a regular exercise routine.",
            "Stay hydrated and track blood glucose regularly.",
            "Consult an endocrinologist for medication review.",
        ],
        "Heart Disease": [
            "Limit saturated fats and processed foods.",
            "Take regular cardiovascular breaks and exercise.",
            "Monitor blood pressure and cholesterol levels.",
            "Visit a cardiologist for detailed evaluation.",
        ],
        "Liver Disease": [
            "Avoid alcohol and reduce medication overuse.",
            "Eat nutrient-rich foods and stay hydrated.",
            "Monitor liver function tests regularly.",
            "Consult a hepatologist for a care plan.",
        ],
        "Parkinson's Disease": [
            "Schedule regular neurology consultations.",
            "Maintain physical activity and balance exercises.",
            "Track symptoms and medication timing carefully.",
            "Consider physiotherapy and speech therapy support.",
        ],
    }
    st.markdown("### Precautions & Next Steps")
    for recommendation in recommendations.get(disease, []):
        st.markdown(f"- {recommendation}")


def predict_diabetes(model):
    st.subheader("Diabetes Prediction")
    col1, col2 = st.columns(2)
    with col1:
        pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, value=0)
        glucose = st.number_input("Glucose Level", min_value=0, max_value=300, value=110)
        blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=70)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0, max_value=100, value=20)
    with col2:
        insulin = st.number_input("Insulin Level", min_value=0, max_value=900, value=80)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=26.0)
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.5)
        age = st.number_input("Age", min_value=1, max_value=120, value=32)

    if st.button("Predict Diabetes"):
        sample = pd.DataFrame([
            [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]
        ], columns=["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"])
        prediction = model.predict(sample)[0]
        probabilities = model.predict_proba(sample)[0]
        score = float(probabilities[1] if prediction == 1 else probabilities[0])
        label = "Positive for Diabetes" if prediction == 1 else "Negative for Diabetes"
        st.success(label)
        st.info(f"Confidence: {score:.1%}")
        show_recommendations("Diabetes")


def predict_heart(model, encoder):
    st.subheader("Heart Disease Prediction")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=55)
        sex = st.selectbox("Sex", ["Male", "Female"])
        chest_pain = st.selectbox("Chest Pain Type", ["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"])
        bp = st.number_input("Resting BP", min_value=0, max_value=250, value=120)
        cholesterol = st.number_input("Cholesterol", min_value=0, max_value=600, value=200)
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No", "Yes"])
    with col2:
        ekg = st.selectbox("Resting ECG Results", ["Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"])
        max_hr = st.number_input("Max Heart Rate Achieved", min_value=0, max_value=250, value=150)
        exercise_angina = st.selectbox("Exercise Induced Angina", ["No", "Yes"])
        st_depression = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.0)
        slope = st.selectbox("Slope of ST Segment", ["Upsloping", "Flat", "Downsloping"])
        vessels = st.selectbox("Number of Major Vessels", [0, 1, 2, 3])
        thallium = st.selectbox("Thallium Stress Test", ["Normal", "Fixed defect", "Reversible defect"])

    mapping = {
        "Male": 1,
        "Female": 0,
        "Typical Angina": 4,
        "Atypical Angina": 3,
        "Non-anginal Pain": 2,
        "Asymptomatic": 1,
        "No": 0,
        "Yes": 1,
        "Normal": 0,
        "ST-T wave abnormality": 1,
        "Left ventricular hypertrophy": 2,
        "Upsloping": 1,
        "Flat": 2,
        "Downsloping": 3,
        "Fixed defect": 6,
        "Reversible defect": 7,
    }

    if st.button("Predict Heart Disease"):
        sample = pd.DataFrame([
            [age, mapping[sex], mapping[chest_pain], bp, cholesterol, mapping[fbs], mapping[ekg], max_hr, mapping[exercise_angina], st_depression, mapping[slope], vessels, mapping[thallium]]
        ], columns=["Age", "Sex", "Chest pain type", "BP", "Cholesterol", "FBS over 120", "EKG results", "Max HR", "Exercise angina", "ST depression", "Slope of ST", "Number of vessels fluro", "Thallium"])
        prediction = model.predict(sample)[0]
        label = encoder.inverse_transform([prediction])[0] if encoder is not None else ("Presence" if prediction == 1 else "Absence")
        probabilities = model.predict_proba(sample)[0]
        score = float(probabilities[1] if prediction == 1 else probabilities[0])
        st.success(f"Prediction: {label}")
        st.info(f"Confidence: {score:.1%}")
        show_recommendations("Heart Disease")


def predict_liver(model, gender_encoder):
    st.subheader("Liver Disease Prediction")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=45)
        gender = st.selectbox("Gender", ["Male", "Female"])
        total_bilirubin = st.number_input("Total Bilirubin", min_value=0.0, max_value=50.0, value=1.0)
        direct_bilirubin = st.number_input("Direct Bilirubin", min_value=0.0, max_value=20.0, value=0.2)
        alkaline_phosphotase = st.number_input("Alkaline Phosphotase", min_value=0, max_value=800, value=120)
    with col2:
        alt = st.number_input("Alamine Aminotransferase (ALT)", min_value=0, max_value=500, value=25)
        ast = st.number_input("Aspartate Aminotransferase (AST)", min_value=0, max_value=500, value=20)
        total_protiens = st.number_input("Total Proteins", min_value=0.0, max_value=15.0, value=6.5)
        albumin = st.number_input("Albumin", min_value=0.0, max_value=10.0, value=3.5)
        ag_ratio = st.number_input("Albumin/Globulin Ratio", min_value=0.0, max_value=3.0, value=1.0)

    if st.button("Predict Liver Disease"):
        gender_value = gender_encoder.transform([gender])[0] if gender_encoder is not None else (1 if gender == "Male" else 0)
        sample = pd.DataFrame([
            [age, gender_value, total_bilirubin, direct_bilirubin, alkaline_phosphotase, alt, ast, total_protiens, albumin, ag_ratio]
        ], columns=["Age", "Gender", "Total_Bilirubin", "Direct_Bilirubin", "Alkaline_Phosphotase", "Alamine_Aminotransferase", "Aspartate_Aminotransferase", "Total_Protiens", "Albumin", "Albumin_and_Globulin_Ratio"])
        prediction = model.predict(sample)[0]
        probabilities = model.predict_proba(sample)[0]
        score = float(probabilities[1] if prediction == 1 else probabilities[0])
        label = "Positive for Liver Disease" if prediction == 1 else "Negative for Liver Disease"
        st.success(label)
        st.info(f"Confidence: {score:.1%}")
        show_recommendations("Liver Disease")


def predict_parkinsons(model):
    st.subheader("Parkinson's Disease Prediction")
    cols = st.columns(2)
    with cols[0]:
        fo = st.number_input("MDVP:Fo(Hz)", min_value=0.0, max_value=500.0, value=120.0)
        fhi = st.number_input("MDVP:Fhi(Hz)", min_value=0.0, max_value=500.0, value=150.0)
        flo = st.number_input("MDVP:Flo(Hz)", min_value=0.0, max_value=500.0, value=100.0)
        jitter_per = st.number_input("MDVP:Jitter(%)", min_value=0.0, max_value=1.0, value=0.005)
        jitter_abs = st.number_input("MDVP:Jitter(Abs)", min_value=0.0, max_value=1.0, value=0.0001)
        rap = st.number_input("MDVP:RAP", min_value=0.0, max_value=1.0, value=0.004)
        ppq = st.number_input("MDVP:PPQ", min_value=0.0, max_value=1.0, value=0.005)
        ddp = st.number_input("Jitter:DDP", min_value=0.0, max_value=1.0, value=0.012)
        shimmer = st.number_input("MDVP:Shimmer", min_value=0.0, max_value=1.0, value=0.04)
        shimmer_db = st.number_input("MDVP:Shimmer(dB)", min_value=0.0, max_value=5.0, value=0.4)
    with cols[1]:
        apq3 = st.number_input("Shimmer:APQ3", min_value=0.0, max_value=1.0, value=0.02)
        apq5 = st.number_input("Shimmer:APQ5", min_value=0.0, max_value=1.0, value=0.03)
        apq = st.number_input("MDVP:APQ", min_value=0.0, max_value=1.0, value=0.03)
        dda = st.number_input("Shimmer:DDA", min_value=0.0, max_value=1.0, value=0.08)
        nhr = st.number_input("NHR", min_value=0.0, max_value=1.0, value=0.02)
        hnr = st.number_input("HNR", min_value=0.0, max_value=50.0, value=20.0)
        rpde = st.number_input("RPDE", min_value=0.0, max_value=1.0, value=0.45)
        dfa = st.number_input("DFA", min_value=0.0, max_value=2.0, value=0.82)
        spread1 = st.number_input("spread1", min_value=-10.0, max_value=10.0, value=-4.0)
        spread2 = st.number_input("spread2", min_value=-10.0, max_value=10.0, value=0.3)
        d2 = st.number_input("D2", min_value=0.0, max_value=5.0, value=2.3)
        ppe = st.number_input("PPE", min_value=0.0, max_value=2.0, value=0.3)

    if st.button("Predict Parkinson's Disease"):
        sample = pd.DataFrame([
            [fo, fhi, flo, jitter_per, jitter_abs, rap, ppq, ddp, shimmer, shimmer_db, apq3, apq5, apq, dda, nhr, hnr, rpde, dfa, spread1, spread2, d2, ppe]
        ], columns=[
            "MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)", "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP",
            "MDVP:Shimmer", "MDVP:Shimmer(dB)", "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR", "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"
        ])
        prediction = model.predict(sample)[0]
        probabilities = model.predict_proba(sample)[0]
        score = float(probabilities[1] if prediction == 1 else probabilities[0])
        label = "Positive for Parkinson's" if prediction == 1 else "Negative for Parkinson's"
        st.success(label)
        st.info(f"Confidence: {score:.1%}")
        show_recommendations("Parkinson's Disease")


def feedback_page(username):
    st.header("Feedback")
    st.write("Share your thoughts about the app and how we can improve it.")

    name = st.text_input("Your Name", value=username)
    message = st.text_area("Feedback")
    if st.button("Submit Feedback"):
        if not name or not message:
            st.error("Please provide both your name and feedback message.")
        else:
            save_feedback(username, name, message)
            st.success("Thank you! Your feedback has been submitted.")
            st.info("Feedback is stored securely for review.")


def main():
    st.set_page_config(page_title="Multi-Disease Prediction App", page_icon="🏥", layout="wide")
    st.markdown("# 🩺 Multi-Disease Prediction Web App")
    st.markdown("Welcome to the healthcare dashboard. Signup or login to begin using disease prediction and consultation features.")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        sidebar_options = ["Dashboard", "Disease Prediction", "Doctor Consultation", "Feedback","History"]
        selected_page = st.sidebar.selectbox("Menu", sidebar_options)
        st.sidebar.markdown("---")
        st.sidebar.write(f"**Logged in as:** {st.session_state.username}")
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""

        models = load_models()

        if selected_page == "Dashboard":
            st.header("Dashboard")
            st.markdown("Use the sidebar to go to different modules. Here you can access disease prediction, doctor platforms, and feedback.")
            st.metric("Logged in user", st.session_state.username)
            st.write("This project demonstrates a beginner-friendly medical prediction dashboard built with Streamlit.")

        elif selected_page == "Disease Prediction":
            st.header("Disease Prediction")
            st.markdown("Select the symptoms you are experiencing and then click Analyze to get a likely condition.")

            selected_symptoms = []
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Symptoms Set 01**")
                for symptom in SYMPTOMS_DATA["Diabetes"]:
                    if st.checkbox(symptom, key=f"sym_diabetes_{symptom}"):
                        selected_symptoms.append(symptom)

            with col2:
                st.markdown("**Symptoms Set 02**")
                for symptom in SYMPTOMS_DATA["Heart Disease"]:
                    if st.checkbox(symptom, key=f"sym_heart_{symptom}"):
                        selected_symptoms.append(symptom)

            col3, col4 = st.columns(2)
            with col3:
                st.markdown("**Symptoms Set 03**")
                for symptom in SYMPTOMS_DATA["Liver Disease"]:
                    if st.checkbox(symptom, key=f"sym_liver_{symptom}"):
                        selected_symptoms.append(symptom)

            with col4:
                st.markdown("**Symptoms Set 04**")
                for symptom in SYMPTOMS_DATA["Parkinson's Disease"]:
                    if st.checkbox(symptom, key=f"sym_parkinsons_{symptom}"):
                        selected_symptoms.append(symptom)

            if selected_symptoms:
                st.markdown("### Selected Symptoms")
                st.write(", ".join(selected_symptoms))

            if st.button("Analyze Symptoms"):
                predicted, match_count, total_symptoms, confidence = predict_from_symptoms(selected_symptoms)
                if predicted is None:
                    st.warning("No matching disease found. Please select more symptoms or consult a professional.")
                else:
                    st.success(f"Likely Condition: {predicted}")
                    risk_level = "High" if confidence > 0.7 else "Moderate" if confidence > 0.4 else "Low"
                    st.info(f"Confidence: {confidence:.1%} | Risk level: {risk_level}")
                    st.write(f"Matching symptoms: {match_count} out of {total_symptoms}")
                    show_recommendations(predicted)
                    platforms = get_doctor_platforms().get(predicted, [])
                    if platforms:
                        st.markdown("---")
                        st.subheader("Recommended Online Doctor Platforms")
                        render_doctor_cards(platforms)

        elif selected_page == "Doctor Consultation":
            st.header("Doctor Consultation Platforms")
            st.write("Choose a disease below to view trusted online doctor consultation platforms.")
            disease = st.selectbox("Select a disease", ["Diabetes", "Heart Disease", "Liver Disease", "Parkinson's Disease"])
            platforms = get_doctor_platforms().get(disease, [])
            render_doctor_cards(platforms)

        elif selected_page == "History":
             history_page(st.session_state.username)

        elif selected_page == "Feedback":
             feedback_page(st.session_state.username)

    else:
        auth_mode = st.sidebar.radio("Authentication", ["Login", "Signup"])
        st.sidebar.markdown("---")
        st.sidebar.write("Please login or signup to continue.")

        if auth_mode == "Login":
            st.subheader("Login")
            with st.form(key="login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Login")
            if login_button:
                if authenticate(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                else:
                    st.error("Invalid username or password.")

        else:
            st.subheader("Signup")
            with st.form(key="signup_form"):
                new_username = st.text_input("Choose a username")
                new_password = st.text_input("Choose a password", type="password")
                signup_button = st.form_submit_button("Signup")
            if signup_button:
                success, message = register_user(new_username, new_password)
                if success:
                    st.success(message)
                    st.info("Please switch to Login to access your account.")
                else:
                    st.error(message)


if __name__ == "__main__":
    init_storage_files()
    main()
