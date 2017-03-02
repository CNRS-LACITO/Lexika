import regex

liste = ["a", "b", "ɓ", "d", "ɗ", "g", "gb", "k", "kp", "v", "ⱱ", "p"]
liste2 = "|".join(sorted(liste, key=lambda mot: len(mot), reverse=True))

mot = "gbakpɓ"

expression = regex.compile(liste2, flags=regex.V0)
print(expression)
résultat = expression.findall(mot)
print(résultat)

print("KP".lower())