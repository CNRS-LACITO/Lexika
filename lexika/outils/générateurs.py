#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import xml.etree.cElementTree
import lxml.etree

class GénérateurXML:
    def __init__(self, configuration, dictionnaire):
        self.configuration = configuration
        self.dictionnaire = dictionnaire

    def obtenir_xml(self, type):
        if type == "structure":
            arborescence = xml.etree.cElementTree.Element("Dictionnaire")
            self.créer_éléments(self.dictionnaire, arborescence)
            with open("résultat.xml", 'w') as sortie:
                texte = xml.etree.cElementTree.tostring(arborescence, encoding="unicode", method="xml")
                sortie.write(texte)
            print("Génération terminée.")

    def créer_éléments(self, objet, branche):
        if isinstance(objet, lexika.linguistique.EntitéLinguistique):
            sous_branche = xml.etree.cElementTree.SubElement(branche, objet.nom_entité_linguistique)
            for nom, élément in objet.__dict__.items():
                if élément:
                    if nom in ["identifiant"]:
                        sous_branche.attrib.update({"id": élément})
                    elif nom not in ["nom_entité_linguistique", "_parent"]:
                        if isinstance(élément, list):
                            sous_branche = xml.etree.cElementTree.SubElement(sous_branche, nom)
                            for sous_élément in élément:
                                self.créer_éléments(sous_élément, sous_branche)
                        elif isinstance(élément, dict):
                            sous_branche = xml.etree.cElementTree.SubElement(sous_branche, nom)
                            for clef_sous_élément, valeur_sous_élément in élément.items():
                                self.créer_éléments(valeur_sous_élément, sous_branche)
                        else:
                            xml.etree.cElementTree.SubElement(sous_branche, "feat", att=nom, val=élément)


class GénérateurLatex:
    def __init__(self, configuration, dictionnaire):
        self.configuration = configuration
        self.dictionnaire = dictionnaire