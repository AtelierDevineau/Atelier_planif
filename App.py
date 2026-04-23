import streamlit as st
from streamlit_calendar import calendar


# Logo centré en haut de page
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Atelier Devineau logo.png", use_container_width=True)
#------------------------------------------------------------------------------------------
st.title("Planification projets")
#------------------------------------------------------------------------------------------
#Onglets
titres_onglets = ['Calendrier', 'Assignation équipe']
Calendrier, Assignation = st.tabs(titres_onglets)
#------------------------------------------------------------------------------------------
#Données projets
if "Data_proj" not in st.session_state:
    st.session_state.Data_proj = {}

#------------------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------------------
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
 #------------------------------------------------------------------------------------------   

# Options calendrier
options_calendrier = {
    "initialView": "dayGridMonth",
    "locale": "fr",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    }
}

#------------------------------------------------------------------------------------------
#Liste des Ressources
Ressources = [
    {"Nom" : "Abraham Lincoln",
    "Dispo" : 100
    },
    { "Nom":"Albert Einstein",
    "Dispo" : 70
    },
    {"Nom" : "Marie Curie",
    "Dispo" : 100
    },
    {"Nom" : "Aya Nakamura",
    "Dispo": 100
    },
    {"Nom" : "Charlie Chaplin",
    "Dispo" : 25
    }]
#------------------------------------------------------------------------------------------
#Liste des Projets :
Projets = [
    {"Nom" : "L'enlèvement au sérail",
    "Client" : "TCE"
    },
    {"Nom" : "Manon Lescaut",
     "Client" : "TCE"
    },
    {"Nom" : "Brundibar",
     "Client": "L'opéra Comique"
    }]

#------------------------------------------------------------------------------------------
# Ajouter du contenu à chaque onglet
with Calendrier:
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
 
with Assignation:
    st.header('Assignation des équipes')
   
    #Choix du projet
    Choix_projet = st.selectbox("Choisir un projet :", options=[p["Nom"] for p in Projets], key="Choix_projet")
  
    if Choix_projet != None:
        st.header(Choix_projet)  
          #Sauvegarde des données
        if Choix_projet not in st.session_state.Data_proj:
            st.session_state.Data_proj[Choix_projet] = {}
        Proj_courant = st.session_state.Data_proj[Choix_projet]
        Nb_Ress = st.number_input("Personnes à affecter à ce projet :", value = Proj_courant.get("Nb_ressources", 0))

        for k in range(Nb_Ress):
            Choix_ressources = st.selectbox(f"Personne {k+1} :", [r["Nom"] for r in Ressources])  
            for res in Ressources:
                if res["Nom"] == Choix_ressources :
                    Dispo = res["Dispo"]
            st.write(Choix ressources, "a", Dispo,"% de disponibilité")
            Pct_ress = st.slider("Charge de travail sur ce projet (%) :", 0,Dispo )

        
        if st.button("Sauvegarder"):
            st.session_state.Data_proj[Choix_projet] = {
                "Nb_ressources": Nb_Ress,
            }
            st.success("✅")
    #Tableau récap
    if st.session_state.Data_proj:
        st.divider()
        st.subheader("Récapitulatif")
        st.dataframe(
            {
            "Projet": list(st.session_state.Data_proj.keys()),
            "Ressources": [v.get("Nb_ressources", 0) for v in st.session_state.Data_proj.values()],
            "Budget": [v.get("Budget", 0) for v in st.session_state.Data_proj.values()],
            }
        )
   

    

















