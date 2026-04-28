import streamlit as st
from datetime import date, timedelta, datetime

def crea_proj_tab():
  """Affiche l'outil de création de projet"""
  st.subheader('Création de projet')
  nom_proj = st.text_input("Entrez le nom du projet")
  date_debut =st.date_input(label="Début du projet", format="YYYY/MM/DD", label_visibility="visible", width="stretch")
  date_fin =st.date_input(label="Fin du projet", format="YYYY/MM/DD", label_visibility="visible", width="stretch")
  
  col1, col2 = st.columns(2)
  with col1:
    date_debut =st.date_input(label="Début du projet", format="YYYY/MM/DD", label_visibility="visible", width="stretch")
  with col2:
    date_fin =st.date_input(label="Fin du projet", format="YYYY/MM/DD", label_visibility="visible", width="stretch")
