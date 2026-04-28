import streamlit as st
import plotly.graph_objects as go
from streamlit_calendar import calendar
from datetime import date, timedelta
from donnees import Projets_gantt, Absences_cal, Options_cal

#-------------CREATION GANTT--------------------
def to_timestamp_ms(date_str):
    """Convertit une date ISO 'YYYY-MM-DD' en timestamp milliseconds pour Plotly."""
    return int(datetime.fromisoformat(date_str).timestamp() * 1000)
    
def semaines_entre(date_debut_str, date_fin_str):
    """Génère les dates des lundis entre deux dates pour les ticks de l'axe."""
    debut = date.fromisoformat(date_debut_str)
    fin = date.fromisoformat(date_fin_str)
    # On recule au lundi précédent
    lundi = debut - timedelta(days=debut.weekday())
    ticks_dates = []
    ticks_labels = []
    while lundi <= fin:
        semaine = lundi.isocalendar()[1]
        annee = lundi.isocalendar()[0]
        ticks_dates.append(lundi.isoformat())
        ticks_labels.append(f"S{semaine:02d} {annee}")
        lundi += timedelta(weeks=1)
    return ticks_dates, ticks_labels

def gantt(projets_data):
    """Construction d'un diagramme de Gantt Plotly à partir de la liste de dicos Projets_gantt"""
    fig = go.Figure()

    # Le premier projet doit être en haut, on parcourt le dico dans le sens inverse
    for projet in reversed(projets_data):
        nom_projet = projet["projet"]
        couleur = projet["couleur"]
        for sous_tache in projet["sous_taches"]:
            label = f"{nom_projet} - {sous_tache['tache']}"
            duree_ms = (
                date.fromisoformat(sous_tache["end"]) -
                date.fromisoformat(sous_tache["start"])
            ).days * 24 * 3600 * 1000  # durée en millisecondes
            base_ms = to_timestamp_ms(sous_tache["start"])

            fig.add_trace(go.Bar(
                name=nom_projet,
                orientation="h",
                y=[label],
                x=[duree],
                base=[sous_tache["start"]],
                marker=dict(color=couleur, line=dict(color="white", width=1)),
                hovertemplate=(
                    f"<b>{nom_projet}</b><br>"
                    f"Tâche : {sous_tache['tache']}<br>"
                    f"Début : {sous_tache['start']}<br>"
                    f"Fin : {sous_tache['end']}<extra></extra>"
                ),
                showlegend=False,
            ))

    # Calcul de la plage de dates globale pour les ticks
    toutes_dates_debut = [st["start"] for p in projets_data for st in p["sous_taches"]]
    toutes_dates_fin   = [st["end"]   for p in projets_data for st in p["sous_taches"]]
    date_min = min(toutes_dates_debut)
    date_max = max(toutes_dates_fin)
    ticks_dates, ticks_labels = semaines_entre(date_min, date_max)

    # Légende manuelle (un carré coloré par projet)
    for projet in projets_data:
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(size=10, color=projet["couleur"], symbol="square"),
            name=projet["projet"],
        ))

    fig.update_layout(
        barmode="overlay",
        xaxis=dict(
            type="date",
            tickvals=ticks_dates,
            ticktext=ticks_labels,
            tickangle=-90,
            showgrid=True,
            gridcolor="#eeeeee",
            side="top",          # axe en haut
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(size=12),
        ),
        height=160 + sum(len(p["sous_taches"]) for p in projets_data) * 40,
        margin=dict(l=20, r=20, t=80, b=120),  # t grand pour axe haut, b grand pour légende bas
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,             # sous l'axe X (qui est en bas de la zone de tracé)
            xanchor="center",
            x=0.5,
        ),
    )
    return fig

           
#-------------ONGLET CALENDRIER----------------------

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
    fig = gantt(Projets_gantt)
    st.plotly_chart(fig, use_container_width=True)
  if selection == "Absences":
    calendar(events = Absences_cal, options = Options_cal)
   
