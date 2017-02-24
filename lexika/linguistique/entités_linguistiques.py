#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class EntitéLinguistique:
    def __init__(self):
        self.nom_entité_linguistique = "entité linguistique"


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
