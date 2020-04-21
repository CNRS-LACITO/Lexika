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
    def __init__(self, nom: str, valeur: str = None, caractéristiques: dict = {}, spécial: dict = {}, données: dict = {}):
        self.nom = nom
        self.valeur = valeur
        self.caractéristiques = copy.deepcopy(caractéristiques)
        self.spécial = copy.deepcopy(spécial)
        self.données = copy.deepcopy(données)
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
    def __init__(self, modèles: list, structure: dict, source: dict):
        self.convertisseur_expressions_rationnelles = ConvertisseurDʼExpressionsRationnelles()
        self.modèles_lien, self.modèles_style, self.modèles_relation, self.modèles_floutage_lien = self.préparer_modèles(modèles)
        self.modèle_groupe = regex.compile(r"(?P<ensemble>\\g<(?P<clef>.+?)>)")
        self.source = source
        self.structure = structure
        self.source_inverse = self.créer_source_inversée(self.source)

    def préparer_modèles(self, modèles):
        """
        Prépare les différents modèles d’expression rationnelle.
        """
        for modèle in modèles:
            modèle["origine"] = regex.compile(self.convertisseur_expressions_rationnelles.inconvertir(modèle["origine"]), flags=regex.V1)
        return [[modèle for modèle in modèles if modèle["type"] == type] for type in ["lien", "style", "relation", "floutage de lien"]]

    def créer_source_inversée(self, source: dict):
        """
        Crée la source inversée permettant de manière exhaustive de retrouver l’identifiant à partir d’une expression simplifiée.
        """
        source_inversée = {}
        for identifiant, renvois in self.source.items():
            if identifiant:
                source_inversée[identifiant] = identifiant
                for identifiant_simplifié in self.créer_identifiants_simplifiés(identifiant):
                    if identifiant_simplifié not in source_inversée:
                        source_inversée[identifiant_simplifié] = identifiant
            for renvoi in renvois:
                if renvoi not in source_inversée:
                    source_inversée[renvoi] = identifiant
        return source_inversée

    def créer_identifiants_simplifiés(self, identifiant: str):
        """
        Crée des identifiants simplifiés (sans aucune constante d’identifiant d’entité, sans aucun caractère facultatif, etc.).
        """
        identifiants = []
        correspondances = str.maketrans({élément["constante"]: "" for élément in self.structure.values()})
        identifiant = identifiant.translate(correspondances)
        identifiants.append(identifiant)
        for modèle in self.modèles_floutage_lien:
            identifiant = modèle["origine"].sub("", identifiant)
            identifiants.append(identifiant)
        return identifiants

    def convertir_texte(self, texte: str) -> str:
        """
        Convertit un texte enrichi en XML (styles et liens).
        """
        return self.convertir_styles(self.convertir_liens(texte))

    def convertir_liens(self, texte: str) -> str:
        """
        Convertit les différents liens en balises XML.
        """
        for modèle in self.modèles_lien:
            texte = modèle["origine"].sub(lambda bilan: self.convertir_lien_intra_expression(bilan, modèle), texte)
        return texte

    def convertir_styles(self, texte: str) -> str:
        """
        Convertit les différents styles en balises XML.
        """
        for modèle in self.modèles_style:
            texte = modèle["origine"].sub(modèle["but"], texte)
        return texte

    def trouver_cible(self, texte: str) -> str:
        """
        Tente de trouver la cible d'un lien dans la source, d'abord par recherche directe, puis par inférence d’identifiant.
        """
        résultat = self.source_inverse.get(texte)
        if not résultat:
            résultat = self.source_inverse.get(texte)
        if not résultat:
            for candidat in self.créer_candidats(texte):
                if candidat in self.source_inverse:
                    résultat = candidat
                    break
        return résultat

    def créer_candidats(self, texte: str) -> list:
        """
        Crée des identifiants de candidats potentiels.
        """
        candidats = []
        for modèle in self.modèles_relation:
            bilan = modèle["origine"].match(texte)
            if bilan:
                éléments = bilan.groupdict()
                meilleur_candidat = ""
                for élément in éléments:
                    élément = self.convertisseur_expressions_rationnelles.exconvertir(élément)
                    if élément in self.structure and bilan.group(self.convertisseur_expressions_rationnelles.inconvertir(élément)):
                        meilleur_candidat += f"{self.structure[élément]['constante']}{bilan.group(self.convertisseur_expressions_rationnelles.inconvertir(élément))}"
                candidats.append(meilleur_candidat)
        return candidats

    def convertir_lien_intra_expression(self, bilan, modèle: dict) -> str:
        """
        Convertit les liens dans les expressions rationnelles de remplacement.
        """
        cible = self.trouver_cible(bilan.group(modèle["cible"]))
        remplacements = {clef: valeur for clef, valeur in {**bilan.groupdict(), "cible": cible}.items() if valeur}
        return self.modèle_groupe.sub(lambda bilan: remplacements.get(bilan.group("clef"), ""), modèle["but"] if cible else modèle["défaut"])


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


class ConvertisseurDʼExpressionsRationnelles:
    """
    Classe qui convertit les noms de groupe des expressions rationnelle pour les rendre compatibles avec la bibliothèque « regex ».
    """
    def __init__(self):
        self.caractères = {" ": "_", "’": "ʼ"}

    def inconvertir(self, expression: str):
        """
        Convertit l’expression rationnelle de la réalité vers la norme de la bibliothèque.
        """
        for ancien_caractère, nouveau_caractère in self.caractères.items():
            expression = expression.replace(ancien_caractère, nouveau_caractère)
        return expression

    def exconvertir(self, expression: str):
        """
        Convertit l’expression rationnelle de la norme de la bibliothèque vers la réalité.
        """
        for nouveau_caractère, ancien_caractère in self.caractères.items():
            expression = expression.replace(ancien_caractère, nouveau_caractère)
        return expression



