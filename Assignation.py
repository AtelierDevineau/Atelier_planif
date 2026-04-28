import streamlit as st
from donnees import Projets, Ressources_base
from Logique import (
    recalculer_dispos,
    get_dispo_restante,
    get_dispo_base,
    get_charge_sur_projet,
    get_noms_ressources_disponibles
)
import pandas as pd
from Logique import get_segments_charge
from donnees import get_couleur_projet, Ressources_base
    
# -------------------------------------------------------
# FONCTIONS D'AFFICHAGE
# -------------------------------------------------------

def init_statut_sauvegarde():
    if "statut_sauvegarde" not in st.session_state:
        st.session_state.statut_sauvegarde = "vide"

def marquer_modifie():
    st.session_state.statut_sauvegarde = "modifie"

def afficher_statut():
    if st.session_state.statut_sauvegarde == "sauvegarde":
        st.success("✅ Sauvegardé")
    elif st.session_state.statut_sauvegarde == "modifie":
        st.warning("❌ Modifications non sauvegardées")


def afficher_bloc_ressource(k, noms_filtres, default_index, assignations_sauvegardees, projet):
    """Affiche le bloc visuel d'une ressource et retourne l'assignation choisie"""
    pct_sauvegarde = next(
        (a["Pct"] for i, a in enumerate(assignations_sauvegardees) if i == k), 0
    )

    with st.container(border=True):
        st.markdown(f"**Personne {k+1}**")

        nom_choisi = st.selectbox(
            "Nom :", noms_filtres,
            index=default_index,
            key=f"select_ress_{projet}_{k}",
            on_change=marquer_modifie
        )

        dispo_restante = get_dispo_restante(nom_choisi, st.session_state.Ressources)
        charge_ce_projet = get_charge_sur_projet(nom_choisi, assignations_sauvegardees)
        max_slider = dispo_restante + charge_ce_projet

        st.caption(f"Disponibilité restante : {dispo_restante}%")
        #Barre de progression
        couleur_projet_courant = get_couleur_projet(projet)
        afficher_barre_charge(nom_choisi, st.session_state.Data_proj, projet, couleur_projet_courant)
        
        pct_choisi = st.slider(
            "Charge :", min_value=0, max_value=max_slider,
            value=pct_sauvegarde,
            key=f"slider_ress_{projet}_{k}",
            on_change=marquer_modifie
        )

    return {"Nom": nom_choisi, "Pct": pct_choisi}

def afficher_tableau_recap():
    """Affiche le récap sous forme de barres de charge par ressource"""
    st.divider()
    st.subheader("Récapitulatif")

    # Petit tableau projet/nb ressources — on le garde
    st.dataframe({
        "Projet": list(st.session_state.Data_proj.keys()),
        "Ressources": [v.get("Nb_ressources", 0) for v in st.session_state.Data_proj.values()]
    })

    st.subheader("Charge par ressource")

    # Pour chaque ressource, on reconstruit ses segments tous projets confondus
    for r in st.session_state.Ressources:
        nom = r["Nom"]

        # Vérifier si cette ressource a au moins une assignation
        est_assigne = any(
            a["Nom"] == nom
            for data in st.session_state.Data_proj.values()
            for a in data.get("Assignations", [])
        )
        if not est_assigne:
            continue

        st.caption(f"**{nom}**")

        # On passe None comme projet_courant pour afficher TOUS les projets
        segments = get_segments_charge(nom, st.session_state.Data_proj, projet_courant=None)

        barres = ""
        legende = ""
        for s in segments:
            if s["pct"] <= 0:
                continue
            nom_projet_safe = s["projet"].replace("'", "&#39;") #Permt de pas avoir e galères avec les apostrophes
            tooltip = f"{nom_projet_safe} : {s['pct']}%"
            barres += (
                f'<div title="{tooltip}" style="'
                f'width:{s["pct"]}%;'
                f'background-color:{s["couleur"]};'
                f'height:20px;'
                f'display:inline-block;'
                f'vertical-align:middle;">'
                f'</div>'
            )
            legende += (
                f'<span style="margin-right:12px;font-size:0.75em;">'
                f'<span style="display:inline-block;width:10px;height:10px;'
                f'background-color:{s["couleur"]};border-radius:2px;'
                f'margin-right:4px;vertical-align:middle;"></span>'
                f'{nom_projet_safe} ({s["pct"]}%)'
                f'</span>'
            )

        html = (
            f'<div style="width:100%;background:#F0F0F0;border-radius:4px;'
            f'overflow:hidden;margin-bottom:4px;">{barres}</div>'
            f'<div style="margin-bottom:8px;">{legende}</div>'
        )
        st.markdown(html, unsafe_allow_html=True)

# -------------------------------------------------------
# ONGLET PRINCIPAL
# -------------------------------------------------------

def assignation_tab():
    st.header('Assignation des équipes')
    init_statut_sauvegarde()

    # --- Choix du projet ---
    projet = st.selectbox(
        "Choisir un projet :",
        options=[p["Nom"] for p in Projets],
        key="choix_projet",
        on_change=marquer_modifie
    )

    if projet is None:
        return

    st.header(projet)

    if projet not in st.session_state.Data_proj:
        st.session_state.Data_proj[projet] = {}

    proj_courant = st.session_state.Data_proj[projet]
    assignations_sauvegardees = proj_courant.get("Assignations", [])
    # --- Préparation des listes ---
    noms_disponibles = get_noms_ressources_disponibles(
        st.session_state.Ressources, assignations_sauvegardees
    )
    
    nb_ress = st.number_input(
        "Personnes à affecter à ce projet :",
        value=proj_courant.get("Nb_ressources", 0),
        min_value=0,
        max_value = len(noms_disponibles),
        key=f"nb_ress_{projet}",
        on_change=marquer_modifie
    )

    

    # --- Grille 2 colonnes ---
    lignes_cols = [st.columns(2) for i in range(0, nb_ress, 2)]

    # --- Boucle ressources ---
    assignation_en_cours = []
    deja_choisis = []

    for k in range(nb_ress):
        # Pré-remplissage depuis la sauvegarde
        if k < len(assignations_sauvegardees):
            nom_sauvegarde = assignations_sauvegardees[k]["Nom"]
        else:
            nom_sauvegarde = None

        # Filtrage sans doublons
        noms_filtres = [n for n in noms_disponibles if n not in deja_choisis]

        # Index par défaut
        default_index = noms_filtres.index(nom_sauvegarde) if nom_sauvegarde in noms_filtres else 0

        # Affichage dans la grille
        with lignes_cols[k // 2][k % 2]:
            assignation = afficher_bloc_ressource(
                k, noms_filtres, default_index, assignations_sauvegardees, projet
            )

        deja_choisis.append(assignation["Nom"])
        assignation_en_cours.append(assignation)

    # --- Sauvegarde ---
    afficher_statut()

    if st.button("Sauvegarder"):
        st.session_state.Data_proj[projet] = {
            "Nb_ressources": nb_ress,
            "Assignations": assignation_en_cours
        }
        recalculer_dispos(
            st.session_state.Data_proj,
            st.session_state.Ressources,
            Ressources_base
        )
        st.session_state.statut_sauvegarde = "sauvegarde"
        st.rerun()

    # --- Tableau récap ---
    if st.session_state.Data_proj:
        afficher_tableau_recap()
