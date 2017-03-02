#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import copy

class EntitéLinguistique:
    def __init__(self):
        self.nom_entité_linguistique = "entité linguistique"
        self._parent = None
        self._attribut_parent = None


class ProentitéLinguistique:
    """
    Classe intimement liée au fichier 'informations_linguistiques" (au format Python) qui lui offre ses différents paramètres comme attributs.
    """
    def __init__(self, données):
        """
        La classe s'instancie en prenant directement les informations du fichier, avec quelques valeurs par défaut.
        :param données: un dictionnaire d'éntités et d'attributs linguistiques.
        :memb informations: Dictionnaire d'informations provenant de la lecture du fichier source (ligne balisée).
        :memb entité; Entité concernée par l'ajout d'informations.
        :memb entité["nom"]: Nom de l'entité concernée.
        :memb entité["attributs"]: Attributs concernés par la mise à jour d'informations (normalement un seul).
        :memb entité["paramètres"]: Attributs auxiliaires (dictionnaire) concernés par la mise à jour d'informations (généralement donnés par la balise).
        :memb entité["structure"]: Informations de structure de l'entité.
        :memb entité["structure"]["identifiant"]: Informations sur la création d'identifiant pour l'entité concernée.
        :memb entité["structure"]["identifiant"]["nom"]: Nom de l'attribut qui sert de base d'identifiant.
        :memb entité["structure"]["identifiant"]["type"]: 'primaire' et 'secondaire' indique l'éventuelle combinaison des bases d'identifiant.
        :memb parents (liste): Entités auxquelles peut se rattacher l'entité concernée, dans l'ordre de préférence en cas d'ambiguïté (hiérarchie souple), ne sert pas en cas de mise à jour d'information d'attribut.
        :memb parents[x]["nom"]: Nom de l'entité parente de l'entité concernée.
        :memb parents[x]["attribut"]: Nom de l'attribut (liste) de l'entité parente à laaquelle se connecte l'entité concernée.
        """
        self.données = copy.deepcopy(données)

        self.informations_entités_propres_potentielles = self.données["entités"]
        self.informations_entités_parentes_potentielles = self.données["parents"]
        self.informations = {}

        self.attribut_cible = None

        self.entité_propre = None
        self.entité_parente = None

    def ajouter_informations(self, informations):
        self.informations.update(informations)

    def rechercher_attribut_cible(self):
        attributs_cibles = [clef for clef, valeur in self.entité_propre["attributs"].items() if valeur is None]
        if len(attributs_cibles) == 1:
            self.attribut_cible = attributs_cibles[0]
        elif len(attributs_cibles) > 1:
            logging.error(_("Attention, il y a plusieurs attributs cibles pour une seule entité (« {} »), il ne devrait y en avoir qu'un seul au maximum.".format(attributs_cibles)))
            raise Exception
        return self.attribut_cible

    def rechercher_entités_adéquates(self, historique, hiérarchie):
        self.rechercher_entité_propre(historique, hiérarchie)
        self.rechercher_entité_parente(historique, hiérarchie)

    def rechercher_entité_propre(self, historique, hiérarchie):
        self.entité_propre = self.rechercher_entité_adéquate(self.informations_entités_propres_potentielles, historique, hiérarchie)
        self.transférer_informations_entité_propre()
        return self.entité_propre

    def rechercher_entité_parente(self, historique, hiérarchie):
        self.entité_parente = self.rechercher_entité_adéquate(self.informations_entités_parentes_potentielles, historique, hiérarchie)
        return self.entité_parente

    def rechercher_entité_adéquate(self, informations_entités, historique, hiérarchie):
        """
        Recherche de l'entité adéquate en cas d'ambiguïté potentielle.
        :param informations_entités_potentielles:
        :return:
        """
        if informations_entités:
            if len(informations_entités) == 1:
                entité = informations_entités[0]
            else:
                if len([entité for entité in informations_entités if "nom" in entité and entité["nom"] in historique]) > 1:
                    noms_entités_adéquates = {}
                    for entité_potentielle in informations_entités:
                        if entité_potentielle["nom"] in historique:
                            noms_entités_adéquates[entité_potentielle["nom"]] = historique.index(entité_potentielle["nom"])
                    noms_entités_adéquates = sorted([(antériorité, nom_entité) for nom_entité, antériorité in noms_entités_adéquates.items()])[0]
                    entité = [entité_potentielle for entité_potentielle in informations_entités if entité_potentielle["nom"] == noms_entités_adéquates[1]][0]
                else:
                    entité = [entité_potentielle for entité_potentielle in informations_entités if "nom" in entité_potentielle and entité_potentielle["nom"] in historique]
                    if entité:
                        entité = entité[0]
                if "entité" in informations_entités[0]:
                    return []
                # if entité and hasattr(hiérarchie[entité["nom"]][-1], self.rechercher_attribut_cible()):
        else:
            entité = None
        return entité

    def transférer_informations_entité_propre(self):
        self.rechercher_attribut_cible()
        if self.attribut_cible and "données" in self.informations:
            self.entité_propre["attributs"][self.attribut_cible] = self.informations["données"]
        for clef, valeur in {clef: valeur for clef, valeur in self.informations.items() if clef not in ["données", "attributs"]}.items():
            self.entité_propre.update({clef: valeur})
        for clef, valeur in {clef: valeur for clef, valeur in self.informations["attributs"].items()}.items():
            self.entité_propre["attributs"][clef] = valeur


class Langue(EntitéLinguistique):
    def __init__(self, code, type_caractères=None, sens_lecture=None, autoglossonyme=None, glossonyme=None, statuts=[]):
        super(Langue, self).__init__()
        self.nom_entité_linguistique = "langue"

        self.code = code
        self.type_caractères = type_caractères
        self.sens_lecture = sens_lecture
        self.autoglossonyme = autoglossonyme
        self.glossonyme = glossonyme
        self.statuts = statuts

    def récupérer_contenu_objet(self):
        return {clef.lstrip("_"): valeur for clef, valeur in self.__dict__.items()}

