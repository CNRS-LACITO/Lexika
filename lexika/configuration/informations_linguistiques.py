#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika


"""
Nomenclature gérérale :
    – balise : élément de début de ligne d’un fichier de données source (exemples : lx, sn, df…) ;
    – entité linguistique : élément de dictionnaire ou de lexique, hiérarchisé (pouvant contenir d’autres entités ou être contenu dans une autre), correspondant à une information sémantique pour l’être humain (exemples : entrée, sens, définition…) ;
    – attribut linguistique : élément informatif associé à une entité linguistique, ne correspondant pas forcément à une information lisible par l’être humain (exemples : langue, type…)

Principe général :
    La fonction générale lit ligne par ligne le fichien d’entrée (par exemple un fichien au format MDF) ; grâce à une expression rationnelle (« modèle de ligne »), elle décompose chaque ligne en balise, information et éventuellement méta-informations ; la balise est ensuite cherchée dans l’objet « InformationsLinguistiques » ci-dessous pour savoir à quelle entité linguistique elle correspond (dictionnaire « balises » dans l’attribut « formats_entrée »), pour enfin savoir comment elle doit se créer (dictionnaire « entités » dans l’attribut « formats_sortie »), en cherchant sous quelle entité parente se placer et en créant éventuellement d’autres entités selon le format choisi.

Informations générales :
    Du fait de l’architecture logicielle et de la structure de données, il peut y avoir une différence entre les hiérarchies apparente humainement visible et structurelle interne. Par exemple, un commentaire discursif d’une définition sera placé avant celle-ci (balise de commentaire avant la balise de définition dans le fichier source) bien qu’il soit structurellement placé après (entité « commentaire » placé comme enfant de l’entité « définition »). Pour pallier cette difficulté, une entité analysée implaçable dans un parent déjà existant sera entreposée en attente de l’analyse d’un parent adéquat.
    Certaines sources incluent du texte enrichi (style, renvois, etc.), l’architecture tente de garder ces informations selon des expressions rationnelles adaptées (« modèle de style » et « modèle de renvoi »).
    Les « constantes » servent à la création non ambigüe d’identifiants en incorporant des caractères Unicode qui ne doivent pas pouvoir être confondus avec des caractères sémantiques.
    Le tri final des entités à trier se configure par le dictionnaire « entités à trier » qui contient les couples (liste des entités à trier/attribut de tri).
"""

class InformationsLinguistiques:
    """
    Cette classe réunit en un seul objet toutes les informations linguistiques afin de permettre un paramétrage fin par format de la lecture des balises d’entrée et d’écriture des entités linguistiques de sortie, notamment par les langues utilisées et le format des lignes d’entrée et de style. Elle contient aussi les correspondances entre les balises et les entités linguistiques, ainsi que les relations de parenté conditionnelle entre ces dernières.
    Elle décrit les paramétrages de base pour des formats relativement standards, les personnalisations plus poussées ou spécifiques sont à détailler dans le fichier homonyme du dossier « personnalisation », qui agit par surdéfinition de la présente classe.
    Pour le format d’entrée, les balises ont les mots clefs suivants :
        – entité : nom de l’entité linguistique associée ;
        – paramètres : structure dictionnaire regroupant les paramètres intrinsèques à la balise (« langue », « type », etc.) ;
        – tête : « primaire » ou « secondaire », pour définir des environnements blocs exclusifs.
    Pour le format de sortie, les entités linguistiques ont des mots clefs suivants :
        – entités : structure liste regroupant les différentes structures dictionnaires correspondant à des entités linguistiques potentielles :
            – nom : nom de l’entité linguistique ;
            – attributs : structure dictionnaire regroupant les attributs informatifs fournis par l’entrée, l’attribut None correspond à l’information directement fournie en entrée ;
            – structure : structure dictionnaire regroupant les paramètres structurels de l’entité linguistique :
                – identifiant : structure dictionnaire regroupant les paramètres permettant de gérer l’identifiant de l’entité linguistique :
                    – nom : nom de l’identifiant (souvent « identifiant ») ;
                    – type : « primaire » (l’identifiant est la valeur de l’attribut informatif correspondant à None) ou « secondaire » (idem mais concaténé à l’identifiant primaire).
        – parents : structure liste regroupant les différentes structures dictionnaires correspondant à des entités linguistiques parentes potentielles :
            – nom : nom de l’entité linguistique parente ;
            – attribut : nom de l’attribut de l’entité linguistique parente sous lequel va se placer l’entité linguistique ;
            et éventuellement :
            – entité : nom de l’entité de sortie à appeler pour créer une entité linguistique parente (par défaut ou préliminaire selon sa position) ;
            – attributs : structure dictionnaire regroupant les attributs informatifs à créer automatiquement.
    """

    def __init__(self, statuts_langues):
        self.créateurs = {
            "nébuleuse d'Orion": lambda configuration: lexika.NébuleuseDʼOrion(configuration),
            "nébuleuse d'Oméga": lambda configuration: lexika.NébuleuseDʼOméga(configuration),
        }

        self.statuts_langues = {
            "source 1": statuts_langues["source 1"] if "source 1" in statuts_langues else None,
            "source 2": statuts_langues["source 2"] if "source 2" in statuts_langues else None,
            "cible 1": statuts_langues["cible 1"] if "cible 1" in statuts_langues else None,
            "cible 2": statuts_langues["cible 2"] if "cible 2" in statuts_langues else None,
            "cible 3": statuts_langues["cible 3"] if "cible 3" in statuts_langues else None,
            "cible 4": statuts_langues["cible 4"] if "cible 4" in statuts_langues else None,
        }

        self.formats_entrée = {
            "MDF": {
                "créateur": "nébuleuse d'Orion",
                "modèle de ligne": r"^\\(?P<balise>\w*) \s*(?P<données>.*)",
                "modèle de style": r"(?P<ensemble>(?P<style>{0}):(?P<texte>[\w,.;:!?/\[\]\(\){{}}\~‘’'–_*+-]+))|(?P<ensemble>\|(?P<style>{0}){{(?P<texte>[\w\s\[\],.;:!?/\[\]\(\){{}}\~‘’'–_*+-]+)}})".format(
                    "|".join(["fl", "fv", "fn", "fr", "fe", "fs", "fi"])),
                "balises": {
                    "_sh": None,
                    "lx": {"entité": "vedette", "paramètres": {}, "tête": "primaire"},
                    "se": {"entité": "sous-vedette", "paramètres": {}, "tête": "secondaire"},

                    "hm": {"entité": "homonyme", "paramètres": {}},

                    "lc": {"entité": "forme de citation", "paramètres": {}},
                    "a": {"entité": "allophone", "paramètres": {}},

                    "ps": {"entité": "classe grammaticale", "paramètres": {}},

                    "ph": {"entité": "phonétique", "paramètres": {}},

                    "sn": {"entité": "acception", "paramètres": {}},

                    "dv": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["source 1"]}},
                    "de": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "dn": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "dr": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["cible 3"]}},

                    "gv": {"entité": "glose", "paramètres": {"langue": self.statuts_langues["source 1"]}},
                    "ge": {"entité": "glose", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "gn": {"entité": "glose", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "gr": {"entité": "glose", "paramètres": {"langue": self.statuts_langues["cible 3"]}},

                    "re": {"entité": "équivalent", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "rn": {"entité": "équivalent", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "rr": {"entité": "équivalent", "paramètres": {"langue": self.statuts_langues["cible 3"]}},

                    "lt": {"entité": "sens littéral", "paramètres": {}},

                    "mr": {"entité": "morphologie", "paramètres": {}},

                    "sc": {"entité": "nom scientifique", "paramètres": {}},

                    "xv": {"entité": "exemple", "paramètres": {"langue": self.statuts_langues["source 1"]}},
                    "xe": {"entité": "traduction d'exemple", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "xn": {"entité": "traduction d'exemple", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "xr": {"entité": "traduction d'exemple", "paramètres": {"langue": self.statuts_langues["cible 3"]}},
                    "xg": {"entité": "glose interlinéaire", "paramètres": {}},
                    "xc": {"entité": "commentaire d'exemple", "paramètres": {}},
                    "rf": {"entité": "référence", "paramètres": {}},

                    "uv": {"entité": "note", "paramètres": {"langue": self.statuts_langues["source 1"], "type": "usage"}},
                    "ue": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "usage"}},
                    "un": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 2"], "type": "usage"}},
                    "ur": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 3"], "type": "usage"}},

                    "nq": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "interrogation"}},
                    "nt": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "général"}},
                    "ng": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "grammaire"}},
                    "np": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "phonologie"}},
                    "nd": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "discours"}},
                    "na": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "anthropologie"}},
                    "ns": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "sociolinguistique"}},

                    "va": {"entité": "variante", "paramètres": {}},
                    "ve": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "variante"}},
                    "vn": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 2"], "type": "variante"}},
                    "vr": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 3"], "type": "variante"}},

                    "bw": {"entité": "relation sémantique", "paramètres": {"type": "emprunt"}},
                    "sy": {"entité": "relation sémantique", "paramètres": {"type": "synonyme"}},
                    "an": {"entité": "relation sémantique", "paramètres": {"type": "antonyme"}},
                    "cf": {"entité": "relation sémantique", "paramètres": {"type": "renvoi"}},
                    "ce": {"entité": "traduction de relation sémantique", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "cn": {"entité": "traduction de relation sémantique", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "cr": {"entité": "traduction de relation sémantique", "paramètres": {"langue": self.statuts_langues["cible 3"]}},

                    "lf": {"entité": "type de relation sémantique", "paramètres": {}},
                    "lv": {"entité": "cible de relation sémantique", "paramètres": {}},
                    "le": {"entité": "traduction de relation sémantique", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "ln": {"entité": "traduction de relation sémantique", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "lr": {"entité": "traduction de relation sémantique", "paramètres": {"langue": self.statuts_langues["cible 3"]}},

                    "sd": {"entité": "domaine sémantique", "paramètres": {}},
                    "is": {"entité": "index sémantique", "paramètres": {}},

                    "th": {"entité": "thésaurus", "paramètres": {}},

                    "bb": {"entité": "référence bibliographique", "paramètres": {}},

                    "rd": {"entité": "reduplication", "paramètres": {}},

                    "ev": {"entité": "information encyclopédique", "paramètres": {"langue": self.statuts_langues["source 1"]}},
                    "ee": {"entité": "information encyclopédique", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "en": {"entité": "information encyclopédique", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "er": {"entité": "information encyclopédique", "paramètres": {"langue": self.statuts_langues["cible 3"]}},

                    "ov": {"entité": "restriction", "paramètres": {"langue": self.statuts_langues["source 1"]}},
                    "oe": {"entité": "restriction", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "on": {"entité": "restriction", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "or": {"entité": "restriction", "paramètres": {"langue": self.statuts_langues["cible 3"]}},

                    "et": {"entité": "étymologie", "paramètres": {}},
                    "el": {"entité": "langue d'étymologie", "paramètres": {}},
                    "eg": {"entité": "glose d'étymologie", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "es": {"entité": "source d'étymologie", "paramètres": {}},
                    "ec": {"entité": "note", "paramètres": {"langue": self.statuts_langues["source 1"], "type": "étymologie"}},

                    "dt": {"entité": "date", "paramètres": {}},
                    "so": {"entité": "source", "paramètres": {}},
                    "st": {"entité": "statut", "paramètres": {}},

                    "pd": {"entité": "paradigme", "paramètres": {}},
                    "pdl": {"entité": "type de paradigme", "paramètres": {}},
                    "pdv": {"entité": "valeur de paradigme", "paramètres": {"langue": self.statuts_langues["source 1"]}},
                    "pde": {"entité": "valeur de paradigme", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "pdn": {"entité": "valeur de paradigme", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "pdr": {"entité": "valeur de paradigme", "paramètres": {"langue": self.statuts_langues["cible 3"]}},
                    "pdc": {"entité": "commentaire de paradigme", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "1s": {"entité": "paradigme", "paramètres": {"nombre grammatical": "singulier", "personne grammaticale": "première"}},
                    "1d": {"entité": "paradigme", "paramètres": {"nombre grammatical": "duel", "personne grammaticale": "première"}},
                    "1t": {"entité": "paradigme", "paramètres": {"nombre grammatical": "triel", "personne grammaticale": "première"}},
                    "1p": {"entité": "paradigme", "paramètres": {"nombre grammatical": "pluriel", "personne grammaticale": "première"}},
                    "1i": {"entité": "paradigme", "paramètres": {"nombre grammatical": "inclusif", "personne grammaticale": "première"}},
                    "1e": {"entité": "paradigme", "paramètres": {"nombre grammatical": "exclusif", "personne grammaticale": "première"}},
                    "2s": {"entité": "paradigme", "paramètres": {"nombre grammatical": "singulier", "personne grammaticale": "deuxième"}},
                    "2d": {"entité": "paradigme", "paramètres": {"nombre grammatical": "duel", "personne grammaticale": "deuxième"}},
                    "2t": {"entité": "paradigme", "paramètres": {"nombre grammatical": "triel", "personne grammaticale": "deuxième"}},
                    "2p": {"entité": "paradigme", "paramètres": {"nombre grammatical": "pluriel", "personne grammaticale": "deuxième"}},
                    "3s": {"entité": "paradigme", "paramètres": {"nombre grammatical": "singulier", "personne grammaticale": "troisième"}},
                    "3d": {"entité": "paradigme", "paramètres": {"nombre grammatical": "duel", "personne grammaticale": "troisième"}},
                    "3t": {"entité": "paradigme", "paramètres": {"nombre grammatical": "triel", "personne grammaticale": "troisième"}},
                    "3p": {"entité": "paradigme", "paramètres": {"nombre grammatical": "pluriel", "personne grammaticale": "troisième"}},
                    "4s": {"entité": "paradigme", "paramètres": {"nombre grammatical": "singulier", "personne grammaticale": "inanimé"}},
                    "4d": {"entité": "paradigme", "paramètres": {"nombre grammatical": "duel", "personne grammaticale": "inanimé"}},
                    "4t": {"entité": "paradigme", "paramètres": {"nombre grammatical": "triel", "personne grammaticale": "inanimé"}},
                    "4p": {"entité": "paradigme", "paramètres": {"nombre grammatical": "pluriel", "personne grammaticale": "inanimé"}},
                    "pl": {"entité": "paradigme", "paramètres": {"nombre grammatical": "pluriel"}},
                    # "vpl": {"entité": "variante de forme plurielle", "paramètres": {"langue": self.statuts_langues["source 1"]}},
                    "pc": {"entité": "média", "paramètres": {"type": "image"}},
                }
            },
            "Lexware": {
                "créateur": "nébuleuse d'Oméga",
                "modèle de ligne": r"^(?P<acception>\d*)(?P<profondeur>[.]*)(?P<balise>[\w]*)\s*(?P<données>.*)",
                "modèle de renvoi automatique": r"(?P<ensemble>\\lang{(?P<cible>[¹²³⁴\d\w\s~\(\)\/-]+)})",
                "balises": {
                    "hw": {"entité": "vedette", "paramètres": {}, "tête": "primaire"},
                    "hix": {"entité": "homonyme", "paramètres": {}},
                    "ps": {"entité": "classe grammaticale", "paramètres": {}},
                    "dff": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "dfe": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["cible 2"]}},
                    "dfn": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["cible 4"]}},
                    "nag": {"entité": "définition", "paramètres": {"langue": self.statuts_langues["cible 3"]}},
                    "dfbot": {"entité": "nom scientifique", "paramètres": {}},
                    "dfi": {"entité": "équivalent", "paramètres": {"langue": self.statuts_langues["cible 1"]}},
                    "emp": {"entité": "note", "paramètres": {"langue": self.statuts_langues["cible 1"], "type": "usage"}},
                }
            },
        }

        self.formats_sortie = {
            "LMF": {
                "modèle de renvoi": r"^(?P<entrée_lexicale>[\w\s~\[\].,\p{Spacing Modifier Letters}#$-]+?)(?P<numéro_dʼhomonyme>[\d]*)$",
                "constantes": {"entrée lexicale": "Ⓔ", "numéro d'homonyme": "Ⓗ", "sous-entrée lexicale": "ⓔ", "sens": "Ⓢ"},
                "entités à trier": {"entrées lexicales": "identifiant"},
                "entités à extraire": [{"parent": {"entité": "entrée lexicale", "attribut": "entrées lexicales", "nom": "entrée principale"}, "enfant": {"entité": "sous-entrée lexicale", "attribut": "sous-entrées lexicales", "nom": "sous-entrée"}}],
                "entités à lier": [{"lemmes": "lexeme"}],
                "entités": {
                    "informations globales": {"entités": {"nom": "informations globales", "attributs": {}, "paramètres": {}, "structure": {}},
                                              "parents": "/"},
                    "dictionnaire": {"entités": {"nom": "dictionnaire", "attributs": {}, "structure": {}},
                                     "parents": "/"},
                    "langue": {"entités": {"nom": "langue", "attributs": {}, "structure": {}},
                               "parents": [{"nom": "informations globales", "attribut": "langues"}]},
                    "entrée": {"entités": [{"nom": "entrée lexicale", "attributs": {},
                                            "structure": {"tête": True, "identifiant": {"nom": "identifiant", "type": "primaire"}}}],
                               "parents": [{"nom": "dictionnaire", "attribut": "entrées lexicales"}]},
                    "sous-entrée": {"entités": [{"nom": "sous-entrée lexicale", "attributs": {},
                                                 "structure": {"tête": True, "identifiant": {"nom": "identifiant", "type": "primaire"}}}],
                                    "parents": [{"nom": "entrée lexicale", "attribut": "sous-entrées lexicales"}]},
                    "vedette": {"entités": [{"nom": "lemme", "attributs": {"lexeme": None}, "structure": {}}],
                                "parents": [{"entité": "entrée", "attributs": {}, "informations à copier": {"identifiant": "lexeme"}},
                                            {"nom": "entrée lexicale", "attribut": "lemmes"}]},
                    "sous-vedette": {"entités": [{"nom": "lemme", "attributs": {"lexeme": None}, "structure": {}}],
                                     "parents": [{"entité": "sous-entrée", "attributs": {}, "informations à copier": {"identifiant": "lexeme"}},
                                                 {"nom": "sous-entrée lexicale", "attribut": "lemmes"}]},
                    "homonyme": {"entités": [{"nom": "entrée lexicale", "attributs": {"numéro d'homonyme": None},
                                              "structure": {"identifiant": {"nom": "numéro d'homonyme", "type": "secondaire"}}}],
                                 "parents": None},
                    "classe grammaticale": {"entités": [{"nom": "entrée lexicale", "attributs": {"partie du discours": None}, "structure": {}},
                                                        {"nom": "sous-entrée lexicale", "attributs": {"partie du discours": None}, "structure": {}}],
                                            "parents": None},
                    "variante": {"entités": [{"nom": "représentation de forme", "attributs": {"variante": None}, "structure": {}}],
                                 "parents": [{"nom": "lemme", "attribut": "représentations"}]},
                    "allophone": {"entités": [{"nom": "représentation de forme", "attributs": {"allophone": None}, "structure": {}}],
                                  "parents": [{"nom": "lemme", "attribut": "représentations"}]},
                    "phonétique": {"entités": [{"nom": "représentation de forme", "attributs": {"phonétique": None}, "structure": {}}],
                                   "parents": [{"nom": "lemme", "attribut": "représentations"}]},
                    "ton": {"entités": [{"nom": "représentation de forme", "attributs": {"ton": None}, "structure": {}}],
                                   "parents": [{"nom": "lemme", "attribut": "représentations"}]},
                    "forme de citation": {"entités": [{"nom": "représentation de forme", "attributs": {"phonétique de surface": None}, "structure": {}}],
                                   "parents": [{"nom": "lemme", "attribut": "représentations"}]},
                    "acception": {"entités": [{"nom": "sens", "attributs": {"numéro de sens": None},
                                               "structure": {"identifiant": {"nom": "numéro de sens", "type": "primaire"}}}],
                                  "parents": [{"nom": "entrée lexicale", "attribut": "sens"},
                                              {"nom": "sous-entrée lexicale", "attribut": "sens"}]},
                    "glose": {"entités": [{"nom": "définition", "attributs": {"glose": None}, "structure": {}}],
                              "parents": [{"nom": "sens", "attribut": "définitions"},
                                          {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "définition": {"entités": [{"nom": "définition", "attributs": {"définition": None}, "structure": {}}],
                                   "parents": [{"nom": "sens", "attribut": "définitions"},
                                               {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "nom scientifique": {"entités": [{"nom": "déclaration", "attributs": {"nom scientifique": None}, "structure": {}}],
                                         "parents": [{"nom": "définition", "attribut": "déclarations"},
                                                     {"entité": "définition", "attributs": {}}]},
                    "sens littéral": {"entités": [{"nom": "représentation de texte", "attributs": {"sens littéral": None}, "structure": {}},
                                                  {"nom": "définition", "attributs": {"sens littéral": None}, "structure": {}},
                                                  {"nom": "traduction de relation sémantique", "attributs": {"sens littéral": None}, "structure": {}}],
                                      "parents": None},
                    "morphologie": {"entités": [{"nom": "paradigme", "attributs": {"morphologie": None}, "structure": {}}],
                                    "parents": [{"nom": "sens", "attribut": "définitions"},
                                                {"entité": "acception", "attributs": {"numéro de sens": "0"},
                                                 "informations": {}}]},
                    "exemple": {
                        "entités": [{"nom": "représentation de texte", "attributs": {"forme écrite": None}, "structure": {}}],
                        "parents": [{"entité": "contexte", "attributs": {"type": "exemple"}},
                                    {"nom": "contexte", "attribut": "représentations de texte"}]},
                    "traduction d'exemple": {
                        "entités": [{"nom": "représentation de texte", "attributs": {"forme écrite": None}, "structure": {}}],
                        "parents": [{"nom": "contexte", "attribut": "représentations de texte"},
                                    {"entité": "contexte", "attributs": {"type": "exemple"}}]},
                    "commentaire d'exemple": {
                        "entités": [{"nom": "déclaration", "attributs": {"commentaire": None}, "structure": {}}],
                        "parents": [{"nom": "contexte", "attribut": "déclarations"},
                                    {"entité": "contexte", "attributs": {"type": "exemple"}}]},
                    "contexte": {"entités": [{"nom": "contexte", "attributs": {"type": None}, "structure": {}}],
                                 "parents": [{"nom": "sens", "attribut": "contextes"},
                                             {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "équivalent": {"entités": [{"nom": "équivalent", "attributs": {"traduction": None}, "structure": {}}],
                                   "parents": [{"nom": "sens", "attribut": "équivalents"},
                                               {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "note": {"entités": [{"nom": "déclaration", "attributs": {"note": None}, "structure": {}}],
                             "parents": [{"nom": "définition", "attribut": "déclarations"},
                                         {"entité": "définition", "attributs": {}}]},
                    "information encyclopédique": {"entités": [{"nom": "déclaration", "attributs": {"information encyclopédique": None}, "structure": {}}],
                             "parents": [{"nom": "définition", "attribut": "informations encyclopédiques"},
                                         {"entité": "définition", "attributs": {}}]},
                    "étymologie": {"entités": [{"nom": "déclaration", "attributs": {"étymologie": None}, "structure": {}}],
                                   "parents": [{"nom": "définition", "attribut": "déclarations"},
                                               {"entité": "définition", "attributs": {}}]},
                    "type de relation sémantique": {"entités": [{"nom": "relation sémantique", "attributs": {"type": None}, "structure": {}}],
                                                    "parents": [{"nom": "sens", "attribut": "équivalents"},
                                                                {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "cible de relation sémantique": {"entités": [{"nom": "relation sémantique", "attributs": {"cible": None}, "structure": {"factorisable": True}}],
                                                     "parents": None},
                    "relation sémantique": {"entités": [{"nom": "relation sémantique", "attributs": {"cible": None}, "structure": {}}],
                                            "parents": [{"nom": "sens", "attribut": "équivalents"},
                                                        {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "type de paradigme": {"entités": [{"nom": "paradigme", "attributs": {"nom": None}, "structure": {}}],
                                          "parents": [{"nom": "sens", "attribut": "paradigmes"},
                                                      {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "valeur de paradigme": {"entités": [{"nom": "paradigme", "attributs": {"paradigme": None}, "structure": {"factorisable": True}}],
                                            "parents": None},
                    "commentaire de paradigme": {"entités": [{"nom": "commentaire de paradigme", "attributs": {"commentaire": None}, "structure": {"factorisable": True}}],
                                            "parents": [{"nom": "paradigme", "attribut": "commentaires de paradigme"},
                                                      {"entité": "type de paradigme", "attributs": {"test": "test"}}]},
                    "paradigme": {"entités": [{"nom": "représentation de forme", "attributs": {"forme écrite": None}, "structure": {}}],
                                  "parents": [{"entité": "forme de mot", "attributs": {}, "informations à transférer": {"nombre grammatical": "nombre grammatical", "personne grammaticale": "personne grammaticale"}},
                                              {"nom": "forme de mot", "attribut": "représentations de forme"}]},
                    "forme apparentée": {"entités": [{"nom": "forme apparentée", "attributs": {"cible": None}, "structure": {}}],
                                         "parents": [{"nom": "entrée lexicale", "attribut": "formes apparentées"}]},
                    "traduction de relation sémantique": {
                        "entités": [{"nom": "traduction de relation sémantique", "attributs": {"traduction": None}, "structure": {}}],
                        "parents": [{"nom": "relation sémantique", "attribut": "traductions"}]},
                    "domaine sémantique": {"entités": [{"nom": "domaine sémantique", "attributs": {"domaine sémantique": None}, "structure": {}}],
                                           "parents": [{"nom": "sens", "attribut": "domaines sémantiques"},
                                                       {"entité": "acception", "attributs": {"numéro de sens": "0"}}]},
                    "forme duelle": {"entités": [{"nom": "représentation de forme", "attributs": {"forme écrite": None}, "structure": {}}],
                                     "parents": [{"entité": "forme de mot", "attributs": {"nombre grammatical": "duel"}},
                                                 {"nom": "forme de mot", "attribut": "représentations de forme"}]},
                    "forme plurielle": {"entités": [{"nom": "représentation de forme", "attributs": {"forme écrite": None}, "structure": {}}],
                                        "parents": [{"entité": "forme de mot", "attributs": {"nombre grammatical": "pluriel"}},
                                                    {"nom": "forme de mot", "attribut": "représentations de forme"}]},
                    "variante de forme plurielle": {"entités": [{"nom": "représentation de forme", "attributs": {"variante": None}, "structure": {}}],
                                                    "parents": [{"nom": "forme de mot", "attribut": "variantes"},
                                                                {"entité": "forme de mot", "attributs": {"nombre grammatical": "pluriel"}}]},
                    "forme de mot": {"entités": [{"nom": "forme de mot", "attributs": {}, "structure": {}}],
                                     "parents": [{"nom": "entrée lexicale", "attribut": "formes de mot"}]},
                    "date": {"entités": [{"nom": "entrée lexicale", "attributs": {"date": None}, "structure": {}}],
                             "parents": None},
                    "source": {"entités": [{"nom": "entrée lexicale", "attributs": {"source": None}, "structure": {}}, ],
                               "parents": None},
                    "média": {"entités": [{"nom": "média", "attributs": {"chemin": None}, "structure": {}}],
                              "parents": [{"nom": "entrée lexicale", "attribut": "médias"}]},
                }
            },
            "LMF bis": {
                "modèle de renvoi": r"^(?P<entrée_lexicale>[\w\s~\[\].-]+?)(?P<numéro_dʼhomonyme>[\d]*)$",
                "constantes": {"entrée lexicale": "Ⓔ", "numéro d'homonyme": "Ⓗ", "sous-entrée lexicale": "ⓔ", "sens général": "Ⓢ", "sens": "ⓢ"},
                "entités à trier": {"entrées lexicales": "identifiant"},
                "entités à extraire": [{"parent": {"entité": "entrée lexicale", "attribut": "entrées lexicales", "nom": "entrée principale"}, "enfant": {"entité": "sous-entrée lexicale", "attribut": "sous-entrées lexicales", "nom": "sous-entrée"}}],
                "entités à lier": [{"lemmes": "lexeme"}],
                "entités": {
                    "informations globales": {"entités": {"nom": "informations globales", "attributs": {}, "paramètres": {}, "structure": {}},
                                              "parents": "/"},
                    "dictionnaire": {"entités": {"nom": "dictionnaire", "attributs": {}, "structure": {}},
                                     "parents": "/"},
                    "langue": {"entités": {"nom": "langue", "attributs": {}, "structure": {}},
                               "parents": [{"nom": "informations globales", "attribut": "langues"}]},
                    "entrée": {"entités": [{"nom": "entrée lexicale", "attributs": {},
                                            "structure": {"tête": True, "identifiant": {"nom": "identifiant", "type": "primaire"}}}],
                               "parents": [{"nom": "dictionnaire", "attribut": "entrées lexicales"}]},
                    "sous-entrée": {"entités": [{"nom": "sous-entrée lexicale", "attributs": {},
                                                 "structure": {"tête": True, "identifiant": {"nom": "identifiant", "type": "primaire"}}}],
                                    "parents": [{"nom": "entrée lexicale", "attribut": "sous-entrées lexicales"}]},
                    "vedette": {"entités": [{"nom": "lemme", "attributs": {"forme écrite": None}, "structure": {}}],
                                "parents": [{"entité": "entrée", "attributs": {}, "informations à copier": {"identifiant": "forme écrite"}},
                                            {"nom": "entrée lexicale", "attribut": "lemmes"}]},
                    "sous-vedette": {"entités": [{"nom": "lemme", "attributs": {"forme écrite": None}, "structure": {}}],
                                     "parents": [{"entité": "sous-entrée", "attributs": {}, "informations à copier": {"identifiant": "forme écrite"}},
                                                 {"nom": "sous-entrée lexicale", "attribut": "lemmes"}]},
                    "homonyme": {"entités": [{"nom": "entrée lexicale", "attributs": {"numéro d'homonyme": None},
                                              "structure": {"identifiant": {"nom": "numéro d'homonyme", "type": "secondaire"}}}],
                                 "parents": None},
                    "classe grammaticale": {"entités": [{"nom": "entrée lexicale", "attributs": {"partie du discours": None}, "structure": {}},
                                                        {"nom": "sous-entrée lexicale", "attributs": {"partie du discours": None}, "structure": {}}],
                                            "parents": None},
                    "variante": {"entités": [{"nom": "représentation de forme", "attributs": {"phonétique": None}, "structure": {}}],
                                 "parents": [{"nom": "lemme", "attribut": "représentations"}]},
                    "phonétique": {"entités": [{"nom": "représentation de forme", "attributs": {"phonétique": None}, "structure": {}}],
                                   "parents": [{"nom": "lemme", "attribut": "représentations"}]},
                    "sens général": {"entités": [{"nom": "sens général", "attributs": {"numéro de sens": None},
                                                  "structure": {"identifiant": {"nom": "numéro de sens", "type": "primaire"}}}],
                                     "parents": [{"nom": "entrée lexicale", "attribut": "sens"},
                                                 {"nom": "sous-entrée lexicale", "attribut": "sens"}]},
                    "acception": {"entités": [{"nom": "sens", "attributs": {"numéro de sens": None},
                                               "structure": {"identifiant": {"nom": "numéro de sens", "type": "primaire"}}}],
                                  "parents": [{"nom": "sens général", "attribut": "sens"},
                                              {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "glose": {"entités": [{"nom": "définition", "attributs": {"glose": None}, "structure": {}}],
                              "parents": [{"nom": "sens général", "attribut": "définitions"},
                                          {"nom": "sens", "attribut": "définitions"},
                                          {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "définition": {"entités": [{"nom": "définition", "attributs": {"définition": None}, "structure": {}}],
                                   "parents": [{"nom": "sens général", "attribut": "définitions"},
                                               {"nom": "sens", "attribut": "définitions"},
                                               {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "nom scientifique": {"entités": [{"nom": "déclaration", "attributs": {"nom scientifique": None}, "structure": {}}],
                                         "parents": [{"nom": "définition", "attribut": "déclarations"},
                                                     {"entité": "définition", "attributs": {}}]},
                    "sens littéral": {"entités": [{"nom": "représentation de texte", "attributs": {"sens littéral": None}, "structure": {}},
                                                  {"nom": "définition", "attributs": {"sens littéral": None}, "structure": {}},
                                                  {"nom": "traduction de relation sémantique", "attributs": {"sens littéral": None}, "structure": {}}],
                                      "parents": None},
                    "morphologie": {"entités": [{"nom": "paradigme", "attributs": {"morphologie": None}, "structure": {}}],
                                    "parents": [{"nom": "sens général", "attribut": "définitions"},
                                                {"nom": "sens", "attribut": "définitions"},
                                                {"entité": "sens général", "attributs": {"numéro de sens": "0"},
                                                 "informations": {}}]},
                    "exemple": {"entités": [{"nom": "représentation de texte", "attributs": {"forme écrite": None}, "structure": {}}],
                                "parents": [{"entité": "contexte", "attributs": {"type": "exemple"}},
                                            {"nom": "contexte", "attribut": "représentations de texte"}]},
                    "traduction d'exemple": {
                        "entités": [{"nom": "représentation de texte", "attributs": {"forme écrite": None}, "structure": {}}],
                        "parents": [{"nom": "contexte", "attribut": "représentations de texte"},
                                    {"entité": "contexte", "attributs": {"type": "exemple"}}]},
                    "contexte": {"entités": [{"nom": "contexte", "attributs": {"type": None}, "structure": {}}],
                                 "parents": [{"nom": "sens général", "attribut": "contextes"},
                                             {"nom": "sens", "attribut": "contextes"},
                                             {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "équivalent": {"entités": [{"nom": "équivalent", "attributs": {"traduction": None}, "structure": {}}],
                                   "parents": [{"nom": "sens général", "attribut": "équivalents"},
                                               {"nom": "sens", "attribut": "équivalents"},
                                               {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "note": {"entités": [{"nom": "déclaration", "attributs": {"note": None}, "structure": {}}],
                             "parents": [{"nom": "définition", "attribut": "déclarations"},
                                         {"entité": "définition", "attributs": {}}]},
                    "étymologie": {"entités": [{"nom": "déclaration", "attributs": {"étymologie": None}, "structure": {}}],
                                   "parents": [{"nom": "définition", "attribut": "déclarations"},
                                               {"entité": "définition", "attributs": {}}]},
                    "type de relation sémantique": {"entités": [{"nom": "relation sémantique", "attributs": {"type": None}, "structure": {}}],
                                                    "parents": [{"nom": "sens général", "attribut": "équivalents"},
                                                                {"nom": "sens", "attribut": "équivalents"},
                                                                {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "cible de relation sémantique": {"entités": [{"nom": "relation sémantique", "attributs": {"cible": None}, "structure": {}}],
                                                     "parents": None},
                    "relation sémantique": {"entités": [{"nom": "relation sémantique", "attributs": {"cible": None}, "structure": {}}],
                                            "parents": [{"nom": "sens général", "attribut": "équivalents"},
                                                        {"nom": "sens", "attribut": "équivalents"},
                                                        {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "type de paradigme": {"entités": [{"nom": "paradigme", "attributs": {"nom": None}, "structure": {}}],
                                          "parents": [{"nom": "sens général", "attribut": "paradigmes"},
                                                      {"nom": "sens", "attribut": "paradigmes"},
                                                      {"entité": "sens général", "attributs": {"numéro de sens": "0"}}]},
                    "valeur de paradigme": {"entités": [{"nom": "paradigme", "attributs": {"paradigme": None}, "structure": {}}],
                                            "parents": None},
                    "forme apparentée": {"entités": [{"nom": "forme apparentée", "attributs": {"cible": None}, "structure": {}}],
                                         "parents": [{"nom": "entrée lexicale", "attribut": "formes apparentées"}]},
                    "traduction de relation sémantique": {
                        "entités": [{"nom": "traduction de relation sémantique", "attributs": {"traduction": None}, "structure": {}}],
                        "parents": [{"nom": "relation sémantique", "attribut": "traductions"}]},
                    "domaine sémantique": {"entités": [{"nom": "champ disciplinaire", "attributs": {"domaine sémantique": None}, "structure": {}}],
                                           "parents": [{"nom": "sens général", "attribut": "définitions"},
                                                       {"nom": "sens", "attribut": "définitions"},
                                                       {"entité": "sens général", "attributs": {"numéro de sens": "0"},
                                                        "informations": {}}]},
                    "forme duelle": {"entités": [{"nom": "représentation de forme", "attributs": {"forme écrite": None}, "structure": {}}],
                                     "parents": [{"entité": "forme de mot", "attributs": {"nombre grammatical": "duel"}},
                                                 {"nom": "forme de mot", "attribut": "représentations de forme"}]},
                    "forme plurielle": {"entités": [{"nom": "représentation de forme", "attributs": {"forme écrite": None}, "structure": {}}],
                                        "parents": [{"entité": "forme de mot", "attributs": {"nombre grammatical": "pluriel"}},
                                                    {"nom": "forme de mot", "attribut": "représentations de forme"}]},
                    "variante de forme plurielle": {"entités": [{"nom": "représentation de forme", "attributs": {"variante": None}, "structure": {}}],
                                                    "parents": [{"nom": "forme de mot", "attribut": "variantes"},
                                                                {"entité": "forme de mot", "attributs": {"nombre grammatical": "pluriel"}}]},
                    "forme de mot": {"entités": [{"nom": "forme de mot", "attributs": {}, "structure": {}}],
                                     "parents": [{"nom": "entrée lexicale", "attribut": "formes de mot"}]},
                    "date": {"entités": [{"nom": "entrée lexicale", "attributs": {"date": None}, "structure": {}}],
                             "parents": None},
                    "source": {"entités": [{"nom": "entrée lexicale", "attributs": {"source": None}, "structure": {}}, ],
                               "parents": None},
                    "média": {"entités": [{"nom": "média", "attributs": {"chemin": None}, "structure": {}}],
                              "parents": [{"nom": "entrée lexicale", "attribut": "médias"}]},
                }
            }
        }
