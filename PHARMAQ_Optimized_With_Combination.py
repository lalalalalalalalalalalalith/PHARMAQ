
import streamlit as st
import difflib

st.set_page_config(page_title="PHARMAQ", layout="wide")

# -----------------------------
# STYLE
# -----------------------------

st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    color: #0a3d62;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 20px;
}
.disclaimer {
    background-color: #2c2f36;
    border-left: 4px solid #ff6b6b;
    padding: 15px;
    border-radius: 8px;
    margin-top: 30px;
    font-size: 14px;
    color: #f1f1f1;
}
.footer {
    position: fixed;
    bottom: 10px;
    right: 20px;
    font-weight: bold;
}
.stButton>button {
    background-color: #0a3d62;
    color: white;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
    transition: 0.2s;
}
.stButton>button:hover {
    background-color: #145374;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">PHARMAQ</div>', unsafe_allow_html=True)

# -----------------------------
# PAGE TOGGLE
# -----------------------------

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

# -----------------------------
# BASE 40 SYMPTOM DATABASE
# -----------------------------

symptom_db = {
"fever":{"Cause":"Viral infection","OTC":"Paracetamol","Adult":"500–650 mg q6–8h","Pediatric":"10–15 mg/kg","Advice":"Hydration & rest","RedFlag":">3 days or bleeding"},
"cold":{"Cause":"Viral URI","OTC":"Cetirizine","Adult":"10 mg OD","Pediatric":"5 mg OD","Advice":"Steam inhalation","RedFlag":"Breathlessness"},
"dry cough":{"Cause":"Viral","OTC":"Dextromethorphan","Adult":"10–20 mg TID","Pediatric":"Label-based","Advice":"Warm fluids","RedFlag":">2 weeks"},
"wet cough":{"Cause":"Bronchitis","OTC":"Ambroxol","Adult":"30 mg TID","Pediatric":"Label-based","Advice":"Steam","RedFlag":"Blood in sputum"},
"acidity":{"Cause":"GERD","OTC":"Pantoprazole","Adult":"40 mg OD","Pediatric":"Not routine","Advice":"Avoid spicy","RedFlag":"Vomiting blood"},
"diarrhea":{"Cause":"Viral","OTC":"ORS + Zinc","Adult":"ORS per stool","Pediatric":"Zinc 20 mg","Advice":"Hydrate","RedFlag":"Dehydration"},
"vomiting":{"Cause":"Gastritis","OTC":"Ondansetron","Adult":"4 mg SOS","Pediatric":"Weight-based","Advice":"Oral fluids","RedFlag":"Persistent"},
"headache":{"Cause":"Tension","OTC":"Paracetamol","Adult":"500 mg","Pediatric":"Avoid <6 yrs","Advice":"Rest","RedFlag":"Sudden severe"},
"body pain":{"Cause":"Viral","OTC":"Paracetamol","Adult":"500 mg","Pediatric":"10–15 mg/kg","Advice":"Rest","RedFlag":"Severe"},
"rash":{"Cause":"Allergy","OTC":"Levocetirizine","Adult":"5 mg","Pediatric":"2.5 mg","Advice":"Avoid trigger","RedFlag":"Breathlessness"},
"constipation":{"Cause":"Low fiber","OTC":"Isabgol","Adult":"1–2 tsp HS","Pediatric":"Half dose","Advice":"Fiber diet","RedFlag":"Severe pain"},
"nasal congestion":{"Cause":"Rhinitis","OTC":"Xylometazoline","Adult":"1 spray BID","Pediatric":"Avoid <6 yrs","Advice":"Max 5 days","RedFlag":"Persistent"},
"joint pain":{"Cause":"Inflammation","OTC":"Ibuprofen","Adult":"400 mg","Pediatric":"Avoid <6 yrs","Advice":"Ice","RedFlag":"Swelling"},
"back pain":{"Cause":"Strain","OTC":"Diclofenac gel","Adult":"Topical","Pediatric":"—","Advice":"Posture care","RedFlag":"Neuro deficit"},
"fungal infection":{"Cause":"Tinea","OTC":"Clotrimazole","Adult":"BD","Pediatric":"—","Advice":"Keep dry","RedFlag":"Spreading"},
"minor burn":{"Cause":"Thermal","OTC":"Silver sulfadiazine","Adult":"Topical","Pediatric":"—","Advice":"Cool water","RedFlag":"Large area"},
"tooth pain":{"Cause":"Caries","OTC":"Paracetamol","Adult":"500 mg","Pediatric":"Weight-based","Advice":"Dental visit","RedFlag":"Swelling"},
"ear pain":{"Cause":"Infection","OTC":"Paracetamol","Adult":"500 mg","Pediatric":"Weight-based","Advice":"Warm compress","RedFlag":"Discharge"},
"eye redness":{"Cause":"Allergy","OTC":"Lubricant drops","Adult":"Label","Pediatric":"—","Advice":"Avoid rubbing","RedFlag":"Vision change"},
"itching":{"Cause":"Allergy","OTC":"Levocetirizine","Adult":"5 mg","Pediatric":"2.5 mg","Advice":"Moisturizer","RedFlag":"Severe rash"}
}

# -----------------------------
# 20 COMBINATION SYMPTOMS
# -----------------------------

combo_db = {
"fever,cold":"Likely viral URTI | Paracetamol + Cetirizine | Hydration | Monitor 3 days",
"fever,dry cough":"Possible viral infection | Paracetamol + Dextromethorphan | Steam",
"fever,wet cough":"Possible bronchitis | Paracetamol + Ambroxol | Medical review if persistent",
"fever,body pain":"Common viral fever | Paracetamol | Rest & fluids",
"cold,dry cough":"URTI | Cetirizine + Dextromethorphan",
"cold,wet cough":"Respiratory infection | Cetirizine + Ambroxol",
"acidity,vomiting":"Gastritis | Pantoprazole + Ondansetron",
"acidity,gas":"GERD + bloating | Pantoprazole + Simethicone",
"diarrhea,vomiting":"Gastroenteritis | ORS + Zinc + Ondansetron | Watch dehydration",
"headache,fever":"Viral fever | Paracetamol | Monitor",
"joint pain,fever":"Possible inflammatory | Paracetamol | Medical review if persistent",
"rash,itching":"Allergic reaction | Levocetirizine",
"back pain,body pain":"Muscle strain | NSAID gel + Rest",
"nasal congestion,headache":"Sinus congestion | Steam + Paracetamol",
"tooth pain,fever":"Dental infection | Paracetamol | Dentist review",
"ear pain,fever":"Ear infection | Paracetamol | ENT consult if persistent",
"vomiting,body pain":"Viral illness | Fluids + Paracetamol",
"fever,rash":"Viral exanthem | Paracetamol | Monitor red flags",
"cold,fever,body pain":"Flu-like illness | Paracetamol + Cetirizine",
"cough,fever,breathlessness":"Respiratory infection | Seek medical evaluation"
}

# -----------------------------
# INTERACTION DATABASE (20)
# -----------------------------

interaction_db = {
("warfarin","aspirin"):("Severe","Bleeding risk","Avoid or monitor INR"),
("warfarin","metronidazole"):("High","↑ INR","Reduce dose"),
("clopidogrel","omeprazole"):("Moderate","Reduced effect","Prefer pantoprazole"),
("metformin","contrast media"):("High","Lactic acidosis","Hold 48 hrs"),
("sildenafil","nitrates"):("Severe","Hypotension","Contraindicated"),
("paracetamol","alcohol"):("Moderate","Hepatotoxicity","Avoid alcohol"),
("lithium","nsaids"):("High","Lithium toxicity","Monitor levels"),
("digoxin","verapamil"):("High","Digoxin toxicity","Monitor"),
("fluoxetine","tramadol"):("High","Serotonin syndrome","Avoid combo"),
("insulin","beta blockers"):("Moderate","Mask hypoglycemia","Monitor glucose"),
("rifampicin","oral contraceptives"):("High","Reduced efficacy","Backup contraception"),
("atorvastatin","clarithromycin"):("Moderate","Myopathy","Monitor"),
("azithromycin","qt drugs"):("Moderate","QT prolongation","ECG caution"),
("amiodarone","warfarin"):("High","CYP inhibition","Reduce warfarin"),
("methotrexate","nsaids"):("High","Reduced clearance","Monitor toxicity"),
("losartan","potassium supplements"):("Moderate","Hyperkalemia","Monitor K"),
("ciprofloxacin","theophylline"):("Moderate","CYP inhibition","Monitor levels"),
("carbamazepine","ocp"):("High","Enzyme induction","Backup contraception"),
("ace inhibitor","spironolactone"):("High","Hyperkalemia","Monitor potassium"),
("warfarin","fluconazole"):("High","CYP inhibition","Monitor INR")
}

# -----------------------------
# PAGE 1 LOGIC
# -----------------------------

if st.session_state.page=="symptom":
    st.subheader("Symptom to OTC Suggestion")
    user_input=st.text_input("Type symptom (comma separated for multiple)").lower()

    if user_input:
        normalized=user_input.replace(" ","")
        if normalized in combo_db:
            st.markdown('<div class="card">',unsafe_allow_html=True)
            st.write(f"### Combination: {user_input}")
            st.write(combo_db[normalized])
            st.markdown('</div>',unsafe_allow_html=True)
        else:
            matches=[k for k in symptom_db if user_input in k]
            if not matches:
                matches=difflib.get_close_matches(user_input,symptom_db.keys(),n=5,cutoff=0.4)
            if matches:
                for m in matches:
                    data=symptom_db[m]
                    st.markdown('<div class="card">',unsafe_allow_html=True)
                    st.write(f"### {m.title()}")
                    st.write(f"**Cause:** {data['Cause']}")
                    st.write(f"**OTC:** {data['OTC']}")
                    st.write(f"**Adult Dose:** {data['Adult']}")
                    st.write(f"**Pediatric:** {data['Pediatric']}")
                    st.write(f"**Advice:** {data['Advice']}")
                    st.error(f"Red Flag: {data['RedFlag']}")
                    st.markdown('</div>',unsafe_allow_html=True)
            else:
                st.warning("No matching symptom found.")

# -----------------------------
# PAGE 2
# -----------------------------

if st.session_state.page=="interaction":
    st.subheader("Drug Interaction Checker")
    d1=st.text_input("Drug 1").lower()
    d2=st.text_input("Drug 2").lower()
    if d1 and d2:
        found=False
        for (a,b),(sev,mech,adv) in interaction_db.items():
            if (d1 in a and d2 in b) or (d1 in b and d2 in a):
                st.markdown('<div class="card">',unsafe_allow_html=True)
                if sev=="Severe":
                    st.error(f"Severity: {sev}")
                elif sev=="High":
                    st.warning(f"Severity: {sev}")
                else:
                    st.info(f"Severity: {sev}")
                st.write(f"**Mechanism:** {mech}")
                st.write(f"**Advice:** {adv}")
                st.markdown('</div>',unsafe_allow_html=True)
                found=True
                break
        if not found:
            st.success("No major interaction found.")

st.markdown('<div class="disclaimer">⚠ Primary care guidance only. Not a substitute for medical consultation.</div>',unsafe_allow_html=True)
st.markdown('<div class="footer">Lalith (Bpharm) (NNRG)</div>',unsafe_allow_html=True)
