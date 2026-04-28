#----------------CALCUL DES DISPOS------------------------
def recalculer_dispos(data_proj, ressources, ressources_base):
    """Repart des dispos de base et recalcule selon tous les projets sauvegardés
    Rappel : 
      -Dans ressources_base on trouve le nom et la dispo de base de chaque ressource
      -data_proj est dans le session_state et contient des données telles que : le projet, des data ?
    """
    for r in ressources:
        r["Dispo_restante"] = next(rb["Dispo_base"] for rb in ressources_base if rb["Nom"] == r["Nom"]) #On repart de la dispo de base
    for proj, data in data_proj.items():
        for assignation in data.get("Assignations", []):
            for r in ressources:
                if r["Nom"] == assignation["Nom"]: #Si une ressource est affectée au projet étudié
                    r["Dispo_restante"] -= assignation["Pct"] #On change sa dispo de base en la nouvelle

#-------------FONCTION POUR RETURN DISPO RESTANTE--------------
def get_dispo_restante(nom, ressources):
    """Retourne la dispo restante d'une ressource"""
    return next(r["Dispo_restante"] for r in ressources if r["Nom"] == nom)

#-------------FONCTION POUR RETURN DISPO BASE--------------
def get_dispo_base(nom, ressources_base):
    """Retourne la dispo de base d'une ressource"""
    return next(r["Dispo_base"] for r in ressources_base if r["Nom"] == nom)

  #-------------FONCTION POUR RETURN CHARGE SUR PROJ ETUDIE--------------
def get_charge_sur_projet(nom, assignations_sauvegardees):
    """Retourne la charge déjà assignée à une ressource sur le projet courant"""
    return next((a["Pct"] for a in assignations_sauvegardees if a["Nom"] == nom), 0)

  #-------------FONCTION POUR RETURN NOMS PERS DISPO + DEJA ASSIGNEES PROJ COURANT--------------
def get_noms_ressources_disponibles(ressources, assignations_sauvegardees):
    """Retourne les ressources avec dispo > 0, plus celles déjà assignées au projet courant"""
    noms_deja_assignes = [a["Nom"] for a in assignations_sauvegardees]
    return [
        r["Nom"] for r in ressources
        if r["Dispo_restante"] > 0 or r["Nom"] in noms_deja_assignes
    ]
