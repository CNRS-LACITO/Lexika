import regex

ordre_lexicographique_général = ["a", "b", "c", "d", ["e", "é", "ê", "è"], "f", "g", "h", "i", "j", "k", "l", "m", "nh", "n", ["o", "ô"], "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
# ordre_lexicographique = {caractère: index for index, caractère in enumerate(ordre_lexicographique)}
valeurs = {}
valeurs_auxiliaires = {}
for index, élément in enumerate(ordre_lexicographique_général):
    if isinstance(élément, str):
        valeurs[élément] = index
        valeurs_auxiliaires[élément] = 0
        valeurs_auxiliaires[élément.upper()] = 1
    elif isinstance(élément, list):
        for sous_index, sous_élément in enumerate(élément):
            valeurs[sous_élément] = index
            valeurs_auxiliaires[sous_élément] = sous_index
ordre_lexicographique = valeurs
sous_ordre_lexicographique = valeurs_auxiliaires

expression_rationnelle_tri_entités = regex.compile(r"{}".format("|".join(sorted(ordre_lexicographique, key=lambda mot: len(mot), reverse=True))), flags=regex.IGNORECASE)
expression_rationnelle_sous_tri_entités = regex.compile(r"{}".format("|".join(sorted(sous_ordre_lexicographique, key=lambda mot: len(mot), reverse=True))), flags=regex.IGNORECASE)

def trier_entités(expression):
    if expression_rationnelle_tri_entités:
        résultat_primaire = [valeurs[1] for valeurs in [(syllabe, ordre_lexicographique[syllabe.lower()]) for syllabe in expression_rationnelle_tri_entités.findall(expression) if syllabe.lower() in ordre_lexicographique]]
        résultat_secondaire = [valeurs[1] for valeurs in [(syllabe, sous_ordre_lexicographique[syllabe.lower()]) for syllabe in expression_rationnelle_sous_tri_entités.findall(expression) if syllabe.lower() in ordre_lexicographique]]
        résultat_tertiaire = [0 if syllabe.islower() else 1 for syllabe in expression_rationnelle_tri_entités.findall(expression) if syllabe.lower() in ordre_lexicographique]
    else:
        résultat_primaire = expression
        résultat_secondaire = résultat_tertiaire = None
    print(expression, résultat_primaire, résultat_secondaire, résultat_tertiaire)
    return résultat_primaire, résultat_secondaire, résultat_tertiaire

mots = ["zozo", "coi", "Arbitre", "arbitre", "éléphant", "être", "espérance", "Coté", "coté", "côte", "Côté", "cote", "côté", "covoiturage", "tamang", "tamanh"]

for mot in sorted(mots, key=lambda entrée: trier_entités(entrée)):
    print(mot)

