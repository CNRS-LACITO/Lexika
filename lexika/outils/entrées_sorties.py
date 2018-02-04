#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.outils
import os
import math


class Lecteur:
    def __init__(self, chemin_accès):
        self.chemin_accès = chemin_accès
        self.données = []
        self.positions_blocs = []
        if not os.path.isfile(self.chemin_accès):
             raise Exception("Chemin d'entrée non valide")

    def lire_source(self,
                    balise_bloc: str = None):
        with lexika.outils.OuvrirFichier(self.chemin_accès, 'r') as entrée:
            for index, ligne in enumerate(entrée.readlines(), 1):
                if ligne not in [os.linesep, ""]:
                    if ligne.startswith("\\"):
                        self.données.append({"index": index, "ligne": ligne.strip()})
                    else:
                        self.données[-1]["ligne"] = f"{self.données[-1]['ligne'].strip()} {ligne.strip()}"
                if balise_bloc and ligne.startswith(balise_bloc):
                    self.positions_blocs.append(len(self.données) - 1)
                    
    def partitionner(self,  
                     nombre: int) -> list:
        blocs = {"corps": []}
        taille_optimale = math.ceil(len(self.données) / nombre)
        positions_optimales = range(0, len(self.données), taille_optimale)
        if len(self.positions_blocs) < nombre:
            positions_suboptimales = self.positions_blocs
        else:
            positions_suboptimales = [self.positions_blocs[next(index for index, valeur in enumerate(self.positions_blocs) if valeur > position_optimale)] for position_optimale in positions_optimales]
        if positions_suboptimales[0] != 0:
            blocs["en-tête"] = self.données[0:positions_suboptimales[0]]
        for position_début, position_fin in zip(positions_suboptimales, [position - 1 for position in positions_suboptimales[1:]] + [len(self.données)]):
            blocs["corps"].append(self.données[position_début:position_fin])
        self.données = blocs


class Écriveur:
    def __init__(self, chemin_cible):
        self.chemin_cible = chemin_cible

    def écrire_résultat(self, données):
        with lexika.outils.OuvrirFichier(self.chemin_cible, 'w') as sortie:
            sortie.write(données)

