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
        self.ordre_lexicographique = self.créer_ordre_lexicographique(self.configuration.ordre_lexicographique) if hasattr(self.configuration, "ordre_lexicographique") else None
        self.trieur = lexika.outils.Trieur(self.ordre_lexicographique) if self.ordre_lexicographique else None
        self.tri = self.configuration.tri if hasattr(self.configuration, "tri") else "normal"
        self.entités_à_trier = self.configuration.format_sortie["entités à trier"] if "entités à trier" in self.configuration.format_sortie else {}
        self.traduire = None

    def obtenir_xml(self, format, langue=None):
        modèle_balise = regex.compile(r"⊣(?P<balise>[\w]+) (?P<attribut>[\w]+)=\"(?P<valeur>[\p{property='Enclosed Alphanumerics'}\w\s\[\]~-]+)\"⊢(?P<texte>[\w\s\[\]~-]+)⊣\/(?P=balise)⊢")
        self.traduire = lexika.outils.Traducteur().traduire if langue == "eng" else lambda expression: expression
        arborescence = lxml.etree.Element(self.traduire("RessourcesLexicales"))
        self.créer_éléments(self.informations_globales, arborescence, modèle_balise, format == "structure totale")
        self.créer_éléments(self.dictionnaire, arborescence, modèle_balise, format == "structure totale")
        texte_structuré = lxml.etree.tostring(arborescence, encoding="unicode", method="xml", pretty_print=True)
        informations = {"style": self.configuration.XML["XSL"], "arborescence": texte_structuré}
        with open("gabarits/XML/dictionnaire.xml", 'r') as gabarit:
            source = string.Template(gabarit.read())
        with open(self.configuration.XML["chemin cible"], 'w') as sortie:
            sortie.write(source.substitute(informations))
        logging.info(_("Génération du fichier XML terminée"))

    def créer_éléments(self, objet, branche_parente, modèle_balise, garder_listes=True):
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
                                sous_branche = lxml.etree.SubElement(branche_actuelle, nom.replace(" ", "_"))
                            else:
                                sous_branche = branche_actuelle
                            if isinstance(élément, list):
                                if nom in self.entités_à_trier and (self.ordre_lexicographique or self.tri):
                                    print(self.entités_à_trier, nom)
                                    for sous_élément in sorted(élément, key=lambda entrée: self.trier_entités(self.trier_éléments(getattr(entrée, self.entités_à_trier[nom])))):
                                        self.créer_éléments(sous_élément, sous_branche, modèle_balise, garder_listes)
                                else:
                                    for sous_élément in élément:
                                        self.créer_éléments(sous_élément, sous_branche, modèle_balise, garder_listes)
                            elif isinstance(élément, dict):
                                for clef_sous_élément, valeur_sous_élément in élément.items():
                                    self.créer_éléments(valeur_sous_élément, sous_branche, modèle_balise, garder_listes)
                        else:
                            sous_élément = lxml.etree.SubElement(branche_actuelle, self.traduire("caractéristique"), attrib={self.traduire("attribut"): self.traduire(nom), self.traduire("valeur"): self.traduire(élément) if nom in ["type", "nombre grammatical"] else élément})
                            self.gérer_balises_xml(sous_élément)
                            self.gérer_intrabalises(sous_élément, modèle_balise)

    def gérer_balises_xml(self, élément):
        if lxml.html.fromstring(élément.attrib[self.traduire("valeur")]).find('.//*') is not None:
            try:
                élément.append(lxml.etree.fromstring("<{}>{}</{}>".format(self.traduire("contenu"), élément.attrib[self.traduire("valeur")], self.traduire("contenu"))))
            except lxml.etree.XMLSyntaxError as exception:
                logging.warning(_("Du XML a été reconnu sans avoir été analysé avec succès ici : « {} » : {}".format(élément.attrib[self.traduire("valeur")], exception)))

    def gérer_intrabalises(self, élément, modèle_balise):
        bilan = modèle_balise.search(élément.attrib[self.traduire("valeur")])
        if bilan:
            texte_épuré = élément.attrib[self.traduire("valeur")].replace("<", "&lt;").replace(">", "&gt;")
            élément.attrib[self.traduire("valeur")] = modèle_balise.sub("\g<texte>", texte_épuré)
            sous_bilan = modèle_balise.match(texte_épuré)
            # print(sous_bilan.groupdict())
            # groupes = sous_bilan.groupdict()
            # groupes["balise"] = "link"
            # groupes["attribut"] = "target"
            # print(groupes)
            # modèle_remplacement = regex.compile(r"(?<=<)(\w+)(?=>)")
            # texte_enrichi = modèle_remplacement.sub(lambda m: groupes.get(m.group(), m.group()), texte_épuré)
            # print("---", texte_enrichi)
            texte_enrichi = modèle_balise.sub("<\g<balise> \g<attribut>=\"\g<valeur>\">\g<texte></\g<balise>>", texte_épuré)
            élément.append(lxml.etree.fromstring("<{}>{}</{}>".format(self.traduire("contenu"), texte_enrichi, self.traduire("contenu"))))

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
        # self.informations_globales = informations_globales
        # self.ordre_lexicographique = {caractère: index for index, caractère in enumerate(self.configuration.ordre_lexicographique)} if hasattr(self.configuration, "ordre_lexicographique") and self.configuration.ordre_lexicographique else None
        # self.tri = self.configuration.tri if hasattr(self.configuration, "tri") else "normal"
        # self.entités_à_trier = self.configuration.format_sortie["entités à trier"] if "entités à trier" in self.configuration.format_sortie else {}
        # self.expression_rationnelle_tri_entités = regex.compile(r"{}".format("|".join(sorted(self.ordre_lexicographique, key=lambda mot: len(mot), reverse=True))), flags=regex.IGNORECASE) if self.ordre_lexicographique else None
        # self.traduire = None

    def obtenir_latex(self, format, langue=None):
        fichier_xml = self.configuration.XML["chemin cible"]
        fichier_xsl = "gabarits/Latex/latex.xsl"

        modèle_document = lxml.etree.parse(fichier_xml)
        transformation = lxml.etree.XSLT(lxml.etree.parse(fichier_xsl))
        nouveau_modèle_document = transformation(modèle_document, profile_run=True)
        texte = str(nouveau_modèle_document).replace("  ", "").replace("\n\n", "").replace("_", "\_").replace("^", "\\textasciicircum ")
        informations = {"titre": self.configuration.dictionnaire["nom"], "auteur": self.configuration.dictionnaire["auteur"], "arborescence": texte}
        with open("gabarits/Latex/dictionnaire.tex", 'r') as gabarit:
            source = string.Template(gabarit.read())
        with open(self.configuration.Latex["chemin cible"], 'w') as sortie:
            sortie.write(source.substitute(informations))
        logging.info(_("Génération du fichier Latex terminée"))
