#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.getcwd(), "lexika"))

import lexika
import lexika.configuration
import lexika.outils
import lexika.linguistique
import locale
import gettext
import regex
import pdb
import time
from pprint import pprint

langue_système = locale.getlocale()[0].split("_")[0]
langue_préférée = gettext.translation("messages", localedir="internationalisation", languages=[langue_système], fallback=True)
langue_préférée.install()


class Déesse:
    """
    Classe qui transforme toutes les poussières de données pour éventuellement donner vie à un dictionnaire selon les différentes interférences paramétriques.
    """
    def __init__(self, chemin_accès_configuration):
        self.chemin_accès_configuration = chemin_accès_configuration
        self.configuration = None
        self.lecteur = None
        self.créateur = None
        self.écriveur = None
        self.langues = None
        self.balises = None
        self.entités_linguistiques = None

    def initialiser(self):
        # Création des objets de configuration.
        self.configuration = lexika.outils.Configuration(self.chemin_accès_configuration)
        self.tâches = self.configuration.tâches if "tâches" in self.configuration.__dict__ else []

        # Création des objets primordiaux.
        self.lecteur = None
        self.créateur = self.configuration.créateur(self.configuration)
        # self.créateur_inverse = self.configuration.créateur_inverse(self.configuration)
        self.écriveur = None
        self.créateur.initialiser()

    def exécuter_tâches(self, niveau, fichier_entrée=None, fichier_sortie=None):
        if fichier_entrée and fichier_sortie:
            for tâche, fonction in [(tâche, fonction) for tâche, fonction in lexika.configuration.tâches.items() if tâche in self.configuration.tâches]:
                print(_("Tâche de niveau « {} » en cours d'exécution : « {} »").format(niveau, tâche))
                try:
                    fonction(fichier_entrée, fichier_sortie)
                except Exception as exception:
                    print(_("Tâche « {} » échouée : {}").format(tâche, exception))

    @lexika.outils.Chronométrer(_("analyse de données"))
    def créer_dictionnaire(self):
        self.exécuter_tâches("initial", self.configuration.chemin_source, self.configuration.chemin_source)
        self.lecteur = lexika.outils.Lecteur(self.configuration.chemin_source)
        for donnée in self.lecteur.données:
            self.créateur.analyser_données(donnée)
        self.écriveur = lexika.outils.Écriveur(self.configuration.chemin_cible)
        self.exécuter_tâches("final")

    def créer_lexique_inverse(self):
        for donnée in self.lecteur.données:
            extraction = self.extracteur.analyser_ligne(donnée)
            if extraction:
                self.créateur.aiguiller_entité_linguistique(extraction)
        self.écriveur = lexika.outils.Écriveur(self.configuration.chemin_cible)


    def générer_XML(self):
        générateur_XML = lexika.outils.GénérateurXML(self.configuration, self.créateur.dictionnaire)
        générateur_XML.obtenir_xml("structure")


def main():
    source_configuration = "./exemples/configuration tamaŋ.yml"
    déesse = Déesse(source_configuration)
    déesse.initialiser()
    déesse.créer_dictionnaire()
    déesse.créer_lexique_inverse()
    déesse.générer_XML()

if __name__ == "__main__":
    main()

