 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import regex


class Trieur:
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
        if len(ordres_lexicographiques) == 1:
            ordres_lexicographiques = [ordres_lexicographiques]
        for ordre_lexicographique in ordres_lexicographiques:
            if ordre_lexicographique == "chiffres":
                ordre_lexicographique_général.append({"ordre": {str(chiffre): chiffre for chiffre in range(10)}, "expression": regex.compile(r"\d")})
            elif isinstance(ordre_lexicographique, list):
                niveau_ordre_lexicographique = self.créer_niveau_ordre_lexicographique(ordre_lexicographique)
                ordre_lexicographique_général.append({"ordre": niveau_ordre_lexicographique, "expression": regex.compile(self.protéger_caractères_spéciaux(r"{}".format("|".join(sorted(niveau_ordre_lexicographique, key=lambda expression: len(expression), reverse=True)))), flags=regex.IGNORECASE)})
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
        for index, expression in enumerate(données):
            index_complet = préindex + [index]
            if isinstance(expression, str):
                ordre[expression] = index_complet
            elif isinstance(expression, list):            
                self.calculer_valeur_tri(ordre, expression, index_complet)

    def trier_éléments(self, expression: str):
        """
        Permet de trier les éléments selon l'ordre lexicographique donnée. Fonctionne optimalement au sein d'une fonction lambda argument des fonctions de base « sort » et « sorted ».
        """
        résultat = []
        for niveau in self.ordre_lexicographique:           
            résultat.append([valeurs[1] for valeurs in [(syllabe, niveau["ordre"][syllabe.lower()]) for syllabe in niveau["expression"].findall(expression) if syllabe.lower() in niveau["ordre"]]])
        return résultat
    
    def protéger_caractères_spéciaux(self, expression: str):
        """
        Protège les caractères spéciaux pour les expressions rationnelles.
        """
        for caractère in ["$", "^", ".", "*", "+", "-", "?"]:
            expression = expression.replace(caractère, f"\{caractère}")
        return expression

#class Trieur:
#    def __init__(self, données: list):
#        self.données = données
#        self.ordre_lexicographique = self.créer_ordre_lexicographique(self.données)
#        self.ordre_numérique = {str(chiffre): chiffre for chiffre in range(10)}
#        self.expression_rationnelle_tri_entités = regex.compile(r"{}".format("|".join(sorted(self.ordre_lexicographique, key=lambda mot: len(mot), reverse=True))), flags=regex.IGNORECASE)
#        self.expression_rationnelle_tri_numérique = regex.compile(r"\d")
#       
#    def créer_ordre_lexicographique(self, données: list):
#        ordre_lexicographique = {}
#        self.calculer_valeur_tri(ordre_lexicographique, données)          
#        return ordre_lexicographique
#       
#    def calculer_valeur_tri(self, ordre: dict, données: list, préindex: list = []):
#        for index, expression in enumerate(données):
#            index_complet = préindex + [index]
#            if isinstance(expression, str):
#                ordre[expression] = index_complet
#            elif isinstance(expression, list):            
#                self.calculer_valeur_tri(ordre, expression, index_complet)
#
#    def trier_entités(self, expression: str):
#        résultat = []
#        if self.expression_rationnelle_tri_entités:
#            résultat.append([valeurs[1] for valeurs in [(syllabe, self.ordre_lexicographique[syllabe.lower()]) for syllabe in self.expression_rationnelle_tri_entités.findall(expression) if syllabe.lower() in self.ordre_lexicographique]])
#            résultat.append([0 if syllabe.islower() else 1 for syllabe in self.expression_rationnelle_tri_entités.findall(expression) if syllabe.lower() in self.ordre_lexicographique])
#            résultat.append([valeurs[1] for valeurs in [(chiffre, self.ordre_numérique[chiffre]) for chiffre in self.expression_rationnelle_tri_numérique.findall(expression)]])
#        else:
#            résultat.append(expression)
#        return résultat