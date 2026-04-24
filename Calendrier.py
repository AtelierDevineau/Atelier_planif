import streamlit as st
from streamlit_calendar import calendar
from Data import Projets_cal, Absences_cal, options_calendrier

def calendrier_tab():
  """Affiche onglet calendrier"""
  st.header('Calendrier')
  # Choix entre absence ou projet
  selection = st.pills(
  " ",
  ["Projets","Absences"],
  selection_mode="single",
  default = "Projets"
  )
  if selection == "Projets" :
    # Affichage du calendrier projet
    calendar(events = Projets_cal, options = options_calendrier)
  if selection == "Absences":
    calendar(events = Absences_cal, options = options_calendrier)
   
