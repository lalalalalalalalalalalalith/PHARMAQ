
import streamlit as st

st.set_page_config(page_title="PHARMAQ - Clinical Primary Care System", layout="wide")

# -----------------------------
# PROFESSIONAL STYLING
# -----------------------------

st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}
.main-title {
    font-size: 48px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #0a3d62;
    text-align: center;
    margin-bottom: 5px;
}
.sub-title {
    font-size: 18px;
    text-align: center;
    color: #1e5f74;
    margin-bottom: 30px;
}
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #145374;
    margin-top: 20px;
}
.stButton>button {
    background-color: #0a3d62;
    color: white;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    transition: all 0.2s ease-in-out;
    border: none;
}
.stButton>button:hover {
    background-color: #145374;
    transform: translateY(-2px);
}
.stButton>button:active {
    background-color: #1abc9c;
    transform: scale(0.97);
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
    font-size: 14px;
    color: #0a3d62;
    font-family: 'Georgia', serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PHARMAQ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Structured Symptom-Based Primary Care Guidance</div>', unsafe_allow_html=True)

# -----------------------------
# DATABASE
# -----------------------------

database = {
"fever": {
    "Possible Causes": "Viral infection, seasonal flu, early bacterial infection.",
    "First Line": "Paracetamol",
    "Adult Dose": "500–650 mg every 6 hrs (max 4g/day)",
    "Child Dose": "10–15 mg/kg",
    "Tips": "Hydrate well, monitor temperature, rest.",
    "Clinical Note": "If persists >3 days, evaluate for dengue/malaria/typhoid.",
    "Red Flags": "Bleeding, severe headache, persistent vomiting."
},
"cold": {
    "Possible Causes": "Common viral URI, allergic rhinitis.",
    "First Line": "Cetirizine 10 mg",
    "Adult Dose": "10 mg once daily",
    "Child Dose": "5 mg once daily",
    "Tips": "Steam inhalation, warm fluids.",
    "Clinical Note": "Usually self-limiting within 1 week.",
    "Red Flags": "Breathlessness, high fever."
},
"cough": {
    "Possible Causes": "Viral infection, throat irritation.",
    "First Line": "Dextromethorphan syrup",
    "Adult Dose": "As per label",
    "Child Dose": "Pediatric dose",
    "Tips": "Hydration, avoid smoke exposure.",
    "Clinical Note": "If >2 weeks, evaluate for TB.",
    "Red Flags": "Blood in sputum, weight loss."
}
}

# -----------------------------
# SYMPTOM TO OTC SECTION
# -----------------------------

st.markdown('<div class="section-title">Symptom to OTC Suggestion</div>', unsafe_allow_html=True)

user_input = st.text_input("Type a symptom (e.g., fever, cough, cold)").lower()

if st.button("Get Clinical Guidance"):
    if user_input in database:
        data = database[user_input]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for key, value in data.items():
            if key == "Red Flags":
                st.markdown(f"### 🚨 {key}")
                st.error(value)
            elif key == "Tips":
                st.markdown(f"### 💡 {key}")
                st.info(value)
            else:
                st.markdown(f"### {key}")
                st.write(value)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Symptom not found in database. Try common terms.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
