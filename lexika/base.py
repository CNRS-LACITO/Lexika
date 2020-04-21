#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import gettext
import locale
import logging
import multiprocessing
import sys
import os.path

sys.path.append('..')  # Pour une utilisation locale sans installation.

import lexika


def démarrer_lexika():
    """
    Fonction initiale de lancement de Lexika par le terminal.
    """
    nombre_cœurs = multiprocessing.cpu_count()
    fichier_configuration = "./exemples/yuanga/configuration alphabétique.yml"
    analyseur_syntaxique = argparse.ArgumentParser()

    analyseur_syntaxique.add_argument("-f", help=_(f"Chemin d'accès au fichier de configuration du dictionnaire (par défaut : {fichier_configuration})."), default=fichier_configuration)
    analyseur_syntaxique.add_argument("-p", help=_(f"Lance le processus de manière multicœur, précisez le nombre de cœurs souhaité (par défaut : {nombre_cœurs})."), default=1, type=int, nargs="?", const=nombre_cœurs)
    analyseur_syntaxique.add_argument("-v", help=_(f"Affiche selon le seuil de précision les détails du déroulement du processus (par défaut : 50)."), default=50, type=int, nargs="?", const=30)

    arguments = analyseur_syntaxique.parse_args()

    lexika.outils.créer_journalisation(os.path.join(os.path.dirname(arguments.f), "journal.log"), arguments.v)

    informations = ", ".join([f"{paramètre} = {valeur}" for paramètre, valeur in vars(arguments).items()])
    logging.info(_(f"Lancement de Lexika dans le dossier courant « {os.getcwd()} » avec les paramètres suivants : « {informations} »."))

    configuration = lexika.outils.ClasseConfigurée()
    configuration.configurer(arguments.f)

    nébuleuse = lexika.NébuleuseDeLʼHélice()
    nébuleuse.créer_dictionnaire(arguments.p)

if __name__ == "__main__":
    démarrer_lexika()

