
import streamlit as st

st.set_page_config(page_title="PHARMAQ - Clinical Primary Care System", layout="wide")

st.markdown("""
<style>
body { background-color: #f4f7fb; }
.main-title {
    font-size: 48px; font-weight: 800; letter-spacing: 3px;
    color: #0a3d62; text-align: center; margin-bottom: 5px;
}
.sub-title {
    font-size: 18px; text-align: center;
    color: #1e5f74; margin-bottom: 30px;
}
.section-title {
    font-size: 22px; font-weight: 700;
    color: #145374; margin-top: 25px;
}
.stButton>button {
    background-color: #0a3d62; color: white;
    border-radius: 8px; padding: 8px 18px;
    font-weight: 600; transition: 0.2s;
}
.stButton>button:hover {
    background-color: #145374; transform: translateY(-2px);
}
.stButton>button:active {
    background-color: #1abc9c; transform: scale(0.97);
}
.card {
    background-color: white; padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}
.footer {
    position: fixed; bottom: 10px; right: 20px;
    font-weight: bold; font-size: 14px;
    color: #0a3d62; font-family: Georgia, serif;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PHARMAQ</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Structured Symptom-Based Primary Care Guidance</div>', unsafe_allow_html=True)

symptom_db = {
    "cold": {
        "Possible Causes": "Viral URI, allergic rhinitis",
        "First Line": "Cetirizine 10 mg",
        "Adult Dose": "10 mg OD",
        "Child Dose": "5 mg OD",
        "Tips": "Steam inhalation",
        "Clinical Note": "Self-limiting 5–7 days",
        "Red Flags": "High fever, breathlessness"
    },
    "fever (mild)": {
        "Possible Causes": "Viral infection",
        "First Line": "Paracetamol 500 mg",
        "Adult Dose": "500–650 mg q6–8h",
        "Child Dose": "10–15 mg/kg",
        "Tips": "Lukewarm sponging",
        "Clinical Note": "Usually viral",
        "Red Flags": ">103°F, >3 days"
    },
    "headache": {
        "Possible Causes": "Tension, stress",
        "First Line": "Paracetamol",
        "Adult Dose": "500 mg SOS",
        "Child Dose": "Avoid <6 yrs OTC",
        "Tips": "Rest, hydration",
        "Clinical Note": "Common benign",
        "Red Flags": "Severe sudden pain"
    },
    "acidity": {
        "Possible Causes": "GERD, spicy food",
        "First Line": "Pantoprazole 40 mg",
        "Adult Dose": "40 mg OD",
        "Child Dose": "Not routine OTC",
        "Tips": "Avoid spicy food",
        "Clinical Note": "Lifestyle related",
        "Red Flags": "Vomiting blood"
    }
}

interaction_db = {
    ("warfarin", "aspirin"): {
        "Type": "Pharmacodynamic (Additive)",
        "Effect": "Increased bleeding risk",
        "Advice": "Avoid combination or monitor INR"
    },
    ("warfarin", "metronidazole"): {
        "Type": "Pharmacokinetic (CYP2C9 inhibition)",
        "Effect": "Increased INR",
        "Advice": "Reduce warfarin dose, monitor INR"
    },
    ("clopidogrel", "omeprazole"): {
        "Type": "CYP2C19 inhibition",
        "Effect": "Reduced antiplatelet effect",
        "Advice": "Prefer pantoprazole"
    },
    ("metformin", "contrast media"): {
        "Type": "Nephrotoxic risk",
        "Effect": "Lactic acidosis risk",
        "Advice": "Hold metformin 48 hrs"
    },
    ("sildenafil", "nitrates"): {
        "Type": "Severe vasodilation",
        "Effect": "Hypotension",
        "Advice": "Contraindicated"
    }
}

st.markdown('<div class="section-title">Symptom to OTC Suggestion</div>', unsafe_allow_html=True)

symptom_input = st.text_input("Type symptom").lower()

if st.button("Get Clinical Guidance"):
    if symptom_input in symptom_db:
        data = symptom_db[symptom_input]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for k, v in data.items():
            if k == "Red Flags":
                st.error(f"{k}: {v}")
            else:
                st.write(f"**{k}:** {v}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("Symptom not found in database.")

st.divider()

st.markdown('<div class="section-title">Drug Interaction Checker</div>', unsafe_allow_html=True)

drug1 = st.text_input("First Drug").lower()
drug2 = st.text_input("Second Drug").lower()

if st.button("Check Interaction"):
    if (drug1, drug2) in interaction_db:
        data = interaction_db[(drug1, drug2)]
    elif (drug2, drug1) in interaction_db:
        data = interaction_db[(drug2, drug1)]
    else:
        data = None

    if data:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"**Type:** {data['Type']}")
        st.write(f"**Effect:** {data['Effect']}")
        st.write(f"**Clinical Advice:** {data['Advice']}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.success("No major interaction found.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
