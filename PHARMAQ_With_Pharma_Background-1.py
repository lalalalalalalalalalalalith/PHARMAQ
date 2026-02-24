
import streamlit as st
import difflib

st.set_page_config(page_title="PHARMAQ", layout="wide")

# ---------------- STYLE WITH PHARMA BACKGROUND ----------------

st.markdown("""
<style>

/* Pharma chemistry background pattern */
.stApp {
    background-color: #0b1c2d;
    background-image:
        radial-gradient(circle at 10% 20%, rgba(0,150,255,0.08) 2px, transparent 2px),
        radial-gradient(circle at 80% 70%, rgba(0,200,255,0.06) 2px, transparent 2px),
        radial-gradient(circle at 40% 80%, rgba(0,180,255,0.05) 2px, transparent 2px);
    background-size: 120px 120px;
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: #3da9fc;
    letter-spacing: 2px;
}

.card {
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.25);
    margin-top: 20px;
}

.disclaimer {
    background-color: rgba(255, 107, 107, 0.15);
    border-left: 4px solid #ff6b6b;
    padding: 15px;
    border-radius: 8px;
    margin-top: 30px;
    font-size: 14px;
    color: #ffffff;
}

.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
    color: #ffffff;
}

.stButton>button {
    background: linear-gradient(135deg, #1e90ff, #00c6ff);
    color: white;
    border-radius: 10px;
    padding: 8px 18px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
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

# ---------------- SYMPTOM DATABASE ----------------

symptom_db = {
"fever":"Paracetamol 500–650 mg | Hydration | Red flag: >3 days",
"dizziness":"Check BP, hydrate | If persistent seek medical review",
"cold":"Cetirizine 10 mg | Steam inhalation",
"dry cough":"Dextromethorphan 10–20 mg TID",
"wet cough":"Ambroxol 30 mg TID",
"acidity":"Pantoprazole 40 mg before food",
"vomiting":"Ondansetron 4 mg SOS",
"diarrhea":"ORS + Zinc",
"headache":"Paracetamol 500 mg | Rest",
"body pain":"Paracetamol 500 mg",
"rash":"Levocetirizine 5 mg",
"eye redness":"Lubricant drops",
"nasal congestion":"Xylometazoline spray (max 5 days)"
}

combo_db = {
frozenset(["fever","cold"]):"Likely viral URTI | PCM + Cetirizine",
frozenset(["diarrhea","vomiting"]):"Gastroenteritis | ORS + Zinc + Ondansetron",
frozenset(["fever","body pain"]):"Viral fever pattern | PCM + fluids"
}

# ---------------- INTERACTION DATABASE ----------------

interaction_db = {
frozenset(["paracetamol","alcohol"]):("Moderate","Hepatotoxicity risk","Avoid alcohol"),
frozenset(["warfarin","aspirin"]):("Severe","Bleeding risk","Avoid combination"),
frozenset(["sildenafil","nitrates"]):("Severe","Severe hypotension","Contraindicated"),
frozenset(["metformin","contrast media"]):("High","Lactic acidosis risk","Hold 48 hrs")
}

# ---------------- SYMPTOM PAGE ----------------

if st.session_state.page == "symptom":
    st.subheader("Symptom to OTC Suggestion")
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
                st.warning("Combination not found in database.")
        else:
            term = parts[0]
            if term in symptom_db:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(symptom_db[term])
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                suggestions = difflib.get_close_matches(term, symptom_db.keys(), n=3, cutoff=0.7)
                if suggestions:
                    st.warning("Symptom not found.")
                    st.write("Did you mean:")
                    for s in suggestions:
                        if st.button(s):
                            st.markdown('<div class="card">', unsafe_allow_html=True)
                            st.write(symptom_db[s])
                            st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Symptom not found in database.")

# ---------------- INTERACTION PAGE ----------------

if st.session_state.page == "interaction":
    st.subheader("Drug Interaction Checker")
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
            st.write(f"Mechanism: {mech}")
            st.write(f"Advice: {adv}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("No major interaction found in database.")

st.markdown('<div class="disclaimer">⚠ Primary care guidance only. Not a substitute for medical consultation.</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
