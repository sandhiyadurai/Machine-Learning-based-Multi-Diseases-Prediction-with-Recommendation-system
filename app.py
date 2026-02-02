# symptom_based_multi_disease_app.py
import streamlit as st
import pickle
import pandas as pd
import time

# Set page configuration
st.set_page_config(
    page_title="Multi-Disease Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Clean white background with blue mixture */
    .stApp {
        background:
            radial-gradient(circle at 30% 20%, rgba(135, 206, 235, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 70% 80%, rgba(70, 130, 180, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(176, 196, 222, 0.08) 0%, transparent 50%),
            linear-gradient(135deg,
                #ffffff 0%,
                #f8f9fa 25%,
                #e3f2fd 50%,
                #f8f9fa 75%,
                #ffffff 100%
            );
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
        label, span,div {
        color: black !important;
    }
    

    /* Add subtle blue accent particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            radial-gradient(circle at 20% 30%, rgba(100, 149, 237, 0.06) 1px, transparent 1px),
            radial-gradient(circle at 80% 70%, rgba(70, 130, 180, 0.04) 0.8px, transparent 0.8px),
            radial-gradient(circle at 60% 10%, rgba(135, 206, 235, 0.05) 1.2px, transparent 1.2px);
        background-size: 120px 120px, 180px 180px, 90px 90px;
        background-position: 0 0, 60px 40px, 30px 80px;
        animation: blueFloat 25s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes blueFloat {
        0%, 100% { transform: translateY(0px) translateX(0px) rotate(0deg); }
        33% { transform: translateY(-20px) translateX(15px) rotate(120deg); }
        66% { transform: translateY(-10px) translateX(-10px) rotate(240deg); }
    }

    /* Main content background with enhanced glassmorphism for light blue theme */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        margin: 2rem;
        padding: 2rem;
        box-shadow:
            0 8px 32px rgba(70, 130, 180, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(135, 206, 235, 0.3);
        color: #000000; /* Black text for main content */
        position: relative;
    }

    /* Add subtle blue inner glow effect */
    .main .block-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 20px;
        background: linear-gradient(135deg,
            rgba(135, 206, 235, 0.05) 0%,
            rgba(176, 196, 222, 0.03) 50%,
            rgba(135, 206, 235, 0.05) 100%
        );
        pointer-events: none;
        z-index: -1;
    }

    /* Specific element color adaptations */
    .main-header {
        color: #000000; /* Dark text on light main container */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #000000; /* Black header for maximum contrast */
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .main-header:hover {
        transform: scale(1.05);
        text-shadow: 3px 3px 6px rgba(0,0,0,0.2);
    }

    .disease-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: black; /* Light text on colored background */
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .disease-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 12px 25px rgba(0,0,0,0.2);
        border-color: rgba(255,255,255,0.3);
    }

    .symptom-tag {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: black;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        display: inline-block;
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid rgba(25, 118, 210, 0.2);
    }
    .symptom-tag:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(25, 118, 210, 0.3);
        background: linear-gradient(135deg, #2c3e50 0%, #1a237e 100%);
    }

    .input-section {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 248, 255, 0.95) 100%);
        backdrop-filter: blur(15px);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #4a90e2;
        transition: all 0.3s ease;
        border: 1px solid rgba(135, 206, 235, 0.2);
        box-shadow:
            0 4px 15px rgba(70, 130, 180, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        color: #000000; /* Dark text on light background */
    }

    .input-section p, .input-section span, .input-section div,
    .input-section h1, .input-section h2, .input-section h3, .input-section h4 {
        color: #000000 !important;
    }
    .input-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, rgba(248, 249, 250, 0.95) 0%, rgba(233, 236, 239, 0.95) 100%);
    }

    .prediction-result {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 50%, #66BB6A 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
        border: 2px solid rgba(255,255,255,0.2);
        animation: fadeIn 0.5s ease-in;
    }
    .prediction-result:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 15px 30px rgba(76, 175, 80, 0.3);
    }

    .recommendation-box {
        background: linear-gradient(135deg, rgba(255, 243, 205, 0.9) 0%, rgba(255, 241, 118, 0.9) 100%);
        backdrop-filter: blur(5px);
        border: 1px solid #ffeaa7;
        color: #000000; /* Dark text on light yellow background */
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .recommendation-box p, .recommendation-box span, .recommendation-box div,
    .recommendation-box h1, .recommendation-box h2, .recommendation-box h3, .recommendation-box h4 {
        color: #000000 !important;
    }
    .recommendation-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(255, 193, 7, 0.2);
        background: linear-gradient(135deg, rgba(255, 243, 205, 0.95) 0%, rgba(255, 241, 118, 0.95) 100%);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 2px solid rgba(255,255,255,0.2);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }

    .sidebar-info {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 248, 255, 0.95) 100%);
        backdrop-filter: blur(15px);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        transition: all 0.3s ease;
        border: 1px solid rgba(135, 206, 235, 0.2);
        box-shadow:
            0 4px 15px rgba(70, 130, 180, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        color: #000000; /* Dark text on light sidebar */
    }

    .sidebar-info p, .sidebar-info span, .sidebar-info div,
    .sidebar-info h1, .sidebar-info h2, .sidebar-info h3, .sidebar-info h4 {
        color: #000000 !important;
    }
    .sidebar-info:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(76, 175, 80, 0.1);
    }

    /* Column hover effects */
    .stColumn {
        transition: all 0.3s ease;
    }
    .stColumn:hover {
        transform: translateY(-2px);
    }

    /* Checkbox hover effects */
    .stCheckbox {
        transition: all 0.3s ease;
    }
    .stCheckbox:hover {
        transform: translateY(-1px);
    }

    /* Input field hover effects */
    .stTextInput, .stNumberInput, .stSelectbox {
        transition: all 0.3s ease;
    }
    .stTextInput:hover, .stNumberInput:hover, .stSelectbox:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    /* Success message hover */
    .stSuccess {
        transition: all 0.3s ease;
    }
    .stSuccess:hover {
        transform: translateY(-2px);
    }

    /* Warning message hover */
    .stWarning {
        transition: all 0.3s ease;
    }
    .stWarning:hover {
        transform: translateY(-2px);
    }

    /* Error message hover */
    .stError {
        transition: all 0.3s ease;
    }
    .stError:hover {
        transform: translateY(-2px);
    }

    /* Info message hover */
    .stInfo {
        transition: all 0.3s ease;
    }
    .stInfo:hover {
        transform: translateY(-2px);
    }

    /* Additional text color overrides for maximum readability */
    .stMarkdown, .stText, .stCaption, .stSubheader {
        color: #000000 !important;
    }

    /* Black colors for form labels and help text */
    .stSelectbox label, .stNumberInput label, .stTextInput label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Help text color - slightly darker gray for hierarchy */
    .stSelectbox .help, .stNumberInput .help, .stTextInput .help {
        color: #333333 !important;
    }

    /* Sidebar text colors - all black */
    .sidebar .stMarkdown, .sidebar p, .sidebar span, .sidebar div,
    .sidebar h1, .sidebar h2, .sidebar h3, .sidebar h4 {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load all models
@st.cache_resource
def load_model(file):
    with open(file, "rb") as f:
        return pickle.load(f)

diabetes_model = load_model("model/diabetes_model.pkl")
heart_model = load_model("model/heart_disease_model.pkl")
liver_model = load_model("model/liver_disease_model.pkl")
parkinsons_model = load_model("model/parkinsons_model.pkl")

# Disease recommendations with more detailed advice
recommendations = {
    "Diabetes": {
        "description": "Diabetes is a condition that affects how your body processes blood sugar.",
        "advice": [
            "🏃‍♂️ Maintain a healthy diet with balanced carbohydrates",
            "💪 Exercise regularly (at least 30 minutes daily)",
            "📊 Monitor blood sugar levels regularly",
            "⚖️ Maintain a healthy weight",
            "👨‍⚕️ Consult with an endocrinologist",
            "🩸 Get regular HbA1c tests"
        ]
    },
    "Heart Disease": {
        "description": "Heart disease refers to various conditions affecting the heart.",
        "advice": [
            "🥗 Avoid fatty and processed foods",
            "🏃‍♀️ Exercise moderately and consistently",
            "🏥 Have regular cardiovascular checkups",
            "🩸 Monitor cholesterol and blood pressure",
            "🚭 Quit smoking if applicable",
            "⚖️ Maintain healthy BMI",
            "👨‍⚕️ Consult a cardiologist"
        ]
    },
    "Liver Disease": {
        "description": "Liver disease includes conditions affecting liver function.",
        "advice": [
            "🚫 Avoid alcohol consumption",
            "🥗 Eat a balanced, nutritious diet",
            "💧 Stay well hydrated",
            "🏥 Get regular liver function tests",
            "💊 Avoid unnecessary medications",
            "🩸 Monitor liver enzymes",
            "👨‍⚕️ Consult a hepatologist"
        ]
    },
    "Parkinson's Disease": {
        "description": "Parkinson's is a neurodegenerative disorder affecting movement.",
        "advice": [
            "🧠 Consult a neurologist immediately",
            "🏃‍♂️ Do physiotherapy and occupational therapy",
            "📝 Monitor symptoms progression",
            "💊 Follow prescribed medication regimen",
            "🧘‍♀️ Consider speech therapy if needed",
            "👥 Join support groups",
            "🏥 Regular follow-ups with specialists"
        ]
    }
}

# Sidebar with information
with st.sidebar:
    st.title("ℹ️ About This System")
    st.markdown("""
    <div class="sidebar-info">
    <h4>🔬 How It Works</h4>
    <p>This AI-powered system uses machine learning models trained on medical datasets to predict potential diseases based on your symptoms and medical parameters.</p>

    <h4>⚠️ Important Disclaimer</h4>
    <p><strong>This is not a substitute for professional medical advice.</strong> Always consult with qualified healthcare professionals for accurate diagnosis and treatment.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏥 Supported Diseases")
    diseases = ["Diabetes", "Heart Disease", "Liver Disease", "Parkinson's Disease"]
    for disease in diseases:
        st.markdown(f"• {disease}")

# Main content
st.markdown('<h1 class="main-header">🏥 Multi-Disease Prediction & Recommendation System</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Select your symptoms and provide medical details for AI-powered disease prediction and personalized recommendations</p>', unsafe_allow_html=True)

# Symptom selection with better UI
st.markdown("### 🎯 Step 1: Select Your Symptoms")
st.markdown("Choose all symptoms you're experiencing:")

col1, col2, col3, col4 = st.columns(4)

symptoms_data = {
    "Diabetes": ["Fatigue", "Frequent urination", "High glucose"],
    "Heart Disease": ["Chest pain", "Shortness of breath", "High cholesterol"],
    "Liver Disease": ["Jaundice", "Nausea", "Abdominal pain"],
    "Parkinson's": ["Tremors", "Voice changes", "Stiffness", "Loss of balance"]
}

selected_symptoms = []

with col1:
    st.markdown("**🍬 Diabetes Symptoms**")
    for symptom in symptoms_data["Diabetes"]:
        if st.checkbox(symptom, key=f"diabetes_{symptom}"):
            selected_symptoms.append(symptom)

with col2:
    st.markdown("**❤️ Heart Disease Symptoms**")
    for symptom in symptoms_data["Heart Disease"]:
        if st.checkbox(symptom, key=f"heart_{symptom}"):
            selected_symptoms.append(symptom)

with col3:
    st.markdown("**🫀 Liver Disease Symptoms**")
    for symptom in symptoms_data["Liver Disease"]:
        if st.checkbox(symptom, key=f"liver_{symptom}"):
            selected_symptoms.append(symptom)

with col4:
    st.markdown("**🧠 Parkinson's Symptoms**")
    for symptom in symptoms_data["Parkinson's"]:
        if st.checkbox(symptom, key=f"parkinsons_{symptom}"):
            selected_symptoms.append(symptom)

# Display selected symptoms
if selected_symptoms:
    st.markdown("### 📋 Your Selected Symptoms:")
    symptom_tags = " ".join([f'<span class="symptom-tag">🔸 {symptom}</span>' for symptom in selected_symptoms])
    st.markdown(f'<div style="margin: 1rem 0;">{symptom_tags}</div>', unsafe_allow_html=True)

# Determine possible disease based on symptoms
disease_predicted = None
numeric_inputs = {}
model = None

# Disease detection logic
if selected_symptoms:
    if any(symptom in selected_symptoms for symptom in symptoms_data["Diabetes"]):
        disease_predicted = "Diabetes"
        model = diabetes_model
    elif any(symptom in selected_symptoms for symptom in symptoms_data["Heart Disease"]):
        disease_predicted = "Heart Disease"
        model = heart_model
    elif any(symptom in selected_symptoms for symptom in symptoms_data["Liver Disease"]):
        disease_predicted = "Liver Disease"
        model = liver_model
    elif any(symptom in selected_symptoms for symptom in symptoms_data["Parkinson's"]):
        disease_predicted = "Parkinson's Disease"
        model = parkinsons_model

# Show disease prediction and input form
if disease_predicted:
    st.markdown("---")
    st.markdown(f'<div class="disease-card"><h3>🎯 Detected Condition: {disease_predicted}</h3><p>{recommendations[disease_predicted]["description"]}</p></div>', unsafe_allow_html=True)

    st.markdown("### 📝 Step 2: Provide Medical Details")
    st.markdown('<div class="input-section">', unsafe_allow_html=True)

    if disease_predicted == "Diabetes":
        st.markdown("**Please provide the following diabetes-related measurements:**")

        col1, col2 = st.columns(2)
        with col1:
            numeric_inputs["Pregnancies"] = st.number_input("Number of Pregnancies", 0, 20, help="Number of times pregnant")
            numeric_inputs["Glucose"] = st.number_input("Glucose Level (mg/dL)", 0, 200, help="Plasma glucose concentration")
            numeric_inputs["BloodPressure"] = st.number_input("Blood Pressure (mm Hg)", 0, 140, help="Diastolic blood pressure")
            numeric_inputs["SkinThickness"] = st.number_input("Skin Thickness (mm)", 0, 100, help="Triceps skin fold thickness")

        with col2:
            numeric_inputs["Insulin"] = st.number_input("Insulin Level (mu U/ml)", 0, 900, help="2-Hour serum insulin")
            numeric_inputs["BMI"] = st.number_input("BMI", 0.0, 70.0, help="Body mass index")
            numeric_inputs["DiabetesPedigreeFunction"] = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, help="Diabetes pedigree function")
            numeric_inputs["Age"] = st.number_input("Age (years)", 1, 120, help="Age in years")

    elif disease_predicted == "Heart Disease":
        st.markdown("**Please provide the following cardiac measurements:**")

        col1, col2 = st.columns(2)
        with col1:
            numeric_inputs["age"] = st.number_input("Age (years)", 1, 120)
            numeric_inputs["sex"] = st.selectbox("Sex", ["Male", "Female"], help="Biological sex")
            numeric_inputs["cp"] = st.selectbox("Chest Pain Type", [
                "Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"
            ], help="Type of chest pain experienced")
            numeric_inputs["trestbps"] = st.number_input("Resting Blood Pressure (mm Hg)", 0, 200, help="Resting blood pressure")
            numeric_inputs["chol"] = st.number_input("Cholesterol Level (mg/dL)", 0, 600, help="Serum cholesterol")

        with col2:
            numeric_inputs["fbs"] = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["No", "Yes"], help="Fasting blood sugar > 120 mg/dl")
            numeric_inputs["restecg"] = st.selectbox("Resting ECG Results", [
                "Normal", "ST-T wave abnormality", "Left ventricular hypertrophy"
            ], help="Resting electrocardiographic results")
            numeric_inputs["thalach"] = st.number_input("Max Heart Rate Achieved", 0, 250, help="Maximum heart rate achieved")
            numeric_inputs["exang"] = st.selectbox("Exercise Induced Angina", ["No", "Yes"], help="Exercise induced angina")
            numeric_inputs["oldpeak"] = st.number_input("ST Depression", 0.0, 10.0, help="ST depression induced by exercise")

        col3, col4 = st.columns(2)
        with col3:
            numeric_inputs["slope"] = st.selectbox("Slope of Peak Exercise ST Segment", [
                "Upsloping", "Flat", "Downsloping"
            ], help="Slope of the peak exercise ST segment")
            numeric_inputs["ca"] = st.number_input("Number of Major Vessels", 0, 3, help="Number of major vessels colored by fluoroscopy")

        with col4:
            numeric_inputs["thal"] = st.selectbox("Thalassemia", [
                "Normal", "Fixed defect", "Reversible defect"
            ], help="Thalassemia status")

        # Convert categorical inputs to numeric
        sex_map = {"Male": 1, "Female": 0}
        fbs_map = {"No": 0, "Yes": 1}
        exang_map = {"No": 0, "Yes": 1}
        cp_map = {"Typical Angina": 0, "Atypical Angina": 1, "Non-anginal Pain": 2, "Asymptomatic": 3}
        restecg_map = {"Normal": 0, "ST-T wave abnormality": 1, "Left ventricular hypertrophy": 2}
        slope_map = {"Upsloping": 0, "Flat": 1, "Downsloping": 2}
        thal_map = {"Normal": 1, "Fixed defect": 2, "Reversible defect": 3}

        numeric_inputs["sex"] = sex_map[numeric_inputs["sex"]]
        numeric_inputs["fbs"] = fbs_map[numeric_inputs["fbs"]]
        numeric_inputs["exang"] = exang_map[numeric_inputs["exang"]]
        numeric_inputs["cp"] = cp_map[numeric_inputs["cp"]]
        numeric_inputs["restecg"] = restecg_map[numeric_inputs["restecg"]]
        numeric_inputs["slope"] = slope_map[numeric_inputs["slope"]]
        numeric_inputs["thal"] = thal_map[numeric_inputs["thal"]]

    elif disease_predicted == "Liver Disease":
        st.markdown("**Please provide the following liver function test results:**")

        col1, col2 = st.columns(2)
        with col1:
            numeric_inputs["Age"] = st.number_input("Age (years)", 1, 120)
            numeric_inputs["Gender"] = st.selectbox("Gender", ["Male", "Female"])
            numeric_inputs["Total_Bilirubin"] = st.number_input("Total Bilirubin (mg/dL)", 0.0, 20.0, help="Total bilirubin level")
            numeric_inputs["Direct_Bilirubin"] = st.number_input("Direct Bilirubin (mg/dL)", 0.0, 10.0, help="Direct bilirubin level")
            numeric_inputs["Alkaline_Phosphate"] = st.number_input("Alkaline Phosphate (IU/L)", 0, 500, help="Alkaline phosphatase level")

        with col2:
            numeric_inputs["SGPT"] = st.number_input("SGPT/ALT (IU/L)", 0, 500, help="Serum glutamic pyruvic transaminase")
            numeric_inputs["SGOT"] = st.number_input("SGOT/AST (IU/L)", 0, 500, help="Serum glutamic oxaloacetic transaminase")
            numeric_inputs["Total_Protiens"] = st.number_input("Total Protein (g/dL)", 0.0, 15.0, help="Total protein level")
            numeric_inputs["Albumin"] = st.number_input("Albumin (g/dL)", 0.0, 10.0, help="Albumin level")
            numeric_inputs["A/G_Ratio"] = st.number_input("Albumin/Globulin Ratio", 0.0, 3.0, help="Albumin to globulin ratio")

        # Convert gender to numeric
        gender_map = {"Male": 1, "Female": 0}
        numeric_inputs["Gender"] = gender_map[numeric_inputs["Gender"]]

    elif disease_predicted == "Parkinson's Disease":
        st.markdown("**Please provide the following voice analysis measurements:**")
        st.info("💡 These measurements typically come from specialized voice analysis software used by neurologists.")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Fundamental Frequency**")
            numeric_inputs["MDVP:Fo(Hz)"] = st.number_input("MDVP:Fo(Hz)", 0.0, 500.0)
            numeric_inputs["MDVP:Fhi(Hz)"] = st.number_input("MDVP:Fhi(Hz)", 0.0, 500.0)
            numeric_inputs["MDVP:Flo(Hz)"] = st.number_input("MDVP:Flo(Hz)", 0.0, 500.0)

        with col2:
            st.markdown("**Jitter Measurements**")
            numeric_inputs["MDVP:Jitter(%)"] = st.number_input("Jitter(%)", 0.0, 1.0)
            numeric_inputs["MDVP:Jitter(Abs)"] = st.number_input("Jitter(Abs)", 0.0, 1.0)
            numeric_inputs["MDVP:RAP"] = st.number_input("RAP", 0.0, 1.0)
            numeric_inputs["MDVP:PPQ"] = st.number_input("PPQ", 0.0, 1.0)
            numeric_inputs["DDP"] = st.number_input("DDP", 0.0, 1.0)

        with col3:
            st.markdown("**Shimmer Measurements**")
            numeric_inputs["MDVP:Shimmer"] = st.number_input("Shimmer", 0.0, 1.0)
            numeric_inputs["MDVP:Shimmer(dB)"] = st.number_input("Shimmer(dB)", 0.0, 5.0)
            numeric_inputs["APQ3"] = st.number_input("APQ3", 0.0, 1.0)
            numeric_inputs["APQ5"] = st.number_input("APQ5", 0.0, 1.0)
            numeric_inputs["APQ"] = st.number_input("APQ", 0.0, 1.0)
            numeric_inputs["DDA"] = st.number_input("DDA", 0.0, 1.0)

        col4, col5 = st.columns(2)
        with col4:
            st.markdown("**Other Measurements**")
            numeric_inputs["NHR"] = st.number_input("NHR", 0.0, 1.0)
            numeric_inputs["HNR"] = st.number_input("HNR", 0.0, 50.0)
            numeric_inputs["RPDE"] = st.number_input("RPDE", 0.0, 2.0)

        with col5:
            st.markdown("**Nonlinear Measures**")
            numeric_inputs["DFA"] = st.number_input("DFA", 0.0, 2.0)
            numeric_inputs["Spread1"] = st.number_input("Spread1", -10.0, 10.0)
            numeric_inputs["Spread2"] = st.number_input("Spread2", -10.0, 10.0)
            numeric_inputs["D2"] = st.number_input("D2", 0.0, 5.0)
            numeric_inputs["PPE"] = st.number_input("PPE", 0.0, 2.0)

    st.markdown('</div>', unsafe_allow_html=True)

    # Prediction section
    st.markdown("### 🔍 Step 3: Get Prediction")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        predict_button = st.button("🔮 Predict Disease", use_container_width=True)

    if predict_button:
        if all(value != 0 and value != "" for value in numeric_inputs.values() if isinstance(value, (int, float))):
            with st.spinner("🔄 Analyzing your data..."):
                time.sleep(1.5)  # Simulate processing time

            input_df = pd.DataFrame([numeric_inputs])
            prediction = model.predict(input_df)
            prediction_proba = model.predict_proba(input_df)[0]

            if disease_predicted == "Diabetes":
                result = "Positive (Has Diabetes)" if prediction[0] == 1 else "Negative (No Diabetes)"
                confidence = prediction_proba[1] if prediction[0] == 1 else prediction_proba[0]
            elif disease_predicted == "Heart Disease":
                result = "Positive (Has Heart Disease)" if prediction[0] == 1 else "Negative (No Heart Disease)"
                confidence = prediction_proba[1] if prediction[0] == 1 else prediction_proba[0]
            elif disease_predicted == "Liver Disease":
                result = "Positive (Has Liver Disease)" if prediction[0] == 1 else "Negative (No Liver Disease)"
                confidence = prediction_proba[1] if prediction[0] == 1 else prediction_proba[0]
            else:  # Parkinson's
                result = "Positive (Has Parkinson's)" if prediction[0] == 1 else "Negative (No Parkinson's)"
                confidence = prediction_proba[1] if prediction[0] == 1 else prediction_proba[0]

            st.markdown(f'''
            <div class="prediction-result">
                <h2>🎯 Prediction Result</h2>
                <h3>{result}</h3>
                <p><strong>Confidence: {confidence:.1%}</strong></p>
                <p>Disease: {disease_predicted}</p>
            </div>
            ''', unsafe_allow_html=True)

            # Recommendations
            st.markdown("### 💡 Personalized Recommendations")
            st.markdown(f'<div class="recommendation-box"><h4>📋 Recommended Actions for {disease_predicted}:</h4></div>', unsafe_allow_html=True)

            for advice in recommendations[disease_predicted]["advice"]:
                st.markdown(f"• {advice}")

            st.markdown("---")
            st.warning("⚠️ **Important:** This prediction is for informational purposes only. Please consult a healthcare professional for proper diagnosis and treatment.")

        else:
            st.error("❌ Please fill in all the required medical parameters before making a prediction.")

else:
    if selected_symptoms:
        st.warning("🤔 The selected symptoms don't match any disease in our current database. Please try selecting different symptoms or consult a healthcare professional.")
    else:
        st.info("👆 Please select your symptoms above to get started with the prediction process.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #000000; padding: 2rem;">
    <p>🏥 <strong>Multi-Disease Prediction System</strong> | Powered by Sandhiya Durai</p>
    <p style="font-size: 0.8rem;">⚠️ Not a substitute for professional medical advice</p>
</div>
""", unsafe_allow_html=True)






