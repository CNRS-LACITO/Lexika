#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cchardet
import colorama
import contextlib
import datetime
import logging
import os

import lexika.outils

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
                    logging.info("Ouverture du fichier « {} » avec l'encodage « {} » (confiance de {:.2f})".format(self.chemin_accès.split(os.sep)[-1], encodage["encoding"], encodage["confidence"]))
                if 'encoding' in self.kwargs:
                    self.kwargs.pop('encoding')
                self.fichier = open(encoding=encodage['encoding'], *self.args, **self.kwargs)
        else:
            self.fichier = open(encoding=self.encodage_préféré, *self.args, **self.kwargs)
        return self.fichier

    def __exit__(self, type, value, traceback):
        self.fichier.close()
        if value:
            logging.error(value)
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
        logging.info("Temps d'exécution de la tâche « {} » : {} s.".format(self.nom, self.durée))


class Témoin:
    """
    Témoin de comportement anormal (avertissement ou erreur) permettant de retrouver les informations posant problème sous la forme d’un message explicite et détaillé.
    """

    compteurs = {"Erreur": 0, "Avertissement": 0, "Information": 0, "Débogage": 0}

    def __init__(self, index, ligne):
        self.niveaux = {"Erreur": 40, "Avertissement": 30, "Information": 20, "Débogage": 10}
        self.index = index
        self.ligne = ligne
        self.description = ""

    def envoyer_message(self, niveau, description):
        Témoin.compteurs[niveau] += 1
        self.description = description
        message = "📖 {} {}\tligne {}\t« {} »\n\t\t🛈 {}".format(niveau, self.compteurs[niveau], self.index, self.ligne, self.description)
        logging.log(self.niveaux[niveau], message)


class GestionnaireConsoleAmélioré(logging.StreamHandler):
    couleurs = {
        'DEBUG': colorama.Style.BRIGHT + colorama.Fore.CYAN,
        'INFO': colorama.Style.BRIGHT + colorama.Fore.GREEN,
        'WARNING': colorama.Style.BRIGHT + colorama.Fore.YELLOW,
        'ERROR': colorama.Style.BRIGHT + colorama.Fore.RED,
        'CRITICAL': colorama.Style.BRIGHT + colorama.Back.RED + colorama.Fore.WHITE
    }

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
    traductions = {# améliorer avec _
        'DEBUG': "DÉBOGAGE",
        'INFO': "INFORMATION",
        'WARNING': "AVERTISSEMENT",
        'ERROR': "ERREUR",
        'CRITICAL': "ERREUR CRITIQUE"
    }

    def format(self, enregistrement):
        return "[{}]\t{}".format(self.traductions[enregistrement.levelname], enregistrement.msg)


def créer_journalisation(nom_fichier):
    colorama.init(autoreset=True)

    with lexika.outils.OuvrirFichier(nom_fichier, 'w'):
        pass

    formateur = FormateurAmélioré()
    journalisateur = logging.getLogger()

    gestionnaire_fichier = logging.FileHandler(nom_fichier, encoding="UTF-8")
    gestionnaire_console = GestionnaireConsoleAmélioré()

    journalisateur.setLevel(10)
    gestionnaire_fichier.setLevel(10)
    gestionnaire_console.setLevel(20)

    gestionnaire_fichier.setFormatter(formateur)
    gestionnaire_console.setFormatter(formateur)

    journalisateur.addHandler(gestionnaire_fichier)
    journalisateur.addHandler(gestionnaire_console)

