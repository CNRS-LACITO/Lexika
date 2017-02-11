#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.getcwd(), "lexika"))

import lexika
import lexika.configuration
import lexika.outils
import lexika.linguistique
import regex
import pdb
import time
from pprint import pprint

class Déesse:
    """
    Classe qui transforme toutes les poussières de données pour éventuellement donner vie à un dictionnaire selon les différentes interférences paramétriques.
    """
    def __init__(self, chemin_accès_configuration):
        self.chemin_accès_configuration = chemin_accès_configuration
        self.configuration = None
        self.lecteur = None
        self.extracteur = None
        self.créateur = None
        self.écriveur = None
        self.langues = None
        self.balises = None
        self.entités_linguistiques = None

    def initialiser(self):
        # Création des objets de configuration.
        self.configuration = lexika.outils.Configuration(self.chemin_accès_configuration)
        # pprint(self.configuration.récupérer_contenu_objet())
        self.tâches = self.configuration.tâches if "tâches" in self.configuration.__dict__ else []

        # Création des objets primordiaux.
        self.lecteur = None
        self.extracteur = Extracteur(self.configuration)
        self.créateur = self.configuration.créateur(self.configuration)
        self.écriveur = None
        self.extracteur.initialiser()
        self.créateur.initialiser()

    def exécuter_tâches(self, niveau, fichier_entrée=None, fichier_sortie=None):
        if fichier_entrée and fichier_sortie:
            for tâche, fonction in [(tâche, fonction) for tâche, fonction in lexika.configuration.tâches.items() if tâche in self.configuration.tâches]:
                print("Tâche de niveau {} en cours d'exécution : '{}'".format(niveau, tâche))
                try:
                    fonction(fichier_entrée, fichier_sortie)
                except Exception as exception:
                    print("Tâche '{}' échouée :\n{}".format(tâche, exception))

    @lexika.outils.Chronométrer("analyse de données")
    def analyser_données(self):
        self.exécuter_tâches("initial", self.configuration.chemin_source, self.configuration.chemin_source)
        self.lecteur = lexika.outils.Lecteur(self.configuration.chemin_source)
        for donnée in self.lecteur.données:
            extraction = self.extracteur.analyser_ligne(donnée)
            if extraction:
                self.créateur.aiguiller_entité_linguistique(extraction)
        self.écriveur = lexika.outils.Écriveur(self.configuration.chemin_cible)
        self.exécuter_tâches("final")

    def générer_XML(self):
        générateur_XML = lexika.outils.GénérateurXML(self.configuration, self.créateur.dictionnaire)
        générateur_XML.obtenir_xml("structure")


class Extracteur:
    def __init__(self, configuration):
        self.configuration = configuration
        self.type_source = None
        self.balises = None

    def initialiser(self):
        self.type_source = self.configuration.type_source
        self.balises = self.configuration.balises
        self.entités_linguistiques = self
        self.modèle_ligne = regex.compile(self.configuration.modèle_ligne)

    def analyser_ligne(self, donnée):
        résultat = None
        bilan = self.modèle_ligne.match(donnée["ligne"])
        if bilan:
            balise = bilan.group("balise")
            métabalise = bilan.group("métabalise") if "métabalise" in bilan.groupdict() else None
            données = bilan.group("données")
            métadonnées = bilan.group("métadonnées")
            if balise in self.balises:
                if not données:
                    print("La balise de type '{}' (ligne {}) ne contient aucune valeur.".format(balise, donnée["index"]))
                if métadonnées:
                    métadonnées = {"balise": métabalise, "données": métadonnées}
                résultat = self.balises[balise]
                résultat["entité"].update({"valeurs": [données], "métainformations": métadonnées})
        #     else:
        #         print("Balise '{}' inconnue à la ligne {}, donc ignorée.".format(balise, donnée["index"]))
        # else:
        #     print("Attention, la ligne '{ligne}' ({index}) n'a pas été validée par l'expression régulière.".format(**donnée))
        return résultat



def main():
    source_configuration = "./exemples/configuration mwotlap.yml"
    déesse = Déesse(source_configuration)
    déesse.initialiser()
    déesse.analyser_données()
    déesse.générer_XML()

if __name__ == "__main__":
    main()

