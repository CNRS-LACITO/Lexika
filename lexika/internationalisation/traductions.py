#!/usr/bin/env python3
# -*- coding: utf-8 -*-

entités = {
    "RessourcesLexicales": "LexicalResource",
    "informations globales": "global informations",
    "nom": "name",
    "auteurs": "authors",
    "commentaire": "comments",
    "dictionnaire": "lexicon",
    "entrée lexicale": "lexical entry",
    "sous-entrée lexicale": "lexical subentry",
    "lemme": "lemma",
    "sens": "sense",
    "numéro de sens": "sense number",
    "numéro d'homonyme": "homonyme number",
    "lexème": "lexeme",
    "phonétique": "phonetic form",
    "définition": "definition",
    "glose": "gloss",
    "paradigme": "paradigm",
    "morphologie": "morphology",
    "sens littéral": "literally",
    "exemple": "example",
    "langue": "language",
    "partie du discours": "part of speech",
    "contexte": "context",
    "représentation de texte": "text representation",
    "représentation de forme": "form representation",
    "forme écrite": "written form",
    "équivalent": "equivalent",
    "traduction": "translation",
    "déclaration": "statement",
    "usage": "use",
    "interrogation": "question",
    "grammaire": "grammar",
    "général": "general",
    "relation sémantique": "sense relation",
    "traduction de relation sémantique": "sense relation translation",
    "champ disciplinaire": "subject field",
    "domaine sémantique": "semantic domain",
    "nom scientifique": "scientific name",
    "forme de mot": "word form",
    "nombre grammatical": "grammatical number",
    "pluriel": "plural",
    "variante": "variant form",
    "duel": "dual",
    "forme apparentée": "related form",
    "entrée principale": "main entry",
    "sous-entrée": "subentry",
}

entités_classe = {"".join([segment[0].upper() + segment[1:] for segment in clef.split()]): "".join([segment[0].upper() + segment[1:] for segment in valeur.split()]) for clef, valeur in entités.items()}
entités_mixtes = {clef: "".join([segment if index == 0 else segment[0].upper() + segment[1:] for index, segment in enumerate(valeur.split())]) for clef, valeur in entités.items()}

mots_clefs = {
    "caractéristique": "feat",
    "attribut": "att",
    "valeur": "val",
    "lien": "link",
    "cible": "target",
    "contenu": "content",
    "emprunt": "loanword"
}

dictionnaires = [entités, entités_classe, mots_clefs, entités_mixtes]
