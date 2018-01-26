#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import multiprocessing
import sys

sys.path.append('..')  # Pour une utilisation locale sans installation.

import lexika
import lexika.outils

def main():
    lexika.outils.créer_journalisation("journal.log")
    nombre_cœurs = multiprocessing.cpu_count()
    fichier_configuration = "./exemples/na/configuration.yml"
    analyseur_syntaxique = argparse.ArgumentParser()
    analyseur_syntaxique.add_argument("-f", help=_(f"Chemin d'accès au fichier de configuration du dictionnaire (par défaut : {fichier_configuration})."), default=fichier_configuration)
    analyseur_syntaxique.add_argument("-p", help=_(f"Lance le processus de manière multicœur, précisez le nombre de cœurs souhaité (par défaut : {nombre_cœurs})."), default=1, type=int, nargs="?", const=nombre_cœurs)
    arguments = analyseur_syntaxique.parse_args()
    nébuleuse = lexika.NébuleuseDeLʼHélice(arguments.f)
    nébuleuse.créer_dictionnaire(arguments.p)

if __name__ == "__main__":
    main()
