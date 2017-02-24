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
        self.informations_globales = None
        self.dictionnaire = None


class NébuleuseObscure(Nébuleuse):
    """Cet objet permet de créer des dictionnaires dynamiquement."""
    def __init__(self, configuration):
        """
        :param configuration:
        :memb hiérarchie: Dictionnaire de tous les types d'entités du dictionnaire, permet de retouver le dernière parent d'un type donné.
        :memb historique: Liste ordonnée par ordre d'ancienneté des entités du dictionnaire, permet de retouver quel parent est le plus proche.
        """
        super(NébuleuseObscure, self).__init__(configuration)

        self.modèle_ligne = regex.compile(self.configuration.modèle_ligne)
        self.balises = self.configuration.balises
        self.entités = self.configuration.entités
        self.expression_renvoi = self.configuration.expression_renvoi

        self.identifiants = {}
        self.hiérarchie = {}
        self.historique = []

    def initialiser(self):
        """
        Initialise la configuration générale et les objets nécessaires à la création du dictionnaire.
        :return:
        """
        informations_globales = {"nom": "informations globales", "attributs": self.configuration.dictionnaire, "paramètres": {}, "structure": {}}
        self.informations_globales = self.créer_entité_linguistique(informations_globales, None)
        informations_dictionnaire = {"nom": "dictionnaire", "attributs": {}, "paramètres": {}, "structure": {}}
        self.dictionnaire = self.créer_entité_linguistique(informations_dictionnaire, None)
        for langue, informations_langue in self.configuration.langues.items():
            self.langues.append(langue)
            informations_langue = {"nom": "langue", "attributs": informations_langue, "paramètres": {}, "structure": {}}
            informations_parent = {"nom": "informations globales", "attribut": "langues"}
            self.créer_entité_linguistique(informations_langue, informations_parent)

    def analyser_données(self, ligne_données):
        """
        Analyse les données (ligne par ligne) afin de savoir comment les traiter selon la configuration spécifique. À ce niveau, les termes de balise et de données sont utilisés.
        :param ligne_données:
        :return:
        """
        bilan = self.modèle_ligne.match(ligne_données["ligne"])
        if bilan:
            balise = bilan.group("balise")
            métabalise = bilan.group("métabalise") if "métabalise" in bilan.groupdict() else None
            données = bilan.group("données")
            métadonnées = bilan.group("métadonnées") if "métadonnées" in bilan.groupdict() else None
            if balise in self.balises:
                informations_balise = self.balises[balise]
                if données:
                    informations_générales = copy.deepcopy(self.entités[informations_balise["entité"]])
                    for entité in informations_générales["entités"]:
                        entité["attributs"].update(informations_balise["paramètres"])
                    # if métabalise:
                    #     profondeur = métabalise.count(".")
                    #     ordinal = métabalise.replace(".", '')
                    #     if ordinal:
                    #         informations = self.balises[informations_générales["entité"]["structure"]["métabalise"]]
                    #         nom_entité_auxiliaire = informations["entité"]["nom"]
                    #         informations["entité"].update({"valeurs": [ordinal], "métainformations": métadonnées})
                    #         if not nom_entité_auxiliaire in self.hiérarchie or (nom_entité_auxiliaire in self.hiérarchie and getattr(self.hiérarchie[nom_entité_auxiliaire][-1], informations["entité"]["structure"]["identifiant"]["nom"]) != ordinal):
                    #             self.aiguiller_entité_linguistique(informations)
                    if métadonnées:
                        métadonnées = {"balise": métabalise, "données": métadonnées}
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
                    else:
                        est_nouveau_bloc = "tête" in informations_balise and informations_balise["tête"]
                        self.transférer_données_entités(informations_générales["entités"], données=données, métadonnées=métadonnées)
                        self.préparer_entités_linguistiques(informations_générales, est_nouveau_bloc)
                else:
                    logging.info(_("La balise de type « {} » (ligne {}) ne contient aucune valeur.").format(balise, ligne_données["index"]))
            else:
                    logging.info(_("Balise « {} » inconnue à la ligne {}, donc ignorée.").format(balise, ligne_données["index"]))
        else:
            logging.warning(_("Attention, la ligne '{ligne}' ({index}) n'a pas été validée par l'expression régulière.").format(**ligne_données))

    def préparer_entités_linguistiques(self, informations_générales, est_nouveau_bloc=False):
        """
        Prépare les différentes entités linguistiques avec les informations, avec la recherche des entités parentes et des entités d'appartenance. À ce niveau, les termes d'entités et d'informations (données traitées) sont utilisés.
        :param informations_générales:
        :return:
        """
        if est_nouveau_bloc:
            self.historique = []
            self.hiérarchie = {"dictionnaire": self.hiérarchie["dictionnaire"]}

        informations_entité = self.rechercher_entité_adéquate(informations_générales["entités"])
        informations_parent = self.rechercher_entité_adéquate(informations_générales["parents"] if "parents" in informations_générales else None)
        # Appels récursifs pour créer les entités parentes manquantes s'il y a normalement une entité parente, à l'aide du dernier parent par défaut.
        if not informations_parent and informations_parent is not None:
            dernier_parent = informations_générales["parents"][-1]
            if "entité" in dernier_parent:
                logging.warning(_("Parent manquant, bordel !"))
                entité = dernier_parent["entité"]
                informations_générales_secondaires = copy.deepcopy(self.entités[entité])
                attributs = dernier_parent["attributs"]
                if "informations" in dernier_parent:
                    attributs.update({clef: informations_générales["entités"][0]["attributs"][valeur] for clef, valeur in dernier_parent["informations"].items()})
                self.transférer_données_entités(informations_générales_secondaires["entités"], attributs=attributs)
                self.préparer_entités_linguistiques(informations_générales_secondaires)
                informations_parent = self.rechercher_entité_adéquate(informations_générales["parents"])

        # Garde-fous pour éviter des mélanges d'informations de différentes entrées, ce qui peut arriver si certaines entités ont été oubliées dans le fichier source.
        # print("*****", informations_entité)
        # if "tête" in informations_entité["structure"] and informations_entité["structure"]["tête"]:
        #     logging.info(_("Nouveau bloc"))
        #     self.historique = []
        #     self.hiérarchie = {"dictionnaire": self.hiérarchie["dictionnaire"]}

        # if any([valeur for valeur in informations_entité["attributs"].values() if valeur]):
        #     self.créer_entité_linguistique(informations_entité, informations_parent)
        # else:
        #     logging.warning(_("Information manquante pour l'entité « {} », elle ne sera pas traitée.").format(informations_entité["nom"]))
        self.créer_entité_linguistique(informations_entité, informations_parent)

    def créer_entité_linguistique(self, informations_entité, informations_parent=None):
        """
        Création d'une entité linguistique. À ce niveau, les termes d'entités et d'informations (données traitées) sont utilisés.
        :param informations_entité:
        :param informations_parent:
        :return:
        """
        nom_entité_linguistique = informations_entité["nom"]
        # Informations de type entité, donc création de cette dernière.
        if informations_parent or nom_entité_linguistique.lower() in ["dictionnaire", "informations globales"]:
            entité = self.créer_objet(nom_entité_linguistique)
            # Liaison de l'entité avec la bonne entité parente, création si besoin est.
            if informations_parent:
                nom_parent = informations_parent["nom"]
                attribut_parent = informations_parent["attribut"]
                if nom_parent not in self.hiérarchie:
                    logging.error(_("L'entité parente « {} » de l'entité « {} » n'a pas été trouvée.").format(nom_parent, entité.nom_entité_linguistique))
                parent = self.hiérarchie[nom_parent][-1]
                if not hasattr(parent, attribut_parent):
                    setattr(parent, attribut_parent, [])
                attribut_parent = getattr(parent, attribut_parent)
                attribut_parent.append(entité)
                setattr(entité, "_parent", parent)
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
        self.mettre_à_jour_entité_linguistique(entité, informations_entité, informations_parent)
        self.mettre_à_jour_identifiant(entité, informations_entité, informations_parent)
        return entité

    def mettre_à_jour_entité_linguistique(self, entité, informations_entité, informations_parent):
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
                logging.error(_("L'attribut « {} » a déjà la valeur « {} » qui ne sera pas remplacée par « {} ».").format(attribut, getattr(entité, attribut), valeur))
            else:
                if valeur:
                    setattr(entité, attribut, str(valeur))
                else:
                    logging.warning(_("L'attribut « {} » n'a pas de valeur.").format(attribut))
        return entité

    def rechercher_entité_adéquate(self, informations_entités_potentielles):
        """
        Recherche de l'entité adéquate en cas d'ambiguïté potentielle.
        :param informations_entités_potentielles:
        :return:
        """
        if informations_entités_potentielles:
            if len(informations_entités_potentielles) == 1:
                entité_adéquate = informations_entités_potentielles[0]
            else:
                noms_entités_potentielles = [entité["nom"] for entité in informations_entités_potentielles if "nom" in entité]
                if len([entité for entité in noms_entités_potentielles if entité in self.historique]) > 1:
                    résultat = {}
                    for nom_entité_potentielle in noms_entités_potentielles:
                        if nom_entité_potentielle in self.historique:
                            résultat[nom_entité_potentielle] = self.historique.index(nom_entité_potentielle)
                    entités_adéquates = sorted([(antériorité, entité) for entité, antériorité in résultat.items()])[0]
                    entité_adéquate = [informations for informations in informations_entités_potentielles if informations["nom"] == entités_adéquates[1]][0]
                else:
                    entité_adéquate = [informations for informations in informations_entités_potentielles if "nom" in informations and informations["nom"] in self.historique]
                    if entité_adéquate:
                        entité_adéquate = entité_adéquate[0]
        else:
            entité_adéquate = None
        return entité_adéquate

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

    def mettre_à_jour_identifiant(self, entité, informations_entité, informations_parent):
        """
        Mise à jour de l'identifiant de l'entité.
        :param entité:
        :param informations_entité:
        :param informations_parent:
        :return:
        """
        if "identifiant" in informations_entité["structure"]:
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
        return entité

    def créer_objet(self, nom_entité_linguistique):
        nom_classe = "".join([segment[0].upper() + segment[1:] for segment in nom_entité_linguistique.split()])
        Entité = type(nom_classe, (lexika.linguistique.EntitéLinguistique,), {})
        entité = Entité()
        entité.nom_entité_linguistique = nom_entité_linguistique
        return entité

    def transférer_données_entités(self, entités, données=None, attributs=None, métadonnées=None):
        for entité in entités:
            attributs_cibles = [clef for clef, valeur in entité["attributs"].items() if valeur is None]
            if len(attributs_cibles) <= 1:
                if données:
                    entité["attributs"][attributs_cibles[0]] = données
                if métadonnées:
                    entité.update({"métainformations": métadonnées})
                if attributs:
                    entité.update({"attributs": attributs})
            else:
                logging.error(_("Attention, il y a plusieurs attributs cibles pour une seule entité (« {} »), il ne devrait y en avoir qu'un seul au maximum.".format(attributs_cibles)))
                raise Exception

    def connecter_renvois(self):
        if self.expression_renvoi:
            modèle = regex.compile(self.configuration.expression_renvoi)
            formes_citation = {entité.forme_citation: entité.identifiant for entité in self.identifiants.values() if hasattr(entité, "forme_citation")}
            self.connecter_renvois_récursivement(self.dictionnaire, modèle, formes_citation)

    def connecter_renvois_récursivement(self, objet, modèle, formes_citation):
        if isinstance(objet, lexika.linguistique.EntitéLinguistique):
            if "cible" in objet.__dict__:
                setattr(objet, "lien", None)
                setattr(objet, "non_lien", None)
            for nom, élément in objet.__dict__.items():
                if nom not in ["nom_entité_linguistique", "_parent"]:
                    if isinstance(élément, list):
                        for sous_élément in élément:
                            self.connecter_renvois_récursivement(sous_élément, modèle, formes_citation)
                    elif isinstance(élément, dict):
                        for clef_sous_élément, valeur_sous_élément in élément.items():
                            self.connecter_renvois_récursivement(valeur_sous_élément, modèle, formes_citation)
                    else:
                        if nom == "cible":
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
                                for identifiant in identifiants:
                                    if identifiant in self.identifiants:
                                        for attribut in ["forme_citation", "vedette", "nom", "acception"]:
                                            if hasattr(self.identifiants[identifiant], attribut):
                                                affichage_cible = getattr(self.identifiants[identifiant], attribut)
                                                break
                                        élément = identifiant
                                        setattr(objet, "lien", élément)
                                        break
                                else:
                                    if élément in formes_citation:
                                        setattr(objet, "lien", formes_citation[élément])
                                    else:
                                        setattr(objet, "non_lien", élément)


# def aiguiller_entité_linguistique(self, informations_entité, informations_parent):
#     """
#     Aiguille les informations d'une entité vers le créateur après un nettoyage. À ce niveau, les termes d'entités et d'informations (données traitées) sont utilisés.
#     :param informations_générales:
#     """
    # if "préentités" in informations:
    #     for préentité in informations["préentités"]:
    #         attributs_entité = {"attributs": {attribut: valeur for attribut, valeur in zip(entité["attributs"], entité["valeurs"]) if valeur}}
    #         entité.pop("attributs")
    #         entité.pop("valeurs")
    #         entité.update(attributs_entité)
    #         if self.balises[préentité["nom"]]["parents"] and len(self.balises[préentité["nom"]]["parents"]) > 1:
    #             parent = self.rechercher_parent_adéquat(self.balises[préentité["nom"]]["parents"])
    #         else:
    #             parent = self.balises[préentité["nom"]]["parents"][0] if self.balises[préentité["nom"]]["parents"] else None
    #         self.créer_entité_linguistique(self.balises[préentité["nom"]]["entité"], parent)

    # entité = informations["entité"]
    # if "expression" in informations:  # à revoir
    #     modèle_informations = regex.compile(informations["expression"])
    #     bilan = modèle_informations.match(entité["valeurs"][0])
    #     valeurs = []
    #     if bilan:
    #         for attribut in informations["entité"]["attributs"]:
    #             valeurs.append(bilan.group(attribut))
    #     attributs_entité = {"attributs": {attribut: valeur for attribut, valeur in zip(entité["attributs"], valeurs) if valeur}}
    #     logging.warning(_("Entité « {nom} » en cours, avec les attributs suivants : « {attributs} » (avec les paramètres suivant : « {paramètres} »).").format(**entité))
    # if parent:
    #     logging.warning(_("Son parent est « {nom} » et l'entité se place dans l'attribut « {attribut} ».").format(**parent))
    # else:
    #     logging.warning(_("Elle est indépendante."))
    # self.créer_entité_linguistique(informations_entité, informations_parent)