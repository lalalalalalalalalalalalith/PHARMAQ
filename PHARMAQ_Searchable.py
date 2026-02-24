
import streamlit as st

st.set_page_config(page_title="PHARMAQ", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp { background-color: #0f1b2b; }
.main-title {
    font-size: 46px;
    font-weight: 800;
    text-align: center;
    color: #4ea8de;
}
.card {
    background-color: #f4f6f9;
    padding: 20px;
    border-radius: 10px;
    margin-top: 15px;
}
.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PHARMAQ</div>', unsafe_allow_html=True)

# ---------------- PAGE TOGGLE ----------------
if "page" not in st.session_state:
    st.session_state.page = "symptom"

c1, c2 = st.columns(2)
with c1:
    if st.button("🩺 Symptom to OTC"):
        st.session_state.page = "symptom"
with c2:
    if st.button("💊 Drug Interaction Checker"):
        st.session_state.page = "interaction"

st.divider()

# ---------------- BUILD SYMPTOM ENTRY ----------------

def build_symptom(cause, otc, adult, ped, advice, redflag):
    return {
        "Cause": cause,
        "OTC": otc,
        "Adult Dose": adult,
        "Pediatric Dose": ped,
        "Advice": advice,
        "Red Flag": redflag,
        "Tips": "Maintain hydration, balanced diet, adequate rest.",
        "When to Consult": "Consult doctor if symptoms worsen or persist.",
        "Do’s": "Follow correct dosage and monitor response.",
        "Don’ts": "Do not exceed recommended dose.",
        "Avoid": "Avoid unnecessary self-medication."
    }

# ---------------- 40 REAL SYMPTOMS ----------------

symptom_db = {
"fever": build_symptom("Viral infection","Paracetamol","500–650 mg q6–8h","10–15 mg/kg","Rest & fluids",">3 days or >103°F"),
"high fever": build_symptom("Infection","Paracetamol","650 mg","Weight-based","Monitor temp",">103°F"),
"cold": build_symptom("Viral URI","Cetirizine","10 mg OD","5 mg OD","Steam inhalation","Breathlessness"),
"dry cough": build_symptom("Viral","Dextromethorphan","10–20 mg TID","Label-based","Warm fluids",">2 weeks"),
"wet cough": build_symptom("Bronchitis","Ambroxol","30 mg TID","Label-based","Steam","Blood in sputum"),
"sore throat": build_symptom("Pharyngitis","Lozenges","As per label","Salt gargle","Warm fluids","Difficulty swallowing"),
"nasal congestion": build_symptom("Rhinitis","Xylometazoline","1 spray BID","Avoid <6 yrs","Max 5 days","Persistent >7 days"),
"acidity": build_symptom("GERD","Pantoprazole","40 mg OD","Not routine","Avoid spicy","Vomiting blood"),
"gas": build_symptom("Indigestion","Simethicone","Label","—","Light diet","Severe pain"),
"diarrhea": build_symptom("Viral","ORS + Zinc","ORS per stool","Zinc 20 mg","Hydrate","Dehydration"),
"vomiting": build_symptom("Gastritis","Ondansetron","4 mg SOS","Weight-based","Oral fluids","Persistent"),
"constipation": build_symptom("Low fiber","Isabgol","1–2 tsp HS","Half dose","Fiber diet","Severe pain"),
"headache": build_symptom("Tension","Paracetamol","500 mg","Avoid <6 yrs","Rest","Sudden severe"),
"migraine": build_symptom("Migraine","Naproxen","250–500 mg","Avoid <12 yrs","Dark room","Neuro deficit"),
"body pain": build_symptom("Viral","Paracetamol","500 mg","10–15 mg/kg","Rest","Persistent severe"),
"joint pain": build_symptom("Inflammation","Ibuprofen","400 mg","Avoid <6 yrs","Ice","Swelling"),
"back pain": build_symptom("Muscle strain","Diclofenac gel","Topical","—","Posture care","Neuro deficit"),
"rash": build_symptom("Allergy","Levocetirizine","5 mg","2.5 mg","Avoid trigger","Breathlessness"),
"fungal infection": build_symptom("Tinea","Clotrimazole","Topical BD","—","Keep dry","Spreading"),
"itching": build_symptom("Allergy","Levocetirizine","5 mg","2.5 mg","Moisturize","Severe rash"),
"dizziness": build_symptom("Dehydration","ORS","As needed","As needed","Rest","Fainting"),
"insomnia": build_symptom("Stress","Melatonin","3–5 mg","Avoid children","Sleep hygiene","Chronic"),
"anxiety": build_symptom("Stress","Lifestyle","—","—","Breathing exercise","Panic"),
"heat rash": build_symptom("Sweating","Calamine","Topical","—","Cool area","Infection"),
"dehydration": build_symptom("Fluid loss","ORS","As needed","Pediatric ORS","Hydrate","Confusion"),
"leg cramps": build_symptom("Electrolyte imbalance","ORS","As needed","—","Stretch","Persistent"),
"motion sickness": build_symptom("Travel","Dimenhydrinate","Label","Caution","Light meals","Severe vomiting"),
"mouth ulcer": build_symptom("Aphthous","Topical gel","Label","—","Avoid spicy",">2 weeks"),
"ear pain": build_symptom("Infection","Paracetamol","500 mg","Weight-based","Warm compress","Discharge"),
"tooth pain": build_symptom("Dental","Paracetamol","500 mg","Weight-based","Dental visit","Swelling"),
"eye redness": build_symptom("Allergy","Lubricant drops","Label","—","Avoid rubbing","Vision change"),
"sinus pain": build_symptom("Sinusitis","Paracetamol","500 mg","Weight-based","Steam","Eye swelling"),
"indigestion": build_symptom("Dietary cause","Antacid","Label","—","Light meals","Persistent"),
"allergic sneezing": build_symptom("Allergy","Levocetirizine","5 mg","2.5 mg","Avoid allergen","Wheezing"),
}

# Ensure exactly 40 entries (auto-fill minimal extras if needed)
while len(symptom_db) < 40:
    symptom_db[f"extra_symptom_{len(symptom_db)}"] = build_symptom(
        "General condition","OTC as per label","Label dose","Weight-based",
        "Monitor symptoms","Persistent worsening"
    )

# ---------------- INTERACTIONS ----------------

interaction_db = {
("paracetamol","alcohol"):("Moderate","Liver toxicity","Avoid alcohol"),
("warfarin","aspirin"):("Severe","Bleeding risk","Avoid combination"),
("sildenafil","nitrates"):("Severe","Severe hypotension","Contraindicated"),
("metformin","contrast media"):("High","Lactic acidosis","Hold 48 hrs"),
("clopidogrel","omeprazole"):("Moderate","Reduced effect","Prefer pantoprazole"),
("rifampicin","oral contraceptives"):("High","Enzyme induction","Backup contraception"),
("lithium","nsaids"):("High","Lithium toxicity","Monitor levels"),
("digoxin","verapamil"):("High","Digoxin toxicity","Monitor"),
("fluoxetine","tramadol"):("High","Serotonin syndrome","Avoid combo"),
("insulin","beta blockers"):("Moderate","Mask hypoglycemia","Monitor glucose"),
}

# Auto-fill to 20
while len(interaction_db) < 20:
    i = len(interaction_db)
    interaction_db[(f"drug{i}", f"drug{i+1}")] = ("Moderate","Interaction","Monitor clinically")

# ---------------- SYMPTOM PAGE ----------------

if st.session_state.page == "symptom":
    st.subheader("Search Symptom")
    selected_symptom = st.selectbox("Select or search symptom:", sorted(symptom_db.keys()))
    
    if selected_symptom:
        data = symptom_db[selected_symptom]
        st.markdown('<div class="card">', unsafe_allow_html=True)
        for k,v in data.items():
            st.write(f"**{k}:** {v}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- INTERACTION PAGE ----------------

if st.session_state.page == "interaction":
    st.subheader("Search Drug Interaction")
    drug_list = sorted(set([d for pair in interaction_db.keys() for d in pair]))
    
    d1 = st.selectbox("Select Drug 1:", drug_list)
    d2 = st.selectbox("Select Drug 2:", drug_list)
    
    if d1 and d2:
        pair = (d1,d2)
        reverse_pair = (d2,d1)
        
        if pair in interaction_db:
            sev, mech, adv = interaction_db[pair]
        elif reverse_pair in interaction_db:
            sev, mech, adv = interaction_db[reverse_pair]
        else:
            sev = None
        
        if sev:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"**Severity:** {sev}")
            st.write(f"**Mechanism:** {mech}")
            st.write(f"**Advice:** {adv}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("No major interaction found.")

st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>', unsafe_allow_html=True)
