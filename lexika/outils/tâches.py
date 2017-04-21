#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika.linguistique
import lexika.outils
import regex

tâches = {
    "remplacer caractères":  lambda fichier_entrée, fichier_sortie: remplacer_caractères(fichier_entrée, fichier_sortie),
    "joindre lignes coupées": lambda fichier_entrée, fichier_sortie: joindre_lignes_coupées(fichier_entrée, fichier_sortie),
    "inverser balises": lambda fichier_entrée, fichier_sortie: inverser_balises(fichier_entrée, fichier_sortie),
    "remplacer indices latex": lambda fichier_entrée, fichier_sortie: remplacer_indices_latex(fichier_entrée, fichier_sortie),
    "remplacer numéros homonyme liens": lambda fichier_entrée, fichier_sortie: remplacer_numéros_homonyme_liens(fichier_entrée, fichier_sortie),
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

def remplacer_indices_latex(fichier_entrée, fichier_sortie):
    résultat = []
    correspondances = {"α": "a", "β": "b", "γ": "c"}
    with lexika.outils.OuvrirFichier(fichier_entrée, 'r') as entrée:
        for ligne in entrée.readlines():
            for clef, valeur in correspondances.items():
                ligne = ligne.replace(clef, "\\textsubscript{{{}}}".format(valeur))
            résultat.append(ligne)
    with lexika.outils.OuvrirFichier(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))

def remplacer_numéros_homonyme_liens(fichier_entrée, fichier_sortie):
    résultat = []
    correspondances = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7":  "₇", "8": "₈", "9": "₉"}
    modèle_recherche = regex.compile(r"(?P<début>\\hyperlink{.+?}{)(?P<cible>.+?)(?P<fin>})")
    modèle_remplacement = regex.compile(r"(?P<numéro>\d)")
    with lexika.outils.OuvrirFichier(fichier_entrée, 'r') as entrée:
        for ligne in entrée.readlines():
            bilan = modèle_recherche.search(ligne)
            if bilan:
                # ligne = r"{}{}{}".format(bilan.group("début"), modèle_remplacement.sub(r"\\textsubscript{{{}}}".format(r"\g<0>"), bilan.group("cible")), bilan.group("fin"))  # Spécifique à Latex.
                sous_bilan = modèle_remplacement.search(bilan.group("cible"))
                if sous_bilan:
                    ligne = r"{}{}{}".format(bilan.group("début"), modèle_remplacement.sub(r"{}".format(correspondances[sous_bilan.group("numéro")]), bilan.group("cible")), bilan.group("fin"))
            résultat.append(ligne)
    with lexika.outils.OuvrirFichier(fichier_sortie, 'w') as sortie:
        sortie.write("".join(résultat))
