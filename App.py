import streamlit as st
from donnees import init_session_state
from Calendrier import calendrier_tab
from Assignation import assignation_tab
from Crea_proj import crea_proj_tab

# ── Init ──────────────────────────────────────────────────────────────────────
init_session_state()

# ── Logo ──────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Atelier Devineau logo.png", use_container_width=True)

# ── Titre centré et en gras ─────────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center; font-weight:bold;'>Planification projets</h1>", unsafe_allow_html=True)
# ── Onglets ───────────────────────────────────────────────────────────────────
Calendrier, Assignation, Crea_proj = st.tabs(["Calendrier", "Assignation équipe","Création projet"])

with Calendrier:
    calendrier_tab()
with Crea_proj:
    crea_proj_tab()
with Assignation:
    assignation_tab()


