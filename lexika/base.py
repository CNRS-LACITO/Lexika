#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys

# sys.path.append(os.path.join(os.getcwd(), "lexika"))
# sys.path.append(os.path.join(os.getcwd()))
sys.path.append('..')

import lexika
import lexika.outils
import locale
import gettext

#langue_système = locale.getlocale()[0].split("_")[0] if locale.getlocale()[0] else "fr"
#langue_préférée = gettext.translation("messages", localedir="internationalisation", languages=[langue_système], fallback=True)
#langue_préférée.install()

def main():
    # Création des éléments techniques divers.
    lexika.outils.créer_journalisation("journal.log")

    # Fichier de configuration par défaut du dictionnaire (si aucun argument fourni à la ligne de commande), fait par l’interface graphique voire à la main en respectant bien le modèle.
    source_configuration = "./exemples/mwotlap/configuration.yml"

    if len(sys.argv) < 2:
        logging.warning(_("Aucun fichier de configuration n’a été donné en argument, le fichier par défaut « {} » sera utilisé.".format(source_configuration)))
    else:
        source_configuration = " ".join(sys.argv[1:])

    nébuleuse = lexika.NébuleuseDeLʼHélice(source_configuration)
    nébuleuse.initialiser()
    nébuleuse.créer_dictionnaire()
    nébuleuse.générer_XML()
#    nébuleuse.générer_Latex()
#    nébuleuse.exécuter_tâches("post-Latex", fichier_entrée=nébuleuse.configuration.Latex["chemin cible"], fichier_sortie=nébuleuse.configuration.Latex["chemin cible"])

if __name__ == "__main__":
    main()
