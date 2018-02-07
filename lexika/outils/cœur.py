#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.configuration
import lexika.internationalisation
import lexika.outils
import logging
import string
import yaml


class Configuration:
    """
    Classe qui charge tous les paramètres de configuration utiles au processus de création de dictionnaires.
    """
    def __init__(self, fichier_source):
        self.fichier_source = fichier_source
        self.variables = {"langues": {}}

        with lexika.outils.OuvrirFichier(self.fichier_source, "r", type="interne") as fichier:
            configuration = yaml.load(fichier)

        for clef, élément in configuration.items():
            self.__dict__.update({clef.replace(" ", "_").replace("’", "ʼ").lower(): élément})

        with lexika.outils.OuvrirFichier("configuration/informations linguistiques.yml", "r", type="interne") as fichier:
            informations_linguistiques = yaml.load(fichier)

        try:
            with lexika.outils.OuvrirFichier(self.configuration["chemin source"], "r", type="interne") as fichier:
                informations_linguistiques_supplémentaires = yaml.load(fichier)
            for type_format in ["entrée", "sortie"]:
                if type_format in informations_linguistiques_supplémentaires["formats"]:
                    for nom_format, informations in informations_linguistiques_supplémentaires["formats"][type_format].items():
                        for sous_information in ["modèles", "balises", "abstractions", "identifiants", "abréviations"]:
                            if informations.get(sous_information):
                                informations[sous_information] = {**informations_linguistiques["formats"][type_format][informations["parent"]][sous_information], **informations[sous_information]}
                        informations_linguistiques["formats"][type_format].update(informations_linguistiques_supplémentaires["formats"][type_format])
        except KeyError as exception:
            logging.critical(_(f"Erreur dans le format de surdéfinition : clef de dictionnaire inconnue."))
            raise exception

        if self.base["format d’entrée"] not in informations_linguistiques["formats"]["entrée"]:
            logging.critical(_(f"Format d’entrée « {self.base['format d’entrée']} » non pris en charge."))
            raise Exception
        elif self.base["format de sortie"] not in informations_linguistiques["formats"]["sortie"]:
            logging.critical(_(f"Format de sortie « {self.base['format de sortie']} » non pris en charge."))
            raise Exception
        else:
            self.informations_entrée = informations_linguistiques["formats"]["entrée"][self.base["format d’entrée"]]
            self.informations_sortie = informations_linguistiques["formats"]["sortie"][self.base["format de sortie"]]

            for langue, informations_langue in self.langues.items():
                statut = "{} {}".format(informations_langue["statut"], len([clef for clef in self.variables["langues"].keys() if clef.startswith(informations_langue["statut"])]) + 1)
                self.variables["langues"][statut] = langue

            self.remplacer_variables_structures(informations_linguistiques)
        
    def remplacer_variables_structures(self, structure, parent=None):
        if isinstance(structure, dict):
            for clef, élément in structure.items():
                self.remplacer_variables_structures(élément, clef)
                if parent == "caractéristiques" and clef == "langue":
                    if élément in self.variables["langues"]:
                        structure[clef] = self.variables["langues"][élément]
        elif isinstance(structure, list):
            for élément in structure:
                    self.remplacer_variables_structures(élément)


class Traducteur:
    """
    Classe qui traduit selon la langue voulue les noms des entités, caractéristiques et autres valeurs de liste fermée à partir des traductions du fichier « internationalisation/traductions.yml ».
    """
    def __init__(self, langue):
        self.langue = langue
        with lexika.outils.OuvrirFichier("internationalisation/traductions.yml", "r", type="interne") as fichier:
            traductions = yaml.load(fichier)
        self.traductions = traductions["langues"].get(self.langue, {})
        self.domaines = traductions["langues"].get(self.langue, {}).get("spécifique", {}).keys()

    def traduire(self, expression, domaine=None):
        if domaine and expression in self.traductions.get("spécifique", {}).get(domaine, {}):
            return self.traductions["spécifique"][domaine][expression]
        elif not domaine and expression in self.traductions.get("général", {}):
            return self.traductions["général"][expression]
        else:
            return expression
    

class Gabarit(string.Template):
    delimiter = "�"
    
