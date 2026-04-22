import streamlit as st
from streamlit_calendar import calendar
st.title("Planification projets")

#Liste des projets (à lier à excel)
Projets = [
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

# Options calendrier
options = {
    "initialView": "dayGridMonth",
    "locale": "fr",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    }
}


# Affichage du calendrier
calendar(events = Projets, options = options)

#Liste des Ressources
#Ressources = ["Abraham Lincoln", "Albert Einstein", "Marie Curie", "Aya Nakamura", "Charlie Chaplin"]


Ressources = {
    "BE" : ["Abraham Lincoln",
   "Albert Einstein",
     "Marie Curie",
    "Aya Nakamura",
     "Charlie Chaplin"]
    "Atelier" : [
    "Blablabla"
]
    }

Choix_ressources = st.multiselect(
    "Qui voulez-vous sélectionner ?",
    Ressources["BE"].values())
st.write("Vous avez choisi : ", Choix_ressources)
