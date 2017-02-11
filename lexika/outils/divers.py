#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cchardet
import contextlib
import datetime
import os

class OuvrirFichier:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.chemin_accès = args[0] if args[0] else kwargs['file']
        self.fichier = None
        self.taille = 200

    def __enter__(self):
        with open(self.chemin_accès, 'rb') as entrée:
            buffer = entrée.read()
            encodage = cchardet.detect(buffer)
            print("Ouverture du fichier {} avec l'encodage {} (confiance de {:.2f})".format(self.chemin_accès.split(os.sep)[-1], encodage["encoding"], encodage["confidence"]))
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
    def __init__(self, nom):
        self.nom = nom
    def __enter__(self):
        self.début = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.durée = (datetime.datetime.now() - self.début).total_seconds()
        print("{} : {}".format(self.nom, self.durée))