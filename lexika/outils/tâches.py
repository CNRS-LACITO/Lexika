#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import regex

tâches = {
    "remplacer caractères":  lambda fichier_entrée, fichier_sortie: remplacer_caractères(fichier_entrée, fichier_sortie),
    "joindre lignes coupées": lambda fichier_entrée, fichier_sortie: joindre_lignes_coupées(fichier_entrée, fichier_sortie),
    "créer liens automatiques": lambda dictionnaire, liste_identifiants: créer_liens_automatiques(dictionnaire, liste_identifiants),
}

def remplacer_caractères(fichier_entrée, fichier_sortie):
    résultat = []
    with open(fichier_entrée, 'r') as entrée:
        for ligne in entrée.readlines():
            # résultat.append(ligne.replace("^", '').replace("<", "‹").replace(">", "›"))
            résultat.append(ligne.replace("^", ''))
    with open(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))

def joindre_lignes_coupées(fichier_entrée, fichier_sortie):
    with open(fichier_entrée, 'r') as entrée:
        résultat = []
        for ligne in entrée.readlines():
            if ligne.strip() and not ligne.startswith("\\"):
                résultat[-1] = "{} {}".format(résultat[-1].rstrip(), ligne)
            else:
                résultat.append(ligne)
    with open(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))
