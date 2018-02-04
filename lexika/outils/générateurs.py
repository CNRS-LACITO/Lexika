#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.outils
import logging
import lxml.etree
import lxml.html
import os


class GénérateurXML:
    def __init__(self, configuration, racine, dictionnaire):
        self.configuration = configuration
        self.écriveur = lexika.outils.Écriveur(self.configuration.xml["chemin cible"])
        self.format = self.configuration.xml["format"] if "format" in self.configuration.xml else "α"
        self.langue = self.configuration.xml["langue"] if "langue" in self.configuration.xml else "fra"
        lexika.outils.Trieur = lexika.outils.Trieur if not os.path.isfile(self.configuration.général.get("chemin du trieur", "")) else lexika.outils.importer_module_personnalisé("lexika.outils.Trieur", self.configuration.général["chemin du trieur"]).Trieur
        
        self.trieur = lexika.outils.Trieur(self.configuration.général["ordre lexicographique"]) if "ordre lexicographique" in self.configuration.général else None
        self.racine = racine
        self.dictionnaire = dictionnaire

    def obtenir_xml(self):
        self.traduire = lexika.outils.Traducteur().traduire if self.langue == "eng" else lambda expression, domaine=None: expression
        arborescence = lxml.etree.Element(self.convertir_nom(self.traduire(self.racine.nom_classe)))
        for élément in self.racine.descendance:
            self.créer_éléments(élément, arborescence)
        texte_structuré = lxml.etree.tostring(arborescence, encoding="unicode", method="xml", pretty_print=True)
        informations = {"style": self.configuration.xml["XSL"], "arborescence": texte_structuré}
        with lexika.outils.OuvrirFichier("gabarits/XML/dictionnaire.xml", 'r', type="interne") as gabarit:
            source = lexika.outils.Gabarit(gabarit.read())
        self.écriveur.écrire_résultat(source.substitute(informations))
        logging.info(_("Génération du fichier XML terminée"))

    def créer_éléments(self, entité, élément_parent):
        if isinstance(entité, lexika.outils.Entité):
            if self.format == "α":
                nom = self.convertir_nom(self.traduire(entité.nom_classe))
                attributs = {self.convertir_nom(self.traduire(clef)): self.traduire(valeur) for clef, valeur in entité.caractéristiques.items()}
                if entité.spécial and "texte enrichi" in entité.spécial.get("drapeaux", {}):
                    élément_actuel = lxml.etree.XML(f"<{nom}>{entité.valeur}</{nom}>", parser=lxml.etree.XMLParser(recover=True))
                    élément_parent.append(élément_actuel)
                    for attribut, valeur in attributs.items():
                        élément_actuel.set(attribut, valeur)
                else:                    
                    élément_actuel = lxml.etree.SubElement(élément_parent, nom, attrib=attributs)
                    élément_actuel.text = entité.valeur
            if hasattr(entité, "descendance"):
                for enfant in sorted(entité.descendance, key=lambda entrée: self.trieur.trier_éléments(entrée.caractéristiques["identifiant"])) if entité == self.dictionnaire else entité.descendance:
                    self.créer_éléments(enfant, élément_actuel)

    def convertir_nom(self, nom):
        return nom.replace(" ", "_").replace("’", "ʼ")


class GénérateurLatex:
    def __init__(self, configuration, dictionnaire):
        self.configuration = configuration
        self.dictionnaire = dictionnaire

    def obtenir_latex(self, format, langue=None):
        fichier_xml = self.configuration.xml["chemin cible"]
        fichier_xsl = self.configuration.latex["gabarit"]

        modèle_document = lxml.etree.parse(fichier_xml)
        transformation = lxml.etree.XSLT(lxml.etree.parse(fichier_xsl))
        nouveau_modèle_document = transformation(modèle_document, profile_run=True)
        # texte = regex.compile(r"(?<![\w])_(?!{)|(_(?=-))").sub("\_", str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").replace("^", "\\textasciicircum ").replace("$", "\$"))
        # texte = str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").replace("^", "\\textasciicircum ").replace("$", "\$").replace("_", "\_").replace("#", "\#")
        texte = []
        limite_caractères_spéciaux = False
        for line in str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").splitlines():
            if r"\begin{document}" in line:
                limite_caractères_spéciaux = True
            if limite_caractères_spéciaux:
                line = line.replace("$", "\$").replace("_", "\_").replace("#", "\#").replace("^", "\^").replace("~", "∼")
            texte.append(line)
        texte = "\n".join(texte)
        informations = {"titre": self.configuration.général["nom"], "auteur": self.configuration.général["auteur"]}
        if "fichiers annexes" in self.configuration.latex:
            for variable, fichier in self.configuration.latex["fichiers annexes"].items():
                if fichier:
                    if os.path.isfile(fichier):
                        with lexika.outils.OuvrirFichier(fichier, 'r') as entrée:
                            contenu = entrée.read()
                    else:
                        contenu = fichier
                    informations.update({variable: contenu})
        source = lexika.outils.Gabarit(texte)
        with lexika.outils.OuvrirFichier(self.configuration.latex["chemin cible"], 'w') as sortie:
            sortie.write(source.safe_substitute(informations))
        logging.info(_("Génération du fichier Latex terminée."))