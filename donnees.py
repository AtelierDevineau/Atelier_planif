import streamlit as st
import json
import requests
import base64

#---------GITHUB---------------------------------------------------------------------------------

GITHUB_REPO = st.secrets["GITHUB_REPO"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

def _headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def _api_url(filename):
    return f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"

def _charger_json_github(filename):
    """Lit un fichier JSON depuis le repo GitHub, retourne (données, sha)"""
    response = requests.get(_api_url(filename), headers=_headers())
    if response.status_code == 200:
        data = response.json()
        contenu = base64.b64decode(data["content"]).decode("utf-8")
        return json.loads(contenu), data["sha"]
    else:
        st.error(f"Erreur de lecture GitHub ({response.status_code}) pour {filename}")
        return [], None

def _sauvegarder_json_github(filename, donnees, sha):
    """Écrit un fichier JSON sur GitHub, retourne le nouveau sha"""
    contenu_encode = base64.b64encode(
        json.dumps(donnees, ensure_ascii=False, indent=4).encode("utf-8")
    ).decode("utf-8")
    payload = {
        "message": f"Mise à jour de {filename} via l'app",
        "content": contenu_encode,
        "sha": sha
    }
    response = requests.put(_api_url(filename), headers=_headers(), json=payload)
    if response.status_code in (200, 201):
        return response.json()["content"]["sha"]
    else:
        st.error(f"Erreur de sauvegarde GitHub ({response.status_code}) pour {filename}")
        return sha

# Fonctions publiques projets
def charger_projets_github():
    return _charger_json_github("projets.json")

def sauvegarder_projets_github(projets, sha):
    return _sauvegarder_json_github("projets.json", projets, sha)

# Fonctions publiques ressources
def charger_ressources_github():
    return _charger_json_github("ressources.json")

def sauvegarder_ressources_github(ressources, sha):
    return _sauvegarder_json_github("ressources.json", ressources, sha)


#---------CALENDRIER---------------------------------------------------------------------------------

Absences_cal = [
    {
        "title": "Abraham Lincoln",
        "start": "2026-04-15",
        "end": "2026-04-25",
        "backgroundColor": "#FF6C6C",
        "borderColor": "#FF6C6C"
    },
    {
        "title": "Aya Nakamura",
        "start": "2026-04-21",
        "end": "2026-04-23",
        "backgroundColor": "#FFBD45",
        "borderColor": "#FFBD45"
    },
    {
        "title": "Charlie Chaplin",
        "start": "2026-04-02",
        "end": "2026-04-12",
        "backgroundColor": "#63CDEB",
        "borderColor": "#63CDEB"
    }
]

Options_cal = {
    "initialView": "dayGridMonth",
    "locale": "fr",
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    }
}

#-------PROJETS-----------------------------------------------------------------------------------
Projets = [
    {"Nom": "L'enlèvement au sérail", "Client": "TCE"},
    {"Nom": "Manon Lescaut", "Client": "TCE"},
    {"Nom": "Brundibar", "Client": "L'opéra Comique"}
]

#-------INITIALISATION SESSION STATE-----------------------------------------------------------------------------------

def init_session_state():
    """Initialise les variables de session si elles n'existent pas encore"""

    # Ressources chargées depuis GitHub (contiennent Nom, Poste, Dispo_base)
    if "Ressources_base" not in st.session_state:
        ressources, sha = charger_ressources_github()
        st.session_state.Ressources_base = ressources
        st.session_state.ressources_sha = sha

    # Ressources avec dispo restante : construites depuis Ressources_base
    if "Ressources" not in st.session_state:
        st.session_state.Ressources = [
            {"Nom": r["Nom"], "Dispo_restante": r["Dispo_base"]}
            for r in st.session_state.Ressources_base
        ]

    # Données projets
    if "Data_proj" not in st.session_state:
        st.session_state.Data_proj = {}

    # Projets Gantt chargés depuis GitHub
    if "Projets_gantt" not in st.session_state:
        projets, sha = charger_projets_github()
        st.session_state.Projets_gantt = projets
        st.session_state.projets_sha = sha

    # Message de succès persisté entre reruns
    if "msg_succes" not in st.session_state:
        st.session_state.msg_succes = None

#------RECUPERER COULEUR PROJET--------------------------------------------------
def get_couleur_projet(nom_projet):
    """Retourne la couleur hex d'un projet depuis le session_state, gris par défaut"""
    for p in st.session_state.Projets_gantt:
        if p["projet"] == nom_projet:
            return p["couleur"]
    return "#CCCCCC"
