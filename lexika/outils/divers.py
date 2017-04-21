#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.outils
import cchardet
import contextlib
import datetime
import logging
import os


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
                    print("Ouverture du fichier « {} » avec l'encodage « {} » (confiance de {:.2f})".format(self.chemin_accès.split(os.sep)[-1], encodage["encoding"], encodage["confidence"]))
                if 'encoding' in self.kwargs:
                    self.kwargs.pop('encoding')
                self.fichier = open(encoding=encodage['encoding'], *self.args, **self.kwargs)
        else:
            self.fichier = open(encoding=self.encodage_préféré, *self.args, **self.kwargs)
        return self.fichier

    def __exit__(self, type, value, traceback):
        self.fichier.close()
        if value:
            print("Erreur :", value)
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
        print("Temps d'exécution de la tâche « {} » : {} s.".format(self.nom, self.durée))


def créer_journalisation(nom_fichier):
    with lexika.outils.OuvrirFichier(nom_fichier, 'w'):
        pass
    logging.basicConfig(filename=nom_fichier, level=logging.ERROR)
    formateur = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    journalisateur = logging.getLogger()
    gestionnaire_fichier = logging.FileHandler(nom_fichier, encoding="UTF-8")
    gestionnaire_fichier.setFormatter(formateur)
    journalisateur.addHandler(gestionnaire_fichier)
    gestionnaire_console = logging.StreamHandler()
    gestionnaire_console.setFormatter(formateur)
    journalisateur.addHandler(gestionnaire_console)