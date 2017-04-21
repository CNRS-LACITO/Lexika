import lxml.html
import regex

# traductions = {"lien": "link", "cible": "target"}
#
# texte = "⊣lien cible=\"aaa\"⊢mot⊣/lien⊢"
# modèle_balise = regex.compile(r"⊣(?P<balise>[\w]+) (?P<attribut>[\w]+)=\"(?P<valeur>[\p{property='Enclosed Alphanumerics'}\w\s\[\]~-]+)\"⊢(?P<texte>[\w\s\[\]~-]+)⊣\/(?P=balise)⊢")
#
# sous_bilan = modèle_balise.match(texte)
#
# print(sous_bilan.groupdict())
# groupes = sous_bilan.groupdict()
# groupes["balise"] = "link"
# groupes["attribut"] = "target"
# print(groupes)
#
# print("-0--", texte)
# texte_enrichi = modèle_balise.sub(lambda match: match.groups(), texte)
# print("-1--", texte_enrichi)
# texte_enrichi = modèle_balise.sub("<{} {}=\"{}\">{}</{}>".format("\g<balise>", "\g<attribut>", "\g<valeur>", "\g<texte>", "\g<balise>"), texte)
# print("-2--", texte_enrichi)

modèle = regex.compile(r"^\\(?P<balise>\w*) (?P<métadonnées><([\w\s]+=[\w\"\s]+)+>)? \s*(?P<données>.*)", flags=regex.VERSION0)

for ligne in ["\\nt <type=\"phono\" lang=\"fra\"> blabla", "\\nt <type=\"phono\"> blabla", "\\nt <qqn=ôo> est utilisé dans", "\\nt <qqn> est utilisé dans", "\\nt <qqn=\"4\"> est utilisé dans"]:
    bilan = modèle.search(ligne)
    if bilan:
        print(bilan, bilan.groupdict())
