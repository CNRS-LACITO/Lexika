 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import regex


class Trieur:
    def __init__(self, ordres_lexicographiques: list):
        self.ordre_lexicographique = self.créer_ordre_lexicographique(ordres_lexicographiques)
        
    def créer_ordre_lexicographique(self, ordres_lexicographiques):
        ordre_lexicographique_général = []
        for ordre_lexicographique in ordres_lexicographiques:
            if ordre_lexicographique == "chiffres":
                ordre_lexicographique_général.append({"ordre": {str(chiffre): chiffre for chiffre in range(10)}, "expression": regex.compile(r"\d")})
            elif isinstance(ordre_lexicographique, list):
                niveau_ordre_lexicographique = self.créer_niveau_ordre_lexicographique(ordre_lexicographique)
                ordre_lexicographique_général.append({"ordre": niveau_ordre_lexicographique, "expression": regex.compile(self.protéger_caractères_spéciaux(r"{}".format("|".join(sorted(niveau_ordre_lexicographique, key=lambda expression: len(expression), reverse=True)))), flags=regex.IGNORECASE)})
        return ordre_lexicographique_général
                
    def créer_niveau_ordre_lexicographique(self, données: list):
        ordre_lexicographique = {}
        self.calculer_valeur_tri(ordre_lexicographique, données)          
        return ordre_lexicographique
       
    def calculer_valeur_tri(self, ordre: dict, données: list, préindex: list = []):
        for index, expression in enumerate(données):
            index_complet = préindex + [index]
            if isinstance(expression, str):
                ordre[expression] = index_complet
            elif isinstance(expression, list):            
                self.calculer_valeur_tri(ordre, expression, index_complet)

    def trier_entités(self, expression: str):
        résultat = []
        for niveau in self.ordre_lexicographique:           
            résultat.append([valeurs[1] for valeurs in [(syllabe, niveau["ordre"][syllabe.lower()]) for syllabe in niveau["expression"].findall(expression) if syllabe.lower() in niveau["ordre"]]])
        print(expression, "\t\t\t\t", résultat)
        return résultat
    
    def protéger_caractères_spéciaux(self, expression: str):
        for caractère in ["$", "^", ".", "*", "+", "-", "?"]:
            expression = expression.replace(caractère, f"\{caractère}")
        return expression
                

# Test simple pour vérifier le tri lexicographique
mots = ["fv˧kʰo˥", "fv˧", "fv˧ʂɯ˩", "fv˩bi˩", "fv˩˧", "fv˩", "fv˥bi˩", "fv˥bv˩", "æ˧", "bv˧1", "bv˧3", "bv˧2", "bv˩", "bv˧", "bv˥", "bvɑ̃", "ʑ˩bi˩", "ʑ˩", "ʑ˩$", "dze˧-ɻ̃#˥", "dze˧-ɻ̃˥", "dze˧ʈʂʰɤ#˥", "dze˧ʈʂʰɤ$˥", "dze˧ʈʂʰɤ˥", "tʰv̩˩β", "tʰv̩˩α"]

import yaml
from pprint import pprint
with open("configuration.yml", "r") as fichier:
    configuration = yaml.load(fichier)

trieur = Trieur(configuration["général"]["ordre lexicographique"])
pprint(trieur.ordre_lexicographique)

print("*********************************")
for mot in sorted(mots, key=lambda expression: trieur.trier_éléments(expression)):
    print(mot)
print("*********************************")