import streamlit as st
import pandas as pd
from donnees import sauvegarder_ressources_github, recalculer_dispos
from donnees import Ressources_base as Ressources_base_statique  # fallback non utilisé

POSTES = ["BE", "Serrurerie", "Construction", "Usinage", "Déco", "Administration", "Régisseur", "Autres"]

# -------------------------------------------------------
# UTILITAIRES
# -------------------------------------------------------

def _ressources_du_poste(poste):
    """Retourne les ressources du session_state pour un poste donné"""
    return [r for r in st.session_state.Ressources_base if r["Poste"] == poste]

def _noms_assignes():
    """Retourne tous les noms utilisés dans Data_proj"""
    noms = set()
    for data in st.session_state.Data_proj.values():
        for a in data.get("Assignations", []):
            noms.add(a["Nom"])
    return noms

def _supprimer_des_assignations(nom):
    """Supprime une ressource de toutes les assignations et décrémente Nb_ressources"""
    for proj, data in st.session_state.Data_proj.items():
        assignations = data.get("Assignations", [])
        nouvelles = [a for a in assignations if a["Nom"] != nom]
        if len(nouvelles) < len(assignations):
            data["Assignations"] = nouvelles
            data["Nb_ressources"] = max(0, data.get("Nb_ressources", 1) - 1)

def _syncer_ressources_restantes():
    """Resynchronise Ressources (dispo restante) depuis Ressources_base après une modif"""
    from Logique import recalculer_dispos
    # Reconstruire la liste Ressources depuis Ressources_base
    noms_base = {r["Nom"] for r in st.session_state.Ressources_base}
    # Garder les restantes existantes, ajouter les nouvelles, supprimer les absentes
    st.session_state.Ressources = [
        {"Nom": r["Nom"], "Dispo_restante": r["Dispo_base"]}
        for r in st.session_state.Ressources_base
    ]
    # Recalculer selon les assignations en cours
    recalculer_dispos(
        st.session_state.Data_proj,
        st.session_state.Ressources,
        st.session_state.Ressources_base
    )

# -------------------------------------------------------
# ONGLET PRINCIPAL
# -------------------------------------------------------

def crea_ress_tab():
    st.subheader("Gestion des ressources")

    # --- Bandeau modifications non sauvegardées ---
    if st.session_state.get("ress_modifiees"):
        st.warning("❌ Modifications non sauvegardées — cliquez sur **Enregistrer** en bas de page.")

    # --- Message de succès persisté ---
    if st.session_state.get("msg_succes_ress"):
        st.success(st.session_state.msg_succes_ress)
        st.session_state.msg_succes_ress = None

    noms_assignes = _noms_assignes()

    for poste in POSTES:
        st.subheader(poste)
        ressources_poste = _ressources_du_poste(poste)

        # --- Tableau éditable ---
        if ressources_poste:
            df = pd.DataFrame([
                {"Nom": r["Nom"], "Dispo de base (%)": r["Dispo_base"]}
                for r in ressources_poste
            ])

            df_edit = st.data_editor(
                df,
                key=f"editor_{poste}",
                num_rows="fixed",        # pas de suppression depuis le tableau
                use_container_width=True,
                column_config={
                    "Dispo de base (%)": st.column_config.NumberColumn(
                        min_value=0, max_value=100, step=5
                    )
                },
                hide_index=True,
            )

            # Détecter les modifications de nom (avertissement) ou de dispo
            for idx, row in df_edit.iterrows():
                nom_original = df.iloc[idx]["Nom"]
                nom_nouveau = row["Nom"]
                dispo_nouvelle = int(row["Dispo de base (%)"])

                if nom_nouveau != nom_original:
                    st.warning(
                        f"⚠️ Vous avez modifié le nom **{nom_original}** → **{nom_nouveau}**. "
                        f"Vérifiez que c'est bien une correction orthographique et non un changement de personne."
                    )

                # Mettre à jour dans session_state
                for r in st.session_state.Ressources_base:
                    if r["Nom"] == nom_original:
                        r["Nom"] = nom_nouveau
                        r["Dispo_base"] = dispo_nouvelle
                        st.session_state.ress_modifiees = True

            # --- Suppression ---
            with st.expander(f"Supprimer une ressource — {poste}"):
                noms_poste = [r["Nom"] for r in ressources_poste]
                nom_a_suppr = st.selectbox(
                    "Ressource à supprimer",
                    options=noms_poste,
                    key=f"suppr_select_{poste}"
                )
                if st.button(f"🗑 Supprimer {nom_a_suppr}", key=f"suppr_btn_{poste}", type="secondary"):
                    if nom_a_suppr in noms_assignes:
                        st.warning(
                            f"⚠️ **{nom_a_suppr}** est assigné à un ou plusieurs projets. "
                            f"La suppression retirera aussi ces assignations."
                        )
                        if st.button(f"Confirmer la suppression de {nom_a_suppr}", key=f"suppr_confirm_{poste}"):
                            _supprimer_des_assignations(nom_a_suppr)
                            st.session_state.Ressources_base = [
                                r for r in st.session_state.Ressources_base if r["Nom"] != nom_a_suppr
                            ]
                            st.session_state.ress_modifiees = True
                            st.rerun()
                    else:
                        st.session_state.Ressources_base = [
                            r for r in st.session_state.Ressources_base if r["Nom"] != nom_a_suppr
                        ]
                        st.session_state.ress_modifiees = True
                        st.rerun()

        else:
            st.caption("Aucune ressource dans ce poste.")

        # --- Formulaire d'ajout ---
        with st.form(key=f"form_add_{poste}", clear_on_submit=True):
            cols = st.columns([3, 1, 1])
            with cols[0]:
                nom_new = st.text_input("Nom", key=f"nom_new_{poste}")
            with cols[1]:
                dispo_new = st.number_input("Dispo (%)", min_value=0, max_value=100, value=100, step=5, key=f"dispo_new_{poste}")
            with cols[2]:
                st.markdown("<br>", unsafe_allow_html=True)
                submitted = st.form_submit_button("➕ Ajouter")

        if submitted:
            if not nom_new.strip():
                st.error("Merci de saisir un nom.")
            elif any(r["Nom"] == nom_new.strip() for r in st.session_state.Ressources_base):
                st.error(f"Une ressource avec le nom **{nom_new.strip()}** existe déjà.")
            else:
                st.session_state.Ressources_base.append({
                    "Nom": nom_new.strip(),
                    "Poste": poste,
                    "Dispo_base": int(dispo_new)
                })
                st.session_state.ress_modifiees = True
                st.rerun()

        st.divider()

    # --- Bouton global Enregistrer ---
    if st.button("✅ Enregistrer toutes les modifications", type="primary"):
        _syncer_ressources_restantes()
        nouveau_sha = sauvegarder_ressources_github(
            st.session_state.Ressources_base,
            st.session_state.ressources_sha
        )
        st.session_state.ressources_sha = nouveau_sha
        st.session_state.ress_modifiees = False
        st.session_state.msg_succes_ress = "✅ Ressources sauvegardées sur GitHub."
        st.rerun()
