import streamlit as st
from donnees import init_session_state
from Calendrier import calendrier_tab
from Assignation import assignation_tab

# ── Init ──────────────────────────────────────────────────────────────────────
init_session_state()

# ── Logo ──────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Atelier Devineau logo.png", use_container_width=True)

# ── Titre ─────────────────────────────────────────────────────────────────────
st.title("Planification projets")

# ── Onglets ───────────────────────────────────────────────────────────────────
Calendrier, Assignation = st.tabs(["Calendrier", "Assignation équipe"])

with Calendrier:
    calendrier_tab()

with Assignation:
    assignation_tab()
