import streamlit as st
from datetime import date, timedelta, datetime

#-------------AFFICHAGE----------------------
def init_statut_sauvegarde():
  if "statut_sauvegarde_proj" not in st.session_state:
      st.session_state.statut_sauvegarde_proj = "vide"

def marquer_modifie():
  st.session_state.statut_sauvegarde_proj = "modifie"

def afficher_statut():
  if st.session_state.statut_sauvegarde_proj == "sauvegarde":
    st.success("✅ Sauvegardé")
  elif st.session_state.statut_sauvegarde_proj == "modifie":
    st.warning("❌ Modifications non sauvegardées")


#-------------ONGLET-----------------------------

def crea_proj_tab():
  init_statut_sauvegarde()
  """Affiche l'outil de création de projet"""
  st.subheader('Création de projet')
  nom_proj = st.text_input("Entrez le nom du projet", on_change=marquer_modifie)
  
  col1, col2 = st.columns(2)
  with col1:
    date_debut =st.date_input("Début du projet", format="YYYY/MM/DD", label_visibility="visible", width="stretch",on_change=marquer_modifie)
  with col2:
    date_fin =st.date_input("Fin du projet", format="YYYY/MM/DD", label_visibility="visible", width="stretch",on_change=marquer_modifie)
  
#------------SAUVERGARDE----------------
afficher_statut()
if st.button("Sauvegarder"):
  st.session_state.proj[projet] = {
    "Nom": nom_proj,
    "Date début": date_debut,
    "Date fin" : date_fin
    }
  st.session_state.statut_sauvegarde_proj = "sauvegarde"
  st.rerun()
