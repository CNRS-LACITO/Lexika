#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika
import lexika.outils
import gettext
import locale

langue_système = locale.getlocale()[0].split("_")[0] if locale.getlocale()[0] else "fr"
langue_préférée = gettext.translation("messages", localedir="internationalisation", languages=[langue_système], fallback=True)
langue_préférée.install()


class NébuleuseDeLʼHélice:
    """
    Classe qui transforme toutes les poussières de données pour éventuellement donner vie à un dictionnaire selon les différentes interférences paramétriques.
    """
    def __init__(self, chemin_accès_configuration):
        self.configuration = lexika.outils.Configuration(chemin_accès_configuration)
        self.créateur = lexika.NébuleuseDʼOméga(self.configuration)

    @lexika.outils.Chronométrer(_("création du dictionnaire"))
    def créer_dictionnaire(self, nombre_cœurs):
        """
        Crée un dictionnaire en exécutant les différentes étapes : lecture du fichier source, envoi des données au créateur et écriture du résultat (le tout avec exécution des différentes tâches spécifiques).
        """
        self.créateur.commencer_accrétion(nombre_cœurs)
        self.créateur.connecter_liens()
        self.générer_xml()
        if hasattr(self.configuration, "latex"):
            self.générer_latex()

    @lexika.outils.Chronométrer(_("génération du fichier XML"))
    def générer_xml(self):
        """
        Génère le fichier XML à partir du dictionnaire nouvellement créé.
        """
        générateur_xml = lexika.outils.GénérateurXML(self.configuration, self.créateur.créateur.racine, self.créateur.créateur.dictionnaire)
        générateur_xml.obtenir_xml()

    @lexika.outils.Chronométrer(_("génération du fichier Latex"))
    def générer_latex(self):
        """
        Génère le fichier Latex à partir du fichier XML nouvellement créé.
        """
        générateur_latex = lexika.outils.GénérateurLatex(self.configuration, self.créateur.créateur.dictionnaire)
        générateur_latex.obtenir_latex(self.configuration.latex["format"], self.configuration.latex["langue"])
