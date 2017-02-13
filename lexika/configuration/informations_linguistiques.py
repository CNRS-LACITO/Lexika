#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika
import os

# Cet objet est fait pour être modifié, mais avec quelques précautions...
types_source = {
    # Attention, la nébuleuse obscure est très puissante et la puissance nécessite des responsabilités...
    "test": {
        "modèle ligne": r"^\\(?P<balise>\w*)(?:\s*<(?P<métadonnées>.*)>\s*)?\s*(?P<données>.*)",
        "balises": {
            "lex": {"entité": {"nom": "entrée", "attributs": ["vedette"], "paramètres": {},
                               "structure": {"identifiant": {"nom": "vedette", "type": "primaire"}}},
                    "parents": [{"nom": "dictionnaire", "attribut": "entrées"}]},
            "hom": {"entité": {"nom": "entrée", "attributs": ["homonyme"], "paramètres": {},
                               "structure": {"identifiant": {"nom": "homonyme", "type": "secondaire"}}},
                    "parents": None},
            "cla": {
                "entité": {"nom": "entrée", "attributs": ["classe_grammaticale"], "paramètres": {}, "structure": {}},
                "parents": None},
            "sns": {"entité": {"nom": "sens", "attributs": ["acception"], "paramètres": {},
                               "structure": {"identifiant": {"nom": "acception", "type": "primaire"}}},
                    "parents": [{"nom": "entrée", "attribut": "sens"}]},
            "def": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "fra"},
                               "structure": {"identifiant": {"nom": None, "type": "primaire"}}},
                    "parents": [{"nom": "sens", "attribut": "définitions"}]},
            "glo": {
                "entité": {"nom": "glose", "attributs": ["glose"], "paramètres": {"langue": "eng"}, "structure": {}},
                "parents": [{"nom": "définition", "attribut": "gloses"}]},
            "exf": {"entité": {"nom": "exemple", "attributs": ["exemple"], "paramètres": {"langue": "fra"},
                               "structure": {"identifiant": {"nom": None, "type": "primaire"}}},
                    "parents": [{"nom": "sens", "attribut": "exemples"}]},
        }
    },
    "Alex": {
        "modèle ligne": r"^\\(?P<balise>\w*)(?:\s*<(?P<métadonnées>.*)>\s*)?\s*(?P<données>.*)",
        "balises": {
            "lx": {"entité": {"nom": "entrée", "attributs": ["vedette"], "paramètres": {},
                              "structure": {"identifiant": {"nom": "vedette", "type": "primaire"}}},
                   "parents": [{"nom": "dictionnaire", "attribut": "entrées"}]},
            "hm": {"entité": {"nom": "entrée", "attributs": ["homonyme"], "paramètres": {},
                              "structure": {"identifiant": {"nom": "homonyme", "type": "secondaire"}}},
                   "parents": None},
            "ps": {"entité": {"nom": "entrée", "attributs": ["classe_grammaticale"], "paramètres": {}, "structure": {}},
                   "parents": None},
            "sn": {"entité": {"nom": "sens", "attributs": ["acception"], "paramètres": {},
                              "structure": {"identifiant": {"nom": "acception", "type": "primaire"}}},
                   "parents": [{"nom": "entrée", "attribut": "sens"}]},
            "de": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "fra"},
                              "structure": {"identifiant": {"nom": None, "type": "primaire"}}},
                   "parents": [{"nom": "sens", "attribut": "définitions"},
                               {"nom": "entrée", "attribut": "définitions"}]},
            "dn": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "eng"},
                              "structure": {"identifiant": {"nom": None, "type": "primaire"}}},
                   "parents": [{"nom": "sens", "attribut": "définitions"},
                               {"nom": "entrée", "attribut": "définitions"}]},
            "xe": {"entité": {"nom": "exemple", "attributs": ["exemple"], "paramètres": {"langue": "fra"},
                              "structure": {"identifiant": {"nom": None, "type": "primaire"}}},
                   "parents": [{"nom": "sens", "attribut": "exemples"}, {"nom": "entrée", "attribut": "définitions"}]},
            "xn": {"entité": {"nom": "exemple", "attributs": ["exemple"], "paramètres": {"langue": "eng"},
                              "structure": {"identifiant": {"nom": None, "type": "primaire"}}},
                   "parents": [{"nom": "sens", "attribut": "exemples"}, {"nom": "entrée", "attribut": "définitions"}]},
        }
    },
    "Martine": {
        "modèle ligne": r"^(?P<métabalise>[\d]*)(?P<balise>[\w.]*)\s+(?P<données>.*)(?:\s*<(?P<métadonnées>.*)>\s*)?$",
        "balises": {
            ".hw": {"expression": r"^(?P<vedette>.*?)(\$(?P<homonyme>.*))?$", "composants": {"vedette": {
                "entité": {"nom": "entrée", "attributs": ["vedette"], "paramètres": {},
                           "structure": {"identifiant": {"nom": "vedette", "type": "primaire"}}},
                "parents": [{"nom": "dictionnaire", "attribut": "entrées"}]}, "homonyme": {
                "entité": {"nom": "entrée", "attributs": ["homonyme"], "paramètres": {},
                           "structure": {"identifiant": {"nom": "homonyme", "type": "secondaire"}}}, "parents": None}}},
            "ps": {"entité": {"nom": "entrée", "attributs": ["classe_grammaticale"], "paramètres": {}, "structure": {"métabalise": "sens"}},
                   "parents": None},
            "dff": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "fra"},
                               "structure": {"identifiant": {"nom": None, "type": "primaire"}, "métabalise": "sens"}},
                    "parents": [{"nom": "sens", "attribut": "définitions"},
                                {"nom": "entrée", "attribut": "définitions"}]},
            "dfe": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "eng"},
                               "structure": {"identifiant": {"nom": None, "type": "primaire"}, "métabalise": "sens"}},
                    "parents": [{"nom": "sens", "attribut": "définitions"},
                                {"nom": "entrée", "attribut": "définitions"}]},
            "dfn": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "nep"},
                               "structure": {"identifiant": {"nom": None, "type": "primaire"}, "métabalise": "sens"}},
                    "parents": [{"nom": "sens", "attribut": "définitions"},
                                {"nom": "entrée", "attribut": "définitions"}]},
            "nag": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "tam"},
                               "structure": {"identifiant": {"nom": None, "type": "primaire"}, "métabalise": "sens"}},
                    "parents": [{"nom": "sens", "attribut": "définitions"},
                                {"nom": "entrée", "attribut": "définitions"}]},
            "sens": {"entité": {"nom": "sens", "attributs": ["acception"], "paramètres": {},
                              "structure": {"identifiant": {"nom": "acception", "type": "primaire"}}},
                   "parents": [{"nom": "entrée", "attribut": "sens"}]},
        }
    },
}

créateurs = {
    "nébuleuse obscure": lambda configuration: lexika.NébuleuseObscure(configuration),
    "nébuleuse diffuse": lambda configuration: lexika.NébuleuseDiffuse(configuration),
    "Alex": lambda configuration: lexika.NébuleuseDiffuse(configuration),
    "Martine": lambda configuration: lexika.NébuleuseLexMartine(configuration)
}

tâches = {
    "remplacer_caractères":  lambda fichier_entrée, fichier_sortie: remplacer_caractères(fichier_entrée, fichier_sortie),
    "joindre lignes coupées": lambda fichier_entrée, fichier_sortie: joindre_lignes_coupées(fichier_entrée, fichier_sortie),
}

def remplacer_caractères(fichier_entrée, fichier_sortie):
    pass

def joindre_lignes_coupées(fichier_entrée, fichier_sortie):
    with open(fichier_entrée, 'r') as entrée:
        résultat = []
        for ligne in entrée.readlines():
            if ligne.strip() and not ligne.startswith("\\"):
                résultat[-1] = "{} {}".format(résultat[-1].rstrip(), ligne)
            else:
                résultat.append(ligne)
    with open(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))







