#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import regex

tâches = {
    "remplacer caractères":  lambda fichier_entrée, fichier_sortie: remplacer_caractères(fichier_entrée, fichier_sortie),
    "joindre lignes coupées": lambda fichier_entrée, fichier_sortie: joindre_lignes_coupées(fichier_entrée, fichier_sortie),
    "créer liens automatiques": lambda dictionnaire, liste_identifiants: créer_liens_automatiques(dictionnaire, liste_identifiants),
}

def remplacer_caractères(fichier_entrée, fichier_sortie):
    résultat = []
    with open(fichier_entrée, 'r') as entrée:
        for ligne in entrée.readlines():
            # résultat.append(ligne.replace("^", '').replace("<", "‹").replace(">", "›"))
            résultat.append(ligne.replace("^", ''))
    with open(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))

def joindre_lignes_coupées(fichier_entrée, fichier_sortie):
    with open(fichier_entrée, 'r') as entrée:
        résultat = []
        for ligne in entrée.readlines():
            if ligne.strip() and not ligne.startswith("\\"):
                résultat[-1] = "{} {}".format(résultat[-1].rstrip(), ligne)
            else:
                résultat.append(ligne)
    with open(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))

def créer_liens_automatiques(dictionnaire, liste_identifiants):
    modèle = regex.compile(r"(?P<ensemble>fv:(?P<cible>[\w_~-]+))|(?P<ensemble>\|fv{(?P<cible>[\w\s~\[\]-]+)})")
    liste_formes_citation = {entité.forme_citation.replace("°", ''): entité.identifiant for entité in liste_identifiants.values() if hasattr(entité, "forme_citation")}
    créer_liens(dictionnaire, modèle, liste_identifiants, liste_formes_citation)

# def créer_liens_automatiques(dictionnaire, liste_identifiants):
#     modèle = regex.compile(r"(?P<ensemble>\\lang{(?P<cible>[¹²³⁴\d\w\s~\(\)\/-]+)})")
#     liste_formes_citation = {}
#     créer_liens(dictionnaire, modèle, liste_identifiants, liste_formes_citation)

def créer_liens(objet, modèle, liste_identifiants, liste_formes_citation):
    if isinstance(objet, lexika.linguistique.EntitéLinguistique):
        for nom, élément in objet.__dict__.items():
            if nom not in ["nom_entité_linguistique", "_parent", "_attribut_parent"]:
                if isinstance(élément, list):
                    for sous_élément in élément:
                        créer_liens(sous_élément, modèle, liste_identifiants, liste_formes_citation)
                elif isinstance(élément, dict):
                    for clef_sous_élément, valeur_sous_élément in élément.items():
                        créer_liens(valeur_sous_élément, modèle, liste_identifiants, liste_formes_citation)
                elif nom not in ["lien", "non_lien"]:
                    bilan = modèle.search(élément)
                    if bilan:
                        bilans = modèle.finditer(élément)
                        for bilan in bilans:
                            ensemble = bilan.group("ensemble")
                            cible = bilan.group("cible").replace("_", " ")
                            identifiants = ["Ⓔ{}".format(cible), "Ⓔ{}Ⓗ1".format(cible)]
                            for identifiant in identifiants:
                                if identifiant in liste_identifiants:
                                    for attribut in ["forme_citation", "vedette", "nom", "acception"]:
                                        if hasattr(liste_identifiants[identifiant], attribut):
                                            affichage_cible = getattr(liste_identifiants[identifiant], attribut)
                                            élément = élément.replace(ensemble, "⊣lien cible=\"{}\"⊢{}⊣/lien⊢".format(identifiant, affichage_cible))
                                            break
                                    break
                            else:
                                if cible in liste_formes_citation:
                                    élément = élément.replace(ensemble, "⊣lien cible=\"{}\"⊢{}⊣/lien⊢".format(liste_formes_citation[cible], cible))
                                else:
                                    for identifiant in liste_identifiants: ## attention aux performances...
                                        if identifiant.endswith("ⓔ{}".format(cible)):
                                            élément = élément.replace(ensemble, "⊣lien cible=\"{}\"⊢{}⊣/lien⊢".format(identifiant, cible))
                                            break
                                    else:
                                        élément = élément.replace(ensemble, cible)
                        setattr(objet, nom, élément)
