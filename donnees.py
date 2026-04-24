import streamlit as st


#---------CALENDRIER---------------------------------------------------------------------------------
#Liste des projets pour calendrier(à lier à excel)
Projets_cal = [
    {
     "title" : "Enlèvement au sérail",
     "start" : "2026-01-01",
     "end" : "2026-05-12",
    "backgroundColor" : "#FF6C6C",
    "borderColor":"#FF6C6C"
     },
    {
     "title" : "Manon Lescaut",
     "start" : "2026-02-03",
     "end" : "2026-10-16",
    "backgroundColor":"#FFBD45",
    "borderColor":"#FFBD45"    
     },
    {
     "title" : "Brundibar",
     "start" : "2026-03-02",
     "end" : "2026-05-15",
    "backgroundColor" : "#63CDEB",
    "borderColor":"#63CDEB"
     }
    ]

#Liste des absences pour calendrier (à lier à excel)
Absences_cal = [
    {
     "title" : "Abraham Lincoln",
     "start" : "2026-04-15",
     "end" : "2026-04-25",
    "backgroundColor" : "#FF6C6C",
    "borderColor":"#FF6C6C"
     },
    {
     "title" : "Aya Nakamura",
     "start" : "2026-04-21",
     "end" : "2026-04-23",
    "backgroundColor":"#FFBD45",
    "borderColor":"#FFBD45"    
     },
    {
     "title" : "Charlie Chaplin",
     "start" : "2026-04-02",
     "end" : "2026-04-12",
    "backgroundColor" : "#63CDEB",
    "borderColor":"#63CDEB"
     }
    ]

# Options calendrier
Options_cal = {
    "initialView": "dayGridMonth",
    "locale": "fr",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    }
}

#----------------RESSOURCES--------------------------------------------------------------------------
#Liste des Ressources de base
Ressources_base= [
    {"Nom" : "Abraham Lincoln", "Dispo_base" : 100},
    { "Nom":"Albert Einstein", "Dispo_base" : 70},
    {"Nom" : "Marie Curie", "Dispo_base" : 100},
    {"Nom" : "Aya Nakamura", "Dispo_base": 100},
    {"Nom" : "Charlie Chaplin", "Dispo_base" : 25}
    ]

#-------PROJETS-----------------------------------------------------------------------------------
#Liste des Projets :
Projets = [
    {"Nom" : "L'enlèvement au sérail","Client" : "TCE"},
    {"Nom" : "Manon Lescaut", "Client" : "TCE"},
    {"Nom" : "Brundibar", "Client": "L'opéra Comique"}
    ]
#-------INITIALISATION SESSION STATE-----------------------------------------------------------------------------------

def init_session_state():
  """Initialise les variables de session si elles n'existent pas encore"""
  #Données ressources
  if "Ressources" not in st.session_state:
      st.session_state.Ressources= [
      {"Nom" : "Abraham Lincoln", "Dispo_restante" : 100},
      { "Nom":"Albert Einstein", "Dispo_restante" : 70},
      {"Nom" : "Marie Curie", "Dispo_restante" : 100},
      {"Nom" : "Aya Nakamura", "Dispo_restante": 100},
      {"Nom" : "Charlie Chaplin", "Dispo_restante" : 25}
      ]
  #Données projets
  if "Data_proj" not in st.session_state:
      st.session_state.Data_proj = {}
