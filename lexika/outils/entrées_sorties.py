#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import lexika.outils

class Lecteur:
    def __init__(self, chemin_source):
        self.chemin_accès = chemin_source
        self.données = self.lire_source()

    def lire_source(self):
        if os.path.isfile(self.chemin_accès):
            with lexika.outils.OuvrirFichier(self.chemin_accès, 'r') as entrée:
                return ({"index": index, "ligne": ligne.strip()} for index, ligne in enumerate(entrée.readlines(), 1) if ligne not in [os.linesep, ""])
        else:
            raise Exception("Chemin d'entrée non valide")


class Écriveur:
    def __init__(self, chemin_cible):
        self.chemin_cible = chemin_cible

    def écrire_résultat(self, données):
        with lexika.outils.OuvrirFichier(self.chemin_cible, 'w') as sortie:
            sortie.write(données)
