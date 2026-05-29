"""
╔══════════════════════════════════════════════════════╗
║        FH6 TUNER STUDIO — Streamlit App              ║
║        Dark motorsport theme | Layout wide           ║
║  Run: streamlit run fh6_tuner_studio.py              ║
╚══════════════════════════════════════════════════════╝
"""

import streamlit as st

# ═══════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════
st.set_page_config(
    page_title="FH6 Tuner Studio",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════════
#  GLOBAL CSS — DARK MOTORSPORT THEME
# ═══════════════════════════════════════════════════════
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
::-webkit-scrollbar-thumb        { background: #c9222c; border-radius: 3px; }

/* ── Masthead ────────────────────────────── */
.fh6-wordmark {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #ffffff;
    text-shadow: 0 0 40px rgba(201,34,44,.45);
    line-height: 1;
    margin: 0;
}
.fh6-tagline {
    font-size: 0.72rem;
    font-weight: 300;
    letter-spacing: 0.48em;
    color: #c9222c;
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
    background: #c9222c;
    box-shadow: 0 0 8px #c9222c;
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
    color: #c9222c;
    margin: 1.8rem 0 0.8rem;
}
.sec-label::before {
    content: '';
    display: inline-block;
    width: 3px; height: 16px;
    background: #c9222c;
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
    border-top: 2px solid #c9222c;
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
    border-color: #c9222c !important;
    box-shadow: 0 0 0 1px rgba(201,34,44,.5) !important;
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
    border-color: #c9222c !important;
    color: #ffffff !important;
    background: #14192a !important;
    box-shadow: inset 0 0 0 0 transparent, 0 0 14px rgba(201,34,44,.2) !important;
}
.stButton > button:active {
    transform: translateY(1px) !important;
}

/* Generate — override via parent class trick */
.generate-zone .stButton > button {
    background: linear-gradient(135deg, #c9222c 0%, #9b1a22 100%) !important;
    color: #ffffff !important;
    border: none !important;
    font-size: 1.05rem !important;
    letter-spacing: 0.32em !important;
    min-height: 58px !important;
    box-shadow: 0 4px 24px rgba(201,34,44,.35) !important;
}
.generate-zone .stButton > button:hover {
    background: linear-gradient(135deg, #e02530 0%, #c9222c 100%) !important;
    box-shadow: 0 6px 36px rgba(201,34,44,.55) !important;
    transform: translateY(-2px) !important;
}

/* ── Feedback / result box ──────────────── */
.result-box {
    background: #0c0f18;
    border: 1px solid #c9222c;
    border-radius: 5px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
}
.result-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    color: #c9222c;
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
    color: #c9222c;
    margin-top: 4px;
}
.sel-chip::before {
    content: '▸';
}
</style>
""",
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════
if "comportement" not in st.session_state:
    st.session_state.comportement = "Neutre"

# ═══════════════════════════════════════════════════════
#  MASTHEAD
# ═══════════════════════════════════════════════════════
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

# ═══════════════════════════════════════════════════════
#  SECTION 1 — CONFIG BUILD
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sec-label">01 &nbsp;— &nbsp;Config Build</div>', unsafe_allow_html=True)

# ── 1-A  Base parameters ────────────────────────────────
st.markdown('<p class="sub-lbl">Paramètres de base</p>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
with c1:
    puissance = st.number_input("Puissance (ch)", min_value=0, max_value=5000, value=450, step=10)
with c2:
    couple = st.number_input("Couple (Nm)", min_value=0, max_value=5000, value=580, step=10)
with c3:
    poids = st.number_input("Poids (kg)", min_value=300, max_value=5000, value=1350, step=10)
with c4:
    poids_avant = st.number_input("% Poids avant (%)", min_value=0, max_value=100, value=52, step=1)

st.markdown('<hr class="fh6-hr">', unsafe_allow_html=True)

# ── 1-B  Aéro + Hauteur de caisse ──────────────────────
col_aero, col_gap, col_haut = st.columns([10, 0.6, 10])

with col_aero:
    st.markdown('<p class="sub-lbl">🌬&nbsp; Aérodynamique</p>', unsafe_allow_html=True)
    a1, a2 = st.columns(2)
    with a1:
        appui_av_min = st.number_input("Appui Av Min",  min_value=0, max_value=999, value=0,   step=1, key="aav_min")
        appui_ar_min = st.number_input("Appui Ar Min",  min_value=0, max_value=999, value=0,   step=1, key="aar_min")
    with a2:
        appui_av_max = st.number_input("Appui Av Max",  min_value=0, max_value=999, value=100, step=1, key="aav_max")
        appui_ar_max = st.number_input("Appui Ar Max",  min_value=0, max_value=999, value=100, step=1, key="aar_max")

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

# ── 1-C  Motricité · Position moteur · Type moteur ─────
st.markdown('<p class="sub-lbl">Configuration mécanique</p>', unsafe_allow_html=True)
m1, m2, m3 = st.columns(3)
with m1:
    motricite = st.radio(
        "Motricité",
        ["RWD", "AWD", "FWD"],
        horizontal=True,
    )
with m2:
    position_moteur = st.radio(
        "Position moteur",
        ["Avant", "Centrale", "Arrière"],
        horizontal=True,
    )
with m3:
    type_moteur = st.selectbox(
        "Type de moteur",
        [
            "Électrique", "Ligne 3", "Rotatif", "Boxer 4",
            "Ligne 4", "Ligne 5", "Ligne 6", "Boxer 6",
            "V6", "V8", "V10", "V12", "W12", "W16",
        ],
        index=8,   # default V6
    )

# ── 1-D  Gomme + Suspension ────────────────────────────
g1, g2, _ = st.columns([4, 4, 2])
with g1:
    gomme = st.selectbox(
        "Gomme / Pneu",
        ["Route", "Sport", "Semi slick", "Slick", "Rallye", "Tout terrain", "Neige", "Drift", "Drag"],
        index=1,
    )
with g2:
    suspension = st.selectbox(
        "Type de suspension",
        ["Street", "Sport", "Race", "Rallye", "Drift"],
        index=2,
    )

# ═══════════════════════════════════════════════════════
#  SECTION 2 — COMPORTEMENT SOUHAITÉ
# ═══════════════════════════════════════════════════════
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
st.markdown(
    f'<p class="sel-chip">Sélectionné : {_icons[st.session_state.comportement]}'
    f' &nbsp;{st.session_state.comportement}</p>',
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════
#  SECTION 3 — OBJECTIF DU RÉGLAGE
# ═══════════════════════════════════════════════════════
st.markdown('<div class="sec-label">03 &nbsp;— &nbsp;Objectif du réglage</div>', unsafe_allow_html=True)

_objectifs = {
    "🏎️  Circuit — Piste lisse, aéro max":                "Circuit",
    "⛰️  Touge — Montagne : Grip + sortie de courbe":      "Touge",
    "🌧️  Rallye — Surface mixte, souple":                 "Rallye",
    "🪨  Tout terrain — Terrain accidenté + jump":         "Tout terrain",
    "🔥  Drift — Angle + Rotation":                        "Drift",
    "⚡  Drag — Ligne droite":                             "Drag",
}

objectif_display = st.selectbox(
    "Objectif",
    list(_objectifs.keys()),
    label_visibility="collapsed",
)
objectif = _objectifs[objectif_display]

# ═══════════════════════════════════════════════════════
#  GENERATE BUTTON
# ═══════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="sec-label">04 &nbsp;— &nbsp;Générer</div>', unsafe_allow_html=True)

gen_l, gen_mid, gen_r = st.columns([1, 4, 1])
with gen_mid:
    st.markdown('<div class="generate-zone">', unsafe_allow_html=True)
    generate = st.button("⚙  GÉNÉRER LE RÉGLAGE", key="btn_gen", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
#  RESULT OUTPUT
# ═══════════════════════════════════════════════════════
if generate:
    params = {
        "Puissance":       f"{puissance} ch",
        "Couple":          f"{couple} Nm",
        "Poids total":     f"{poids} kg",
        "Poids avant":     f"{poids_avant} %",
        "Appui Av":        f"[{appui_av_min} → {appui_av_max}]",
        "Appui Ar":        f"[{appui_ar_min} → {appui_ar_max}]",
        "Hauteur Av":      f"[{haut_av_min} → {haut_av_max} mm]",
        "Hauteur Ar":      f"[{haut_ar_min} → {haut_ar_max} mm]",
        "Motricité":       motricite,
        "Pos. moteur":     position_moteur,
        "Type moteur":     type_moteur,
        "Gomme / Pneu":   gomme,
        "Suspension":      suspension,
        "Comportement":    st.session_state.comportement,
        "Objectif":        objectif,
    }

    # Build grid HTML
    rows_html = "".join(
        f'<div class="result-row">'
        f'<span class="result-key">{k}</span>'
        f'<span class="result-val">{v}</span>'
        f'</div>'
        for k, v in params.items()
    )

    st.markdown(
        f"""
        <div class="result-box">
            <div class="result-title">
                <span class="pulse-dot" style="display:inline-block;"></span>
                &nbsp;Calcul en cours avec les paramètres :
            </div>
            <div class="result-grid">
                {rows_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
