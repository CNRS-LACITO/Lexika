#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika

import logging


class NébuleuseDeLʼHélice(lexika.outils.ClasseConfigurée):
    """
    Classe qui transforme toutes les poussières de données pour éventuellement donner vie à un dictionnaire selon les différentes interférences paramétriques.
    """
    def __init__(self):
        super().__init__()
        self.créateur = lexika.NébuleuseDʼOméga()

    @lexika.outils.Chronométrer(_("création du dictionnaire"))
    def créer_dictionnaire(self, nombre_cœurs):
        """
        Crée un dictionnaire en exécutant les différentes étapes : lecture du fichier source, envoi des données au créateur et écriture du résultat (le tout avec exécution des différentes tâches spécifiques).
        """
        self.créateur.commencer_accrétion(nombre_cœurs)
        self.créateur.connecter_liens()
        self.générer_xml()
        self.afficher_statistiques()
        if self.configuration.informations.get("latex"):
            self.générer_latex()

    @lexika.outils.Chronométrer(_("génération du fichier XML"))
    def générer_xml(self):
        """
        Génère le fichier XML à partir du dictionnaire nouvellement créé.
        """
        générateur_xml = lexika.outils.GénérateurXML(self.créateur.créateur.racine, self.créateur.créateur.dictionnaire)
        générateur_xml.obtenir_xml()

    @lexika.outils.Chronométrer(_("génération du fichier Latex"))
    def générer_latex(self):
        """
        Génère le fichier Latex à partir du fichier XML nouvellement créé.
        """
        générateur_latex = lexika.outils.GénérateurLatex(self.créateur.créateur.dictionnaire)
        générateur_latex.obtenir_latex(self.configuration.informations["latex"]["format"], self.configuration.informations["latex"]["langue"])

    def afficher_statistiques(self):
        """
        Affiche diverses informations statistiques utiles.
        """
        texte_identifiants = "\n".join([f"{clef} : {valeur}" for clef, valeur in self.créateur.créateur.convertisseur_texte_enrichi.source_inverse.items()])
        logging.info(_(f"Liste des identifiants et de leurs renvois :\n{texte_identifiants}\n"))
        texte_balises = "\n".join([f"{clef} : {valeur}" for clef, valeur in self.créateur.créateur.balises.items()])
        logging.info(_(f"Liste des balises et de leurs occurrences :\n{texte_balises}\n"))
