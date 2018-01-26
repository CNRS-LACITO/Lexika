#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cchardet
import colorama
import contextlib
import datetime
import importlib.util
import logging
import os

import lexika.outils


def importer_module_personnalisé(nom, chemin):
    spécifications = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spécifications)
    spécifications.loader.exec_module(module)
    return module

#def surdéfinir_classe(classe, chemin):
#    print(classe)
##    try:
#    if os.path.isfile(chemin):
#        classe = getattr(importer_module_personnalisé("", chemin), classe.__name__)
##    except Exception as exception:
##        print(exception)
#    print(classe)
#    return classe

class OuvrirFichier:
    """
    Gestionnaire de contexte permettant d'ouvrir un fichier d'encodage inconnu en l'inférant statistiquement avant.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.chemin_accès = args[0] if args[0] else kwargs['file']
        self.fichier = None
        self.encodage_préféré = "UTF-8"

    def __enter__(self):
        if "r" in self.args[1]:
            if "type" in self.kwargs and self.kwargs["type"] == "interne":
                self.fichier = open(encoding=self.encodage_préféré, *self.args)
            else:
                with open(self.chemin_accès, 'rb') as entrée:
                    buffer = entrée.read()
                    encodage = cchardet.detect(buffer)
                    if not encodage["encoding"]:
                        encodage = {"encoding": self.encodage_préféré, "confidence": 1}
                    logging.info(_(f"Ouverture du fichier « {self.chemin_accès.split(os.sep)[-1]} » avec l'encodage « {encodage['encoding']} »."))
                if 'encoding' in self.kwargs:
                    self.kwargs.pop('encoding')
                self.fichier = open(encoding=encodage['encoding'], *self.args, **self.kwargs)
        else:
            self.fichier = open(encoding=self.encodage_préféré, *self.args, **self.kwargs)
        return self.fichier

    def __exit__(self, type, valeur, trace):
        self.fichier.close()
        if valeur:
            logging.error(valeur)
        return


class Chronométrer(contextlib.ContextDecorator):
    """
    Gestionnaire de contexte permettant de chronométrer le temps d'exécution d'une tâche.
    """
    def __init__(self, nom):
        self.nom = nom
    def __enter__(self):
        self.début = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.durée = (datetime.datetime.now() - self.début).total_seconds()
        print(_(f"Temps d'exécution de la tâche « {self.nom} » : {self.durée} s."))


class Témoin:
    """
    Témoin de comportement anormal (avertissement ou erreur) permettant de retrouver les informations posant problème sous la forme d’un message explicite et détaillé.
    """
    compteurs = {"Erreur critique": 0, 
                 "Erreur": 0, 
                 "Avertissement": 0, 
                 "Information": 0,
                 "Débogage": 0}
    couleurs = {"Débogage": colorama.Fore.CYAN,
                "Information": colorama.Fore.GREEN,
                "Avertissement": colorama.Fore.YELLOW,
                "Erreur": colorama.Fore.RED,
                "Erreur critique": colorama.Back.RED + colorama.Fore.WHITE}

    def __init__(self):
        self.niveaux = {"Erreur critique": 50,  
                        "Erreur": 40,
                        "Avertissement": 30,
                        "Information": 20,
                        "Débogage": 10}
        self.niveau = 0
        self.index = None
        self.ligne = None
        self.nom_abstraction = None
        self.nom_abstraction_appelante = None
        self.message = ""

    def initialiser(self, index, ligne):
        self.index = index
        self.ligne = ligne
        self.nom_abstraction = None
        self.nom_abstraction_appelante = None
        self.message = f"\n📖 Source \tligne {self.index}\t« {self.ligne} »\n"
        self.niveau = 0

    def compléter_message(self, niveau, description):
        Témoin.compteurs[niveau] += 1
        self.niveau = max(self.niveau, self.niveaux[niveau])
        sous_message = _(f" appelée par l'abstraction « {self.nom_abstraction_appelante} »") if self.nom_abstraction_appelante else ""
        self.message += _(f"\t🌀 Abstraction « {self.nom_abstraction} »{sous_message}\n\t\t{self.couleurs[niveau]}🛈 {description}{colorama.Style.RESET_ALL}\n")

    def envoyer_message(self):
        logging.log(self.niveau, f"{self.message}\n" )

    def erreur_critique(self, description):
        self.compléter_message("Erreur critique", description)

    def erreur(self, description):
        self.compléter_message("Erreur", description)

    def avertissement(self, description):
        self.compléter_message("Avertissement", description)

    def information(self, description):
        self.compléter_message("Information", description)

    def débogage(self, description):
        self.compléter_message("Débogage", description)

class GestionnaireConsoleAmélioré(logging.StreamHandler):
    couleurs = {"DEBUG": colorama.Fore.CYAN,
                "INFO": colorama.Fore.GREEN,
                "WARNING": colorama.Fore.YELLOW,
                "ERROR": colorama.Fore.RED,
                "CRITICAL": colorama.Back.RED + colorama.Fore.WHITE}
    
    def emit(self, enregistrement):
        try:
            message = self.format(enregistrement)
            self.stream.write(self.couleurs[enregistrement.levelname] + message + colorama.Style.RESET_ALL)
            self.stream.write(self.terminator)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(enregistrement)


class FormateurAmélioré(logging.Formatter):
    traductions = {"DEBUG": "DÉBOGAGE",
                   "INFO": "INFORMATION",
                   "WARNING": "AVERTISSEMENT",
                   "ERROR": "ERREUR",
                   "CRITICAL": "ERREUR CRITIQUE"}

    def format(self, enregistrement):
        return f"[{self.traductions[enregistrement.levelname]}]\t{enregistrement.msg}"


def créer_journalisation(nom_fichier):
    colorama.init(autoreset=True)

    with lexika.outils.OuvrirFichier(nom_fichier, 'w'):
        pass

    formateur = FormateurAmélioré()
    journalisateur = logging.getLogger()

    gestionnaire_fichier = logging.FileHandler(nom_fichier, encoding="UTF-8")
    gestionnaire_console = GestionnaireConsoleAmélioré()

    journalisateur.setLevel(10)
    gestionnaire_fichier.setLevel(20)
    gestionnaire_console.setLevel(50)

    gestionnaire_fichier.setFormatter(formateur)
    gestionnaire_console.setFormatter(formateur)

    journalisateur.addHandler(gestionnaire_fichier)
    journalisateur.addHandler(gestionnaire_console)

