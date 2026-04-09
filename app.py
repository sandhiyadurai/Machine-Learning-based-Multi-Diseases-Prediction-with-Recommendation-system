# symptom_based_multi_disease_app.py
import streamlit as st
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
        color: white; /* Light text on colored background */
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
    /* Doctor referral section */
    .doctor-section {
        background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(123,97,255,0.08));
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
    }
    .doctor-section h3 {
        color: black;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .doctor-section p { color: #8899aa; font-size: 0.9rem; margin-bottom: 1.5rem; }

    .doctor-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
    }

    .doctor-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .doctor-card:hover {
        border-color: rgba(0,212,255,0.4);
        background: rgba(0,212,255,0.06);
        transform: translateY(-3px);
    }
    .doctor-card .platform-name {
        font-weight: 700;
        font-size: 1rem;
        color: black;
        margin-bottom: 0.3rem;
    }
    .doctor-card .platform-desc {
        font-size: 0.78rem;
        color: #8899aa;
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }
    .doctor-card .visit-btn {
        display: inline-block;
        background: linear-gradient(135deg, #7b61ff, #00d4ff);
        color: black !important;
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        text-decoration: none;
        letter-spacing: 0.03em;
    }
    .doctor-card .specialty-tag {
        display: inline-block;
        background: rgba(123,97,255,0.15);
        color: black;
        padding: 0.2rem 0.6rem;
        border-radius: 50px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .symptom-tag {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #1976d2;
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
</style>
""", unsafe_allow_html=True)

# Disease recommendations with more detailed advice
recommendations = {
    "Diabetes": {
        "description": "Diabetes is a condition that affects how your body processes blood sugar.",
        "specialist": "Endocrinologist",
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
        "specialist": "Cardiologist",
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
        "specialist": "Hepatologist",
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
        "specialist": "Neurologist",
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

# ─── Doctor referral platforms ───────────────────────────────────────────────
doctor_platforms = {
    "Diabetes": [
        {"name": "Practo", "url": "https://www.practo.com/consult/endocrinologist", "desc": "Book certified endocrinologists in minutes. Video, audio, or chat consult.", "specialty": "Endocrinology"},
        {"name": "Apollo 247", "url": "https://apollo247.com/specialties/endocrinology", "desc": "24/7 access to Apollo doctors. Trusted network across India.", "specialty": "Endocrinology"},
        {"name": "1mg Health", "url": "https://www.1mg.com/consult", "desc": "Doctor consultations + medicine delivery. Convenient all-in-one.", "specialty": "General & Specialist"},
        {"name": "DocOnline", "url": "https://doconline.com", "desc": "Instant doctor consultations online. Subscription-based plans available.", "specialty": "Endocrinology"},
        {"name": "Healthplix", "url": "https://healthplix.com", "desc": "AI-assisted smart clinic platform connecting patients with specialists.", "specialty": "Specialist"},
        {"name": "mfine", "url": "https://www.mfine.co", "desc": "Top hospital doctors online. Multispecialty consultations from home.", "specialty": "Multispecialty"},
    ],
    "Heart Disease": [
        {"name": "Practo", "url": "https://www.practo.com/consult/cardiologist", "desc": "Top cardiologists available online instantly. Rated & reviewed.", "specialty": "Cardiology"},
        {"name": "Apollo 247", "url": "https://apollo247.com/specialties/cardiology", "desc": "24/7 cardiac consultations from Apollo's expert cardiologists.", "specialty": "Cardiology"},
        {"name": "Max Healthcare", "url": "https://www.maxhealthcare.in/speciality/cardiology", "desc": "World-class cardiac care. Tele-consult with senior cardiologists.", "specialty": "Cardiology"},
        {"name": "mfine", "url": "https://www.mfine.co", "desc": "Hospital-grade cardiac specialists accessible from your home.", "specialty": "Cardiology"},
        {"name": "Medibuddy", "url": "https://www.medibuddy.in", "desc": "Corporate health plans & instant specialist consults. Pan-India.", "specialty": "Multispecialty"},
        {"name": "Lybrate", "url": "https://www.lybrate.com/cardiology-specialist", "desc": "Real-time Q&A and video consults with verified cardiologists.", "specialty": "Cardiology"},
    ],
    "Liver Disease": [
        {"name": "Practo", "url": "https://www.practo.com/consult/gastroenterologist", "desc": "Verified gastroenterologists & hepatologists available now.", "specialty": "Hepatology"},
        {"name": "Apollo 247", "url": "https://apollo247.com/specialties/gastroenterology", "desc": "Expert liver specialists from Apollo's network.", "specialty": "Gastroenterology"},
        {"name": "Fortis Healthcare", "url": "https://www.fortishealthcare.com/speciality/hepatology", "desc": "Specialised hepatology tele-consult with senior consultants.", "specialty": "Hepatology"},
        {"name": "1mg Health", "url": "https://www.1mg.com/consult", "desc": "Consult + liver function test packages. End-to-end liver care.", "specialty": "Hepatology"},
        {"name": "Lybrate", "url": "https://www.lybrate.com/gastroenterologist", "desc": "Chat, call, or video with experienced gastroenterologists.", "specialty": "Gastroenterology"},
        {"name": "mfine", "url": "https://www.mfine.co", "desc": "Hospital-affiliated liver specialists at your fingertips.", "specialty": "Multispecialty"},
    ],
    "Parkinson's Disease": [
        {"name": "Practo", "url": "https://www.practo.com/consult/neurologist", "desc": "Top neurologists for Parkinson's consultations online.", "specialty": "Neurology"},
        {"name": "Apollo 247", "url": "https://apollo247.com/specialties/neurology", "desc": "Apollo neurologists available 24/7 for tele-consultations.", "specialty": "Neurology"},
        {"name": "NIMHANS Tele", "url": "https://nimhans.ac.in", "desc": "India's premier neuroscience institute with tele-neurology services.", "specialty": "Neurology"},
        {"name": "Max Healthcare", "url": "https://www.maxhealthcare.in/speciality/neurology", "desc": "Senior Parkinson's specialists for video consultations.", "specialty": "Neurology"},
        {"name": "mfine", "url": "https://www.mfine.co", "desc": "Certified neurologists from top hospitals. Easy scheduling.", "specialty": "Neurology"},
        {"name": "Lybrate", "url": "https://www.lybrate.com/neurologist", "desc": "Expert neurologists for movement disorder consultations.", "specialty": "Neurology"},
    ]
}

# Sidebar with information
with st.sidebar:
    st.title("ℹ️ About This System")
    st.markdown("""
    <div class="sidebar-info">
    <h4>🔬 How It Works</h4>
    <p>This AI-powered system uses symptom-based analysis to predict potential diseases and provide personalized health recommendations.</p>

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
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Select your symptoms and get AI-powered disease prediction with personalized recommendations</p>', unsafe_allow_html=True)

# Symptom selection with better UI
st.markdown("### 🎯 Select Your Symptoms")
st.markdown("Choose all symptoms you're experiencing:")

col1, col2, col3, col4 = st.columns(4)

symptoms_data = {
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
    "Parkinson's": [
        "Tremors", "Voice changes", "Stiffness", "Loss of balance",
        "Slow movement (bradykinesia)", "Mask-like facial expression",
        "Micrographia (small handwriting)", "Sleep disturbances",
        "Reduced arm swing while walking", "Constipation",
        "Loss of smell", "Depression or anxiety", "Drooling"
    ]
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

# Disease detection logic - simplified symptom-based prediction
if selected_symptoms:
    # Count symptoms per disease
    diabetes_count = sum(1 for s in selected_symptoms if s in symptoms_data["Diabetes"])
    heart_count = sum(1 for s in selected_symptoms if s in symptoms_data["Heart Disease"])
    liver_count = sum(1 for s in selected_symptoms if s in symptoms_data["Liver Disease"])
    parkinsons_count = sum(1 for s in selected_symptoms if s in symptoms_data["Parkinson's"])

    # Find disease with most matching symptoms
    counts = {
        "Diabetes": diabetes_count,
        "Heart Disease": heart_count,
        "Liver Disease": liver_count,
        "Parkinson's Disease": parkinsons_count
    }

    max_count = max(counts.values())
    if max_count > 0:
        # Get diseases with max count, prefer the first one if tie
        candidates = [d for d, c in counts.items() if c == max_count]
        disease_predicted = candidates[0]

# Show disease prediction and recommendations
if disease_predicted:
    st.markdown("---")
    st.markdown(f'<div class="disease-card"><h3>🎯 Detected Condition: {disease_predicted}</h3><p>{recommendations[disease_predicted]["description"]}</p></div>', unsafe_allow_html=True)

    # Prediction section
    st.markdown("### 🔍 Get Analysis & Recommendations")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        analyze_button = st.button("🔮 Analyze Symptoms", use_container_width=True)

    if analyze_button:
        with st.spinner("🔄 Analyzing your symptoms..."):
            time.sleep(1.5)

        # Calculate confidence based on symptom count
        symptom_count = sum(1 for s in selected_symptoms if s in symptoms_data[disease_predicted])
        total_symptoms = len(symptoms_data[disease_predicted])
        confidence = min(0.95, symptom_count / total_symptoms * 0.8 + 0.2)  # Cap at 95%, minimum 20%

        result = f"Potential {disease_predicted} Detected"
        risk_level = "High" if confidence > 0.7 else "Moderate" if confidence > 0.5 else "Low"

        st.markdown(f'''
        <div class="prediction-result">
            <h2>🎯 Analysis Result</h2>
            <h3>{result}</h3>
            <p><strong>Risk Level: {risk_level}</strong></p>
            <p>Confidence: {confidence:.1%}</p>
            <p>Matching Symptoms: {symptom_count} out of {total_symptoms}</p>
        </div>
        ''', unsafe_allow_html=True)

        # Recommendations
        st.markdown("### 💡 Personalized Health Recommendations")
        st.markdown(f'<div class="recommendation-box"><h4>📋 Recommended Actions for {disease_predicted}:</h4></div>', unsafe_allow_html=True)

        for advice in recommendations[disease_predicted]["advice"]:
            st.markdown(f"• {advice}")

        st.markdown("---")
        st.warning("⚠️ **Important:** This analysis is for informational purposes only. Please consult a healthcare professional for proper diagnosis and treatment.")

        # ─── Doctor Referral Section ──────────────────────────────────────────
        st.markdown("---")
        specialist = recommendations[disease_predicted]["specialist"]
        platforms = doctor_platforms.get(disease_predicted, [])

        st.markdown(f"""
        <div class="doctor-section">
            <h3>👨‍⚕️ Consult a {specialist} Online</h3>
            <p>Based on your symptoms, we recommend consulting a qualified {specialist}.
            Below are trusted telemedicine platforms where you can book an online consultation from the comfort of your home.</p>
            <div class="doctor-grid">
        """, unsafe_allow_html=True)

        for p in platforms:
            st.markdown(f"""
                <div class="doctor-card">
                    <div class="specialty-tag">{p['specialty']}</div>
                    <div class="platform-name">{p['name']}</div>
                    <div class="platform-desc">{p['desc']}</div>
                    <a href="{p['url']}" target="_blank" class="visit-btn">Book Now →</a>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

else:
    if selected_symptoms:
        st.warning("🤔 The selected symptoms don't strongly match any disease in our database. Please try selecting different symptoms or consult a healthcare professional.")
    else:
        st.info("👆 Please select your symptoms above to get started with the analysis.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:1.5rem 0; color:#556677;">
    <p style="font-size:1rem; font-weight:700; color:#7b61ff;">🏥 MediPredict </p>
    <p style="font-size:0.8rem;">Not a substitute for professional medical advice</p>
</div>
""", unsafe_allow_html=True)
