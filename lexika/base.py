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

langue_système = locale.getlocale()[0].split("_")[0]
langue_préférée = gettext.translation("messages", localedir="internationalisation", languages=[langue_système], fallback=True)
langue_préférée.install()

def main():
    # Création des éléments techniques divers.
    lexika.outils.créer_journalisation("journal.log")

    source_configuration = "./exemples/na/configuration.yml"

    if len(sys.argv) < 2:
        logging.warning(_("Aucun fichier de configuration n'a été donné en argument, le fichier par défaut « {} » sera utilisé.".format(source_configuration)))
    else:
        source_configuration = " ".join(sys.argv[1:])

    créateur = lexika.NébuleuseDeLʼHélice(source_configuration)
    créateur.initialiser()
    créateur.créer_dictionnaire()
    créateur.générer_XML()
    créateur.générer_Latex()

if __name__ == "__main__":
    main()
