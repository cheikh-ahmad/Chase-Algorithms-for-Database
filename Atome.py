""" 
La classe AtomeRelationnel modélise un AtomeRelationnel , 
il comporte deux attributs  à savoir le nom de la raltion correspondante  et la listes des colonnes de la relation.
"""


class AtomeRelationel:
    def __init__(self, nom_relation, variables):
        self.nom_relation = nom_relation
        self.variables = variables

    def get_nom_relation(self):
        return self.nom_relation


""" 
On modélise un Atome d'égalité intituivement comme suit :  
(' nom_colonn_x ' , ' relation_de_la_colonnex ')= (' nom_colonn_y ', ' relation_de_la_colonney ')
et dans la classe AtomeEgalité ci dessous  la partie gauche est stockée un nommé gauche  et la partie droite dans un attribut nommé droite.
"""


class AtomeEgalite:
    def __init__(self, gauche, droite):
        self.gauche = gauche
        self.droite = droite
