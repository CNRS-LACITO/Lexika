#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import lexika.outils
import logging
import lxml.etree
import lxml.html
import os
import regex
import string


class GénérateurXML:
    def __init__(self, configuration, dictionnaire, informations_globales=None):
        self.configuration = configuration
        self.dictionnaire = dictionnaire
        self.informations_globales = informations_globales
        self.ordre_lexicographique = self.créer_ordre_lexicographique(self.configuration.ordre_lexicographique) if hasattr(self.configuration, "ordre_lexicographique") else None
        self.trieur = lexika.outils.Trieur(self.ordre_lexicographique) if self.ordre_lexicographique else None
        self.tri = self.configuration.tri if hasattr(self.configuration, "tri") else "normal"
        self.entités_à_trier = self.configuration.format_sortie["entités à trier"] if "entités à trier" in self.configuration.format_sortie else {}
        self.traduire = None
        self.modèle_balise_xml = regex.compile(r"<(?P<balise>[\w]+)(?P<attributs>[\w\s\"=]*)>(?P<texte>.*)<\/(?P=balise)>")
        self.modèle_balise_lien = regex.compile(r"⊣(?P<balise>[\w]+) (?P<attribut>[\w]+)=\"(?P<valeur>.+?)\"⊢(?P<texte>.+?)⊣\/(?P=balise)⊢")
        self.modèle_style = regex.compile(self.configuration.modèle_style) if self.configuration.modèle_style else None

    def obtenir_xml(self, format, langue=None):
        self.traduire = lexika.outils.Traducteur().traduire if langue == "eng" else lambda expression, domaine=None: expression
        arborescence = lxml.etree.Element(self.traduire("RessourcesLexicales"))
        self.créer_éléments(self.informations_globales, arborescence, format == "structure totale")
        self.créer_éléments(self.dictionnaire, arborescence, format == "structure totale")
        texte_structuré = lxml.etree.tostring(arborescence, encoding="unicode", method="xml", pretty_print=True)
        informations = {"style": self.configuration.XML["XSL"], "arborescence": texte_structuré}
        with lexika.outils.OuvrirFichier("gabarits/XML/dictionnaire.xml", 'r', type="interne") as gabarit:
            source = lexika.outils.Gabarit(gabarit.read())
        with lexika.outils.OuvrirFichier(self.configuration.XML["chemin cible"], 'w') as sortie:
            sortie.write(source.substitute(informations))             
        logging.info(_("Génération du fichier XML terminée"))

    def créer_éléments(self, objet, branche_parente, garder_listes=True):
        if isinstance(objet, lexika.linguistique.EntitéLinguistique):
            branche_actuelle = lxml.etree.SubElement(branche_parente, self.traduire(objet.__class__.__name__).replace(" ", "_").replace("'", ""))
            for nom, élément in objet.__dict__.items():
                if élément:
                    if nom in ["identifiant"]:
                        branche_actuelle.attrib.update({"id": élément})
                    elif nom in ["lien", "non_lien"]:
                        sous_élément = lxml.etree.SubElement(branche_actuelle, self.traduire(nom), attrib={self.traduire("cible"): élément})
                        sous_élément.text = objet.cible
                    elif nom not in ["nom_entité_linguistique", "_parent", "_attribut_parent"]:
                        if isinstance(élément, (list, dict)):
                            if garder_listes:
                                sous_branche = lxml.etree.SubElement(branche_actuelle, nom.replace(" ", "_").replace("'", "ʼ"))
                            else:
                                sous_branche = branche_actuelle
                            if isinstance(élément, list):
                                if nom in self.entités_à_trier and (self.ordre_lexicographique or self.tri):
                                    for sous_élément in sorted(élément, key=lambda entrée: self.trier_entités(self.trier_éléments(getattr(entrée, self.entités_à_trier[nom])))):
                                        self.créer_éléments(sous_élément, sous_branche, garder_listes)
                                else:
                                    for sous_élément in élément:
                                        self.créer_éléments(sous_élément, sous_branche, garder_listes)
                            elif isinstance(élément, dict):
                                for clef_sous_élément, valeur_sous_élément in élément.items():
                                    self.créer_éléments(valeur_sous_élément, sous_branche, garder_listes)
                        else:
                            sous_élément = lxml.etree.SubElement(branche_actuelle, self.traduire("caractéristique"), attrib={self.traduire("attribut"): self.traduire(nom), self.traduire("valeur"): self.traduire(élément, nom)})
                            if self.modèle_style:
                                self.gérer_styles(sous_élément)
                            self.gérer_balises(sous_élément)

    def gérer_styles(self, élément):
        texte = élément.attrib[self.traduire("valeur")]
        bilan = self.modèle_style.search(texte)
        if bilan:
            élément.attrib[self.traduire("valeur")] = self.modèle_style.sub("<style type=\"\g<style>\">\g<texte></style>", texte)

    def gérer_balises(self, élément):
        texte = élément.attrib[self.traduire("valeur")]
        if self.modèle_balise_xml.search(texte) and lxml.html.fromstring(élément.attrib[self.traduire("valeur")]).find('.//*') is not None or self.modèle_balise_lien.search(texte):
            bilan = self.modèle_balise_lien.search(texte)
            if bilan:
                texte = self.modèle_balise_lien.sub("<\g<balise> \g<attribut>=\"\g<valeur>\">\g<texte></\g<balise>>", texte)
            try:
                élément.append(lxml.etree.fromstring("<{0}>{1}</{0}>".format(self.traduire("contenu"), texte.replace("&", "&amp;"))))
            except lxml.etree.XMLSyntaxError as exception:
                logging.warning(_("Du XML a été reconnu sans avoir été analysé avec succès ici : « {} » : {}".format(élément.attrib[self.traduire("valeur")], exception)))
            élément.attrib[self.traduire("valeur")] = self.modèle_balise_xml.sub("\g<texte>", texte)

    def trier_entités(self, expression):
        if self.trieur:
            résultat = self.trieur.trier_entités(expression)
            logging.info("Le tri des entités a pris en compte l'expression « {} » avec l'ordre des syllabes suivant : « {} ».".format(expression, résultat))
        else:
            résultat = expression
        return résultat

    def trier_éléments(self, expression):
        if self.configuration.tri == "inverse":
            résultat = [caractère.lower().replace("-", '') for caractère in reversed(expression)]
        else:
            résultat = expression
        return résultat

    def créer_ordre_lexicographique(self, ordre_lexicographique):
        # {caractère: index for index, caractère in enumerate(self.configuration.ordre_lexicographique)} if hasattr(self.configuration, "ordre_lexicographique") and self.configuration.ordre_lexicographique else None
        valeurs = {}
        for index, caractère in enumerate(ordre_lexicographique):
            if isinstance(caractère, str):
                valeurs[caractère] = index
            else:
                for sous_caractère in caractère:
                    valeurs[sous_caractère] = index
        return valeurs

class GénérateurLatex:
    def __init__(self, configuration, dictionnaire, informations_globales=None):
        self.configuration = configuration
        self.dictionnaire = dictionnaire

    def obtenir_latex(self, format, langue=None):
        fichier_xml = self.configuration.XML["chemin cible"]
        fichier_xsl = self.configuration.Latex["gabarit"]

        modèle_document = lxml.etree.parse(fichier_xml)
        transformation = lxml.etree.XSLT(lxml.etree.parse(fichier_xsl))
        nouveau_modèle_document = transformation(modèle_document, profile_run=True)
        # texte = regex.compile(r"(?<![\w])_(?!{)|(_(?=-))").sub("\_", str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").replace("^", "\\textasciicircum ").replace("$", "\$"))
        # texte = str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").replace("^", "\\textasciicircum ").replace("$", "\$").replace("_", "\_").replace("#", "\#")
        texte = []
        for line in str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").splitlines():
            if not(line.startswith("\\newenvironment{") or line.startswith("\\newcommand{")):
                line = line.replace("$", "\$").replace("_", "\_").replace("#", "\#").replace("^", "\^").replace("~", "∼")
            texte.append(line)
        texte = "\n".join(texte)
        informations = {"titre": self.configuration.dictionnaire["nom"], "auteur": self.configuration.dictionnaire["auteur"]}
        if "fichiers annexes" in self.configuration.Latex:
            for variable, fichier in self.configuration.Latex["fichiers annexes"].items():
                if fichier:
                    if os.path.isfile(fichier):
                        with lexika.outils.OuvrirFichier(fichier, 'r') as entrée:
                            contenu = entrée.read()
                    else:
                        contenu = fichier
                    informations.update({variable: contenu})
        source = lexika.outils.Gabarit(texte)
        with lexika.outils.OuvrirFichier(self.configuration.Latex["chemin cible"], 'w') as sortie:
            sortie.write(source.safe_substitute(informations))
        logging.info(_("Génération du fichier Latex terminée."))
