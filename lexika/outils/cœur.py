#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.configuration
import yaml


class Configuration:
    """
    Cette classe est intimement liée au fichier 'fichier_source' (au format YML) qui lui offre ses différents paramètres comme attributs.
    """
    def __init__(self, fichier_source):
        self.fichier_source = fichier_source
        with open(fichier_source, 'r') as entrée:
            # Mise à jour des attributs de l'objet en ajoutant des _ pour la compatibilité Python.
            self.__dict__.update({
                                     clef.replace(" ", "_"): valeur if clef != "langues" else {
                                         sous_valeur["identifiant"]: {sous_sous_clef.replace(" ", "_"): sous_sous_valeur for
                                                               sous_sous_clef, sous_sous_valeur in sous_valeur.items()
                                                               }
                                         for sous_valeur in valeur} for clef, valeur in yaml.safe_load(entrée).items()
                                     })
        if self.type_source in lexika.configuration.types_source:
            self.__dict__.update({clef.replace(" ", "_"): valeur for clef, valeur in lexika.configuration.types_source[self.type_source].items()})
            self.créateur = lexika.configuration.créateurs[self.créateur]
        else:
            raise Exception("Format '{}' non pris en charge.".format(self.type_source))

    def récupérer_contenu_objet(self):
        return {clef.lstrip("_"): valeur for clef, valeur in self.__dict__.items()}



