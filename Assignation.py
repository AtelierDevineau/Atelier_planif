import streamlit as st
from donnees import Projets, Ressources_base

def assignation_tab():
  """Affiche le contenu de l'onglet Assignation des équipes"""
  st.header('Assignation des équipes')
  assignation_en_cours = []
    
  #------------------CHOIX DU PROJET---------------------------------------------------

  Choix_projet = st.selectbox("Choisir un projet :", options=[p["Nom"] for p in Projets], key="Choix_projet")
  
  if Choix_projet != None:
    st.header(Choix_projet)
    #Sauvegarde des données
    if Choix_projet not in st.session_state.Data_proj:
      st.session_state.Data_proj[Choix_projet] = {}
        
    Proj_courant = st.session_state.Data_proj[Choix_projet]
    Nb_Ress = st.number_input("Personnes à affecter à ce projet :", value = Proj_courant.get("Nb_ressources", 0), key=f"nb_ress_{Choix_projet}")

    #-----------BOUCLE RESSOURCES------------------
    # Préparation des valeurs sauvegardées pour donner les index nécessaires aux widgets
    noms_ressources = [r["Nom"] for r in st.session_state.Ressources if r["Dispo_restante"] > 0]
    assignations_sauvegardees = Proj_courant.get("Assignations", [])
        
    for k in range(Nb_Ress):
      #Pré remplissage depuis la sauvegarde    
      if k < len(assignations_sauvegardees): #Permet que si on n'a assigné que 2 personnes, il ne cherche pas 3
        nom_sauvegarde = assignations_sauvegardees[k]["Nom"]
        #Donne le nom sur lequel le multiselect va se mettre par défaut, surtout pratique si anciennes sauvegardes
        default_index = noms_ressources.index(nom_sauvegarde) if nom_sauvegarde in noms_ressources else 0 
        #Garde aussi le pourcentage
        pct_sauvegarde = assignations_sauvegardees[k]["Pct"]
            
      else:
        #Sinon on garde les paramètres par défaut (projet non touché)
        default_index = 0
        pct_sauvegarde = 0

      #On ne pioche pas le nom de la personne dans le session state Ressources, mais bien dans la liste avec l'index qui nous intéresse pour se souvenir de ce qui a été modifié
            
      Choix_ressources = st.selectbox(f"Personne {k+1} :", noms_ressources, index=default_index, key=f"select_ress_{Choix_projet}_{k}")   
            
      #Calcul des dispos
      Dispo_base = next(r["Dispo_base"] for r in Ressources_base if r["Nom"] == Choix_ressources)
      Dispo_restante = next(r["Dispo_restante"] for r in st.session_state.Ressources if r["Nom"] == Choix_ressources)
      st.write(Choix_ressources, "a", Dispo_restante, "% de disponibilité")
             
      # Pourcentage restant, pareil on dit clairement si ça a déjà été modifié
      Pct_ress = st.slider("Charge de travail sur ce projet (%) :", min_value=0, max_value=Dispo_base, value=pct_sauvegarde, key=f"slider_ress_{Choix_projet}_{k}")
           
      # Compter les % d'assignation pour maj
      assignation_en_cours.append({"Nom": Choix_ressources, "Pct" : Pct_ress})
    #-------------SAUVEGARDE---------------------------------  
    if st.button("Sauvegarder"):
    # On repart des dispos de base
    for r in st.session_state.Ressources:
        r["Dispo_restante"] = next(rb["Dispo_base"] for rb in Ressources_base if rb["Nom"] == r["Nom"])
    
    # On sauvegarde d'abord
    st.session_state.Data_proj[Choix_projet] = {
        "Nb_ressources": Nb_Ress,
        "Assignations": assignation_en_cours
    }
    
    # Puis on recalcule en tenant compte de TOUS les projets sauvegardés
    for proj, data in st.session_state.Data_proj.items():
        for a in data.get("Assignations", []):
            for r in st.session_state.Ressources:
                if r["Nom"] == a["Nom"]:
                    r["Dispo_restante"] -= a["Pct"]
    
    st.success("✅")
    
  #----------------TABLEAU RECAP---------------------------------------------
  if st.session_state.Data_proj:
    st.divider()
    st.subheader("Récapitulatif")
    st.dataframe(
      {"Projet": list(st.session_state.Data_proj.keys()),
      "Ressources": [v.get("Nb_ressources", 0) for v in st.session_state.Data_proj.values()]}
        )
   

    






