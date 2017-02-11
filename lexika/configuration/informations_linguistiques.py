#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika
import os

# Cet objet ne devrait pas être modifié à la légère...
entités_linguistiques = {
    "entrée": lambda objet, attribut, information, paramètres, métainformations: objet.manipuler_entrée(attribut, information, paramètres, métainformations),
    "groupe": lambda objet, attribut, information, paramètres, métainformations: objet.manipuler_groupe(attribut, information, paramètres, métainformations),
    "sens": lambda objet, attribut, information, paramètres, métainformations: objet.manipuler_sens(attribut, information, paramètres, métainformations),
    "définition": lambda objet, attribut, information, paramètres, métainformations: objet.manipuler_définition(attribut, information, paramètres, métainformations),
    "exemple": lambda objet, attribut, information, paramètres, métainformations: objet.manipuler_exemple(attribut, information, paramètres, métainformations),
}

# Cet objet ne devrait pas être modifié à la légère...
paramètres_linguistiques = {
    "langue": None,
    "paradigme": None,
}

# Cet objet est fait pour être modifié, mais avec quelques précautions...
types_source = {
    # Attention, la nébuleuse obscure est très puissante et la puissance nécessite des responsabilités...
    "test": {
        "modèle ligne": r"^\\(?P<balise>\w*)(?:\s*<(?P<métadonnées>.*)>\s*)?\s*(?P<données>.*)",
        "modèle entrée": r"^(?P<entrée>.*)$",
        "balises": {
            "lex": {"entité": {"nom": "entrée", "attributs": ["vedette"], "paramètres": {}, "structure": {"identifiant": {"nom": "vedette", "type": "primaire"}}}, "parent": [{"nom": "dictionnaire", "attribut": "entrées"}]},
            "hom": {"entité": {"nom": "entrée", "attributs": ["homonyme"], "paramètres": {}, "structure": {"identifiant": {"nom": "homonyme", "type": "secondaire"}}}, "parent": None},
            "cla": {"entité": {"nom": "entrée", "attributs": ["classe_grammaticale"], "paramètres": {}, "structure": {}}, "parent": None},
            "sns": {"entité": {"nom": "sens", "attributs": ["acception"], "paramètres": {}, "structure": {"identifiant": {"nom": "acception", "type": "primaire"}}}, "parent": [{"nom": "entrée", "attribut": "entrées"}]},
            "def": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "fra"}, "structure": {"identifiant": {"nom": None, "type": "primaire"}}}, "parent": [{"nom": "sens", "attribut": "définitions"}]},
            "exf": {"entité": {"nom": "exemple", "attributs": ["exemple"], "paramètres": {"langue": "fra"}, "structure": {"identifiant": {"nom": None, "type": "primaire"}}}, "parent": [{"nom": "sens", "attribut": "exemples"}]},
        }
    },
    "Alex": {
        "modèle ligne": r"^\\(?P<balise>\w*)(?:\s*<(?P<métadonnées>.*)>\s*)?\s*(?P<données>.*)",
        "modèle entrée": r"^(?P<entrée>.*)$",
        "balises": {
            "lx": {"entité": {"nom": "entrée", "attributs": ["vedette"], "paramètres": {}, "structure": {"identifiant": {"nom": "vedette", "type": "primaire"}}}, "parent": [{"nom": "dictionnaire", "attribut": "entrées"}]},
            "hm": {"entité": {"nom": "entrée", "attributs": ["homonyme"], "paramètres": {}, "structure": {"identifiant": {"nom": "homonyme", "type": "secondaire"}}}, "parent": None},
            "ps": {"entité": {"nom": "entrée", "attributs": ["classe_grammaticale"], "paramètres": {}, "structure": {}}, "parent": None},
            "sn": {"entité": {"nom": "sens", "attributs": ["acception"], "paramètres": {}, "structure": {"identifiant": {"nom": "acception", "type": "primaire"}}}, "parent": [{"nom": "entrée", "attribut": "entrées"}]},
            "de": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "fra"}, "structure": {"identifiant": {"nom": None, "type": "primaire"}}}, "parent": [{"nom": "sens", "attribut": "définitions"}, {"nom": "entrée", "attribut": "définitions"}]},
            "dn": {"entité": {"nom": "définition", "attributs": ["définition"], "paramètres": {"langue": "eng"}, "structure": {"identifiant": {"nom": None, "type": "primaire"}}}, "parent": [{"nom": "sens", "attribut": "définitions"}, {"nom": "entrée", "attribut": "définitions"}]},
            "xe": {"entité": {"nom": "exemple", "attributs": ["exemple"], "paramètres": {"langue": "fra"}, "structure": {"identifiant": {"nom": None, "type": "primaire"}}}, "parent": [{"nom": "sens", "attribut": "exemples"}, {"nom": "entrée", "attribut": "définitions"}]},
            "xn": {"entité": {"nom": "exemple", "attributs": ["exemple"], "paramètres": {"langue": "eng"}, "structure": {"identifiant": {"nom": None, "type": "primaire"}}}, "parent": [{"nom": "sens", "attribut": "exemples"}, {"nom": "entrée", "attribut": "définitions"}]},
        }
    },
    # La nébuleuse diffuse est plus simple à utiliser, mais moins puissante...
    # "nébuleuse diffuse": {
    #     "modèle ligne": r"^\\(?P<balise>\w*)(?:\s*<(?P<métadonnées>.*)>\s*)? (?P<données>.*)",
    #     "modèle entrée": r"^(?P<entrée>.*)$",
    #     "balises": {
    #         "lex": {"entité": {"nom": "entrée", "attribut": "vedette", "paramètres": {}}},
    #         "hom": {"entité": {"nom": "entrée", "attribut": "homonyme", "paramètres": {}}},
    #         "cla": {"entité": {"nom": "entrée", "attribut": "classe_grammaticale", "paramètres": {}}},
    #         "sns": {"entité": {"nom": "sens", "attribut": "acception", "paramètres": {}}},
    #         "def": {"entité": {"nom": "définition", "attribut": "définition", "paramètres": {"langue": "fra"}}},
    #         "exf": {"entité": {"nom": "exemple", "attribut": "exemple", "paramètres": {"langue": "fra"}}},
    #     }
    # },
    # "MDF": {
    #     "modèle ligne": r"^\\(?P<balise>\w*)(?:\s*<(?P<métadonnées>.*)>\s*)? (?P<données>.*)",
    #     "modèle entrée": r"^(?P<entrée>.*)$",
    #     "balises": {
    #         "lx": {"entité": {"nom": "entrée", "attribut": "vedette", "paramètres": {}}},
    #         "hm": {"entité": {"nom": "entrée", "attribut": "homonyme", "paramètres": {}}},
    #         "ph": {"entité": {"nom": "entrée", "attribut": "phonétique", "paramètres": {}}},
    #         "ps": {"entité": {"nom": "entrée", "attribut": "classe_grammaticale", "paramètres": {}}},
    #         "wr": {"entité": {"nom": "groupe", "attribut": "nom", "paramètres": {"niveau": 1}}},
    #         "se": {"entité": {"nom": "groupe", "attribut": None, "paramètres": {"niveau": 2}}},
    #         "sn": {"entité": {"nom": "sens", "attribut": "acception", "paramètres": {}}},
    #         # "de": {"entité": "définition", "attribut": "définition", "paramètres": {"langue": "fra"}},
    #     }
    # },
    # "Lexika": {
    #     "modèle ligne": r"^(?P<métabalise>[\d.]*)(?P<balise>\w*)\s+(?P<données>.*?)(?:\s*<(?P<métadonnées>.*)>\s*)?$",
    #     "modèle entrée": r"^(?P<entrée>[\d\w\s'-:$|?’]*)\$?(?P<homonyme>\d*)$",
    #     "balises": {
    #         "hw": {"entité": {"nom": "entrée", "attribut": "vedette", "paramètres": {}}},
    #         "ps": {"entité": {"nom": "entrée", "attribut": "classe grammaticale", "paramètres": {}}},
    #         "dff": {"entité": {"nom": "définition", "attribut": "définition", "paramètres": {"langue": "fra"}}},
    #         "dfe": {"entité": {"nom": "définition", "attribut": "définition", "paramètres": {"langue": "eng"}}},
    #         "dfn": {"entité": {"nom": "définition", "attribut": "définition", "paramètres": {"langue": "nep"}}},
    #         "nag": {"entité": {"nom": "définition", "attribut": "définition", "paramètres": {"langue": "hin"}}},
    #
    #     }
    # }
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







