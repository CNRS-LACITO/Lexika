#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.configuration
import lexika.internationalisation
import lexika.outils
import regex
import yaml
from pprint import pprint

class Configuration:
    """
    Classe intimement liée au fichier 'fichier_source' (au format YML) qui lui offre ses différents paramètres comme attributs.
    """
    def __init__(self, fichier_source):
        self.fichier_source = fichier_source
        self.informations_linguistiques = lexika.configuration.InformationsLinguistiques()
        self.statuts_langues = {}
        with open(fichier_source, 'r') as entrée:
            # Mise à jour des attributs de l'objet en ajoutant des _ pour la compatibilité Python.
            self.__dict__.update({clef.replace(" ", "_"): valeur if clef != "langues" else {
                sous_valeur["identifiant"]: {sous_sous_clef.replace(" ", "_"): sous_sous_valeur for
                                             sous_sous_clef, sous_sous_valeur in sous_valeur.items()
                                             }
                for sous_valeur in valeur} for clef, valeur in yaml.safe_load(entrée).items()
                                  })
        for langue, informations_langue in self.langues.items():
            statut = "{} {}".format(informations_langue["statut"], len([clef for clef in self.statuts_langues.keys() if clef.startswith(informations_langue["statut"])]) + 1)
            self.statuts_langues[statut] = langue
        self.informations_linguistiques.statuts_langues.update(self.statuts_langues)
        self.informations_linguistiques.initialiser()
        if self.format_entrée in self.informations_linguistiques.format_entrée:
            self.format_entrée = self.informations_linguistiques.format_entrée[self.format_entrée]
            self.format_sortie = self.informations_linguistiques.format_sortie[self.format_sortie]
            self.modèle_ligne = self.format_entrée["modèle de ligne"]
            self.balises = self.format_entrée["balises"]
            self.entités = self.format_sortie["entités"]
            self.constantes = self.format_sortie["constantes"] if "constantes" in self.format_sortie else None
            self.entités_à_trier = self.format_sortie["entités à trier"] if "entités à trier" in self.format_sortie else None
            self.entités_à_extraire = self.format_sortie["entités à extraire"] if "entités à extraire" in self.format_sortie else None
            self.modèle_renvoi = self.format_sortie["modèle de renvoi"] if "modèle de renvoi" in self.format_sortie else None
            self.modèle_renvoi_automatique = self.format_entrée["modèle de renvoi automatique"] if "modèle de renvoi automatique" in self.format_entrée else None
            self.entités_à_lier = self.format_sortie["entités à lier"] if "entités à lier" in self.format_sortie else None
            self.créateur = self.informations_linguistiques.créateurs[self.format_entrée["créateur"]]
        else:
            raise Exception("Format « {} » non pris en charge.".format(self.format_entrée))

    def récupérer_contenu_objet(self):
        return {clef.lstrip("_"): valeur for clef, valeur in self.__dict__.items()}



class Traducteur:
    def __init__(self, données=lexika.internationalisation.dictionnaires):
        self.données = données
        self.dictionnaire = {}

        for dictionnaire in données:
            self.dictionnaire.update(dictionnaire)

    def traduire(self, expression):
        if expression in self.dictionnaire:
            return self.dictionnaire[expression]
        else:
            return expression


class Trieur:
    def __init__(self, données):
        self.données = données
        self.ordre_lexicographique = None
        self.sous_ordre_lexicographique = None
        self.expression_rationnelle_tri_entités = None
        self.expression_rationnelle_sous_tri_entités = None
        self.initialiser()

    def initialiser(self):
        valeurs = {}
        valeurs_auxiliaires = {}
        for index, élément in enumerate(self.données):
            if isinstance(élément, str):
                valeurs[élément] = index
            elif isinstance(élément, list):
                for sous_index, sous_élément in enumerate(élément):
                    valeurs[sous_élément] = index
                    valeurs_auxiliaires[sous_élément] = sous_index
        self.ordre_lexicographique = valeurs
        self.sous_ordre_lexicographique = valeurs_auxiliaires
        regex.compile(r"{}".format("|".join(sorted(self.ordre_lexicographique, key=lambda mot: len(mot), reverse=True))), flags=regex.IGNORECASE) if self.ordre_lexicographique else None
        self.expression_rationnelle_tri_entités = regex.compile(r"{}".format("|".join(sorted(self.ordre_lexicographique, key=lambda mot: len(mot), reverse=True))), flags=regex.IGNORECASE)
        self.expression_rationnelle_sous_tri_entités = regex.compile(r"{}".format("|".join(sorted(self.sous_ordre_lexicographique, key=lambda mot: len(mot), reverse=True))), flags=regex.IGNORECASE)
        print(self.ordre_lexicographique)
        print(self.sous_ordre_lexicographique)

    def trier_entités(self, expression):
        if self.expression_rationnelle_tri_entités:
            résultat_primaire = [valeurs[1] for valeurs in [(syllabe, self.ordre_lexicographique[syllabe.lower()]) for syllabe in self.expression_rationnelle_tri_entités.findall(expression) if syllabe.lower() in self.ordre_lexicographique]]
            résultat_secondaire = [valeurs[1] for valeurs in [(syllabe, self.sous_ordre_lexicographique[syllabe.lower()]) for syllabe in self.expression_rationnelle_sous_tri_entités.findall(expression) if syllabe.lower() in self.ordre_lexicographique]]
            résultat_tertiaire = [0 if syllabe.islower() else 1 for syllabe in self.expression_rationnelle_tri_entités.findall(expression) if syllabe.lower() in self.ordre_lexicographique]
        else:
            résultat_primaire = expression
            résultat_secondaire = résultat_tertiaire = None
        return résultat_primaire, résultat_secondaire, résultat_tertiaire
