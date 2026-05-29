import streamlit as st

# =================================================================
# MOTEUR DE CALCUL (FONCTIONS MATHÉMATIQUES)
# =================================================================
def calculer_arb(rep_av, min_av, max_av, min_ar, max_ar, trans, biais):
    r_av = rep_av / 100.0; r_ar = 1.0 - r_av
    b_av = (max_av - min_av) * r_av + min_av
    b_ar = (max_ar - min_ar) * r_ar + min_ar
    if trans == "AWD": b_av *= 0.55; b_ar *= 1.40
    elif trans == "RWD": b_av *= 1.10; b_ar *= 0.90
    elif trans == "FWD": b_av *= 0.60; b_ar *= 1.50
    if biais == "survireur": b_av *= 1.20; b_ar *= 0.80
    elif biais == "sous-vireur": b_av *= 0.80; b_ar *= 1.20
    return round(max(min_av, min(b_av, max_av)), 2), round(max(min_ar, min(b_ar, max_ar)), 2)

def calculer_ressorts(rep_av, min_av, max_av, min_ar, max_ar, biais, aero):
    r_av = rep_av / 100.0; r_ar = 1.0 - r_av
    b_av = (max_av - min_av) * r_av + min_av
    b_ar = (max_ar - min_ar) * r_ar + min_ar
    if aero == "fort": b_av *= 1.20; b_ar *= 1.20
    if biais == "survireur": b_av *= 1.15; b_ar *= 0.85
    elif biais == "sous-vireur": b_av *= 0.85; b_ar *= 1.15
    return round(max(min_av, min(b_av, max_av)), 2), round(max(min_ar, min(b_ar, max_ar)), 2)

def calculer_pression_pneus(rep_av, trans):
    r_av = rep_av / 100.0; r_ar = 1.0 - r_av
    p_av = 2.1 + ((0.50 - r_av) * 0.5)
    p_ar = 2.1 + ((0.50 - r_ar) * 0.5)
    if trans == "RWD": p_ar -= 0.10
    elif trans == "FWD": p_av -= 0.15; p_ar += 0.05
    elif trans == "AWD": p_av -= 0.05; p_ar -= 0.05
    return round(max(1.0, min(p_av, 3.8)), 2), round(max(1.0, min(p_ar, 3.8)), 2)

def calculer_differentiel(trans, biais):
    diff = {'av_acc': 30, 'av_dec': 5, 'ar_acc': 75, 'ar_dec': 20, 'centre': 65}
    if trans == "RWD": diff = {'ar_acc': 65, 'ar_dec': 25}
    elif trans == "FWD": diff = {'av_acc': 70, 'av_dec': 10}
    if biais == "survireur":
        if "ar_acc" in diff: diff['ar_acc'] -= 10
        if "centre" in diff: diff['centre'] -= 5
    elif biais == "sous-vireur":
        if "ar_acc" in diff: diff['ar_acc'] += 10
        if "centre" in diff: diff['centre'] += 5
    return diff

def calculer_geometrie(type_s, biais):
    geo = {'cam_av': -1.5, 'cam_ar': -1.0, 'toe_av': 0.1, 'toe_ar': -0.1, 'caster': 5.5}
    if biais == "survireur": geo['toe_ar'] -= 0.1
    elif biais == "sous-vireur": geo['toe_av'] += 0.1
    return geo

def calculer_amortisseurs(rep_av, min_a, max_a, biais):
    r_av = rep_av / 100.0; r_ar = 1.0 - r_av
    d_av = (max_a - min_a) * r_av + min_a
    d_ar = (max_a - min_a) * r_ar + min_a
    c_av = d_av * 0.6; c_ar = d_ar * 0.6
    return round(d_av, 1), round(d_ar, 1), round(c_av, 1), round(c_ar, 1)

def calculer_aero(min_av, max_av, min_ar, max_ar, circ, biais):
    b_av = min_av + (max_av - min_av) * 0.5; b_ar = min_ar + (max_ar - min_ar) * 0.5
    if biais == "survireur": b_av *= 0.9; b_ar *= 1.15
    elif biais == "sous-vireur": b_av *= 1.15; b_ar *= 0.9
    return round(b_av, 0), round(b_ar, 0)

def calculer_freins(rep_av, biais, aero):
    bal = rep_av - 2.0; pres = 115 if aero == "fort" else 100
    if biais == "survireur": bal += 3.0; pres -= 5
    elif biais == "sous-vireur": bal -= 3.0
    return round(max(0, min(bal, 100)), 0), round(pres, 0)

def calculer_boite(circ):
    pont = 3.30; rapports = [2.9, 2.1, 1.6, 1.3, 1.1, 0.9]
    return pont, rapports

# =================================================================
# UI STREAMLIT
# =================================================================
st.set_page_config(layout="wide")
st.title("⚙ FH6 TUNER STUDIO")

# Layout de saisie
c1, c2, c3 = st.columns(3)
with c1:
    poids_av = st.slider("Répartition avant (%)", 40.0, 60.0, 52.0)
    trans = st.selectbox("Transmission", ["AWD", "RWD", "FWD"])
with c2:
    biais = st.selectbox("Comportement", ["neutre", "survireur", "sous-vireur"])
    objectif = st.selectbox("Objectif", ["Circuit", "Rallye", "Drift"])
with c3:
    aero = st.selectbox("Aéro", ["standard", "fort"])
    gen = st.button("GÉNÉRER LE RÉGLAGE")

if gen:
    # Calculs
    arb_av, arb_ar = calculer_arb(poids_av, 1.0, 65.0, 1.0, 65.0, trans, biais)
    res_av, res_ar = calculer_ressorts(poids_av, 20.0, 200.0, 20.0, 200.0, biais, aero)
    p_av, p_ar = calculer_pression_pneus(poids_av, trans)
    diff = calculer_differentiel(trans, biais)
    geo = calculer_geometrie("course", biais)
    d_av, d_ar, c_av, c_ar = calculer_amortisseurs(poids_av, 1.0, 20.0, biais)
    ae_av, ae_ar = calculer_aero(0, 100, 0, 100, "equilibre", biais)
    f_bal, f_pres = calculer_freins(poids_av, biais, aero)
    pont, rap = calculer_boite("equilibre")

    # Onglets
    tabs = st.tabs(["PNEUS", "BOÎTE", "GÉOMÉTRIE", "ARB", "RESSORTS", "AMORTISSEURS", "AÉRO", "FREINS", "DIFFÉRENTIEL"])
    with tabs[0]: st.metric("Av", f"{p_av} Bar"), st.metric("Ar", f"{p_ar} Bar")
    with tabs[1]: st.write(f"Pont: {pont}"), st.write(rap)
    with tabs[2]: st.write(geo)
    with tabs[3]: st.metric("Av", arb_av), st.metric("Ar", arb_ar)
    with tabs[4]: st.metric("Av", res_av), st.metric("Ar", res_ar)
    with tabs[5]: st.write(f"Détente: {d_av}/{d_ar}"), st.write(f"Comp: {c_av}/{c_ar}")
    with tabs[6]: st.metric("Av", ae_av), st.metric("Ar", ae_ar)
    with tabs[7]: st.metric("Balance", f"{f_bal}%"), st.metric("Pression", f"{f_pres}%")
    with tabs[8]: st.write(diff)
