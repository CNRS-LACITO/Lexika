#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika

import logging
import regex


class NébuleuseDʼOrion(lexika.outils.ClasseConfigurée):
    """
    Classe qui permet de créer des dictionnaires dynamiquement.
    """
    def __init__(self):
        super().__init__()

        self.racine = None
        self.dictionnaire = None

        self.lexique_inverse = None

        self.identifiants = {}

        self.balises = {}
        self.lignes_mémorisées = {"factorisation": None, "antéposition": []}

        self.entrée_actuelle = None
        self.famille_actuelle = []
        self.ascendance_actuelle = []
        self.informations_entités = {}

        self.dépôt = {}
        self.appels_dépôt = []

        self.modèle_ligne = regex.compile(self.configuration.informations["entrée"]["modèles"]["ligne"])
        self.modèle_métadonnées = regex.compile(self.configuration.informations["entrée"]["modèles"]["métadonnées"])
        self.informations_balises = self.configuration.informations["entrée"]["balises"]

        self.créateur_abstractions = lexika.outils.CréateurDʼAbstractions(self.configuration.informations["sortie"]["abstractions"])
        self.convertisseur_abréviations = lexika.outils.ConvertisseurDʼAbréviations(self.configuration.informations["sortie"]["abréviations"])
        self.témoin = lexika.outils.Témoin()

    def préparer_dictionnaire(self):
        """
        Prépare le dictionnaire en créant les entités uniques.
        """
        for élément_spécial in ["racine", "métainformations", "dictionnaire"]:
            nom, informations = [(abstraction, informations) for abstraction, informations in self.configuration.informations["sortie"]["abstractions"].items() if élément_spécial in informations.get("spécial", {}).get("drapeaux", {})][0]
            self.analyser_abstraction(self.créateur_abstractions.créer_abstraction(nom))
            if élément_spécial == "métainformations":
                self.récupérer_métainformations(nom, informations["entité"]["données"])

    def récupérer_métainformations(self, nom_parent: str, informations: dict):
        """
        Récupère les métainformations diverses.
        """
        parent = self.trouver_entités(nom_parent)[0]
        if informations["source"] == "configuration":
            informations = {clef: self.configuration.informations[clef] for clef in informations["clefs"]}
            self.récupérer_métainformation(parent, informations)

    def récupérer_métainformation(self, parent: lexika.outils.Entité, informations: dict):
        """
        Récupère récursivement les métainformations.
        """
        if not hasattr(parent, "descendance"):
            setattr(parent, "descendance", [])
        if isinstance(informations, dict):
            for nom, élément in informations.items():
                entité = lexika.outils.Entité(**{"nom": nom})
                parent.descendance.append(entité)
                self.récupérer_métainformation(entité, élément)
        elif isinstance(informations, list):
            for élément in informations:
                entité = lexika.outils.Entité(**{"nom": "élément"})
                parent.descendance.append(entité)
                self.récupérer_métainformation(entité, élément)
        else:
            parent.valeur = informations

    def lire_données(self, bloc_données: list):
        """
        Lit le bloc de données.
        """
        for donnée in bloc_données:
            self.témoin.initialiser(**donnée)
            try:
                self.analyser_ligne_données(donnée)
            except Exception as exception:
                raise exception
            finally:
                self.témoin.envoyer_message()

    def analyser_ligne_données(self, ligne_données: str, ligne_entreposée: bool = False):
        """
        Analyse les données (sur une ligne) afin de savoir comment les traiter selon la configuration spécifique. À ce niveau, les termes de balise et de données sont utilisés. La « valeur » est l’information principale tandis que les « caractéristiques » sont les informations secondaires relatives aux informations principales, mais ces choix relèvent principalement de l’utilisateur par l’intermédiaire du fichier de configuration.
        Il s'agit de la fonction d'entrée de la triade principale, qui gère les balises et crée des abstractions.
        """
        bilan = self.modèle_ligne.match(ligne_données["ligne"])
        if bilan:
            balise = bilan.group("balise")
            données = bilan.group("données")
            métadonnées = bilan.group("métadonnées") if "métadonnées" in bilan.groupdict() else None
            self.balises[balise] = self.balises.get(balise, 0) + 1
            self.témoin.débogage(_(f"Ligne décomposée en cours : balise = « {balise} » – données = « {données} » – métadonnées = « {métadonnées} »"))
            if balise in self.informations_balises:
                informations_balise = self.informations_balises[balise]
                if données:
                    if informations_balise:
                        # Traitements spécifiques pour des balises ayant une syntaxe particulière.
                        if not ligne_entreposée and informations_balise.get("drapeaux"):
                            if "bloc" in informations_balise["drapeaux"]:
                                self.lignes_mémorisées = {"factorisation": None, "antéposition": []}
                            elif "factorisation" in informations_balise["drapeaux"]:
                                self.lignes_mémorisées["factorisation"] = {"balise": informations_balise["drapeaux"]["factorisation"], "ligne": ligne_données, "actif": False}
                            elif "antéposition" in informations_balise["drapeaux"]:
                                self.lignes_mémorisées["antéposition"].append({"balise": informations_balise["drapeaux"]["antéposition"], "ligne": ligne_données})
                                return
                        # Traitement des balises implicites factorisées.
                        if self.lignes_mémorisées["factorisation"] and self.lignes_mémorisées["factorisation"]["balise"] == balise:
                            if self.lignes_mémorisées["factorisation"]["actif"]:
                                self.analyser_ligne_données(self.lignes_mémorisées["factorisation"]["ligne"], True)
                            else:
                                self.lignes_mémorisées["factorisation"]["actif"] = True
                        # Traitement normal.
                        if informations_balise.get("abstraction") or informations_balise.get("abstractions"):
                            proabstractions = [informations_balise["abstraction"]] if informations_balise.get("abstraction") else informations_balise.get("abstractions")
                            for proabstraction in proabstractions:
                                if isinstance(proabstraction, str):
                                    proabstraction = {"nom": proabstraction, "valeur": données, "caractéristiques": informations_balise.get("caractéristiques", {}), "drapeaux": {}}
                                else:
                                    proabstraction = {"nom": proabstraction["nom"], "valeur": proabstraction.get("valeur", données), "caractéristiques":  proabstraction.get("caractéristiques", {}), "drapeaux": {}}
                                if proabstraction["nom"] in self.créateur_abstractions.dictionnaire:
                                    if métadonnées:
                                        proabstraction["caractéristiques"].update({valeur[0]: valeur[1] for valeur in self.modèle_métadonnées.findall(métadonnées)})
                                    self.analyser_abstraction(self.créateur_abstractions.créer_abstraction(**proabstraction))
                                else:
                                    self.témoin.erreur(_(f"L'abstraction de type « {proabstraction['nom']} » n'est pas configurée."))
                        else:
                            self.témoin.avertissement(_(f"La balise de type « {balise} » n'est associée à aucune abstraction."))
                        # Traitement des balises antéposées.
                        if self.lignes_mémorisées["antéposition"]:
                            lignes_mémorisées = [ligne_mémorisée for ligne_mémorisée in self.lignes_mémorisées["antéposition"] if ligne_mémorisée["balise"] == balise]
                            for ligne_mémorisée in lignes_mémorisées:
                                self.analyser_ligne_données(ligne_mémorisée["ligne"], True)
                                self.lignes_mémorisées["antéposition"].remove(ligne_mémorisée)
                    else:
                        self.témoin.avertissement(_(f"La balise de type « {balise} » n'est pas utilisée."))
                else:
                    self.témoin.information(_(f"La balise de type « {balise} » ne contient aucune valeur."))
            else:
                self.témoin.avertissement(_(f"Balise « {balise} » inconnue donc ignorée."))
        else:
            self.témoin.avertissement(_("Attention, la ligne n'a pas été validée par l'expression rationnelle."))

    def analyser_abstraction(self, abstraction: lexika.outils.Abstraction):
        """
        Analyse l’abstraction pour en tirer les entités et caractéristiques à créer (éventuellement en analysant d’autres abstractions par récursion). Si le parent adéquat est trouvé, l'entité sera créée, sinon elle sera entreposée.
        Il s'agit de la fonction centrale de le triade principale, qui gère uniquement les abstractions avec des récursions possibles et les différentes conditions.
        """
        self.témoin.nom_abstraction = abstraction.nom
        self.témoin.nom_abstraction_appelante = abstraction.appelants[-1].nom if abstraction.appelants else None
        # Cas singulier (racine, impérativement vers le début).
        if "racine" in abstraction.spécial.get("drapeaux", {}):
            self.racine = self.créer_entité(abstraction, None)
            self.mettre_à_jour_ascendance(None, self.racine)
            self.témoin.information(_(f"Racine trouvée."))
        # Cas général (entité associée à un parent nommé).
        elif abstraction.parent.get("nom"):
            # Analyse des préabstractions conditionnelles (possibles appels récursifs).
            if abstraction.préabstraction:
                noms_préabstractions = [nom for nom in abstraction.préabstraction["nom"]]
                # Voie impérieuse : création systématique.
                if abstraction.préabstraction.get("voie") == "impérieuse":
                    self.témoin.information(_(f"Abstraction impérieuse à analyser au préalable : « {abstraction.préabstraction['nom']} »."))
                    self.analyser_abstraction(self.créateur_abstractions.créer_abstraction(noms_préabstractions[0], appelants=abstraction.appelants + [abstraction]))
                # Voie contextuelle : création selon les potentiels parents de l'ascendance.
                elif abstraction.préabstraction.get("voie") == "contextuelle":
                    préabstraction = abstraction.préabstraction["nom"][0]
                    noms_parents_potentiels = abstraction.parent["nom"] + self.créateur_abstractions.créer_abstraction(préabstraction, appelants=abstraction.appelants + [abstraction]).parent["nom"]
                    for parent_potentiel in reversed(self.ascendance_actuelle):
                        if parent_potentiel.nom in noms_parents_potentiels:
                            parent = parent_potentiel
                            if parent.nom not in abstraction.parent["nom"] and abstraction.parent["nom"] not in parent.descendance:
                                self.analyser_abstraction(self.créateur_abstractions.créer_abstraction(noms_préabstractions[0], appelants=abstraction.appelants + [abstraction]))
                            break
                else:
                    parent = self.trouver_parent(abstraction)  # À FAIRE : améliorer pour éviter un double appel parfois inutile à cette fonction…
                    # Cas sub-optimal : le parent n'a pas été trouvé mais la préabstraction pour le créer est précisée et va être appelée.
                    if not parent:
                        sous_message = _(" ou ".join([parent for parent in abstraction.parent['nom']]))
                        self.témoin.information(_(f"Parent « {sous_message} » manquant, abstraction à analyser au préalable : « {abstraction.préabstraction['nom']} »."))
                        self.analyser_abstraction(self.créateur_abstractions.créer_abstraction(noms_préabstractions[0], appelants=abstraction.appelants + [abstraction]))
            # Analyse de l’abstraction dans tous les cas.
            parent = self.trouver_parent(abstraction)
            # Cas optimal : le parent a été trouvé et l'entité étudiée va y être rattachée.
            if parent:
                self.témoin.information(_(f"Parent « {parent.nom} » trouvé."))
                if abstraction.entité.get("type") == "caractéristique":
                    self.mettre_à_jour_entité(abstraction, parent)
                else:
                    entité = self.créer_entité(abstraction, parent)
                    est_nouvelle = "entrée" in abstraction.spécial.get("drapeaux", {})
                    self.mettre_à_jour_famille(entité, est_nouvelle)
                    self.mettre_à_jour_informations_entité(entité, abstraction, est_nouvelle)
                    self.mettre_à_jour_ascendance(parent, entité)
                    if "dictionnaire" in abstraction.spécial.get("drapeaux", {}):
                        self.dictionnaire = entité
                        self.témoin.information(_(f"Dictionnaire trouvé."))
                    if "entrée" in abstraction.spécial.get("drapeaux", {}):
                        self.entrée_actuelle = entité
                        self.témoin.information(_(f"Nouvelle entrée."))
                    if "identifiant" in abstraction.spécial.get("drapeaux", {}):
                        self.mettre_à_jour_identifiant(abstraction)
                    if abstraction.spécial.get("tri"):
                        self.mettre_à_jour_critère_tri(abstraction)
                # Analyse du dépôt après la création éventuelle des préentités.
                if abstraction.appelants:
                    if abstraction.nom in self.dépôt:
                        self.appels_dépôt.append(abstraction.entité["nom"])
                elif self.dépôt.get(self.famille_actuelle[0]):
                    for abstraction_en_attente in self.récupérer_abstractions(self.famille_actuelle[0], abstraction.nom):
                        self.analyser_abstraction(abstraction_en_attente)
            # Cas rare : le parent n'a pas été trouvé, aucune préabstraction n'est précisée, donc l'entité sera entreposée en espérant que le parent soit trouvé ultérieurement.
            else:
                self.déposer_abstraction(self.famille_actuelle[0], abstraction)
                self.témoin.erreur(_(f"L’entité « {abstraction.entité['nom']} » de l’abstraction « {abstraction.nom} » ne semble pas avoir de parent adéquat « {abstraction.parent['nom']} » et a donc été entreposée."))

    def mettre_à_jour_entité(self, abstraction: lexika.outils.Abstraction, parent: lexika.outils.Entité):
        parent.caractéristiques[abstraction.entité["nom"]] = abstraction.entité["valeur"]

    def créer_entité(self, abstraction: lexika.outils.Abstraction, parent: lexika.outils.Entité) -> lexika.outils.Entité:
        """
        Crée l’entité linguistique d’après son nom et avec ses caractéristiques (ici, la valeur est celle d’une entité, éventuellement accompagnée d’autres caractéristiques).
        Il s'agit de la fonction finale de la triade principale, qui crée des entités linguistiques et met à jour l'architecture interne.
        """
        # Entité = type(nom_classe, (lexika.outils.Entité,), {})  # Ne fonctionne pas ainsi avec le module multiprocessing (pas de sérialisation possible pour une classe créée dynamiquement).
        entité = lexika.outils.Entité(**abstraction.entité)
        setattr(entité, "parent", parent)
        if parent:
            if not hasattr(parent, "descendance"):
                setattr(parent, "descendance", [])
            parent.descendance.append(entité)
        if hasattr(abstraction, "spécial") and "correspondance" in abstraction.spécial.get("drapeaux", []):
            entité.valeur = self.convertisseur_abréviations.convertir(abstraction.nom, entité.valeur)
        if parent:
            self.témoin.information(_(f"Entité « {entité.nom} » créée et rattachée au parent « {parent.nom} »."))
        return entité

    def trouver_parent(self, abstraction: lexika.outils.Abstraction) -> lexika.outils.Entité:
        """
        Trouve le parent adéquat de l’entité s’il existe (fonction générale de recherche de parenté).
        Il s'agit d'une fonction auxiliaire critique et améliorable sur laquelle repose une grande partie de l'architecture.
        """
        parents = self.trouver_entités(abstraction.parent.get("nom"))
        if parents:
            if abstraction.parent.get("conditions"):
                self.témoin.information(_(f"L’abstraction « {abstraction.nom} » a des conditions parentales et leur analyse va avoir lieu."))
                parents = self.tester_parenté(abstraction, parents)
            else:
                self.témoin.information(_(f"L’abstraction « {abstraction.nom} » n'a aucune condition parentale."))
            sous_message = " ou ".join([parent.nom for parent in parents])
            self.témoin.information(_(f"L’abstraction « {abstraction.nom} » verra son parent le plus proche (le dernier) choisi parmi les suivants : « {sous_message} »."))
            parent = parents[-1] if parents else None
        else:
            self.témoin.information(_(f"L’abstraction « {abstraction.nom} » n’a aucun parent."))
            parent = None
        return parent

    def tester_parenté(self, abstraction: lexika.outils.Abstraction, parents: list) -> lexika.outils.Entité:
        """
        Teste chaque parent potentiel (fonction intermédiaire de recherche de parenté).
        """
        conditions = abstraction.parent["conditions"]
        # Teste l'égalité de caractéristiques chez les descendants du parent potentiel.
        if conditions.get("caractéristiques"):
            for parent_potentiel in reversed(parents):
                if conditions.get("caractéristiques").get("égalité"):
                    caractéristiques = conditions.get("caractéristiques").get("égalité")
                    if not self.rechercher_condition_parentale(abstraction, parents, parent_potentiel, parent_potentiel, caractéristiques):
                        parents.remove(parent_potentiel)
        # Teste la présence d'entités chez le parent potentiel.
        if conditions.get("entité"):
            if conditions["entité"] == "absente":
                for parent_potentiel in reversed(parents):
                    if hasattr(parent_potentiel, "descendance") and abstraction.entité["nom"] in [descendant.nom for descendant in parent_potentiel.descendance]:
                        parents.remove(parent_potentiel)
            elif conditions["entité"].get("nom") and conditions["entité"].get("état"):
                for parent_potentiel in parents:
                    if parent_potentiel.nom == conditions["entité"]["nom"]:
                        if conditions["entité"]["état"] == "absent":
                            if abstraction.entité["nom"] in [descendant.nom for descendant in parent_potentiel.descendance]:
                                parents.remove(parent_potentiel)
        # Teste l'environnement du parent potentiel.
        if conditions.get("environnements interdits"):
            for parent_potentiel in reversed(parents):
                if any([environnement_interdit in [parent.nom for parent in self.ascendance_actuelle[0:self.ascendance_actuelle.index(parent_potentiel)]] for environnement_interdit in conditions["environnements interdits"]]):
                    parents.remove(parent_potentiel)
        return parents

    def rechercher_condition_parentale(self, abstraction: lexika.outils.Abstraction, parents: list, parent_origine: lexika.outils.Entité, entité: lexika.outils.Entité, caractéristiques: dict) -> lexika.outils.Entité:
        """
        Recherche et teste récursivement les conditions parentales par caractéristiques pour un parent potentiel (fonction spécifique de recherche de parenté).
        """
        if hasattr(entité, "descendance"):
            for descendant in reversed(entité.descendance):
                if all([descendant.caractéristiques.get(caractéristique) == abstraction.entité["caractéristiques"].get(caractéristique) for caractéristique in caractéristiques]):
                    return parent_origine
                else:
                    return self.rechercher_condition_parentale(abstraction, parents, parent_origine, descendant, caractéristiques)

    def trouver_entités(self, noms: list) -> list:
        """
        Trouve les entités de la famille selon les noms possibles. Fonction critique, plusieurs mises en œuvre sont possible : visibilité de toute la famille (dangereux car il faut ensuite plein de conditions pour filtrer), visibilité de l'ascendance uniquement (insuffisant du fait de la différence structurelle entre MDF et le format voulu), visibilité du dernier parent potentiel (dangereux car il peut briser la hiérarchie logique et parfois il faut le créer), visibilité de la fratrie directe, etc.
        """
        entités = [entité for entité in self.ascendance_actuelle if entité.nom in noms]
        if not entités:
            entités = [entité for entité in (self.ascendance_actuelle[-2].descendance if len(self.ascendance_actuelle) > 1 and hasattr(self.ascendance_actuelle[-2], "descendance") else []) if entité.nom in noms]
#            famille = list({entité.nom: entité for entité in self.famille_actuelle if entité.nom in noms}.values())

        return entités

    def déposer_abstraction(self, entrée: lexika.outils.Entité, abstraction: lexika.outils.Abstraction):
        """
        Dépose une abstraction non résolue en attente d'une analyse au moment opportun défini par le nom de l'entité parente manquante.
        """
        if entrée not in self.dépôt:
            self.dépôt[entrée] = []
        self.dépôt[entrée].append(abstraction)

    def récupérer_abstractions(self, entrée: lexika.outils.Entité, nom: str) -> list:
        """
        Récupère toutes les abstractions du dépôt pour un nom d’entité donné et les analyse à nouveau pour tenter de les replacer.
        """
        abstractions = [abstraction for abstraction in self.dépôt[entrée] if nom in abstraction.parent["nom"]]
        for abstraction in abstractions:
            self.dépôt[entrée].remove(abstraction)
        return abstractions

    def mettre_à_jour_famille(self, entité: lexika.outils.Entité, nouvelle: bool = False):
        """
        Met à jour la famille qui garde une trace dans l'ordre chronologique de toutes les entités de l'entrée en cours, cette dernière étant en première position ; visibilité horizontale.
        """
        if nouvelle:
            self.famille_actuelle.clear()
        self.famille_actuelle.append(entité)
        self.témoin.information(_(f"Ajout de l'entité « {entité.nom} » dans la famille actuelle"))

    def mettre_à_jour_ascendance(self, parent: lexika.outils.Entité, entité: lexika.outils.Entité):
        """
        Met à jour l'ascendance qui garde une trace de tous les parents de l'entité en cours, ce qui permet de garder en mémoire les différents environnements auxquels une abstraction en cours d'analyse a accès (donc le parent direct et ses parents successifs), ce qui cloisonne les environnements pour éviter qu'une entité puisse se rattacher à une entité inadéquate (typiquement, les sens, les sous-entrées, etc.) ; visibilité verticale.
        """
        if parent:
            if parent in self.ascendance_actuelle:
                del self.ascendance_actuelle[self.ascendance_actuelle.index(parent):]
            self.ascendance_actuelle.append(parent)
        self.ascendance_actuelle.append(entité)
        sous_message = " ➢ ".join([str(entité) for entité in self.ascendance_actuelle])
        self.témoin.information(_(f"Environnement hiérarchique actuel : « {sous_message} »."))

    def mettre_à_jour_informations_entité(self, entité: lexika.outils.Entité, abstraction: lexika.outils.Abstraction, nouvelle: bool = False):
        if nouvelle:
            self.informations_entités.clear()
        self.informations_entités[entité] = abstraction.appelants + [abstraction]

    def mettre_à_jour_identifiant(self, abstraction: lexika.outils.Abstraction):
        """
        Crée et met à jour les identifiants de certaines entités.
        """
        informations_identifiant = self.configuration.informations["sortie"]["identifiants"][abstraction.nom]
        entité = self.trouver_entités([informations_identifiant["ascendant"]])[-1]
        parent = [entité for entité in reversed(self.ascendance_actuelle) if entité.caractéristiques.get("identifiant")]
        identifiant_parent = parent[0].caractéristiques["identifiant"] if parent else ""
        identifiant = f"{identifiant_parent}{informations_identifiant['constante']}{abstraction.entité['valeur']}"
        entité.caractéristiques["identifiant"] = identifiant

    def connecter_liens(self):
        """
        Connecte les liens (cibles avec identifiant).
        """
        self.rapatrier_renvois(self.racine)
        self.convertisseur_texte_enrichi = lexika.outils.ConvertisseurDeTexteEnrichi(self.configuration.informations["entrée"]["modèles"]["texte enrichi"], self.configuration.informations["sortie"]["identifiants"], self.identifiants)
        self.connecter_lien(self.racine)

    def rapatrier_renvois(self, entité: lexika.outils.Entité, identifiant: str = None):
        """
        Rapatrie tous les éléments susceptibles d’être renvoyés pour des liens.
        """
        identifiant = entité.caractéristiques.get("identifiant", identifiant)
        if identifiant not in self.identifiants:
            self.identifiants[identifiant] = []
        if hasattr(entité, "spécial") and "renvoyable" in entité.spécial.get("drapeaux", {}):
            if entité.valeur in self.identifiants:
                logging.warning(_(f"Le renvoi « {entité.valeur} » est déjà présent dans la liste des identifiants en tant que « {self.identifiants[entité.valeur]} » et ne sera pas remplacé par « {identifiant} »."))
            self.identifiants[self.identifiants.get(entité.valeur, identifiant)].append(entité.valeur)
        if hasattr(entité, "descendance"):
            for enfant in entité.descendance:
                self.rapatrier_renvois(enfant, identifiant)

    def connecter_lien(self, entité: lexika.outils.Entité):
        """
        Connecte récursivement les liens (directs ou inclus dans des texte enrichis).
        """
        if hasattr(entité, "spécial") and "lien" in entité.spécial.get("drapeaux", {}):
            cible = self.convertisseur_texte_enrichi.trouver_cible(entité.valeur)
            if cible:
                entité.caractéristiques["cible"] = cible
        if hasattr(entité, "spécial") and "texte enrichi" in entité.spécial.get("drapeaux", {}):
            entité.valeur = self.convertisseur_texte_enrichi.convertir_texte(entité.valeur)
        if hasattr(entité, "descendance"):
            for enfant in entité.descendance:
                self.connecter_lien(enfant)

    def mettre_à_jour_critère_tri(self, abstraction: lexika.outils.Abstraction):
        self.entrée_actuelle.spécial["tri"] = {**self.entrée_actuelle.spécial.get("tri", {}), **{abstraction.spécial["tri"]["type"]: abstraction.entité["valeur"]}}

