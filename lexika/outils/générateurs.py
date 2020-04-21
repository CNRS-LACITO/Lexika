#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika
from lexika import outils

import logging
import lxml.etree
import lxml.html
import os
import regex


class Générateur(outils.ClasseConfigurée):
    """
    Classe abstraite permettant de générer un fichier de sortie depuis une dictionnaire et selon une configuration précise.
    """

    def __init__(self, dictionnaire):
        self.dictionnaire = dictionnaire


class GénérateurXML(Générateur):
    """
    Classe permettant de générer un fichier XML depuis un dictionnaire et selon une configuration précise.
    """
    def __init__(self, racine, dictionnaire):
        super().__init__(dictionnaire)

        self.chemin_accès_gabarit = os.path.join(os.path.dirname(lexika.__file__), "gabarits/XML/dictionnaire.xml")
        self.écriveur = lexika.outils.Écriveur(self.configuration.informations["xml"]["chemin cible"])
        self.format = self.configuration.informations["xml"]["format"] if "format" in self.configuration.informations["xml"] else "α"
        self.langue = self.configuration.informations["xml"]["langue"] if "langue" in self.configuration.informations["xml"] else "fra"
        lexika.outils.Trieur = lexika.outils.TrieurLexicographique if not os.path.isfile(self.configuration.informations["général"].get("chemin du trieur", "")) else lexika.outils.importer_module_personnalisé("lexika.outils.Trieur", self.configuration.informations["général"]["chemin du trieur"]).Trieur

        self.trieur = lexika.outils.TrieurLexicographique(self.configuration.informations["général"].get("ordre lexicographique"))
        self.racine = racine
        self.dictionnaire = dictionnaire

    def obtenir_xml(self):
        self.traduire = lexika.outils.Traducteur(self.langue).traduire if self.langue != "fra" else lambda expression, domaine=None: expression
        arborescence = lxml.etree.Element(self.convertir_nom(self.traduire(self.racine.nom_classe), "chameau"))
        for élément in self.racine.descendance:
            self.créer_éléments(élément, arborescence)
        texte_structuré = lxml.etree.tostring(arborescence, encoding="unicode", method="xml", pretty_print=True)
        informations = {"style": self.configuration.informations["xml"]["XSL"], "arborescence": texte_structuré}
        with lexika.outils.OuvrirFichier(self.chemin_accès_gabarit, 'r', type="interne") as gabarit:
            source = lexika.outils.Gabarit(gabarit.read())
        self.écriveur.écrire_résultat(source.substitute(informations))
        logging.info(_("Génération du fichier XML terminée"))

    def créer_éléments(self, entité, élément_parent):
        if isinstance(entité, lexika.outils.Entité):
            if self.format == "α":
                nom = self.convertir_nom(self.traduire(entité.nom), "chameau")
                attributs = {self.convertir_nom(self.traduire(clef), "serpent"): self.traduire(valeur) for clef, valeur in entité.caractéristiques.items()}
                if entité.spécial and "texte enrichi" in entité.spécial.get("drapeaux", {}):
                    élément_actuel = lxml.etree.XML(f"<{nom}>{entité.valeur}</{nom}>", parser=lxml.etree.XMLParser(recover=True))
                    élément_parent.append(élément_actuel)
                    for attribut, valeur in attributs.items():
                        élément_actuel.set(attribut, valeur)
                else:
                    élément_actuel = lxml.etree.SubElement(élément_parent, nom, attrib=attributs)
                    élément_actuel.text = self.traduire(entité.valeur, entité.nom)
            if hasattr(entité, "descendance"):
                for enfant in sorted(entité.descendance, key=lambda entrée: self.trieur.trier_expressions(entrée.spécial["tri"]["lexicographique"])) if entité == self.dictionnaire else entité.descendance:
                    self.créer_éléments(enfant, élément_actuel)

    def convertir_nom(self, nom, méthode):
        if méthode == "chameau":
            return "".join([segment[0].upper() + segment[1:] for segment in regex.split(r"[\s'’]", nom)])
        elif méthode == "serpent":
            return "".join([segment if index == 0 else segment[0].upper() + segment[1:] for index, segment in enumerate(regex.split(r"[\s'’]", nom))])
        else:
            return regex.sub(r"['’]", "ʼ", nom)


class GénérateurLatex(Générateur):
    """
    Classe permettant de générer un fichier Latex depuis un dictionnaire et selon une configuration précise.
    """
    def __init__(self, dictionnaire):
        super().__init__(dictionnaire)

        self.écriveur = lexika.outils.Écriveur(self.configuration.informations["latex"]["chemin cible"])

    def obtenir_latex(self, format, langue=None):
        fichier_xml = self.configuration.informations["xml"]["chemin cible"]
        fichier_xsl = self.configuration.informations["latex"]["chemin du gabarit"]

        modèle_document = lxml.etree.parse(fichier_xml)
        transformation = lxml.etree.XSLT(lxml.etree.parse(fichier_xsl))
        nouveau_modèle_document = transformation(modèle_document, profile_run=True)
        texte = []
        limite_caractères_spéciaux = False
        for ligne in str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").splitlines():
            if r"\begin{document}" in ligne:
                limite_caractères_spéciaux = True
            if limite_caractères_spéciaux:
                for caractère in ["$", "^", "_", "#", "~", "&"]:
                    ligne = ligne.replace(caractère, f"\{caractère}")
            texte.append(ligne)
        texte = "\n".join(texte)
        informations = {"titre": self.configuration.informations["général"]["nom"], "auteur": self.configuration.informations["général"]["auteur"]}
        if "fichiers annexes" in self.configuration.informations["latex"]:
            for variable, fichier in self.configuration.informations["latex"]["fichiers annexes"].items():
                if fichier:
                    if os.path.isfile(fichier):
                        with lexika.outils.OuvrirFichier(fichier, 'r') as entrée:
                            contenu = entrée.read()
                    else:
                        contenu = fichier
                    informations.update({variable: contenu})
        source = lexika.outils.Gabarit(texte)
        self.écriveur.écrire_résultat(source.safe_substitute(informations))
        logging.info(_("Génération du fichier Latex terminée."))
