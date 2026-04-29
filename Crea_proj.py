import streamlit as st
from datetime import date, timedelta

#-------------AFFICHAGE----------------------
# Palette de couleurs proposées
COULEURS_PALETTE = {
    "Rouge":    "#FF6C6C",
    "Orange":   "#FFBD45",
    "Bleu":     "#63CDEB",
    "Vert":     "#6BCB77",
    "Violet":   "#A78BFA",
    "Rose":     "#F472B6",
    "Gris":     "#94A3B8",
}
#-------------ONGLET-----------------------------

def crea_proj_tab():
  st.subheader("Gestion des projets")
  projets = st.session_state.Projets_gantt
  #----------LISTE PROJETS EXISTANTS------------
  if projets:
    st.subheader("Projets existants")

    for i, projet in enumerate(projets):
      couleur = projet["couleur"]
      with st.expander(f"**{projet['projet']}** - {len(projet['sous_taches'])} sous-tache(s)"):
        #---------------EDITION DU PROJET---------------
        new_proj = st.text_input("Nom du projet",
          value = projet["projet"],
          key = f"nom_{i}"
                  )
        #Sélecteur de couleur
        noms_couleurs = list(COULEURS_PALETTE.keys())
        couleurs_hex = list(COULEURS_PALETTE.values())
        index_couleur = couleurs_hex.index(couleur) if couleur in couleurs_hex else 0
        choix_couleur = st.selectbox(
          "Couleur",
          options=noms_couleurs,
          key=f"couleur_{i}",
          format_func = lambda nom: f"{nom} ({COULEURS_PALETTE[nom]})"
        )
        new_color = COULEURS_PALETTE[choix_couleur]

        #---------------SOUS TACHES----------------------
        st.markdown("**Sous-tâches**")
        sous_taches = projet["sous_taches"]
        a_supp = None

        for j, st_data in enumerate(sous_taches):
          cols = st.columns([3,2,2,0.6])
          with cols[0]:
            sous_taches[j]["tache"]=st.text_input("Nom", value = st_data["tache"], key= f"tache_{i}_{j}", label_visibility = "collapsed")
          with cols[1]:
            sous_taches[j]["start"] = st.date_input(
              "Début", 
              value=date.fromisoformat(st_data["start"]),
              key= f"start_{i}_{j}", 
              label_visibility="collapsed").isoformat()
          with cols[2]:
            sous_taches[j]["end"] = st.date_input(
              "Fin", 
              value=date.fromisoformat(st_data["end"]),
              key= f"end_{i}_{j}", 
              label_visibility="collapsed").isoformat()
          with cols[3]:
            if st.button("🗑️", key= f"del_st_{i}_{j}", help="Supprimer cette tâche"):
              a_supp = j
        if a_supp is not None:
          sous_taches.pop(a_supp)
          st.rerun()
        #----------------AJOUT SOUS-TÂCHE-----------------------
        if st.button("➕ Ajouter une sous-tâche", key=f"add_st_{i}"):
          #Date par défaut : lendemain de la fin de la dernière sous-tâche
          if sous_taches:
            last_end = date.fromisoformat(sous_taches[-1]["end"])
          else:
            last_end = date.today()
          sous_taches.append({
            "tache" : "Nouvelle tâche",
            "start" : last_end.isoformat(),
            "end" : (last_end + timedelta(weeks=2)).isoformat(),
          })
          st.rerun()
        #--------------BOUTONS--------------------------
        col_save, col_del = st.columns([1,1])
        with col_save:
          if st.button("✅ Enregistrer les modifications", key=f"save_{i}"):
            projets[i]["projet"] = new_proj
            projets[i]["couleur"] = new_color
            projets[i]["sous-taches"] = sous_taches
            st.success(f"Projet « {new_proj} » mis à jour.")
            st.rerun()
        with col_del:
          if st.button("🗑 Supprimer ce projet", key=f"suppr_{i}", type="secondary"):
            projets.pop(i)
            st.warning("Projet supprimé")
            st.rerun()
  
    else:
        st.info("Aucun projet. Créez-en un ci-dessous.")


    #-----------------CREATION NOUVEAU PROJET----------------------
    st.divider()
    st.subheader("Nouveau projet")
    
    with st.form("form_nouveau_projet", clear_on_submit = True):
      nom_new = st.text_input("Nom du projet")
      choix_couleur_new = st.selectbox("Couleur", options = list(COULEURS_PALETTE.keys()), format_func = lambda nom: f"{nom} ({COULEURS_PALETTE[nom]})")
      
      submitted = st.form_submit_button("Créer le projet")
    
    if submitted:
      if not nom_new.strip(): #Au cas où aucun nom est rentré
        st.error("Merci de saisir le nom du projet")
      elif any(p["projet"] == nom_new.strip() for p in projets): #Si le projet existe déjà
        st.error("Un projet avec ce nom existe déjà")
      else:
        projets.append({
          "projet" : nom_new.strip(),
          "couleur" : COULEURS_PALETTE[choix_couleur_new],
          "sous_taches":[]
        })
        st.success(f"Projet {nom_new.strip()} créé ! Dépliez le ci-dessus pour ajouter des sous-tâches.")
        st.rerun()
      










