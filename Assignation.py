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

        pct_choisi = st.slider(
            "Charge :", min_value=0, max_value=max_slider,
            value=pct_sauvegarde,
            key=f"slider_ress_{projet}_{k}",
            on_change=marquer_modifie
        )

    return {"Nom": nom_choisi, "Pct": pct_choisi}

def afficher_tableau_recap():
    """Affiche le tableau récapitulatif de toutes les assignations"""
    st.divider()
    st.subheader("Récapitulatif")
    st.dataframe({
        "Projet": list(st.session_state.Data_proj.keys()),
        "Ressources": [v.get("Nb_ressources", 0) for v in st.session_state.Data_proj.values()]
    })

    lignes = [
        {"Ressource": a["Nom"], "Projet": nom_proj, "Charge (%)": a["Pct"]}
        for nom_proj, data in st.session_state.Data_proj.items()
        for a in data.get("Assignations", [])
    ]
    if lignes:
        df_pivot = (
            pd.DataFrame(lignes)
            .pivot_table(index="Ressource", columns="Projet", values="Charge (%)", aggfunc="sum")
            .fillna(0).astype(int)
        )
        st.dataframe(df_pivot, use_container_width=True)

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
