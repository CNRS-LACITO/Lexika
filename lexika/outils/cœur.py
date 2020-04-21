#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika

import logging
import os
import pprint
import string
import yaml




class ClasseConfigurée:
    """
    Classe abstraite de laquelle héritent toutes les classes nécessitant un accès aux informations de configuration.
    """
    configuration = None

    def __init__(self):
        pass

    def configurer(self, chemin_accès_configuration):
        self.__class__.configuration = lexika.outils.Configuration(chemin_accès_configuration)


class Configuration:
    """
    Classe qui charge tous les paramètres de configuration utiles au processus de création de dictionnaires.
    """
    def __init__(self, fichier_source):
        self.fichier_source = fichier_source
        self.informations = {}
        self.variables = {"langues": {}}
        self.chemin_accès_fichier_configuration_primordial = os.path.join(os.path.dirname(lexika.__file__), "configuration/informations linguistiques.yml")
        self.préparer_informations()

    def préparer_informations(self):
        with lexika.outils.OuvrirFichier(self.fichier_source, "r", type="interne") as fichier:
            configuration = yaml.load(fichier)

        self.informations.update(configuration)

        for catégorie, informations in self.informations.items():
            if isinstance(informations, dict):
                for nom, information in informations.items():
                    if nom.startswith("chemin"):
                        informations[nom] = self.absolutiser_chemin_accès(information)

        with lexika.outils.OuvrirFichier(self.chemin_accès_fichier_configuration_primordial, "r", type="interne") as fichier:
            informations_linguistiques = yaml.load(fichier)

        try:
            with lexika.outils.OuvrirFichier(self.informations["configuration"]["chemin source"], "r", type="interne") as fichier:
                informations_linguistiques_supplémentaires = yaml.load(fichier)
            for type_format in ["entrée", "sortie"]:
                if type_format in informations_linguistiques_supplémentaires["formats"]:
                    for nom_format, informations in informations_linguistiques_supplémentaires["formats"][type_format].items():
                        for sous_information in ["modèles", "balises", "abstractions", "identifiants", "abréviations"]:
                            informations[sous_information] = {**informations_linguistiques["formats"][type_format][informations["parent"]].get(sous_information, {}), **informations.get(sous_information, {})}
                        informations_linguistiques["formats"][type_format].update(informations_linguistiques_supplémentaires["formats"][type_format])
        except KeyError as exception:
            logging.critical(_(f"Erreur dans le format de surdéfinition : clef de dictionnaire inconnue."))
            raise exception

        if self.informations["base"]["format d’entrée"] not in informations_linguistiques["formats"]["entrée"]:
            logging.critical(_(f"Format d’entrée « {self.informations['base']['format d’entrée']} » non pris en charge."))
            raise Exception
        elif self.informations["base"]["format de sortie"] not in informations_linguistiques["formats"]["sortie"]:
            logging.critical(_(f"Format de sortie « {self.informations['base']['format de sortie']} » non pris en charge."))
            raise Exception
        else:
            self.informations["entrée"] = informations_linguistiques["formats"]["entrée"][self.informations["base"]["format d’entrée"]]
            self.informations["sortie"] = informations_linguistiques["formats"]["sortie"][self.informations["base"]["format de sortie"]]

            for langue in self.informations["langues"]:
                statut = "{} {}".format(langue["statut"], len([clef for clef in self.variables["langues"].keys() if clef.startswith(langue["statut"])]) + 1)
                self.variables["langues"][statut] = langue["code"]

            self.remplacer_variables_structures(informations_linguistiques)

        logging.info(pprint.pformat(self.informations))
        
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

    def absolutiser_chemin_accès(self, chemin_accès):
        résultat = os.path.abspath(os.path.join(os.path.dirname(self.fichier_source), chemin_accès))
        print(chemin_accès, résultat)
        return résultat


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




