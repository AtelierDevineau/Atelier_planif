import streamlit as st
import plotly.graph_objects as go
from streamlit_calendar import calendar
from donnees import Projets_gantt, Absences_cal, Options_cal

#-------------CREATION GANTT--------------------
def gantt(projets_data):
  """Construction d'un diagramme de Gantt Plotly à partir de la liste de dicos Projets_gantt"""
  fig = go.Figure()
  #Le premier projet doit être en haut, on parcourt le dico dans le sens inverse
  for projet in reversed(projets_data):
    nom_projet = projet["projet"]
    couleur = projet["couleur"]
    for sous_tache in projet["sous_taches"]:
      label = f"{nom_projet} - {sous_tache['tache']}"
      fig.add_trace(go.Bar(
        name = nom_projet,
        orientation = "h",
        y=[label]
        x=[(__import__("datetime").date.fromisoformat(sous_tache["end"]) -
                    __import__("datetime").date.fromisoformat(sous_tache["start"])).days],
         base=[sous_tache["start"]],
         marker=dict(color=couleur, line=dict(color="white", width=1)),
         hovertemplate =(f"<b>{nom_projet}</b><br>"
                    f"Tâche : {sous_tache['tache']}<br>"
                    f"Début : {sous_tache['start']}<br>"
                    f"Fin : {sous_tache['end']}<extra></extra>"
                ),
         showlegend=False,
        ))
  #Legende manuelle
  for projet in projets_data:
        fig.add_trace(go.Scatter(
          x=[None],y=[None],
          mode="markers",
          marker=dict(size=10, color=projet["couleur"], symbol="square"),
          name =projet["projer"],
        ))
  fig.update_layout(
    barmode = "overlay",
    xaxis= dict(
      type="date",
      tickformat= "%b %Y",
      tickangle = -45,
      showgrid = True
      gridcolor="#eeeeee",
      ),
    yaxis= dict(
      autorange="reversed",
      tickfront= dict(size=12),
    ),
    height = 120 + sum(len(p["sous_taches"]) for p in projets_data) * 40,
    margin = dict(l=20, r=20, t=40, b=40),
    plot_bgcolor = "white",
    legend = dict(
      orientation ="h",
      yanchor = "bottom",
      y=1.02,
      xanchor = "left",
      x=0
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
    st.plotly_chart(fig, use_caontainer_width=True)
  if selection == "Absences":
    calendar(events = Absences_cal, options = Options_cal)
   
