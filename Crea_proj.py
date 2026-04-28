import streamlit as st

def crea_proj_tab():
  """Affiche l'outil de création de projet"""
  st.subheader('Création de projet')
  nom_proj = st.text_input("Entrez le nom du projet")
  
