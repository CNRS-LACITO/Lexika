#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

    def __enter__(self):
        with open(self.chemin_accès, 'rb') as entrée:
            buffer = entrée.read()
            encodage = cchardet.detect(buffer)
            print("Ouverture du fichier « {} » avec l'encodage « {} » (confiance de {:.2f})".format(self.chemin_accès.split(os.sep)[-1], encodage["encoding"], encodage["confidence"]))
        if 'encoding' in self.kwargs:
            self.kwargs.pop('encoding')
        self.fichier = open(encoding=encodage['encoding'], *self.args, **self.kwargs)
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
    with open(nom_fichier, 'w'):
        pass
    logging.basicConfig(filename=nom_fichier, level=logging.INFO)
    formateur = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    journalisateur = logging.getLogger()
    gestionnaire_fichier = logging.FileHandler(nom_fichier)
    gestionnaire_fichier.setFormatter(formateur)
    journalisateur.addHandler(gestionnaire_fichier)
    gestionnaire_console = logging.StreamHandler()
    gestionnaire_console.setFormatter(formateur)
    journalisateur.addHandler(gestionnaire_console)