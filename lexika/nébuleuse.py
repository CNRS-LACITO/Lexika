#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import copy

import regex

from pprint import pprint


class Nébuleuse:
    """
    Modèle de créateur pour des dictionnaires simples n'ayant que des entrées (pas de sous-entrées) et des sens (sans sous-sens).
    """
    def __init__(self, configuration):
        self.configuration = configuration
        self.constantes = {"doublon": "‽", "groupe": "Ⓖ", "entrée": "Ⓔ", "homonyme": "Ⓗ", "sens": "Ⓢ", "définition": "Ⓓ", "exemple": "ⓔ"}
        self.langues = []

        self.dictionnaire = None


class NébuleuseObscure(Nébuleuse):
    """Cet objet permet de créer des dictionnaires dynamiquement."""
    def __init__(self, configuration):
        super(NébuleuseObscure, self).__init__(configuration)

        self.modèle_ligne = regex.compile(self.configuration.modèle_ligne)
        self.balises = self.configuration.balises

        self.hiérarchie = {}
        self.historique = []

    def initialiser(self):
        informations_dictionnaire = {"nom": "dictionnaire", "attributs": self.configuration.dictionnaire, "paramètres": {}, "structure": {}}
        self.dictionnaire = self.créer_entité_linguistique(informations_dictionnaire, None)
        for langue, informations_langue in self.configuration.langues.items():
            self.langues.append(langue)
            informations_langue = {"nom": "langue", "attributs": informations_langue, "paramètres": {}, "structure": {}}
            informations_parent = {"nom": "dictionnaire", "attribut": "langues"}
            self.créer_entité_linguistique(informations_langue, informations_parent)

    def analyser_données(self, ligne_données):
        bilan = self.modèle_ligne.match(ligne_données["ligne"])
        if bilan:
            balise = bilan.group("balise")
            métabalise = bilan.group("métabalise") if "métabalise" in bilan.groupdict() else None
            données = bilan.group("données")
            métadonnées = bilan.group("métadonnées")
            if balise in self.balises:
                if not données:
                    pass
                #     print(_("La balise de type « {} » (ligne {}) ne contient aucune valeur.").format(balise, ligne_données["index"]))
                else:
                    informations_générales = copy.deepcopy(self.balises[balise])
                    if métabalise:
                        profondeur = métabalise.count(".")
                        ordinal = métabalise.replace(".", '')
                        if ordinal:
                            informations = self.balises[informations_générales["entité"]["structure"]["métabalise"]]
                            nom_entité_auxiliaire = informations["entité"]["nom"]
                            informations["entité"].update({"valeurs": [ordinal], "métainformations": métadonnées})
                            if not nom_entité_auxiliaire in self.hiérarchie or (nom_entité_auxiliaire in self.hiérarchie and getattr(self.hiérarchie[nom_entité_auxiliaire][-1], informations["entité"]["structure"]["identifiant"]["nom"]) != ordinal):
                                self.aiguiller_entité_linguistique(informations)
                    if métadonnées:
                        métadonnées = {"balise": métabalise, "données": métadonnées}
                    if "expression" in informations_générales:
                        modèle_informations = regex.compile(informations_générales["expression"])
                        sous_bilan = modèle_informations.match(données)
                        if sous_bilan:
                            composants = informations_générales["composants"]
                            for entité, informations in composants.items():
                                if sous_bilan.group(entité):
                                    informations["entité"].update({"valeurs": [sous_bilan.group(entité)], "métainformations": métadonnées})
                                    self.aiguiller_entité_linguistique(informations)
                        #         else:
                        #             print(_("La sous-entité de type « {} » ne contient aucune valeur.").format(entité))
                        # else:
                        #     print(_("La ligne « {} » (de valeur « {} ») ne correspond pas à l'expression régulière.".format(ligne_données["ligne"], données)))
                    else:
                        résultat = self.balises[balise]
                        informations_générales["entité"].update({"valeurs": [données], "métainformations": métadonnées})
                        self.aiguiller_entité_linguistique(informations_générales)
            # else:
            #         print(_("Balise « {} » inconnue à la ligne {}, donc ignorée.").format(balise, donnée["index"]))
        # else:
        #     print(_("Attention, la ligne '{ligne}' ({index}) n'a pas été validée par l'expression régulière.").format(**donnée))

    def aiguiller_entité_linguistique(self, informations_générales):
        # print("**", informations_générales)
        informations = copy.deepcopy(informations_générales)
        entité = informations["entité"]
        if "expression" in informations:
            modèle_informations = regex.compile(informations["expression"])
            bilan = modèle_informations.match(entité["valeurs"][0])
            valeurs = []
            if bilan:
                for attribut in informations["entité"]["attributs"]:
                    valeurs.append(bilan.group(attribut))

            attributs_entité = {"attributs": {attribut: valeur for attribut, valeur in zip(entité["attributs"], valeurs) if valeur}}
        else:
            attributs_entité = {"attributs": {attribut: valeur for attribut, valeur in zip(entité["attributs"], entité["valeurs"]) if valeur}}
        entité.pop("attributs")
        entité.pop("valeurs")
        entité.update(attributs_entité)
        if informations["parents"] and len(informations["parents"]) > 1:
            parent = self.rechercher_parent_adéquat(informations["parents"])
        else:
            parent = informations["parents"][0] if informations["parents"] else None
        # print(_("Entité « {nom} » en cours, avec les attributs suivants : « {attributs} » (avec les paramètres suivant : « {paramètres} »).").format(**entité))
        # if parent:
        #     print(_("Son parent est « {nom} » et l'entité se place dans l'attribut « {attribut} ».").format(**parent))
        # else:
        #     print(_("Elle est indépendante."))
        self.créer_entité_linguistique(entité, parent)

    def rechercher_parent_adéquat(self, informations_parents_potentiels):
        noms_parent_potentiel = [parent["nom"] for parent in informations_parents_potentiels]
        if len([parent for parent in noms_parent_potentiel if parent in self.historique]) > 1:
            résultat = {}
            for nom_parent_potentiel in noms_parent_potentiel:
                résultat[nom_parent_potentiel] = self.historique.index(nom_parent_potentiel)
            parents_adéquats = sorted([(antériorité, parent) for parent, antériorité in résultat.items()])[0]
            parent_adéquat = [informations for informations in informations_parents_potentiels if informations["nom"] == parents_adéquats[1]][0]
        else:
            parent_adéquat = [informations for informations in informations_parents_potentiels if informations["nom"] in self.historique][0]
        return parent_adéquat

    def mettre_à_jour_hiérarchie(self, entité):
        if entité.nom_entité_linguistique not in self.hiérarchie:
            self.hiérarchie[entité.nom_entité_linguistique] = []
        self.hiérarchie[entité.nom_entité_linguistique].append(entité)
        self.historique.insert(0, entité.nom_entité_linguistique)

    def créer_entité_linguistique(self, informations_entité, informations_parent):
        nom_entité_linguistique = informations_entité["nom"]
        nom_classe = nom_entité_linguistique[0].upper() + nom_entité_linguistique[1:]
        # Informations de type entité, donc création de cette dernière.
        if informations_parent or nom_entité_linguistique == "dictionnaire":
            Entité = type(nom_classe, (lexika.linguistique.EntitéLinguistique,), {})
            entité = Entité()
            entité.nom_entité_linguistique = nom_entité_linguistique
            self.mettre_à_jour_hiérarchie(entité)
            # Liaison de l'entité avec la bonne entité parente, création si besoin est.
            if informations_parent:
                nom_parent = informations_parent["nom"]
                attribut_parent = informations_parent["attribut"]
                if nom_parent in self.hiérarchie:
                    parent = self.hiérarchie[nom_parent][-1]
                    if not hasattr(parent, attribut_parent):
                        setattr(parent, attribut_parent, [])
                    attribut_parent = getattr(parent, attribut_parent)
                    attribut_parent.append(entité)
                    setattr(entité, "_parent", parent)
            else:
                setattr(entité, "_parent", None)
        # Informations de type attribut d'entité.
        else:
            entité = self.hiérarchie[nom_entité_linguistique][-1]
        self.mettre_à_jour_entité_linguistique(entité, informations_entité, informations_parent)
        self.mettre_à_jour_identifiant(entité, informations_entité, informations_parent)
        return entité

    def mettre_à_jour_entité_linguistique(self, entité, informations_entité, informations_parent):
        attributs = informations_entité["attributs"]
        if informations_entité["paramètres"]:
            attributs.update({attribut: valeur for attribut, valeur in informations_entité["paramètres"].items()})
            if "langue" in informations_entité["paramètres"] and informations_entité["paramètres"]["langue"] not in self.langues:
                print(_("Langue « {} » non présente dans les paramètres de configuration.").format(informations_entité["paramètres"]["langue"]))
        for attribut, valeur in attributs.items():
            setattr(entité, attribut, str(valeur))
        return entité

    def mettre_à_jour_identifiant(self, entité, informations_entité, informations_parent):
        if "identifiant" in informations_entité["structure"]:
            if informations_entité["structure"]["identifiant"]["nom"]:
                identifiant = getattr(entité, informations_entité["structure"]["identifiant"]["nom"])
            else:
                identifiant = str(len(getattr(entité._parent, informations_parent["attribut"])))
            if informations_entité["structure"]["identifiant"]["type"] == "primaire":
                identifiant = "{}{}".format(self.constantes[informations_entité["nom"]], identifiant)
            elif informations_entité["structure"]["identifiant"]["type"] == "secondaire":
                identifiant = "{}{}{}".format(entité.identifiant, self.constantes[informations_entité["structure"]["identifiant"]["nom"]], identifiant)
            identifiant = "{}{}".format(entité._parent.identifiant if hasattr(entité, "_parent") and hasattr(entité._parent, "identifiant") else '', identifiant)
            setattr(entité, "identifiant", identifiant)
        return entité


class NébuleuseDiffuse(Nébuleuse):
    """Cet objet permet de créer des lexiques inverses dynamiquement."""
    def __init__(self, configuration):
        super(NébuleuseDiffuse, self).__init__(configuration)

        self.hiérarchie = {}
        self.historique = []

    def créer_entité_linguistique(self):
        print