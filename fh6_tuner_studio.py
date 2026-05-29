# =================================================================
# MOTEUR DE CALCUL (FONCTIONS DÉVELOPPÉES)
# =================================================================

# --- MODULE 1 : BARRES ANTI-ROULIS (ARB) ---
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

# --- MODULE 2 : RESSORTS (SPRINGS) ---
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

# --- MODULE 3 : PNEUMATIQUES ---
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

# --- MODULE 4 : DIFFÉRENTIEL ---
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

# --- MODULE 5 : GÉOMÉTRIE ---
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

# --- MODULE 6 : AMORTISSEURS ---
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

# --- MODULE 7 : AÉRODYNAMIQUE ---
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

# --- MODULE 8 : FREINS ---
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

# --- MODULE 9 : BOÎTE DE VITESSES ---
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

# 1. Traduction des variables UI pour le moteur de calcul
    map_comportement = {"Sous-virage": "sous-vireur", "Neutre": "neutre", "Survirage": "survireur"}
    math_comp = map_comportement.get(st.session_state.comportement, "neutre")

    map_suspension = {"Street": "course", "Sport": "course", "Race": "course", "Rallye": "rallye", "Drift": "drift"}
    math_susp = map_suspension.get(suspension, "course")

    map_circuit = {"Circuit": "virage", "Touge": "equilibre", "Rallye": "equilibre", "Tout terrain": "equilibre", "Drift": "equilibre", "Drag": "vitesse"}
    math_circ = map_circuit.get(objectif, "equilibre")

    math_aero = "fort" if objectif == "Circuit" else "standard"
    nb_vitesses = 6

    # 2. Exécution des 9 modules de calcul
    arb_av, arb_ar = calculer_arb(poids_avant, 1.0, 65.0, 1.0, 65.0, motricite, math_comp)
    res_av, res_ar = calculer_ressorts(poids_avant, 20.0, 200.0, 20.0, 200.0, math_comp, math_aero)
    pneus_av, pneus_ar = calculer_pression_pneus(poids_avant, motricite)
    diff_resultats = calculer_differentiel(motricite, math_comp)
    geo_resultats = calculer_geometrie(math_susp, math_comp)
    det_av, det_ar, comp_av, comp_ar = calculer_amortisseurs(poids_avant, 1.0, 20.0, math_comp)
    aero_av, aero_ar = calculer_aero(appui_av_min, appui_av_max, appui_ar_min, appui_ar_max, math_circ, math_comp)
    freins_bal, freins_pres = calculer_freins(poids_avant, math_comp, math_aero)
    pont, rapports_boite = calculer_boite(math_circ, nb_vitesses)

    # 3. Affichage final dans les onglets (votre UI d'origine)
    st.markdown('<div class="sec-label">05 &nbsp;— &nbsp;Réglage Optimal</div>', unsafe_allow_html=True)
    onglets = st.tabs(["PNEUS", "BOÎTE", "GÉOMÉTRIE", "ARB", "RESSORTS", "AMORTISSEURS", "AÉRO", "FREINS", "DIFFÉRENTIEL"])

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
        c1.metric("Carrossage Av/Ar", f"{geo_resultats['cam_av']}° / {geo_resultats['cam_ar']}°")
        c2.metric("Parallélisme Av/Ar", f"{geo_resultats['toe_av']}° / {geo_resultats['toe_ar']}°")
        c3.metric("Chasse", f"{geo_resultats['caster']}°")
    with onglets[3]:
        c1, c2 = st.columns(2)
        c1.metric("Anti-Roulis Av", arb_av)
        c2.metric("Anti-Roulis Ar", arb_ar)
    with onglets[4]:
        c1, c2 = st.columns(2)
        c1.metric("Ressorts Av", res_av)
        c2.metric("Ressorts Ar", res_ar)
    with onglets[5]:
        c1, c2 = st.columns(2)
        c1.write(f"Détente: {det_av} / {det_ar}")
        c1.write(f"Compression: {comp_av} / {comp_ar}")
    with onglets[6]:
        c1, c2 = st.columns(2)
        c1.metric("Appui Av", aero_av)
        c2.metric("Appui Ar", aero_ar)
    with onglets[7]:
        c1, c2 = st.columns(2)
        c1.metric("Balance", f"{freins_bal}%")
        c2.metric("Pression", f"{freins_pres}%")
    with onglets[8]:
        st.write(diff_resultats)
