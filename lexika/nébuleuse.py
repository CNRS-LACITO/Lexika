#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import regex

from pprint import pprint

class Nébuleuse:
    """
    Modèle de créateur pour des dictionnaires simples n'ayant que des entrées (pas de sous-entrées) et des sens (sans sous-sens).
    """
    def __init__(self, configuration):
        self.configuration = configuration
        self.entités_linguistiques = lexika.configuration.entités_linguistiques
        self.constantes = {"doublon": "‽", "groupe": "Ⓖ", "entrée": "Ⓔ", "homonyme": "Ⓗ", "sens": "Ⓢ", "définition": "Ⓓ", "exemple": "ⓔ"}
        self.langues = []
        self.modèle_entrée = None

        self.dictionnaire = None

    def initialiser(self):
        self.modèle_entrée = regex.compile(self.configuration.modèle_entrée)
        self.langues = [lexika.linguistique.Langue(**informations_langue) for code_langue, informations_langue in self.configuration.langues.items()]
        self.dictionnaire = lexika.linguistique.Dictionnaire(self.configuration.identifiant, self.configuration.nom, self.configuration.catégorie, self.langues)

    def aiguiller_entité_linguistique(self, informations):
        entité = informations["entité"]
        if entité["nom"] in self.entités_linguistiques:
            print("Entité '{nom}' en cours, avec pour attribut '{attribut}' et pour valeur '{information}' (avec les paramètres suivant : '{paramètres}').".format(**entité))
            fonction = self.entités_linguistiques[entité["nom"]]
            fonction(self, **{clef: valeur for clef, valeur in entité.items() if clef not in ["nom"]})
        else:
            print("Attention, l'entité linguistique '{}' n'est pas reconnue.".format(entité))


class NébuleuseObscure(Nébuleuse):
    def __init__(self, configuration):
        super(NébuleuseObscure, self).__init__(configuration)

        self.hiérarchie = {}
        self.historique = []

    def aiguiller_entité_linguistique(self, informations):
        entité = informations["entité"]
        attributs_entité = {"attributs": {attribut: valeur for attribut, valeur in zip(entité["attributs"], entité["valeurs"])}}
        entité.pop("attributs")
        entité.pop("valeurs")
        entité.update(attributs_entité)
        if informations["parent"] and len(informations["parent"]) > 1:
            parent = self.rechercher_parent_adéquat(informations["parent"])
        else:
            parent = informations["parent"][0] if informations["parent"] else None
        # print("Entité '{nom}' en cours, avec les attributs suivants : '{attributs}' (avec les paramètres suivant : '{paramètres}').".format(**entité))
        # if parent:
        #     print("Son parent est '{nom}' et l'entité se place dans l'attribut '{attribut}'".format(**parent))
        # else:
        #     print("Elle est indépendante.")
        self.créer_entité_linguistique(entité, parent)

    def initialiser(self):
        informations_dictionnaire = {"nom": "dictionnaire", "attributs": self.configuration.dictionnaire, "paramètres": {}, "structure": {}}
        self.dictionnaire = self.créer_entité_linguistique(informations_dictionnaire, None)
        for langue, informations_langue in self.configuration.langues.items():
            self.langues.append(langue)
            informations_langue = {"nom": "langue", "attributs": informations_langue, "paramètres": {}, "structure": {}}
            informations_parent = {"nom": "dictionnaire", "attribut": "langues"}
            self.créer_entité_linguistique(informations_langue, informations_parent)

    def rechercher_parent_adéquat(self, informations_parent_potentiel):
        noms_parent_potentiel = [parent["nom"] for parent in informations_parent_potentiel]
        résultat = {}
        for nom_parent_potentiel in noms_parent_potentiel:
            résultat[nom_parent_potentiel] = self.historique.index(nom_parent_potentiel)
        parent_adéquat = sorted([(antériorité, parent) for parent, antériorité in résultat.items()])[0]
        return [informations for informations in informations_parent_potentiel if informations["nom"] == parent_adéquat[1]][0]

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
                print("Langue '{}' non présente dans les paramètres de configuration.".format(informations_entité["paramètres"]["langue"]))
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
