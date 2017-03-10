#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import copy
import logging
import regex

from pprint import pprint


class Nébuleuse:
    """
    Modèle de créateur pour des dictionnaires simples n'ayant que des entrées (pas de sous-entrées) et des sens (sans sous-sens).
    """
    def __init__(self, configuration):
        self.configuration = configuration
        self.constantes = self.configuration.constantes if self.configuration.constantes else {"doublon": "‽", "groupe": "Ⓖ", "entrée": "Ⓔ", "sous-entrée": "ⓔ", "homonyme": "Ⓗ", "sens": "Ⓢ", "définition": "Ⓓ", "exemple": "⒠", "tableau": "Ⓣ"}
        self.langues = []
        self.statuts_langues = {}
        self.informations_globales = None
        self.dictionnaire = None


class NébuleuseDʼOrion(Nébuleuse):
    """Cet objet permet de créer des dictionnaires dynamiquement."""
    def __init__(self, configuration):
        """
        :param configuration:
        :memb hiérarchie: Dictionnaire de tous les types d'entités du dictionnaire, permet de retouver le dernière parent d'un type donné.
        :memb historique: Liste ordonnée par ordre d'ancienneté des entités du dictionnaire, permet de retouver quel parent est le plus proche.
        """
        super(NébuleuseDʼOrion, self).__init__(configuration)

        self.modèle_ligne = regex.compile(self.configuration.modèle_ligne)
        self.balises = self.configuration.balises
        self.entités = self.configuration.entités
        self.modèle_renvoi = self.configuration.modèle_renvoi
        self.entités_à_extraire = self.configuration.entités_à_extraire
        self.entités_à_lier = self.configuration.entités_à_lier

        self.identifiants = {}
        self.hiérarchie = {}
        self.historique = []

    def initialiser(self):
        """
        Initialise la configuration générale et les objets nécessaires à la création du dictionnaire.
        :return:
        """
        informations_globales = {"nom": "informations globales", "attributs": self.configuration.dictionnaire, "structure": {}}
        informations_globales.update({"voie de création": "Lexika"})
        self.informations_globales = self.créer_entité_linguistique(informations_entité=informations_globales, informations_parent=None)
        informations_dictionnaire = {"nom": "dictionnaire", "attributs": {}, "structure": {}}
        self.dictionnaire = self.créer_entité_linguistique(informations_entité=informations_dictionnaire, informations_parent=None)
        for langue, informations_langue in self.configuration.langues.items():
            self.langues.append(langue)
            informations_langue = {"nom": "langue", "attributs": informations_langue, "structure": {}}
            informations_parent = {"nom": "informations globales", "attribut": "langues"}
            self.créer_entité_linguistique(informations_entité=informations_langue, informations_parent=informations_parent)

    def analyser_données(self, ligne_données):
        """
        Analyse les données (ligne par ligne) afin de savoir comment les traiter selon la configuration spécifique. À ce niveau, les termes de balise et de données sont utilisés.
        :param ligne_données:
        :return:
        """
        logging.info(_("Ligne {index} en cours : « {ligne} »").format(**ligne_données))
        bilan = self.modèle_ligne.match(ligne_données["ligne"])
        if bilan:
            balise = bilan.group("balise")
            données = bilan.group("données")
            métadonnées = bilan.group("métadonnées") if "métadonnées" in bilan.groupdict() else None
            if balise in self.balises:
                informations_balise = self.balises[balise]
                if données:
                    if informations_balise["entité"] in self.entités:
                        proentité = lexika.linguistique.ProentitéLinguistique(self.entités[informations_balise["entité"]])
                        proentité.ajouter_informations({"attributs": informations_balise["paramètres"]})
                        # if "expression" in informations_générales: # à revoir
                        #     modèle_informations = regex.compile(informations_générales["expression"])
                        #     sous_bilan = modèle_informations.match(données)
                        #     if sous_bilan:
                        #         composants = informations_générales["composants"]
                        #         for entité, informations in composants.items():
                        #             if sous_bilan.group(entité):
                        #                 informations["entité"].update({"valeurs": [sous_bilan.group(entité)], "métainformations": métadonnées})
                        #                 self.préparer_entités_linguistiques(informations)
                        #             else:
                        #                 logging.warning(_("La sous-entité de type « {} » ne contient aucune valeur.").format(entité))
                        #     else:
                        #         logging.warning(_("La ligne « {} » (de valeur « {} ») ne correspond pas à l'expression régulière.".format(ligne_données["ligne"], données)))
                        # else:
                        est_nouveau_bloc = informations_balise["tête"] if "tête" in informations_balise else None
                        proentité.ajouter_informations({"données": données, "métadonnées": métadonnées})
                        self.aiguiller_entités_linguistiques(proentité, est_nouveau_bloc)
                    else:
                        logging.error(_("L'entité de type « {} » n'est pas configurée.").format(informations_balise["entité"]))
                else:
                    logging.info(_("La balise de type « {} » (ligne {}) ne contient aucune valeur.").format(balise, ligne_données["index"]))
            else:
                    logging.info(_("Balise « {} » inconnue à la ligne {}, donc ignorée.").format(balise, ligne_données["index"]))
        else:
            logging.warning(_("Attention, la ligne « {ligne} »  ({index}) n'a pas été validée par l'expression régulière.").format(**ligne_données))

    def aiguiller_entités_linguistiques(self, proentité, nouveau_bloc=False):
        """
        Prépare les différentes entités linguistiques avec les informations, avec la recherche des entités parentes et des entités d'appartenance. À ce niveau, les termes d'entités et d'informations (données traitées) sont utilisés.
        :param informations_générales:
        :return:
        """
        if nouveau_bloc == "primaire":
            self.historique = []
            self.hiérarchie = {"dictionnaire": self.hiérarchie["dictionnaire"]}
        elif nouveau_bloc == "secondaire":
            self.historique = []

        proentité.rechercher_entités_adéquates(self.historique, self.hiérarchie)

        # Appels récursifs pour créer les entités parentes manquantes s'il y a normalement une entité parente, à l'aide du dernier parent par défaut.
        if not proentité.entité_parente and proentité.entité_parente is not None:
            parent_par_défaut = [parent for parent in proentité.informations_entités_parentes_potentielles if "entité" in parent][0]
            if "entité" in proentité.informations_entités_parentes_potentielles[0]:
                del proentité.informations_entités_parentes_potentielles[0]
            logging.warning(_("Le parent adéquat n'a pas été trouvé et un parent par défaut « {} » sera créé.".format(parent_par_défaut["entité"])))
            proentité_auxiliaire = lexika.linguistique.ProentitéLinguistique(self.entités[parent_par_défaut["entité"]])
            attributs = parent_par_défaut["attributs"]
            if "informations" in parent_par_défaut:
                attributs.update({clef: proentité.entité_propre["attributs"][valeur] for clef, valeur in parent_par_défaut["informations"].items()})
            proentité_auxiliaire.ajouter_informations({"attributs": attributs})
            self.aiguiller_entités_linguistiques(proentité_auxiliaire)
            proentité.rechercher_entité_parente(self.historique, self.hiérarchie)
        self.créer_entité_linguistique(proentité=proentité)

    def créer_entité_linguistique(self, informations_entité=None, informations_parent=None, proentité=None):
        """
        Création d'une entité linguistique. À ce niveau, les termes d'entités et d'informations (données traitées) sont utilisés.
        :param informations_entité:
        :param informations_parent:
        :return:
        """
        if proentité:
            informations_entité = proentité.entité_propre
            informations_parent = proentité.entité_parente
        nom_entité_linguistique = informations_entité["nom"]
        # Informations de type entité, donc création de cette dernière.
        if informations_parent or nom_entité_linguistique.lower() in ["dictionnaire", "informations globales"]:
            entité = self.créer_objet(nom_entité_linguistique)
            # Liaison de l'entité avec la bonne entité parente, création si besoin est.
            if informations_parent:
                nom_parent = informations_parent["nom"]
                nom_attribut_parent = informations_parent["attribut"]
                if nom_parent in self.hiérarchie:
                    parent = self.hiérarchie[nom_parent][-1]
                    if not hasattr(parent, nom_attribut_parent):
                        setattr(parent, nom_attribut_parent, [])
                    attribut_parent = getattr(parent, nom_attribut_parent)
                    attribut_parent.append(entité)
                    setattr(entité, "_parent", parent)
                    setattr(entité, "_attribut_parent", nom_attribut_parent)
                else:
                    logging.error(_("L'entité parente « {} » de l'entité « {} » (informations : « {} ») n'a pas été trouvée.").format(nom_parent, entité.nom_entité_linguistique, informations_entité["attributs"]))
                    raise Exception
            else:
                setattr(entité, "_parent", None)
            self.mettre_à_jour_hiérarchie(entité)
        # Informations de type attribut d'entité.
        else:
            if nom_entité_linguistique in self.hiérarchie:
                entité = self.hiérarchie[nom_entité_linguistique][-1]
            else:
                logging.error(_("L'entité « {} » à mettre à jour n'existe pas.".format(nom_entité_linguistique)))
                return
        self.mettre_à_jour_entité_linguistique(entité, informations_entité, informations_parent, proentité)
        self.mettre_à_jour_identifiant(entité, informations_entité, informations_parent, proentité)
        return entité

    def mettre_à_jour_entité_linguistique(self, entité, informations_entité, informations_parent, proentité=None):
        """
        Mise à jour des attributs (principaux et secondaires, appelés paramètres) d'une entité linguistique. À ce niveau, les termes d'entités et d'informations (données traitées) sont utilisés.
        :param entité:
        :param informations_entité:
        :param informations_parent:
        :return:
        """
        for attribut, valeur in informations_entité["attributs"].items():
            if "langue" in informations_entité["attributs"] and informations_entité["attributs"]["langue"] not in self.langues:
                logging.warning(_("Langue « {} » non présente dans les paramètres de configuration.").format(informations_entité["attributs"]["langue"]))
            if hasattr(entité, attribut):
                if "factorisable" in proentité.entité_propre["structure"] and proentité.entité_propre["structure"]["factorisable"]:
                    logging.info(_("L'attribut « {} » a déjà la valeur « {} », une nouvelle entité « {} » sera créée pour la valeur « {} ».").format(attribut, getattr(entité, attribut), entité.nom_entité_linguistique,valeur))
                    self.reprendre_entité_linguistique(entité, attribut, valeur)
                else:
                    logging.error(_("L'attribut « {} » a déjà la valeur « {} » qui ne sera pas remplacée par « {} ».").format(attribut, getattr(entité, attribut), valeur))
            else:
                if valeur:
                    setattr(entité, attribut, str(valeur))
                else:
                    logging.warning(_("L'attribut « {} » n'a pas de valeur.").format(attribut))
        return entité

    def reprendre_entité_linguistique(self, entité, attribut, valeur):
        attributs = {clef: valeur for clef, valeur in entité.__dict__.items() if clef not in ["_parent", "_attribut_parent", "nom_entité_linguistique", attribut]}
        attributs.update({attribut: valeur})
        informations_entité = {"nom": entité.nom_entité_linguistique, "attributs": attributs, "structure": {}}
        informations_parent = {"nom": entité._parent.nom_entité_linguistique, "attribut": entité._attribut_parent}
        self.créer_entité_linguistique(informations_entité=informations_entité, informations_parent=informations_parent)

    def mettre_à_jour_hiérarchie(self, entité):
        """
        Mise à jour de la hiérarchie et de l'historique des entités afin de savoir qui sont les derniers éléments d'un certain type et les derniers parents potentiels.
        :param entité:
        :return:
        """
        if entité.nom_entité_linguistique not in self.hiérarchie:
            self.hiérarchie[entité.nom_entité_linguistique] = []
        self.hiérarchie[entité.nom_entité_linguistique].append(entité)
        self.historique.insert(0, entité.nom_entité_linguistique)

    def mettre_à_jour_identifiant(self, entité, informations_entité, informations_parent, proentité=None):
        """
        Mise à jour de l'identifiant de l'entité.
        :param entité:
        :param informations_entité:
        :param informations_parent:
        :return:
        """
        if "identifiant" in informations_entité["structure"]:
            if informations_entité["nom"] in self.constantes:
                if informations_entité["structure"]["identifiant"]["nom"]:
                    identifiant = getattr(entité, informations_entité["structure"]["identifiant"]["nom"])
                else:
                    identifiant = str(len(getattr(entité._parent, informations_parent["attribut"])))
                if informations_entité["structure"]["identifiant"]["type"] == "primaire":
                    identifiant = "{}{}".format(self.constantes[informations_entité["nom"]], identifiant)
                elif informations_entité["structure"]["identifiant"]["type"] == "secondaire":
                    del self.identifiants[entité.identifiant]
                    identifiant = "{}{}{}".format(entité.identifiant, self.constantes[informations_entité["structure"]["identifiant"]["nom"]], identifiant)
                identifiant = "{}{}".format(entité._parent.identifiant if hasattr(entité, "_parent") and hasattr(entité._parent, "identifiant") else '', identifiant)
                setattr(entité, "identifiant", identifiant)
                self.identifiants[identifiant] = entité
            else:
                logging.error(_("La constante d'identification « {} » n'existe pas.".format(informations_entité["nom"])))
        return entité

    def créer_objet(self, nom_entité_linguistique):
        nom_classe = "".join([segment[0].upper() + segment[1:] for segment in nom_entité_linguistique.split()])
        Entité = type(nom_classe, (lexika.linguistique.EntitéLinguistique,), {})
        entité = Entité()
        entité.nom_entité_linguistique = nom_entité_linguistique
        return entité

    def extraire_sous_entrées(self):
        self.hiérarchie.clear()
        if self.entités_à_extraire:
            for parent_général, entité_à_extraire in [[valeur for clef, valeur in dictionnaire.items()] for dictionnaire in self.entités_à_extraire]:
                self.extraire_sous_entrée(self.dictionnaire, parent_général, entité_à_extraire)

    def extraire_sous_entrée(self, objet, parent_général, entité_à_extraire):
        if isinstance(objet, lexika.linguistique.EntitéLinguistique):
            self.mettre_à_jour_hiérarchie(objet)
            for nom, élément in list(objet.__dict__.items()):
                if élément and nom not in ["_parent", "_attribut_parent"]:
                    if isinstance(élément, list):
                        for sous_élément in élément:
                            self.extraire_sous_entrée(sous_élément, parent_général, entité_à_extraire)
                    if nom == entité_à_extraire["attribut"]:
                        getattr(self.dictionnaire, parent_général["attribut"]).extend(getattr(objet, nom))
                        for objet_entité in getattr(objet, nom):
                            self.mettre_à_jour_hiérarchie(objet_entité)
                            informations_entité = {"nom": "forme apparentée", "attributs": {"cible": objet.identifiant, "type": "entrée principale"}, "structure": {}}
                            informations_parent = {"nom": entité_à_extraire["entité"], "attribut": "formes apparentées"}
                            self.créer_entité_linguistique(informations_entité=informations_entité, informations_parent=informations_parent)
                            informations_entité = {"nom": "forme apparentée", "attributs": {"cible": objet_entité.identifiant, "type": "sous-entrée"}, "structure": {}}
                            informations_parent = {"nom": parent_général["entité"], "attribut": "formes apparentées"}
                            self.créer_entité_linguistique(informations_entité=informations_entité, informations_parent=informations_parent)
                        setattr(objet, nom, [])

    def connecter_renvois(self):
        if self.modèle_renvoi:
            modèle = regex.compile(self.configuration.modèle_renvoi)
            modèle_automatique = regex.compile(self.configuration.modèle_renvoi_automatique)
            formes_citation = {entité.forme_citation: entité.identifiant for entité in self.identifiants.values() if hasattr(entité, "forme_citation")}
            self.connecter_renvois_récursivement(self.dictionnaire, modèle, modèle_automatique,formes_citation)

    def connecter_renvois_récursivement(self, objet, modèle, modèle_automatique, formes_citation):
        if isinstance(objet, lexika.linguistique.EntitéLinguistique):
            for nom, élément in list(objet.__dict__.items()):
                if nom not in ["nom_entité_linguistique", "_parent", "_attribut_parent"]:
                    if isinstance(élément, list):
                        for sous_élément in élément:
                            self.connecter_renvois_récursivement(sous_élément, modèle, modèle_automatique, formes_citation)
                    elif isinstance(élément, dict):
                        for clef_sous_élément, valeur_sous_élément in élément.items():
                            self.connecter_renvois_récursivement(valeur_sous_élément, modèle, modèle_automatique, formes_citation)
                    else:
                        if nom == "cible":
                            print("*", élément)
                            bilan = modèle.match(élément)
                            if bilan:
                                identifiants = []
                                particules = bilan.groupdict()
                                if any([True for particule in particules if bilan.group(particule)]):
                                    identifiant = ''
                                    for particule in particules:
                                        if bilan.group(particule):
                                            identifiant += "{}{}".format(self.constantes[particule.replace("_", " ")], bilan.group(particule))
                                    identifiants.insert(0, identifiant)
                                identifiants.append("Ⓔ{}Ⓗ1".format(élément))
                                print(identifiants, nom, élément)
                                for identifiant in identifiants:
                                    if identifiant in self.identifiants:
                                        setattr(objet, "lien", identifiant)
                                        break
                                else:
                                    if élément in formes_citation:
                                        setattr(objet, "lien", formes_citation[élément])
                                    else:
                                        setattr(objet, "non_lien", élément)
                        elif nom not in ["lien", "non_lien"]:
                            bilan = modèle_automatique.search(élément)
                            if bilan:
                                bilans = modèle_automatique.finditer(élément)
                                for bilan in bilans:
                                    ensemble = bilan.group("ensemble")
                                    cible = bilan.group("cible").replace("_", " ")
                                    identifiants = ["Ⓔ{}".format(cible), "Ⓔ{}Ⓗ1".format(cible)]
                                    for identifiant in identifiants:
                                        if identifiant in self.identifiants:
                                            print('*', identifiant, self.identifiants[identifiant].__dict__, self.entités_à_lier)
                                            for attribut, entité in [(clef, valeur) for entité_à_lier in self.entités_à_lier for clef, valeur in entité_à_lier.items()]:
                                                if hasattr(getattr(self.identifiants[identifiant], attribut)[0], entité):
                                                    affichage_cible = getattr(getattr(self.identifiants[identifiant], attribut)[0], entité)
                                                    élément = élément.replace(ensemble, "⊣lien cible=\"{}\"⊢{}⊣/lien⊢".format(identifiant, affichage_cible))
                                                    break
                                            break
                                    else:
                                        élément = élément.replace(ensemble, cible)
                                setattr(objet, nom, élément)


class NébuleuseDʼOméga(NébuleuseDʼOrion):
    """Cet objet permet de créer des dictionnaires dynamiquement."""
    def __init__(self, configuration):
        super(NébuleuseDʼOméga, self).__init__(configuration)

    def analyser_données(self, ligne_données):
        """
        Analyse les données (ligne par ligne) afin de savoir comment les traiter selon la configuration spécifique. À ce niveau, les termes de balise et de données sont utilisés.
        :param ligne_données:
        :return:
        """
        logging.info(_("Ligne {index} en cours : « {ligne} »").format(**ligne_données))
        bilan = self.modèle_ligne.match(ligne_données["ligne"])
        if bilan:
            balise = bilan.group("balise")
            données = bilan.group("données")
            métadonnées = bilan.group("métadonnées") if "métadonnées" in bilan.groupdict() else None
            if balise in self.balises:
                informations_balise = self.balises[balise]
                if données:
                    if informations_balise["entité"] in self.entités:
                        proentité = lexika.linguistique.ProentitéLinguistique(self.entités[informations_balise["entité"]])
                        proentité.ajouter_informations({"attributs": informations_balise["paramètres"]})
                        est_nouveau_bloc = informations_balise["tête"] if "tête" in informations_balise else None
                        proentité.ajouter_informations({"données": données, "métadonnées": métadonnées})
                        for clef, valeur in {clef: valeur for clef, valeur in bilan.groupdict().items() if valeur and clef not in ["balise", "données"]}.items():
                            if clef == "profondeur":
                                valeur = valeur.count(".")  # à finir
                            if clef == "acception":
                                if "sens" not in self.hiérarchie or getattr(self.hiérarchie["sens"][-1], "numéro de sens") != valeur:
                                    proentité_auxiliaire = lexika.linguistique.ProentitéLinguistique(self.entités[clef])
                                    proentité_auxiliaire.ajouter_informations({"attributs": {}, "données": valeur})
                                    self.aiguiller_entités_linguistiques(proentité_auxiliaire)
                        self.aiguiller_entités_linguistiques(proentité, est_nouveau_bloc)
                    else:
                        logging.error(_("L'entité de type « {} » n'est pas configurée.").format(informations_balise["entité"]))
                else:
                    logging.info(_("La balise de type « {} » (ligne {}) ne contient aucune valeur.").format(balise, ligne_données["index"]))
            else:
                logging.info(_("Balise « {} » inconnue à la ligne {}, donc ignorée.").format(balise, ligne_données["index"]))
        else:
            logging.warning(_("Attention, la ligne « {ligne} »  ({index}) n'a pas été validée par l'expression régulière.").format(**ligne_données))