#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import lxml.etree
from typing import Union
import regex


def convertir_nom_classe(nom):
    return "".join([segment[0].upper() + segment[1:] for segment in regex.compile(r"[\s’]+").split(nom)])


class Abstraction:
    """
    Classe majeure qui concentre toutes les informations nécessaires pour créer une unique entité (parents potentiels, préabstractions en cas de nécessité, paramètres divers influant sur la création de l'entité, etc.). L'abstraction se situe entre la balise de la source et l'entité du résultat.
    """
    def __init__(self, nom: str, structure: dict, valeur: str = None, caractéristiques: dict = {}, drapeaux: Union[dict, list] = None, appelants: list = []):
        self.nom: str = nom
        self.nom_classe = convertir_nom_classe(nom)
        self.appelants = appelants
        self.entité: dict = copy.deepcopy(structure["entité"])
        self.parent: dict = copy.deepcopy(structure.get("parent", {}))
        self.préabstraction: dict = copy.deepcopy(structure.get("préabstraction", {}))
        self.spécial: dict = copy.deepcopy(structure.get("spécial", {}))
        self.entité["valeur"]: str = valeur
        self.entité["caractéristiques"]: dict = {}
        self.entité["caractéristiques"].update(caractéristiques)
        if "nom" in self.parent and isinstance(self.parent["nom"], str):
            self.parent["nom"] = [self.parent["nom"]]
        if "nom" in self.préabstraction and isinstance(self.préabstraction["nom"], str):
            self.préabstraction["nom"] = [self.préabstraction["nom"]]
        if drapeaux:
            self.spécial.get("drapeaux", []).append(drapeaux)

    def __repr__(self):
        return _(f"<abstraction {self.nom_classe} à {hex(id(self))}>")


class Entité:
    """
    Classe majeure qui concentre toutes les informations relatives à une entité linguistique (nom, valeur, caractéristiques, etc.).
    """
    def __init__(self, nom: str, valeur: str = None, caractéristiques: dict = {}, structure: dict = {}, attribut: str = None, spécial: dict = {}, données: dict = {}):
        self.nom = nom
        self.valeur = valeur
        self.caractéristiques = caractéristiques
        self.structure = structure
        self.attribut = attribut
        self.spécial = spécial
        self.données = données
        self.nom_classe = convertir_nom_classe(nom)
        
    def __repr__(self):
        return _(f"<entité {self.nom_classe} à {hex(id(self))}>")
    

class CréateurDʼAbstractions:
    """
    Classe permettant de créer des abstractions sans gérer le dictionnaire de données des entités qui peut être surdéfini.
    """
    compteur: int = 0
    def __init__(self, dictionnaire_abstractions: dict):
        self.dictionnaire = dictionnaire_abstractions

    def créer_abstraction(self, nom: str,valeur: str = None, caractéristiques: dict = {}, drapeaux: Union[dict, list] = None, appelants: list = []) -> Abstraction:
        structure = self.dictionnaire[nom]
        abstraction = Abstraction(nom, structure, valeur, caractéristiques, drapeaux, appelants)
        self.compteur += 1
        return abstraction


class ConvertisseurDeTexteEnrichi:
    """
    Classe gérant la conversion des textes enrichis selon la configuration des balises (liens et styles divers).
    """
    def __init__(self, modèles: list, structure: dict, source: dict, anéantir: bool = False):
        self.modèle_style = regex.compile(modèles["style"])
        self.modèle_lien = regex.compile(modèles["lien"])
        self.format_style = "<style type=\"\g<style>\">\g<texte></style>" if not anéantir else "\g<texte>"    
        self.source = {identifiant: entité for entité, identifiant in source.items()}        
        self.constantes = {informations["ascendant"]: informations["constante"] for abstraction, informations in structure.items() if informations.get("type") != "facultatif"}
        self.constantes_facultatives = {informations["ascendant"]: informations["constante"] for abstraction, informations in structure.items() if informations.get("type") == "facultatif"}

    def convertir_texte(self, texte: str) -> str:
        """
        Convertit un texte enrichi en XML (styles et liens).
        """
        return self.convertir_styles(self.convertir_liens(texte))
    
    def convertir_liens(self,  texte: str) -> str:
        """
        Convertit les différents liens en balises XML.
        """
        return self.modèle_lien.sub(self.remplacer_par_identifiant, texte)  
    
    def convertir_styles(self, texte: str) -> str:
        """
        Convertit les différents styles en balises XML.
        """  
        return self.modèle_style.sub(self.format_style, texte)        

    def trouver_cible(self, texte: str, entités: list) -> str:
        """
        Tente de trouver la cible d'un lien dans la source.
        """
        if entités:
            for candidat in self.créer_candidats(texte, entités):
                if candidat in self.source:
                    return candidat
        return None
    
    def créer_candidats(self, texte: str, entités: list) -> list:
        """
        Crée des identifiants de candidats potentiels selon les types d'entité.
        """
        candidats = [f"{self.constantes[entité]}{texte}" for entité in entités]
        candidats += [f"{self.constantes[entité]}{texte}{self.constantes_facultatives[entité]}1" for entité in entités if entité in self.constantes_facultatives]
        return candidats
    
    def remplacer_par_identifiant(self, bilan):
        """
        Crée le texte enrichi associé à un lien (trouvé ou non).
        """
        cible = self.trouver_cible(bilan.group("entrée"), ["entrée lexicale"])
        if cible:
            résultat = f"<lien cible=\"{cible}\">{bilan.group('entrée')}</lien>"
        else:
            résultat = f"<lien>{bilan.group('entrée')}</lien>"
        return résultat

        
class ConvertisseurDʼAbréviations:
    """
    Classe qui convertit les abréviations pour les informations de type liste fermée.
    """
    def __init__(self, dictionnaire: dict):
        self.dictionnaire = {}
        for catégorie, correspondances in dictionnaire.items():
            self.dictionnaire[catégorie] = {abréviation: terme for terme, abréviations in correspondances.items() for abréviation in (abréviations if isinstance(abréviations, list) else [abréviations])}
        
    def convertir(self, catégorie: str, terme: str) -> str:
        """
        Convertit un terme d'une catégorie selon le dictionnaire interne dérivé de la configuration s'il est présent, le renvoie tel quel sinon.
        """
        return self.dictionnaire.get(catégorie, {}).get(terme, terme)
    


