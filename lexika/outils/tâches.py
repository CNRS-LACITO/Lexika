#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import lexika.outils
import regex

tâches = {
    "remplacer caractères":  lambda fichier_entrée, fichier_sortie: remplacer_caractères(fichier_entrée, fichier_sortie),
    "joindre lignes coupées": lambda fichier_entrée, fichier_sortie: joindre_lignes_coupées(fichier_entrée, fichier_sortie),
    "inverser balises": lambda fichier_entrée, fichier_sortie: inverser_balises(fichier_entrée, fichier_sortie),
}

def remplacer_caractères(fichier_entrée, fichier_sortie):
    résultat = []
    with lexika.outils.OuvrirFichier(fichier_entrée, 'r') as entrée:
        for ligne in entrée.readlines():
            résultat.append(ligne.replace("^", ''))
    with lexika.outils.OuvrirFichier(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))

def joindre_lignes_coupées(fichier_entrée, fichier_sortie):
    with lexika.outils.OuvrirFichier(fichier_entrée, 'r') as entrée:
        résultat = []
        for ligne in entrée.readlines():
            if ligne.strip() and not ligne.startswith("\\"):
                résultat[-1] = "{} {}".format(résultat[-1].rstrip(), ligne)
            else:
                résultat.append(ligne)
    with lexika.outils.OuvrirFichier(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))

def inverser_balises(fichier_entrée, fichier_sortie):
    with lexika.outils.OuvrirFichier(fichier_entrée, 'r') as entrée:
        contenu = entrée.read()
        # contenu = regex.compile(r"(\\el .*)\n(\\et .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\ps .*)\n(\\wr .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\rf .*)\n(\\xv .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\rf .*)\n(\\se .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\he .*)\n(\\de .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\hn .*)\n(\\dn .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\oe .*)\n(\\xe .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\on .*)\n(\\xn .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
        # contenu = regex.compile(r"(\\on .*)\n(\\xn .*)", flags=regex.MULTILINE).sub(r"\2\n\1", contenu)
    with lexika.outils.OuvrirFichier(fichier_sortie, 'w') as sortie:
        sortie.write(contenu)
