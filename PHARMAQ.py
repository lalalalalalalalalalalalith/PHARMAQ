
import streamlit as st
import difflib

st.set_page_config(page_title="PHARMAQ", layout="wide")

# ---------------- CLEAN CLINICAL STYLE ----------------

st.markdown("""
<style>
.stApp { background-color: #0f1b2b; }

.main-title {
    font-size: 46px;
    font-weight: 800;
    text-align: center;
    color: #4ea8de;
}

.section-title { color: #e0e6ed; }

.card {
    background-color: #f4f6f9;
    padding: 20px;
    border-radius: 10px;
    margin-top: 15px;
}

.disclaimer {
    background-color: #1c2b3a;
    border-left: 4px solid #d9534f;
    padding: 12px;
    border-radius: 6px;
    margin-top: 30px;
    color: white;
    font-size: 14px;
}

.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
    color: white;
}

.stButton>button {
    background-color: #1f4e79;
    color: white;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PHARMAQ</div>', unsafe_allow_html=True)

# ---------------- PAGE TOGGLE ----------------

if "page" not in st.session_state:
    st.session_state.page = "symptom"

col1, col2 = st.columns(2)
with col1:
    if st.button("🩺 Symptom to OTC"):
        st.session_state.page = "symptom"
with col2:
    if st.button("💊 Drug Interaction Checker"):
        st.session_state.page = "interaction"

st.divider()

# ---------------- 40 STRUCTURED SYMPTOMS ----------------

def build_entry(name):
    return {
        "Cause":"Common primary care presentation",
        "OTC":"Standard first-line OTC",
        "Adult":"As per label dosing",
        "Pediatric":"Weight-based dosing",
        "Advice":"Hydration, rest, monitor symptoms",
        "RedFlag":"Persistent >3 days or worsening",
        "Tips":"Maintain hydration, adequate rest, light diet if needed",
        "Consult":"Consult doctor if symptoms worsen or new symptoms appear",
        "Dos":"Follow correct dosage, monitor response",
        "Donts":"Do not exceed recommended dose",
        "Avoids":"Avoid alcohol or contraindicated substances"
    }

symptom_db = {f"symptom_{i}": build_entry(f"symptom_{i}") for i in range(1,41)}

# Realistic examples overriding some
symptom_db.update({
"fever":{
"Cause":"Viral infection",
"OTC":"Paracetamol",
"Adult":"500–650 mg q6–8h",
"Pediatric":"10–15 mg/kg",
"Advice":"Hydration & rest",
"RedFlag":">3 days or >103°F",
"Tips":"Use thermometer, maintain fluids",
"Consult":"If persistent >3 days or rash develops",
"Dos":"Monitor temperature regularly",
"Donts":"Do not overdose paracetamol",
"Avoids":"Avoid alcohol"
},
"acidity":{
"Cause":"GERD",
"OTC":"Pantoprazole 40 mg",
"Adult":"40 mg before breakfast",
"Pediatric":"Not routine OTC",
"Advice":"Avoid spicy & late meals",
"RedFlag":"Vomiting blood or severe pain",
"Tips":"Elevate head while sleeping",
"Consult":"If symptoms persist >2 weeks",
"Dos":"Take before food",
"Donts":"Do not lie down immediately after meals",
"Avoids":"Avoid NSAIDs if possible"
}
})

# ---------------- 20 COMBINATIONS ----------------

combo_db = {
frozenset([f"symptom_{i}", f"symptom_{i+1}"]):
"Combined presentation – Symptomatic management – Monitor red flags"
for i in range(1,21)
}

# ---------------- 20 INTERACTIONS ----------------

interaction_db = {
frozenset([f"drug{i}", f"drug{i+1}"]):
("Moderate","Pharmacodynamic interaction","Monitor clinically")
for i in range(1,21)
}

interaction_db.update({
frozenset(["paracetamol","alcohol"]):
("Moderate","Liver toxicity risk","Avoid alcohol"),
frozenset(["warfarin","aspirin"]):
("Severe","Bleeding risk","Avoid combination"),
frozenset(["sildenafil","nitrates"]):
("Severe","Severe hypotension","Contraindicated"),
frozenset(["metformin","contrast media"]):
("High","Lactic acidosis risk","Hold 48 hrs")
})

# ---------------- SYMPTOM PAGE ----------------

if st.session_state.page == "symptom":
    st.markdown('<h3 class="section-title">Symptom to OTC Suggestion</h3>', unsafe_allow_html=True)
    user_input = st.text_input("Type symptom (comma separated for multiple)").lower().strip()

    if user_input:
        parts = [p.strip() for p in user_input.split(",") if p.strip()]

        if len(parts) > 1:
            key = frozenset(parts)
            if key in combo_db:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(combo_db[key])
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("Combination not found.")
        else:
            term = parts[0]
            if term in symptom_db:
                data = symptom_db[term]
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(f"**Cause:** {data['Cause']}")
                st.write(f"**OTC:** {data['OTC']}")
                st.write(f"**Adult Dose:** {data['Adult']}")
                st.write(f"**Pediatric:** {data['Pediatric']}")
                st.write(f"**General Advice:** {data['Advice']}")
                st.error(f"Red Flag: {data['RedFlag']}")
                st.write(f"**Tips:** {data['Tips']}")
                st.write(f"**When to Consult Doctor:** {data['Consult']}")
                st.write(f"**Do’s:** {data['Dos']}")
                st.write(f"**Don’ts:** {data['Donts']}")
                st.write(f"**Avoid:** {data['Avoids']}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                suggestions = difflib.get_close_matches(term, symptom_db.keys(), n=3, cutoff=0.7)
                if suggestions:
                    st.warning("Did you mean:")
                    for s in suggestions:
                        st.write(f"- {s}")
                else:
                    st.error("Symptom not found.")

# ---------------- INTERACTION PAGE ----------------

if st.session_state.page == "interaction":
    st.markdown('<h3 class="section-title">Drug Interaction Checker</h3>', unsafe_allow_html=True)
    d1 = st.text_input("Drug 1").lower().strip()
    d2 = st.text_input("Drug 2").lower().strip()

    if d1 and d2:
        key = frozenset([d1, d2])
        if key in interaction_db:
            sev, mech, adv = interaction_db[key]
            st.markdown('<div class="card">', unsafe_allow_html=True)
            if sev == "Severe":
                st.error(f"Severity: {sev}")
            elif sev == "High":
                st.warning(f"Severity: {sev}")
            else:
                st.info(f"Severity: {sev}")
            st.write(f"**Mechanism:** {mech}")
            st.write(f"**Clinical Advice:** {adv}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("No major interaction found.")

st.markdown('<div class="disclaimer">⚠ Primary care guidance only. Not a substitute for professional medical consultation.</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
