#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika

import logging
import os
import math


class Lecteur:
    """
    Classe qui permet de lire le fichier source en le partitionnant éventuellement en cas de paraléllisme.
    """
    def __init__(self, chemin_accès):
        self.chemin_accès = chemin_accès
        self.données = []
        self.positions_blocs = []
        if not os.path.isfile(self.chemin_accès):
            logging.critical(_(f"Chemin d'entrée « {self.chemin_accès} » non valide."))
            raise

    def lire_source(self, balise_bloc: str = None):
        """
        Lit le fichier source en ne gardant pas les lignes vides, en concaténant les lignes coupées (ne commençant pas par une balise) et en indexant les positions des blocs d’intérêt le cas échéant (pour le parallélisme).
        """
        with lexika.outils.OuvrirFichier(self.chemin_accès, 'r') as entrée:
            for index, ligne in enumerate(entrée.readlines(), 1):
                if ligne not in [os.linesep, ""]:
                    if ligne.startswith("\\"):
                        self.données.append({"index": index, "ligne": ligne.strip()})
                    else:
                        self.données[-1]["ligne"] = f"{self.données[-1]['ligne'].strip()} {ligne.strip()}"
                if balise_bloc and ligne.startswith(balise_bloc):
                    self.positions_blocs.append(len(self.données) - 1)

    def partitionner(self, nombre_processus: int) -> list:
        """
        Partitionne la source en autant de blocs que nécessaire pour optimiser leur taille relative.
        """
        blocs = {"corps": []}        
        positions_optimales = self.optimiser_index(nombre_processus)
        if positions_optimales[0] != 0:
            blocs["en-tête"] = self.données[0:positions_optimales[0]]
        for position_début, position_fin in zip(positions_optimales, [position for position in positions_optimales[1:]] + [len(self.données)]):
            blocs["corps"].append(self.données[position_début:position_fin])
        self.données = blocs
        
    def optimiser_index(self, nombre_processus: int):
        """
        Optimise les index des blocs.
        """
        taille_optimale = math.ceil(len(self.données[self.positions_blocs[0]:]) / min(len(self.positions_blocs), nombre_processus))
        positions_naïves = range(self.positions_blocs[0], len(self.données), taille_optimale)
        résultat = [] 
        for position_naïve in positions_naïves:
            résultat.append(next((position_bloc for position_bloc in self.positions_blocs if position_bloc >= position_naïve and position_bloc not in résultat), self.positions_blocs[-1]))
        return résultat


class Écriveur:
    """
    Classe qui permet d’écrire dans un fichier.
    """
    def __init__(self, chemin_cible):
        self.chemin_cible = chemin_cible

    def écrire_résultat(self, données):
        with lexika.outils.OuvrirFichier(self.chemin_cible, 'w') as sortie:
            sortie.write(données)

