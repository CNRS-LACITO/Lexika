 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import lexika

import multiprocessing, multiprocessing.managers


class NébuleuseDʼOméga(lexika.outils.ClasseConfigurée):
    """
    Classe qui permet de préparer la création de dictionnaires avec la gestion du parallélisme.
    """
    def __init__(self, paralléliser: bool = True):
        super().__init__()
        self.paralléliser = paralléliser
        self.lecteur = lexika.outils.Lecteur(self.configuration.informations["base"]["chemin source"])
        self.créateur = lexika.NébuleuseDʼOrion()
        self.nombre_cœurs = multiprocessing.cpu_count()
        self.gestionnaire = multiprocessing.Manager()
        self.résultats = self.gestionnaire.dict({"entrées": self.gestionnaire.dict(), "identifiants": self.gestionnaire.dict(), "balises": self.gestionnaire.dict()})
        self.informations_processus = {}

    def commencer_accrétion(self, nombre_cœurs):
        """
        Commence l'accumulation de données en vue de créer le dictionaire, éventuellement en partitionnnant au préalable les données en cas de parallélisme. 
        """
        self.créateur.préparer_dictionnaire()
        if nombre_cœurs == 1:
            self.lecteur.lire_source()
            self.créateur.lire_données(self.lecteur.données)
        else:   
            balise_bloc = [informations["drapeaux"]["bloc"] for balise, informations in self.configuration.informations["entrée"]["balises"].items() if "bloc" in informations.get("drapeaux", {})][0]
            self.lecteur.lire_source(balise_bloc)
            self.lecteur.partitionner(nombre_cœurs)
            if "en-tête" in self.lecteur.données:
                self.créateur.lire_données(self.lecteur.données["en-tête"])
                en_tête = {clef: valeur for clef, valeur in self.créateur.balises.items()}
                self.créateur.balises.clear()
            for index, bloc_données in enumerate(self.lecteur.données["corps"]):
                processus = multiprocessing.Process(target=self.analyser_bloc_données, args=(bloc_données, index, self.résultats))
                self.informations_processus[index] = processus
                processus.start()
            for processus in self.informations_processus.values():
                processus.join()
            self.créateur.dictionnaire.descendance = [entrée for position, entrées in sorted(self.résultats["entrées"].items()) for entrée in entrées]
            self.créateur.identifiants = {entité: identifiant for position, identifiants in sorted(self.résultats["identifiants"].items()) for entité, identifiant in identifiants.items()}
            occurrences_balises = {**en_tête, **{balise: sum([balises.get(balise, 0) for balises in self.résultats["balises"].values()]) for balises in self.résultats["balises"].values() for balise in balises.keys()}}
            self.créateur.balises = {clef: occurrences_balises[clef] for clef in sorted(occurrences_balises, key=occurrences_balises.get, reverse=True)}
            
    @lexika.outils.Chronométrer(_("analyse du bloc"))
    def analyser_bloc_données(self, bloc_données: list, index: int, résultats: multiprocessing.managers.DictProxy):
        """
        Analyse les blocs de données en parallèle ; cette fonction se trouve dans un autre processus et n'a accès au processus parent que par la variable « résultats ».
        """
        self.créateur.lire_données(bloc_données)
        résultats["entrées"][index] = self.créateur.dictionnaire.descendance
        résultats["identifiants"][index] = self.créateur.identifiants
        résultats["balises"][index] = self.créateur.balises
        
    def connecter_liens(self):
        self.créateur.connecter_liens()

