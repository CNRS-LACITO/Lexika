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

#
# class Dictionnaire(EntitéLinguistique):
#     def __init__(self, identifiant, nom, catégorie, langues):
#         super(Dictionnaire, self).__init__()
#         self.nom_entité_linguistique = "dictionnaire"
#
#         self.identifiant = identifiant
#         self.nom = nom
#         self.catégorie = catégorie
#         self.langues = langues
#         self.entrées = []
#
#     def trier_entrées(self):
#         pass
#
#     def vérifier_renvois(self):
#         pass
#
# class Groupe(EntitéLinguistique):
#     def __init__(self, identifiant=None, nom=None, classe_grammaticale=None):
#         super(Groupe, self).__init__()
#         self.nom_entité_linguistique = "Groupe"
#
#         self.identifiant = identifiant
#         self.nom = nom
#         self.classe_grammaticale = classe_grammaticale
#         self.sens = []
#         self.entrées = []
#
#
# class Entrée(EntitéLinguistique):
#     def __init__(self, identifiant=None, vedette=None, homonyme=None, phonétique=None, classe_grammaticale=None, entrée_parente=None):
#         super(Entrée, self).__init__()
#         self.nom_entité_linguistique = "Entrée"
#
#         self.identifiant = identifiant
#         self.vedette = vedette
#         self.homonyme = homonyme
#         self.phonétique = phonétique
#         self.classe_grammaticale = classe_grammaticale
#         self.entrée_parente = entrée_parente
#         self.groupes = []
#         self.sens = []
#
#
# class Sens(EntitéLinguistique):
#     def __init__(self, identifiant=None, acception=None):
#         super(Sens, self).__init__()
#         self.nom_entité_linguistique = "Sens"
#
#         self.identifiant = identifiant
#         self.acception = acception
#         self.définitions = []
#         self.exemples = []
#         self.sens = []
#         self.relations_sémantiques = []
#
#
# class Définition(EntitéLinguistique):
#     def __init__(self, identifiant=None, définition=None, langue=None, glose=None):
#         super(Définition, self).__init__()
#         self.nom_entité_linguistique = "Définition"
#
#         self.identifiant = identifiant
#         self.définition = définition
#         self.langue = langue
#         self.glose = glose
#
#
# class Exemple(EntitéLinguistique):
#     def __init__(self, identifiant=None, exemple=None, langue=None):
#         super(Exemple, self).__init__()
#         self.nom_entité_linguistique = "Exemple"
#
#         self.identifiant = identifiant
#         self.exemple = exemple
#         self.langue = langue
#
