 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import regex


class TrieurLexicographique:
    """
    Classe qui permet de trier des éléments selon un ordre lexicographique complexe multiniveau.
    """
    def __init__(self, ordres_lexicographiques: list):
        self.ordre_lexicographique = self.créer_ordre_lexicographique(ordres_lexicographiques)

    def créer_ordre_lexicographique(self, ordres_lexicographiques: list):
        """
        Crée l'ordre lexicographique multiniveau selon les informations des différents niveaux de tri. Il s'agit d'une liste de sous-ordres lexicographiques de priorité décroissante (le tri n + 1 est utilisé seulement si le tri n ne suffit pas pour ordonner), chaque niveau étant un dictionnaire comprenant d'une part le sous-ordre lui-même et d'autre part l'expression rationnelle détectant les caractères d'intérêt pour ledit sous-ordre.
        """
        ordre_lexicographique_général = []
        for ordre_lexicographique in ordres_lexicographiques:
            if ordre_lexicographique == "chiffres":
                ordre_lexicographique_général.append({"ordre": {str(chiffre): chiffre for chiffre in range(10)}, "expression": regex.compile(r"\d")})
            elif isinstance(ordre_lexicographique, list):
                niveau_ordre_lexicographique = self.créer_niveau_ordre_lexicographique(ordre_lexicographique)
                ordre_lexicographique_général.append({"ordre": niveau_ordre_lexicographique, "expression": regex.compile(self.protéger_caractères_spéciaux(r"{}".format("|".join(sorted(niveau_ordre_lexicographique, key=lambda expression: len(expression), reverse=True)))), flags=regex.IGNORECASE)})
                print(ordre_lexicographique_général)
        return ordre_lexicographique_général

    def créer_niveau_ordre_lexicographique(self, données: list):
        """
        Crée pour chaque niveau d'ordre lexicographique les valeurs de tri.
        """
        ordre_lexicographique = {}
        self.calculer_valeur_tri(ordre_lexicographique, données)
        return ordre_lexicographique

    def calculer_valeur_tri(self, ordre: dict, données: list, préindex: list = []):
        """
        Calcule récursivement les valeurs de tri des éléments d'une liste.
        """
        for index, graphème in enumerate(données):
            index_complet = préindex + [index]
            if isinstance(graphème, str):
                ordre[graphème] = index_complet
            elif isinstance(graphème, list):
                self.calculer_valeur_tri(ordre, graphème, index_complet)

    def trier_expressions(self, expression: str):
        """
        Permet de trier les éléments selon l'ordre lexicographique donné. Fonctionne optimalement au sein d'une fonction lambda argument des fonctions de base « sort » et « sorted ».
        """
        résultat = []
        for niveau in self.ordre_lexicographique:
            prérésultat = [valeurs[1] for valeurs in [(graphème, niveau["ordre"][graphème.lower()]) for graphème in niveau["expression"].findall(expression) if graphème.lower() in niveau["ordre"]]]
            prérésultat = zip(*prérésultat)
            résultat.extend(prérésultat)
        logging.info(_(f"Vedette « {expression} » a pour valeur de tri : {résultat}"))
        print(expression, résultat)
        return résultat

    def protéger_caractères_spéciaux(self, expression: str):
        """
        Protège les caractères spéciaux pour les expressions rationnelles.
        """
        for caractère in ["$", "^", ".", "*", "+", "-", "?"]:
            expression = expression.replace(caractère, f"\{caractère}")
        return expression


class TrieurThématique:
    def __init__(self, données: dict):
        self.données = données
        self.hiérarchie = {}
        self.identifiants = {}
        self.titres = {}

        self.créer_hiérarchie()
        self.créer_titres()


    def créer_hiérarchie(self):
        """
        Crée la hiérarchie thématique.
        """
        self.calculer_valeur_tri(self.hiérarchie, self.identifiants, self.données["hiérarchie"])

    def calculer_valeur_tri(self, hiérarchie: dict, identifiants: dict, données: list, position_mère: list = []):
        """
        Crée récursivement les thèmes d'un itérable d’intérêt.
        """
        if isinstance(données, (list, dict)):
            for position, élément in enumerate(données, 1):
                position_complète = position_mère + [position]
                if isinstance(élément, list):
                    self.calculer_valeur_tri(hiérarchie, identifiants, élément, position_complète)
                elif isinstance(élément, dict):
                    if "identifiant" in élément:
                        identifiants[élément["identifiant"]] = position_complète
                    hiérarchie[élément["valeur"]] = position_complète
                    self.calculer_valeur_tri(hiérarchie, identifiants, élément.get("enfants"), position_complète)

    def créer_titres(self):
        """
        Crée les titres de chaque élément hiérarchiques.
        """
        for nom, position in self.hiérarchie.items():
            position = reversed(position) if self.données["numérotation"]["sens"] == "inverse" else position
            self.titres[nom] = f"{self.données['numérotation']['séparateur'].join([str(indice) for indice in position])}{self.données['numérotation']['séparateur']} {nom}"

    def trier_expressions(self, expression: str):
        """
        Permet de trier les éléments selon l'ordre donné. Fonctionne optimalement au sein d'une fonction lambda argument des fonctions de base « sort » et « sorted ».
        """
        return self.identifiants.get(expression, -1)
