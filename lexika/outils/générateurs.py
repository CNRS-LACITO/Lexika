#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import lexika.outils
import logging
import lxml.etree
import lxml.html
import regex
import string


class GénérateurXML:
    def __init__(self, configuration, dictionnaire, informations_globales=None):
        self.configuration = configuration
        self.dictionnaire = dictionnaire
        self.informations_globales = informations_globales
        self.ordre_lexicographique = {caractère: index for index, caractère in enumerate(self.configuration.ordre_lexicographique)} if hasattr(self.configuration, "ordre_lexicographique") and self.configuration.ordre_lexicographique else None
        self.tri = self.configuration.tri if hasattr(self.configuration, "tri") else None
        self.traduire = None

    def obtenir_xml(self, format, langue=None):
        modèle_balise = regex.compile(r"⊣(?P<balise>[\w]+) (?P<attribut>[\w]+)=\"(?P<valeur>[\p{property='Enclosed Alphanumerics'}\w\s\[\]~-]+)\"⊢(?P<texte>[\w\s\[\]~-]+)⊣\/(?P=balise)⊢")
        if langue == "eng":
            self.traduire = lexika.outils.Traducteur().traduire
        else:
            self.traduire = lambda expression: expression
        arborescence = lxml.etree.Element(self.traduire("RessourcesLexicales"))
        if format == "structure totale":
            self.créer_éléments(self.informations_globales, arborescence, modèle_balise)
            self.créer_éléments(self.dictionnaire, arborescence, modèle_balise)
        elif format == "structure sans listes":
            self.créer_éléments(self.informations_globales, arborescence, modèle_balise, False)
            self.créer_éléments(self.dictionnaire, arborescence, modèle_balise, False)
        texte_structuré = lxml.etree.tostring(arborescence, encoding="unicode", method="xml", pretty_print=True)
        informations = {"style": self.configuration.XML["XSL"], "arborescence": texte_structuré}
        with open("gabarits/XML/dictionnaire.xml", 'r') as gabarit:
            source = string.Template(gabarit.read())
        with open("résultat.xml", 'w') as sortie:
            sortie.write(source.substitute(informations))
        logging.info(_("Génération du fichier XML terminée"))

    def créer_éléments(self, objet, branche_parente, modèle_balise, garder_listes=True):
        if isinstance(objet, lexika.linguistique.EntitéLinguistique):
            branche_actuelle = lxml.etree.SubElement(branche_parente, self.traduire(objet.__class__.__name__).replace(" ", "_"))
            for nom, élément in objet.__dict__.items():
                if élément:
                    if nom in ["identifiant"]:
                        branche_actuelle.attrib.update({"id": élément})
                    elif nom in ["lien", "non_lien"]:
                        sous_élément = lxml.etree.SubElement(branche_actuelle, self.traduire(nom), attrib={self.traduire("cible"): élément})
                        sous_élément.text = objet.cible
                    elif nom not in ["nom_entité_linguistique", "_parent"]:
                        if isinstance(élément, (list, dict)):
                            if garder_listes:
                                sous_branche = lxml.etree.SubElement(branche_actuelle, nom.replace(" ", "_"))
                            else:
                                sous_branche = branche_actuelle
                            if isinstance(élément, list):
                                if nom in ["entrées"] and (self.ordre_lexicographique or self.tri):
                                    for sous_élément in sorted(élément, key= lambda entrée: self.trier_éléments(entrée.vedette)):
                                        self.créer_éléments(sous_élément, sous_branche, modèle_balise, garder_listes)
                                else:
                                    for sous_élément in élément:
                                        self.créer_éléments(sous_élément, sous_branche, modèle_balise, garder_listes)
                            elif isinstance(élément, dict):
                                for clef_sous_élément, valeur_sous_élément in élément.items():
                                    self.créer_éléments(valeur_sous_élément, sous_branche, modèle_balise, garder_listes)
                        else:
                            sous_élément = lxml.etree.SubElement(branche_actuelle, self.traduire("caractéristique"), attrib={self.traduire("attribut"): self.traduire(nom), self.traduire("valeur"): self.traduire(élément) if nom in ["type"] else élément})
                            self.gérer_balises_xml(sous_élément)
                            self.gérer_intrabalises(sous_élément, modèle_balise)

    def gérer_balises_xml(self, élément):
        if lxml.html.fromstring(élément.attrib[self.traduire("valeur")]).find('.//*') is not None:
            try:
                élément.append(lxml.etree.fromstring("<contenu>{}</contenu>".format(élément.attrib[self.traduire("valeur")])))
            except lxml.etree.XMLSyntaxError as exception:
                logging.error(_("Du XML a été reconnu sans avoir été analysé avec succès ici : « {} » : {}".format(élément.attrib[self.traduire("valeur")], exception)))

    def gérer_intrabalises(self, élément, modèle_balise):
        bilan = modèle_balise.search(élément.attrib[self.traduire("valeur")])
        if bilan:
            texte_épuré = élément.attrib[self.traduire("valeur")].replace("<", "&lt;").replace(">", "&gt;")
            texte_enrichi = modèle_balise.sub("<\g<balise> \g<attribut>=\"\g<valeur>\">\g<texte></lien>", texte_épuré)
            élément.append(lxml.etree.fromstring("<contenu>{}</contenu>".format(texte_enrichi)))

    def trier_entités(self, entité):
        pass

    def trier_éléments(self, mot):
        if self.configuration.tri == "inverse":
            résultat = [caractère.lower().replace("-", '') for caractère in reversed(mot)]
        else:
            résultat = mot
        if self.ordre_lexicographique:
            résultat = [self.ordre_lexicographique[caractère.lower()] for caractère in résultat if caractère.lower() in self.ordre_lexicographique]
        return résultat


class GénérateurLatex:
    def __init__(self, configuration, dictionnaire):
        self.configuration = configuration
        self.dictionnaire = dictionnaire