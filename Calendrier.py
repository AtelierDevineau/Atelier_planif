import streamlit as st
from streamlit_calendar import calendar
from donnees import Projets_cal, Absences_cal, Options_cal

def calendrier_tab():
  """Affiche onglet calendrier"""
  st.subheader('Calendrier')
  # Choix entre absence ou projet
  selection = st.pills(
  " ",
  ["Projets","Absences"],
  selection_mode="single",
  default = "Projets"
  )
  if selection == "Projets" :
    # Affichage du calendrier projet
    calendar(events = Projets_cal, options = Options_cal)
  if selection == "Absences":
    calendar(events = Absences_cal, options = Options_cal)
   
