#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.configuration
import lexika.internationalisation
import lexika.outils
import yaml
from pprint import pprint

class Configuration:
    """
    Classe intimement liée au fichier 'fichier_source' (au format YML) qui lui offre ses différents paramètres comme attributs.
    """
    def __init__(self, fichier_source):
        self.fichier_source = fichier_source
        with open(fichier_source, 'r') as entrée:
            # Mise à jour des attributs de l'objet en ajoutant des _ pour la compatibilité Python.
            self.__dict__.update({clef.replace(" ", "_"): valeur if clef != "langues" else {
                sous_valeur["identifiant"]: {sous_sous_clef.replace(" ", "_"): sous_sous_valeur for
                                             sous_sous_clef, sous_sous_valeur in sous_valeur.items()
                                             }
                for sous_valeur in valeur} for clef, valeur in yaml.safe_load(entrée).items()
                                  })
        self.créateur = lexika.configuration.créateurs[self.créateur]
        if self.format_entrée in lexika.configuration.format_entrée:
            self.format_entrée = lexika.configuration.format_entrée[self.format_entrée]
            self.format_sortie = lexika.configuration.format_sortie[self.format_sortie]
            self.modèle_ligne = self.format_entrée["modèle de ligne"]
            self.balises = self.format_entrée["balises"]
            self.entités = self.format_sortie["entités"]
            self.constantes = self.format_sortie["constantes"] if "constantes" in self.format_sortie else None
            self.expression_renvoi = self.format_sortie["expression de renvoi"] if "expression de renvoi" in self.format_sortie else None
        else:
            raise Exception("Format « {} » non pris en charge.".format(self.format_entrée))

    def récupérer_contenu_objet(self):
        return {clef.lstrip("_"): valeur for clef, valeur in self.__dict__.items()}



class Traducteur:
    def __init__(self, données=lexika.internationalisation.dictionnaires):
        self.données = données
        self.dictionnaire = {}

        for dictionnaire in données:
            self.dictionnaire.update(dictionnaire)

    def traduire(self, expression):
        if expression in self.dictionnaire:
            return self.dictionnaire[expression]
        else:
            return expression


class InformationEntité:
    """
    Classe intimement liée au fichier 'informations_linguistiques" (au format Python) qui lui offre ses différents paramètres comme attributs.
    """
    def __init__(self, données):
        """
        La classe s'instancie en prenant directement les informations du fichier, avec quelques valeurs par défaut.
        :param données: un dictionnaire d'éntités et d'attributs linguistiques.
        :memb entité; Entité concernée par l'ajout d'informations.
        :memb entité["nom"]: Nom de l'entité concernée.
        :memb entité["attributs"]: Attributs concernés par la mise à jour d'informations (normalement un seul).
        :memb entité["paramètres"]: Attributs auxiliaires (dictionnaire) concernés par la mise à jour d'informations (généralement donnés par la balise).
        :memb entité["structure"]: Informations de structure de l'entité.
        :memb entité["structure"]["identifiant"]: Informations sur la création d'identifiant pour l'entité concernée.
        :memb entité["structure"]["identifiant"]["nom"]: Nom de l'attribut qui sert de base d'identifiant.
        :memb entité["structure"]["identifiant"]["type"]: 'primaire' et 'secondaire' indique l'éventuelle combinaison des bases d'identifiant.
        :memb préentités (liste): Entités à créer préalablement avant l'ajout d'informations des entités concernées (facultatif, nécessaire en cas de première information nichée).
        :memb préentités[x]["nom"]: Nom de l'entité à créer (appelle le dictionnaire de l'entité en question, qui est similaire à l'actuel).
        :memb préentités[x]["paramètres"]: Attributs auxiliaires (dictionnaire) à mettre à jour.
        :memb parents (liste): Entités auxquelles peut se rattacher l'entité concernée, dans l'ordre de préférence en cas d'ambiguïté (hiérarchie souple), ne sert pas en cas de mise à jour d'information d'attribut.
        :memb parents[x]["nom"]: Nom de l'entité parente de l'entité concernée.
        :memb parents[x]["attribut"]: Nom de l'attribut (liste) de l'entité parente à laaquelle se connecte l'entité concernée.
        """
        self.entités= données["entité"] if "entité" in données else None
        self.préentités = données["préentités"] if "préentités" in données else None
        self.parents = données["parents"] if "parents" in données else None


