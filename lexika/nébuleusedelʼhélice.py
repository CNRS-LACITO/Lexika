#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
import lexika
import lexika.configuration
import lexika.outils
import lexika.linguistique
import locale
import gettext

langue_système = locale.getlocale()[0].split("_")[0]
langue_préférée = gettext.translation("messages", localedir="internationalisation", languages=[langue_système], fallback=True)
langue_préférée.install()


class NébuleuseDeLʼHélice:
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
        """
        Initialise la configuration générale et les objets nécessaires à la création d'un dictionnaire.
        :return:
        """
        # Création des objets de configuration.
        self.configuration = lexika.outils.Configuration(self.chemin_accès_configuration)
        self.tâches = self.configuration.tâches if "tâches" in self.configuration.__dict__ else []

        # Création des objets primordiaux.
        self.lecteur = None
        self.créateur = self.configuration.créateur(self.configuration)
        self.écriveur = None
        self.créateur.initialiser()

    @lexika.outils.Chronométrer(_("exécution d'une tâche"))
    def exécuter_tâches(self, niveau, **mots_clefs):
        """
        Exécute des tâches spécifiques choisies par l'utilisateur à différent niveau de la création du dictionnaire.
        :param niveau: initial, final
        :param fichier_entrée:
        :param fichier_sortie:
        :return:
        """
        for tâche, fonction in [(tâche, fonction) for tâche, fonction in lexika.outils.tâches.items() if niveau in self.configuration.tâches and self.configuration.tâches[niveau] and tâche in self.configuration.tâches[niveau]]:
            logging.info(_("Tâche de niveau « {} » en cours d'exécution : « {} »").format(niveau, tâche))
            fonction(**mots_clefs)
            # try:
            #
            # except Exception as exception:
            #     print(_("Tâche « {} » échouée : {}").format(tâche, exception))

    @lexika.outils.Chronométrer(_("création du dictionnaire"))
    def créer_dictionnaire(self):
        """
        Crée un dictionnaire en exécutant les différentes étapes : lecture du fichier source, envoi des données au créateur et écriture du résultat (le tout avec exécution des différentes tâches spécifiques).
        :return:
        """
        self.exécuter_tâches("initial", fichier_entrée=self.configuration.chemin_source, fichier_sortie=self.configuration.chemin_source)
        self.lecteur = lexika.outils.Lecteur(self.configuration.chemin_source)
        for donnée in self.lecteur.données:
            self.créateur.analyser_données(donnée)
        self.créateur.connecter_renvois()
        self.créateur.extraire_sous_entrées()
        self.écriveur = lexika.outils.Écriveur(self.configuration.XML["chemin cible"])
        self.exécuter_tâches("final", dictionnaire=self.créateur.dictionnaire, liste_identifiants=self.créateur.identifiants)

    @lexika.outils.Chronométrer(_("génération du fichier XML"))
    def générer_XML(self):
        """
        Génère le fichier XML à partir du dictionnaire nouvellement créé.
        :return:
        """
        # self.exécuter_tâches("pré-XML")
        générateur_XML = lexika.outils.GénérateurXML(self.configuration, self.créateur.dictionnaire, self.créateur.informations_globales)
        générateur_XML.obtenir_xml(self.configuration.XML["format"], self.configuration.XML["langue"])
        # self.exécuter_tâches("post-XML")

    @lexika.outils.Chronométrer(_("génération du fichier Latex"))
    def générer_Latex(self):
        """
        Génère le fichier Latex à partir du fichier XML nouvellement créé.
        :return:
        """
        # self.exécuter_tâches("pré-Latex")
        générateur_Latex = lexika.outils.GénérateurLatex(self.configuration, self.créateur.dictionnaire, self.créateur.informations_globales)
        générateur_Latex.obtenir_latex(self.configuration.Latex["format"], self.configuration.Latex["langue"])
        # self.exécuter_tâches("post-Latex")

