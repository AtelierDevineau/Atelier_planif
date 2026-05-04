import streamlit as st
from datetime import date, timedelta

#-------------AFFICHAGE----------------------
# Palette de couleurs proposées
COULEURS_PALETTE = {
    "Rouge":    "#FF6C6C",
    "Orange":   "#FFBD45",
    "Bleu":     "#63CDEB",
    "Vert":     "#6BCB77",
    "Violet":   "#A78BFA",
    "Rose":     "#F472B6",
    "Gris":     "#94A3B8",
}

#-------------ONGLET-----------------------------

def crea_proj_tab():
    st.subheader("Gestion des projets")
    projets = st.session_state.Projets_gantt

    # ---------- LISTE PROJETS EXISTANTS ------------
    if projets:
        st.subheader("Projets existants")

        # Couleurs déjà utilisées par les autres projets (pour le selectbox de chaque expander)
        couleurs_prises = {p["couleur"] for p in projets}

        for i, projet in enumerate(projets):
            couleur = projet["couleur"]

            # Persistance de l'état ouvert/fermé de l'expander
            key_expander = f"expander_open_{i}"
            if key_expander not in st.session_state:
                st.session_state[key_expander] = False

            with st.expander(
                f"**{projet['projet']}** - {len(projet['sous_taches'])} sous-tache(s)",
                expanded=st.session_state[key_expander]
            ):
                # Réinitialiser le flag après ouverture
                st.session_state[key_expander] = False

                # --------------- EDITION DU PROJET ---------------
                new_proj = st.text_input(
                    "Nom du projet",
                    value=projet["projet"],
                    key=f"nom_{i}"
                )

                # Sélecteur de couleur : on exclut les couleurs prises par les AUTRES projets
                couleurs_disponibles = {
                    nom: hex_
                    for nom, hex_ in COULEURS_PALETTE.items()
                    if hex_ == couleur or hex_ not in couleurs_prises
                }
                noms_disponibles = list(couleurs_disponibles.keys())
                hex_disponibles = list(couleurs_disponibles.values())
                index_couleur = hex_disponibles.index(couleur) if couleur in hex_disponibles else 0

                choix_couleur = st.selectbox(
                    "Couleur",
                    options=noms_disponibles,
                    index=index_couleur,
                    key=f"couleur_{i}",
                    format_func=lambda nom: f"{nom} ({COULEURS_PALETTE[nom]})"
                )
                new_color = COULEURS_PALETTE[choix_couleur]

                # --------------- SOUS TACHES ----------------------
                st.markdown("**Sous-tâches**")
                sous_taches = projet["sous_taches"]
                a_supp = None

                for j, st_data in enumerate(sous_taches):
                    cols = st.columns([3, 2, 2, 0.6])
                    with cols[0]:
                        sous_taches[j]["tache"] = st.text_input(
                            "Nom", value=st_data["tache"],
                            key=f"tache_{i}_{j}", label_visibility="collapsed"
                        )
                    with cols[1]:
                        sous_taches[j]["start"] = st.date_input(
                            "Début",
                            value=date.fromisoformat(st_data["start"]),
                            key=f"start_{i}_{j}",
                            label_visibility="collapsed"
                        ).isoformat()
                    with cols[2]:
                        sous_taches[j]["end"] = st.date_input(
                            "Fin",
                            value=date.fromisoformat(st_data["end"]),
                            key=f"end_{i}_{j}",
                            label_visibility="collapsed"
                        ).isoformat()
                    with cols[3]:
                        if st.button("🗑️", key=f"del_st_{i}_{j}", help="Supprimer cette tâche"):
                            a_supp = j

                if a_supp is not None:
                    sous_taches.pop(a_supp)
                    st.session_state[key_expander] = True
                    st.rerun()

                # ---------------- AJOUT SOUS-TÂCHE -----------------------
                if st.button("➕ Ajouter une sous-tâche", key=f"add_st_{i}"):
                    if sous_taches:
                        last_end = date.fromisoformat(sous_taches[-1]["end"])
                    else:
                        last_end = date.today()
                    sous_taches.append({
                        "tache": "Nouvelle tâche",
                        "start": last_end.isoformat(),
                        "end": (last_end + timedelta(weeks=2)).isoformat(),
                    })
                    st.session_state[key_expander] = True
                    st.rerun()

                # -------------- BOUTONS --------------------------
                col_save, col_del = st.columns([1, 1])
                with col_save:
                    if st.button("✅ Enregistrer les modifications", key=f"save_{i}"):
                        projets[i]["projet"] = new_proj
                        projets[i]["couleur"] = new_color
                        projets[i]["sous_taches"] = sous_taches
                        st.success(f"Projet « {new_proj} » mis à jour.")
                        st.rerun()
                with col_del:
                    if st.button("🗑 Supprimer ce projet", key=f"suppr_{i}", type="secondary"):
                        projets.pop(i)
                        st.warning("Projet supprimé")
                        st.rerun()

    # ----------------- CREATION NOUVEAU PROJET ----------------------
    st.divider()
    st.subheader("Nouveau projet")

    # Couleurs déjà prises → on choisit la première couleur libre comme défaut
    couleurs_prises = {p["couleur"] for p in projets}
    couleur_defaut = next(
        (hex_ for hex_ in COULEURS_PALETTE.values() if hex_ not in couleurs_prises),
        list(COULEURS_PALETTE.values())[0]  # fallback si toutes prises
    )

    with st.form("form_nouveau_projet", clear_on_submit=True):
        nom_new = st.text_input("Nom du projet")
        submitted = st.form_submit_button("Créer le projet")

    if submitted:
        if not nom_new.strip():
            st.error("Merci de saisir le nom du projet")
        elif any(p["projet"] == nom_new.strip() for p in projets):
            st.error("Un projet avec ce nom existe déjà")
        else:
            projets.append({
                "projet": nom_new.strip(),
                "couleur": couleur_defaut,
                "sous_taches": []
            })
            st.success(f"Projet « {nom_new.strip()} » créé ! Dépliez-le ci-dessus pour ajouter des sous-tâches et choisir sa couleur.")
            st.rerun()
