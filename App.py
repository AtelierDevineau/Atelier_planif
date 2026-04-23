import streamlit as st
from streamlit_calendar import calendar
st.title("Planification projets")

# ---- Logo centré en haut de page ----
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Atelier Devineau logo.png", use_container_width=True)


#Onglets
titres_onglets = ['Calendrier', 'Assignation équipe']
Calendrier, Assignation = st.tabs(titres_onglets)
 

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


#Liste des Ressources
Ressources = ["Abraham Lincoln", "Albert Einstein", "Marie Curie", "Aya Nakamura", "Charlie Chaplin"]



# Ajouter du contenu à chaque onglet
with Calendrier:
    st.header('Calendrier')
    
    # Affichage du calendrier
    calendar(events = Projets, options = options)
 
with Assignation:
    st.header('Assignation des équipes')
    Choix_ressources = st.multiselect("Qui voulez-vous sélectionner ?", Ressources)
    st.write("Vous avez choisi : ", Choix_ressources)


