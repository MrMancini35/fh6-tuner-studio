"""
╔══════════════════════════════════════════════════════╗
║        FH6 TUNER STUDIO — Streamlit App              ║
║        Dark motorsport theme (Cyan) | Layout wide    ║
╚══════════════════════════════════════════════════════╝
"""

import streamlit as st

# =================================================================
# 1. MOTEUR DE CALCUL (FONCTIONS DÉVELOPPÉES)
# =================================================================

def calculer_arb(repartition_avant, min_av, max_av, min_ar, max_ar, transmission="AWD", biais_comportement="neutre"):
    ratio_av = repartition_avant / 100.0
    ratio_ar = 1.0 - ratio_av
    base_av = (max_av - min_av) * ratio_av + min_av
    base_ar = (max_ar - min_ar) * ratio_ar + min_ar
    
    if transmission == "AWD":
        base_av *= 0.55
        base_ar *= 1.40
    elif transmission == "RWD":
        base_av *= 1.10
        base_ar *= 0.90
    elif transmission == "FWD":
        base_av *= 0.60
        base_ar *= 1.50
        
    if biais_comportement == "survireur": 
        base_av *= 1.20
        base_ar *= 0.80
    elif biais_comportement == "sous-vireur":
        base_av *= 0.80
        base_ar *= 1.20
        
    final_av = max(min_av, min(base_av, max_av))
    final_ar = max(min_ar, min(base_ar, max_ar))
    return round(final_av, 2), round(final_ar, 2)

def calculer_ressorts(repartition_avant, min_av, max_av, min_ar, max_ar, biais_comportement="neutre", appui_aero="standard"):
    ratio_av = repartition_avant / 100.0
    ratio_ar = 1.0 - ratio_av
    base_av = (max_av - min_av) * ratio_av + min_av
    base_ar = (max_ar - min_ar) * ratio_ar + min_ar
    
    if appui_aero == "fort":
        base_av *= 1.20
        base_ar *= 1.20
        
    if biais_comportement == "survireur": 
        base_av *= 1.15
        base_ar *= 0.85
    elif biais_comportement == "sous-vireur":
        base_av *= 0.85
        base_ar *= 1.15
        
    final_av = max(min_av, min(base_av, max_av))
    final_ar = max(min_ar, min(base_ar, max_ar))
    return round(final_av, 2), round(final_ar, 2)

def calculer_pression_pneus(repartition_avant, transmission="AWD", pression_cible=2.1, min_p=1.0, max_p=3.8):
    ratio_av = repartition_avant / 100.0
    ratio_ar = 1.0 - ratio_av
    pression_av = pression_cible + ((0.50 - ratio_av) * 0.5)
    pression_ar = pression_cible + ((0.50 - ratio_ar) * 0.5)
    
    if transmission == "RWD":
        pression_ar -= 0.10
    elif transmission == "FWD":
        pression_av -= 0.15
        pression_ar += 0.05
    elif transmission == "AWD":
        pression_av -= 0.05
        pression_ar -= 0.05
        
    final_av = max(min_p, min(pression_av, max_p))
    final_ar = max(min_p, min(pression_ar, max_p))
    return round(final_av, 2), round(final_ar, 2)

def calculer_differentiel(transmission, biais_comportement="neutre"):
    diff = {}
    if transmission == "RWD":
        diff = {'ar_acc': 65, 'ar_dec': 25}
    elif transmission == "FWD":
        diff = {'av_acc': 70, 'av_dec': 10}
    elif transmission == "AWD":
        diff = {'av_acc': 30, 'av_dec': 5, 'ar_acc': 75, 'ar_dec': 20, 'centre': 65}
        
    if biais_comportement == "survireur":
        if "ar_acc" in diff: diff['ar_acc'] -= 10
        if "ar_dec" in diff: diff['ar_dec'] += 5
        if transmission == "AWD": diff['centre'] -= 5
    elif biais_comportement == "sous-vireur":
        if "ar_acc" in diff: diff['ar_acc'] += 10
        if transmission == "AWD": diff['centre'] += 5
            
    for cle, valeur in diff.items():
        diff[cle] = max(0, min(valeur, 100))
    return diff

def calculer_geometrie(type_suspension="course", biais_comportement="neutre"):
    geo = {}
    if type_suspension == "course":
        geo = {'cam_av': -1.5, 'cam_ar': -1.0, 'toe_av': 0.1, 'toe_ar': -0.1, 'caster': 5.5}
    elif type_suspension == "rallye":
        geo = {'cam_av': -0.5, 'cam_ar': -0.5, 'toe_av': 0.0, 'toe_ar': 0.0, 'caster': 5.0}
    elif type_suspension == "drift":
        geo = {'cam_av': -5.0, 'cam_ar': -0.5, 'toe_av': 0.5, 'toe_ar': 0.0, 'caster': 7.0}
    else:
        geo = {'cam_av': -1.0, 'cam_ar': -1.0, 'toe_av': 0.0, 'toe_ar': 0.0, 'caster': 5.0}
        
    if biais_comportement == "survireur":
        geo['toe_ar'] -= 0.1 
    elif biais_comportement == "sous-vireur":
        geo['toe_av'] += 0.1 
        
    for cle, valeur in geo.items():
        geo[cle] = round(valeur, 1)
    return geo

def calculer_amortisseurs(repartition_avant, min_amort, max_amort, biais_comportement="neutre"):
    ratio_av = repartition_avant / 100.0
    ratio_ar = 1.0 - ratio_av
    
    detente_av = (max_amort - min_amort) * ratio_av + min_amort
    detente_ar = (max_amort - min_amort) * ratio_ar + min_amort
    
    compression_av = detente_av * 0.60
    compression_ar = detente_ar * 0.60
    
    if biais_comportement == "survireur":
        detente_av *= 1.15
        compression_av *= 1.15
        detente_ar *= 0.85
        compression_ar *= 0.85
    elif biais_comportement == "sous-vireur":
        detente_av *= 0.85
        compression_av *= 0.85
        detente_ar *= 1.15
        compression_ar *= 1.15
        
    detente_av = max(min_amort, min(detente_av, max_amort))
    detente_ar = max(min_amort, min(detente_ar, max_amort))
    compression_av = max(min_amort, min(compression_av, max_amort))
    compression_ar = max(min_amort, min(compression_ar, max_amort))
    
    return round(detente_av, 1), round(detente_ar, 1), round(compression_av, 1), round(compression_ar, 1)

def calculer_aero(min_av, max_av, min_ar, max_ar, type_circuit="equilibre", biais_comportement="neutre"):
    if type_circuit == "vitesse":
        base_av = min_av + (max_av - min_av) * 0.10
        base_ar = min_ar + (max_ar - min_ar) * 0.20
    elif type_circuit == "virage":
        base_av = min_av + (max_av - min_av) * 0.90
        base_ar = min_ar + (max_ar - min_ar) * 0.95
    else: 
        base_av = min_av + (max_av - min_av) * 0.50
        base_ar = min_ar + (max_ar - min_ar) * 0.55

    if biais_comportement == "survireur":
        base_av *= 0.90
        base_ar *= 1.15
    elif biais_comportement == "sous-vireur":
        base_av *= 1.15
        base_ar *= 0.90

    final_av = max(min_av, min(base_av, max_av))
    final_ar = max(min_ar, min(base_ar, max_ar))
    return round(final_av, 0), round(final_ar, 0)

def calculer_freins(repartition_avant, biais_comportement="neutre", appui_aero="standard"):
    balance = repartition_avant - 2.0 
    pression = 100
    if appui_aero == "fort":
        pression += 15 
        
    if biais_comportement == "survireur":
        balance += 3.0 
        pression -= 5
    elif biais_comportement == "sous-vireur":
        balance -= 3.0 
        
    balance = max(0.0, min(balance, 100.0))
    pression = max(0, min(pression, 200))
    
    return round(balance, 0), round(pression, 0)

def calculer_boite(type_circuit="equilibre", nb_vitesses=6):
    if type_circuit == "vitesse":
        pont = 2.80
        r_1 = 2.80
        r_n = 0.70
    elif type_circuit == "virage":
        pont = 3.80
        r_1 = 3.20
        r_n = 0.90
    else:
        pont = 3.30
        r_1 = 3.00
        r_n = 0.80

    rapports = []
    for i in range(nb_vitesses):
        ratio = r_1 * ((r_n / r_1) ** (i / (nb_vitesses - 1)))
        rapports.append(round(ratio, 2))
        
    return pont, rapports

# =================================================================
# 2. CONFIGURATION DE LA PAGE & DESIGN (THÈME CYAN)
# =================================================================
st.set_page_config(
    page_title="FH6 Tuner Studio",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Barlow+Condensed:ital,wght@0,300;0,400;0,600;0,800;1,400&display=swap');

/* ── Reset & root ───────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
.stApp {
    background-color: #07090f !important;
    color: #c9d1e0 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
}

[data-testid="stHeader"]      { background: transparent !important; }
[data-testid="stToolbar"]     { display: none !important; }
[data-testid="stDecoration"]  { display: none !important; }
footer                        { display: none !important; }

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 3rem !important;
    max-width: 100% !important;
}

/* ── Scrollbar ──────────────────────────── */
::-webkit-scrollbar              { width: 5px; }
::-webkit-scrollbar-track        { background: #07090f; }
::-webkit-scrollbar-thumb        { background: #0ea5e9; border-radius: 3px; }

/* ── Masthead ────────────────────────────── */
.fh6-wordmark {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #ffffff;
    text-shadow: 0 0 40px rgba(14,165,233,.45);
    line-height: 1;
    margin: 0;
}
.fh6-tagline {
    font-size: 0.72rem;
    font-weight: 300;
    letter-spacing: 0.48em;
    color: #0ea5e9;
    text-transform: uppercase;
    margin: 5px 0 0;
}
.fh6-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.28em;
    color: #4a576b;
    text-transform: uppercase;
}
.pulse-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #0ea5e9;
    box-shadow: 0 0 8px #0ea5e9;
    animation: heartbeat 2.2s ease-in-out infinite;
}
@keyframes heartbeat {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:.35; transform:scale(.85); }
}

/* ── Section labels ─────────────────────── */
.sec-label {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    color: #0ea5e9;
    margin: 1.8rem 0 0.8rem;
}
.sec-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 16px;
    background: #0ea5e9;
    border-radius: 2px;
    flex-shrink: 0;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1c2233 0%, transparent 100%);
}

/* ── Group card ─────────────────────────── */
.card {
    background: #0c0f18;
    border: 1px solid #161d2d;
    border-top: 2px solid #0ea5e9;
    border-radius: 5px;
    padding: 1.1rem 1.4rem 1.4rem;
    margin-bottom: 0.5rem;
}
.card-inner {
    background: #10141f;
    border: 1px solid #161d2d;
    border-radius: 4px;
    padding: 0.9rem 1.1rem;
}
.sub-lbl {
    font-size: 0.64rem;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #3a4760;
    margin-bottom: 0.55rem;
}

/* ── Number inputs ──────────────────────── */
.stNumberInput > label {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #5a6880 !important;
    margin-bottom: 2px !important;
}
.stNumberInput input {
    background-color: #10141f !important;
    border: 1px solid #1c2538 !important;
    border-radius: 3px !important;
    color: #ffffff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}
.stNumberInput input:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 1px rgba(14,165,233,.5) !important;
}
.stNumberInput [data-testid="stNumberInputStepDown"],
.stNumberInput [data-testid="stNumberInputStepUp"] {
    color: #3a4760 !important;
}

/* ── Selectbox ──────────────────────────── */
.stSelectbox > label {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #5a6880 !important;
}
.stSelectbox > div > div {
    background-color: #10141f !important;
    border: 1px solid #1c2538 !important;
    border-radius: 3px !important;
    color: #ffffff !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 1rem !important;
}
.stSelectbox svg { fill: #5a6880 !important; }

/* ── Radio buttons ──────────────────────── */
.stRadio > label {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #5a6880 !important;
}
div[data-testid="stRadio"] > div {
    gap: 6px !important;
}
div[data-testid="stRadio"] label span {
    font-family: 'Barlow Condensed', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    color: #c9d1e0 !important;
}

/* ── Behaviour & Generate buttons ──────── */
.stButton > button {
    background: #10141f !important;
    color: #7a8aa8 !important;
    border: 1px solid #1c2538 !important;
    border-radius: 3px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.22em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 1rem !important;
    height: auto !important;
    min-height: 48px !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    border-color: #0ea5e9 !important;
    color: #ffffff !important;
    background: #14192a !important;
    box-shadow: inset 0 0 0 0 transparent, 0 0 14px rgba(14,165,233,.2) !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
}

/* Generate — override via parent class trick */
.generate-zone .stButton > button {
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.32em !important;
    min-height: 58px !important;
    box-shadow: 0 4px 24px rgba(14,165,233,.35) !important;
}
.generate-zone .stButton > button:hover {
    background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%) !important;
    box-shadow: 0 6px 36px rgba(14,165,233,.55) !important;
    transform: translateY(-2px) !important;
}

/* ── Feedback / result box ──────────────── */
.result-box {
    background: #0c0f18;
    border: 1px solid #0ea5e9;
    border-radius: 5px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
    margin-bottom: 2rem;
}
.result-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    color: #0ea5e9;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 6px;
}
.result-row {
    display: flex;
    flex-direction: column;
    background: #10141f;
    border: 1px solid #161d2d;
    border-radius: 3px;
    padding: 7px 11px;
}
.result-key {
    font-size: 0.64rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #3a4760;
    line-height: 1.4;
}
.result-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #e8ecf4;
    letter-spacing: 0.04em;
}

/* ── Horizontal rule ────────────────────── */
.fh6-hr {
    border: none;
    border-top: 1px solid #161d2d;
    margin: 1rem 0;
}

/* ── Selected-state chip (comportement) ─── */
.sel-chip {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #0ea5e9;
    margin-top: 4px;
}
.sel-chip::before {
    content: '▸';
}
</style>
""",
    unsafe_allow_html=True,
)

# =================================================================
# 3. INTERFACE UTILISATEUR
# =================================================================

if "comportement" not in st.session_state:
    st.session_state.comportement = "Neutre"

col_head, col_stat = st.columns([6, 1])
with col_head:
    st.markdown(
        """
        <p class="fh6-wordmark">⚙ FH6&nbsp;&nbsp;Tuner&nbsp;&nbsp;Studio</p>
        <p class="fh6-tagline">Performance Tuning System · Build Configuration Module</p>
        """,
        unsafe_allow_html=True,
    )
with col_stat:
    st.markdown(
        """
        <div style="height:100%;display:flex;align-items:center;justify-content:flex-end;padding-top:.5rem;">
            <span class="fh6-status"><span class="pulse-dot"></span>System Online</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="sec-label">01 &nbsp;— &nbsp;Config Build</div>', unsafe_allow_html=True)

st.markdown('<p class="sub-lbl">Paramètres de base</p>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    puissance = st.number_input("Puissance (ch)", min_value=0, max_value=5000, value=450, step=10)
with c2:
    couple = st.number_input("Couple (Nm)", min_value=0, max_value=5000, value=580, step=10)
with c3:
    poids = st.number_input("Poids (kg)", min_value=300, max_value=5000, value=1350, step=10)
with c4:
    poids_avant = st.number_input("% Poids avant (%)", min_value=0.0, max_value=100.0, value=56.0, step=0.1)

st.markdown('<hr class="fh6-hr">', unsafe_allow_html=True)

col_aero, col_gap, col_haut = st.columns([10, 0.6, 10])
with col_aero:
    st.markdown('<p class="sub-lbl">🌬&nbsp; Aérodynamique</p>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        appui_av_min = st.number_input("Appui Av Min",  min_value=0.0, max_value=999.0, value=70.0,   step=1.0, key="aav_min")
        appui_ar_min = st.number_input("Appui Ar Min",  min_value=0.0, max_value=999.0, value=100.0,   step=1.0, key="aar_min")
    with a2:
        appui_av_max = st.number_input("Appui Av Max",  min_value=0.0, max_value=999.0, value=150.0, step=1.0, key="aav_max")
        appui_ar_max = st.number_input("Appui Ar Max",  min_value=0.0, max_value=999.0, value=250.0, step=1.0, key="aar_max")

with col_haut:
    st.markdown('<p class="sub-lbl">📏&nbsp; Hauteur de caisse</p>', unsafe_allow_html=True)
    h1, h2 = st.columns(2)
    with h1:
        haut_av_min = st.number_input("Hauteur Av Min (mm)", min_value=0, max_value=500, value=50,  step=5, key="hav_min")
        haut_ar_min = st.number_input("Hauteur Ar Min (mm)", min_value=0, max_value=500, value=55,  step=5, key="har_min")
    with h2:
        haut_av_max = st.number_input("Hauteur Av Max (mm)", min_value=0, max_value=500, value=150, step=5, key="hav_max")
        haut_ar_max = st.number_input("Hauteur Ar Max (mm)", min_value=0, max_value=500, value=160, step=5, key="har_max")

st.markdown('<hr class="fh6-hr">', unsafe_allow_html=True)

st.markdown('<p class="sub-lbl">Configuration mécanique</p>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
with m1:
    motricite = st.radio("Motricité", ["RWD", "AWD", "FWD"], horizontal=True)
with m2:
    position_moteur = st.radio("Position moteur", ["Avant", "Centrale", "Arrière"], horizontal=True)
with m3:
    type_moteur = st.selectbox("Type de moteur", ["Électrique", "Ligne 3", "Rotatif", "Boxer 4", "Ligne 4", "Ligne 5", "Ligne 6", "Boxer 6", "V6", "V8", "V10", "V12", "W12", "W16"], index=8)

g1, g2, _ = st.columns([4, 4, 2])
with g1:
    gomme = st.selectbox("Gomme / Pneu", ["Route", "Sport", "Semi slick", "Slick", "Rallye", "Tout terrain", "Neige", "Drift", "Drag"], index=1)
with g2:
    suspension = st.selectbox("Type de suspension", ["Street", "Sport", "Race", "Rallye", "Drift"], index=2)

st.markdown('<div class="sec-label">02 &nbsp;— &nbsp;Comportement souhaité</div>', unsafe_allow_html=True)
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("↰  SOUS-VIRAGE", key="btn_sv", use_container_width=True):
        st.session_state.comportement = "Sous-virage"
        st.rerun()
with b2:
    if st.button("⚖   NEUTRE", key="btn_neu", use_container_width=True):
        st.session_state.comportement = "Neutre"
        st.rerun()
with b3:
    if st.button("↱  SURVIRAGE", key="btn_sur", use_container_width=True):
        st.session_state.comportement = "Survirage"
        st.rerun()

_icons = {"Sous-virage": "🔻", "Neutre": "⚖️", "Survirage": "🔺"}
st.markdown(f'<p class="sel-chip">Sélectionné : {_icons[st.session_state.comportement]} &nbsp;{st.session_state.comportement}</p>', unsafe_allow_html=True)

st.markdown('<div class="sec-label">03 &nbsp;— &nbsp;Objectif du réglage</div>', unsafe_allow_html=True)
_objectifs = {
    "🏎️  Circuit — Piste lisse, aéro max": "Circuit",
    "⛰️  Touge — Montagne : Grip + sortie de courbe": "Touge",
    "🌧️  Rallye — Surface mixte, souple": "Rallye",
    "🪨  Tout terrain — Terrain accidenté + jump": "Tout terrain",
    "🔥  Drift — Angle + Rotation": "Drift",
    "⚡  Drag — Ligne droite": "Drag",
}
objectif_display = st.selectbox("Objectif", list(_objectifs.keys()), label_visibility="collapsed")
objectif = _objectifs[objectif_display]

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="sec-label">04 &nbsp;— &nbsp;Générer</div>', unsafe_allow_html=True)

gen_l, gen_mid, gen_r = st.columns([1, 4, 1])
with gen_mid:
    st.markdown('<div class="generate-zone">', unsafe_allow_html=True)
    generate = st.button("⚙  GÉNÉRER LE RÉGLAGE", key="btn_gen", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# =================================================================
# 4. EXÉCUTION & RÉSULTATS (C'est ce qui manquait)
# =================================================================
if generate:
    params = {
        "Puissance": f"{puissance} ch", "Couple": f"{couple} Nm", "Poids total": f"{poids} kg", "Poids avant": f"{poids_avant} %",
        "Appui Av": f"[{appui_av_min} → {appui_av_max}]", "Appui Ar": f"[{appui_ar_min} → {appui_ar_max}]",
        "Hauteur Av": f"[{haut_av_min} → {haut_av_max} mm]", "Hauteur Ar": f"[{haut_ar_min} → {haut_ar_max} mm]",
        "Motricité": motricite, "Pos. moteur": position_moteur, "Type moteur": type_moteur,
        "Gomme / Pneu": gomme, "Suspension": suspension, "Comportement": st.session_state.comportement, "Objectif": objectif,
    }

    rows_html = "".join(f'<div class="result-row"><span class="result-key">{k}</span><span class="result-val">{v}</span></div>' for k, v in params.items())

    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                <span class="pulse-dot" style="display:inline-block;"></span>
                &nbsp;Calcul en cours avec les paramètres :
            </div>
            <div class="result-grid">{rows_html}</div>
        </div>
        """, unsafe_allow_html=True
    )

    # Traduction UI -> Math
    map_comportement = {"Sous-virage": "sous-vireur", "Neutre": "neutre", "Survirage": "survireur"}
    math_comp = map_comportement.get(st.session_state.comportement, "neutre")
    map_suspension = {"Street": "course", "Sport": "course", "Race": "course", "Rallye": "rallye", "Drift": "drift"}
    math_susp = map_suspension.get(suspension, "course")
    map_circuit = {"Circuit": "virage", "Touge": "equilibre", "Rallye": "equilibre", "Tout terrain": "equilibre", "Drift": "equilibre", "Drag": "vitesse"}
    math_circ = map_circuit.get(objectif, "equilibre")
    math_aero = "fort" if objectif == "Circuit" else "standard"
    nb_vitesses = 6

    # Limites fixes Forza par défaut
    arb_min, arb_max = 1.0, 65.0
    ressort_min, ressort_max = 20.0, 200.0
    amort_min, amort_max = 1.0, 20.0

    # Lancement des calculs
    arb_av, arb_ar = calculer_arb(poids_avant, arb_min, arb_max, arb_min, arb_max, motricite, math_comp)
    res_av, res_ar = calculer_ressorts(poids_avant, ressort_min, ressort_max, ressort_min, ressort_max, math_comp, math_aero)
    pneus_av, pneus_ar = calculer_pression_pneus(poids_avant, motricite)
    diff_resultats = calculer_differentiel(motricite, math_comp)
    geo_resultats = calculer_geometrie(math_susp, math_comp)
    det_av, det_ar, comp_av, comp_ar = calculer_amortisseurs(poids_avant, amort_min, amort_max, math_comp)
    aero_av, aero_ar = calculer_aero(appui_av_min, appui_av_max, appui_ar_min, appui_ar_max, math_circ, math_comp)
    freins_bal, freins_pres = calculer_freins(poids_avant, math_comp, math_aero)
    pont, rapports_boite = calculer_boite(math_circ, nb_vitesses)

    # Affichage des onglets
    st.markdown('<div class="sec-label">05 &nbsp;— &nbsp;Réglage Optimal</div>', unsafe_allow_html=True)
    onglets = st.tabs(["PNEUS", "BOÎTE", "GÉOMÉTRIE", "BARRES ARB", "RESSORTS", "AMORTISSEURS", "AÉRO", "FREINS", "DIFFÉRENTIEL"])

    with onglets[0]:
        c1, c2 = st.columns(2)
        c1.metric("Pression Avant", f"{pneus_av} Bar")
        c2.metric("Pression Arrière", f"{pneus_ar} Bar")

    with onglets[1]:
        st.metric("Rapport de Pont final", pont)
        cols = st.columns(len(rapports_boite))
        for i, ratio in enumerate(rapports_boite):
            cols[i].metric(f"Vitesse {i+1}", ratio)

    with onglets[2]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Carrossage Av / Ar", f"{geo_resultats['cam_av']}° / {geo_resultats['cam_ar']}°")
        c2.metric("Parallélisme Av / Ar", f"{geo_resultats['toe_av']}° / {geo_resultats['toe_ar']}°")
        c3.metric("Chasse", f"{geo_resultats['caster']}°")

    with onglets[3]:
        c1, c2 = st.columns(2)
        c1.metric("Anti-Roulis Avant", arb_av)
        c2.metric("Anti-Roulis Arrière", arb_ar)

    with onglets[4]:
        c1, c2 = st.columns(2)
        c1.metric("Ressorts Avant", res_av)
        c2.metric("Ressorts Arrière", res_ar)

    with onglets[5]:
        c1, c2 = st.columns(2)
        c1.metric("Détente Avant", det_av)
        c1.metric("Compression Avant", comp_av)
        c2.metric("Détente Arrière", det_ar)
        c2.metric("Compression Arrière", comp_ar)

    with onglets[6]:
        c1, c2 = st.columns(2)
        c1.metric("Appui Avant", aero_av)
        c2.metric("Appui Arrière", aero_ar)

    with onglets[7]:
        c1, c2 = st.columns(2)
        c1.metric("Balance", f"{freins_bal}% vers l'avant")
        c1.metric("Pression", f"{freins_pres}%")

    with onglets[8]:
        c1, c2, c3 = st.columns(3)
        if motricite in ["AWD", "FWD"]:
            c1.metric("Avant (Accélération)", f"{diff_resultats.get('av_acc', 0)}%")
            c1.metric("Avant (Décélération)", f"{diff_resultats.get('av_dec', 0)}%")
        if motricite in ["AWD", "RWD"]:
            c2.metric("Arrière (Accélération)", f"{diff_resultats.get('ar_acc', 0)}%")
            c2.metric("Arrière (Décélération)", f"{diff_resultats.get('ar_dec', 0)}%")
        if motricite == "AWD":
            c3.metric("Centre", f"{diff_resultats.get('centre', 0)}% vers l'arrière")

```
