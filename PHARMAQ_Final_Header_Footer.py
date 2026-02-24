
import streamlit as st

st.set_page_config(page_title="PHARMAQ - Clinical Primary Care System", layout="wide")

# -----------------------------
# PROFESSIONAL STYLING + HEADER + FOOTER
# -----------------------------

st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}

/* Header Styling */
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

/* Button Styling */
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

/* Card Styling */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Footer Styling */
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
# SAMPLE DATABASE
# -----------------------------

database = {
"Respiratory": {
    "Common Cold": {
        "Possible Causes": "Viral upper respiratory infection, allergic rhinitis.",
        "First Line": "Cetirizine 10 mg once daily",
        "Adult Dose": "10 mg OD",
        "Child Dose": "5 mg OD",
        "Tips": "Steam inhalation, warm fluids, rest.",
        "Clinical Note": "Usually resolves in 5–7 days.",
        "Red Flags": "Breathlessness, high fever >3 days."
    }
},
"Gastrointestinal": {
    "Acidity": {
        "Possible Causes": "Gastritis, dietary factors.",
        "First Line": "Pantoprazole 40 mg before food",
        "Adult Dose": "40 mg OD",
        "Child Dose": "Consult pediatric dose",
        "Tips": "Avoid spicy food, small frequent meals.",
        "Clinical Note": "Reassess if persistent >2 weeks.",
        "Red Flags": "Black stools, severe pain."
    }
}
}

interactions = {
    ("warfarin","aspirin"): ("Severe","High bleeding risk"),
    ("fluoxetine","tramadol"): ("High","Serotonin syndrome risk")
}

# -----------------------------
# NAVIGATION
# -----------------------------

st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["Primary Care Guidance", "Drug Interaction Checker"])

if section == "Primary Care Guidance":
    st.header("🩺 Primary Care Guidance")

    category = st.selectbox("Select Category", list(database.keys()))
    condition = st.selectbox("Select Condition", list(database[category].keys()))

    if st.button("Get Clinical Guidance"):
        data = database[category][condition]
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

elif section == "Drug Interaction Checker":
    st.header("🔎 Drug Interaction Checker")

    drug1 = st.text_input("Enter First Drug").lower()
    drug2 = st.text_input("Enter Second Drug").lower()

    if st.button("Check Interaction"):
        if (drug1,drug2) in interactions:
            severity,message = interactions[(drug1,drug2)]
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.error(f"Severity: {severity}")
            st.write(f"Interaction: {message}")
            st.markdown('</div>', unsafe_allow_html=True)
        elif (drug2,drug1) in interactions:
            severity,message = interactions[(drug2,drug1)]
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.error(f"Severity: {severity}")
            st.write(f"Interaction: {message}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("No major interaction found in database.")

st.markdown('<div class="footer">By Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
