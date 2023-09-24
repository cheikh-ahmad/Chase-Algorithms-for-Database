"""
Dans ce tout ce qui suit on modélise une base de données comme un dictionnaire dont les clés correspondent aux noms des relations de la base de donnée . Ainsi chaque clé stocke à son tour un dictionnaire contenant deux clés qui sont :  

1°) "columns" qui contient une liste des noms de colonnes 

2°) "rows" qui stocke les lignes de la table correspondante. Ainsi on définit une ligne / tuple comme un dictionnaire dont chaque cle correspond au nom de colonne et la valeur correspondante .

Toutefois, avant de s'avancer dans le code , nous vous proposons un aperçu de la structure d'une base de donnée conforme tel qu'impléméntée ( cf parties suivantes) :

base_de_donnée = 
{

    'nom_relation_1' :
    {
        'columns' : ['colonne_x', 'colonne_y']
        'rows' : [ {'colonne_x': val_1; 'colonne_y': val_2}, 
                   {'colonne_x': val_3; 'colonne_y': val_4}
                 ]
    }
                    
    'nom_relation_2' :
    {
        'columns' : ['colonne_s', 'colonne_t']
        'rows' : [ {'colonne_s': val_1; 'colonne_t': val_2}, 
                   {'colonne_s': val_3; 'colonne_t': val_4}
                 ]
    }                
                    
 }

"""
from Atome import AtomeRelationel, AtomeEgalite
from Dependance import TGD, EGD
from UnknownValue import UnknownValue
import time


class BDD:

    def __init__(self):

        self.tables = {}

    def add_table(self, nom, colonnes):

        self.tables[nom] = {"columns": colonnes, "rows": []}

    def add_tuple(self, table, values):

        if table not in self.tables:

            raise ValueError(
                f" La ralation {table} n'existe pas dans la base de donées")

        if len(values) != len(self.tables[table]['columns']):

            raise ValueError(
                f"Nombre de valeurs incorrect pour la table {table}.")

        self.tables[table]['rows'].append(
            dict(zip(self.tables[table]['columns'], values)))

    def get_table(self, table):

        return self.tables[table]

    def afficher_table(self, table):

        columns = self.tables[table]['columns']
        rows = self.tables[table]['rows']

        # Afficher les noms de colonnes
        print(table.upper())
        print('-' * (len(columns) * 15))
        for col in columns:
            print('{:<15}'.format(col), end='')
        print()

        # Afficher les données
        for row in rows:
            for col in columns:
                print('{:<15}'.format(row[col]), end='')
            print()
        print()

    def afficher_toutes_les_tables(self):
        for table in self.tables:
            self.afficher_table(table)

    def get_tuples_satisfy_body_EGD(self, EGD):
        """
            pour récupérer les tuples satisfaisant le body d'un EGD cette méthode procède aux étapes suivantes :

            - 1°) il stocke séparémment les atomes relationnels et atomes d'égalités respectivement dans des listes relational_atom
              et equality_atom

            - 2°) puis on récupère tous les tuples de chaque table correspondant aux atomes raltionnels qu'on stocke dans un 
              dictionnaire nommé 'rows' et ayant la forme rows = { 'nom_table': [liste de tuples ]}

            - 3°) ensuite définir une sous-fonction nommé verify_egality_EGD(tuples, equality_atom) qui recoit en arguments rows et
              equality_atom cité à l'étape 2 et 1  et on vérifie les tuples en faisant un parcours selon chaque atome d'égalité
        """

        relational_atom = [
            atom for atom in EGD.corps if isinstance(atom, AtomeRelationel)]

        equality_atom = [
            eq for eq in EGD.corps if isinstance(eq, AtomeEgalite)]

        rows = {atom.get_nom_relation(): self.get_table(atom.get_nom_relation())[
            "rows"] for atom in relational_atom}

        def verify_egality_EGD(tuples, equality_atom):

            tuples_satisfies_body = []

            for equality in equality_atom:

                # rappel: un atome d'égalité est modélisé comme suit: [("nom_colonne","nom_relation")]
                for row_1 in rows[equality.gauche[1]]:

                    for row_2 in rows[equality.droite[1]]:

                        if row_1[equality.gauche[0]] == row_2[equality.droite[0]]:

                            this_tuple_verify_body = (
                                (equality.gauche[1], row_1), (equality.droite[1], row_2))

                            tuples_satisfies_body.append(
                                this_tuple_verify_body)
                            # print(tuples_satisfies_body)

                        if not (row_1[equality.gauche[0]] == row_2[equality.gauche[0]]):

                            this_tuple_verify_body = (
                                (equality.gauche[1], row_1), (equality.droite[1], row_2))

                            if this_tuple_verify_body in tuples_satisfies_body:

                                tuples_satisfies_body.remove(
                                    this_tuple_verify_body)

            return tuples_satisfies_body

        tuples_satisfies_body = verify_egality_EGD(rows, equality_atom)

        return (tuples_satisfies_body)

    def is_EGD_head_is_satisfied(self, T, EGD):
        """
          - cette méthode reçoit T un couple (('relation_du_tuple_x', 'tuple_x'),('relation_tuple_y','tuple_y')) satisfaisant le corps de l'EGD 
             et qui est renvoyé par la méthode get_tuples_satisfy_body_EGD

         -  on rappelle qu'une ligne pour nous c'est un dictionnaire de la forme --> {'colonne_s': val_1; 'colonne_t': val_2}

         - Pour vérifier si la tete de l'EGD est satisfaite l'idée est la suivante :
             1°) on vérifie si la colonne sépécifée dans la partie gauche ou droite de l'égalité est dans les clés du tuple_x,
             2°) si oui on sait maintenant que cette colonne est dans la relation relation_du_tuple_x 
             et l'autre colonne de l'égalité est forcément une colonne de la relation oû appartient tuple_y c'est à dire appartient à relation_tuple_y

        """

        # ( tete = [AtomeEgalite( gauche= (colonne ,nom_relationx), droite =(colonne,nom_relationy))]
        variables = EGD.tete
        print(variables[0].gauche)
        #tuple = list(T)

        if variables[0].gauche[0] in T[0][1].keys():
            print(T[0][1][variables[0].gauche[0]])
            print(T[1][1][variables[0].droite[0]])
            if T[0][1][variables[0].gauche[0]] == T[1][1][variables[0].droite[0]]:

                return True

        else:

            if T[0][1][variables[0].droite[0]] == T[1][1][variables[0].gauche[0]]:

                return True

        return False

    def apply_EGD_rules(self, T, EGD):
        """
        - cette méthode reçoit T un couple (('relation_du_tuple_x', 'tuple_x'),('relation_tuple_y','tuple_y')) satisfaisant le corps de l'EGD 
         et qui est renvoyé par la méthode get_tuples_satisfy_body_EGD

         Pour appliquer la règle de l'EGD en procédant aux étapes suivantes:

         1°) on vérifie si la colonne sépécifée dans la partie gauche ou doite de l'égalité est dans les clé du tuple_x,
         2°) si oui on stocke la valeur de T[O][1] dans une variable old_value
         3°) on change dans T la valeur  de la colonne de T[0][1][variables[0].gauche[0] par celle de la colonne T[0][1][variables[0].droite[0] 
         4°) enfin on remplace directement dans la base l'ancien tuple par le nouveau 

        """

        # variables = [AtomeEgalite(gauche=(colone_x, 'relation_de_x'), droite=(colonne_y,'relation_y'))]
        variables = EGD.tete
        # on refait la vérification comme précedemment
        if variables[0].gauche[0] in T[0][1].keys():
            old_value = T[0][1]  # on stocke l'ancienne valeur
            # ici on change dans T la valeur  de la colonne de T[0][1][variables[0].gauche[0] par celle de la colonne T[0][1][variables[0].droite[0]
            T[0][1][variables[0].gauche[0]] = T[1][1][variables[0].droite[0]]
            # une fois fait on fait la mise à jour en insérant  T[0][1] à la place de old_value et ceci en allant checher dans la BDD
            self.tables[T[0][0]]["rows"] = [T[0][1] if tuple ==
                                            old_value else tuple for tuple in self.tables[T[0][0]]["rows"]]

            for index, tuple_ in enumerate(self.tables[T[0][0]]["rows"]):

                if tuple_[variables[0].gauche[0]] == old_value[variables[0].gauche[0]]:
                    print(tuple_)
                    self.tables[T[0][0]]["rows"][index][variables[0].gauche[0]
                                                        ] = T[0][1][variables[0].gauche[0]]

        else:
            old_value = T[1][1]
            T[1][1][variables[0].droite[0]] = T[0][1][variables[0].gauche[0]]

    def get_tuples_satisfy_body_TGD(self, TGD):

        # ici on ne s'intéresse qu'aux atomes relationnels
        relational_atom = [atom for atom in TGD.body]
        rows = {atom.get_nom_relation(): self.get_table(atom.get_nom_relation())["rows"]
                if len(self.get_table(atom.get_nom_relation())["rows"]) != 0 else self.get_table(atom.get_nom_relation())["rows"]
                for atom in relational_atom
                }

        # on fait tous les tuples de la table excepté s'il est vide parceque le tgd est satisfait doffice et pas utile
        return rows

    def is_TGD_head_is_satisfied(self, T, TGD):
        """
        on suppose avoir une seule relation dans le body et aussi une seule dans le head 
        pour vérifier si la tete du tgd est satisfait on procède comme suit :

        1°) on stocke repectivement dans les variables body et head l'atome relationnel du corps et l'atome relationnel du head
        2°) on parcoourt les listes des colonnes du body et du head en meme temps pour trouver des variables/communes aux deux relations
        3°) ensuite  pour chaque tuple tuple_ contenu dans la relation du head on vérifie si tuple_  et T sont en accord sur les variables
        4°) s'ils sont en accord on return True sinon False
        """

        #print("ligne =",T)
        body = TGD.corps     # on récupère le corps du TGD et la tête du tgd
        head = TGD.tete
        cond = False
        cond_2 = True
        commons_variables = []

        for variable_ in body[0].variables:

            if variable_ in head[0].variables:

                commons_variables.append(variable_)

        # maintenant on  parcourt chaque ligne noté tuple_ de la relation du head
        for tuple_ in self.tables[head[0].get_nom_relation()]["rows"]:

            # pusi on vérifie si tuple[variable] = T[variable]
            for variable in commons_variables:

                if tuple_[variable] == T[variable]:

                    cond_2 = cond_2 and True

                else:

                    cond_2 = cond_2 and False

            if cond_2 != cond:
                return cond_2

        return cond

    def get_tuples_satisfy_body_TGD(self, TGD):
        """
         là on part du fait que dans la tête du TGD passé en arguments contient au moins
         un atome relationnel avec un body vide et un head exprimant une égalité entres variables
         et on admet par définition que les head et les body ne sont constiutés que des atomes relationels
        """

        relational_atom = [atom for atom in TGD.corps]
        rows = {atom.get_nom_relation(): self.get_table(atom.get_nom_relation())["rows"]
                if len(self.get_table(atom.get_nom_relation())["rows"]) != 0 else self.get_table(atom.get_nom_relation())["rows"]
                for atom in relational_atom
                }

        return rows

    def apply_TGD_rules(self, T, TGD):
        """"
        on suppose avoir une seule relation dans le body et aussi une seule dans le head 
        pour vérifier si la tete du tgd est satisfait on procède comme suit :

        1°) on stocke repectivement dans les variables body et head l'atome relationnel du corps et l'atome relationnel du head
        2°) on parcoourt les listes des colonnes du body et du head en meme temps pour trouver des variables/communes aux deux relations
        3°) on réupère les olonnes de la relation du head qui nous permettra l'ajout dans notre base de donnée
        4°) et enfin on crée un tuple vide quelconque qu'on remplit avec les valeurs des colonnes spécifiées dans le TGD. Apres avoir
            rempli s'il reste des valeurs none on les remplace par des null marqué grace à la class unknownValue
        """

        body = TGD.corps
        head = TGD.tete

        commons_variables = []

        for variable_ in body[0].variables:

            if variable_ in head[0].variables:

                commons_variables.append(variable_)

        # on récupère les colonnes de relation correspondant au head
        colonnes_relation = self.tables[head[0].get_nom_relation()]["columns"]

        new_tuple = {key: None for key in colonnes_relation}

        for variable in T.keys():

            if variable in commons_variables:

                new_tuple[variable] = T[variable]

                for k, v in new_tuple.items():

                    if v is None:

                        new_tuple[k] = UnknownValue()
                        print(new_tuple)

        self.add_tuple(head[0].get_nom_relation(), new_tuple.values())

    def is_bdd_satisfies_all_constraints(self, constraints):

        rep = True

        for c in constraints:

            if isinstance(c, EGD):

                tuples_satisfy_body_EGD = self.get_tuples_satisfy_body_EGD(c)

                for tuple_ in tuples_satisfy_body_EGD:

                    # ici on fait un  ET-logique pour s'assurer que base de donnée satisfait la conctrainte pour tous les tuples admis
                    rep = rep and self.is_EGD_head_is_satisfied(tuple_, c)
                    print("rep =", rep)
            if isinstance(c, TGD):

                tuples_satisfy_body_TGD = self.get_tuples_satisfy_body_TGD(c)

                for tuple_ in tuples_satisfy_body_TGD[(c.corps[0].get_nom_relation())]:

                    rep = rep and self.is_TGD_head_is_satisfied(tuple_, c)
        return rep

    def standard_chase(self, constraints):
        T = None
        for e in constraints:

            if isinstance(e, EGD):

                # là on récupère tous les tuples qui satifassent le corps de l'EGD
                T = self.get_tuples_satisfy_body_EGD(e)

                for tuple_ in T:

                    if not self.is_EGD_head_is_satisfied(tuple_, e):
                        self.apply_EGD_rules(tuple_, e)

            if isinstance(e, TGD):

                # là on récupère tous les tuples qui satifassent le corps du TGD
                T = self.get_tuples_satisfy_body_TGD(e)
                for k, v in T.items():

                    for tuple_ in v:

                        if not self.is_TGD_head_is_satisfied(tuple_, e):

                            self.apply_TGD_rules(tuple_, e)

    def oblivious_chase(self, constraints):
        for tgd in constraints:

            tuples_satisfy_body = self.get_tuples_satisfy_body_TGD(tgd)
            count = 0

            while len(tuples_satisfy_body) != 0 and count <= 5:

                if len(tuples_satisfy_body) != 0:

                    self.afficher_toutes_les_tables()

                    for k, v in tuples_satisfy_body.items():

                        for tuple in v:

                            self.apply_TGD_rules(tuple, tgd)

                    count += 1
                    if count >= 5:
                        return 0
                    #tuples_satisfy_body = self.get_tuples_satisfy_body_TGD(tgd)

    def Oblivious_skolem_chase(self, EGD):

        equality_atom = [
            eq for eq in EGD.corps if isinstance(eq, AtomeEgalite)]

        variables = EGD.tete

        self.add_table("E", [variables[0].gauche[0] +
                       "i", variables[0].droite[0]+"j"])

        print(self.get_table('E'))

        tuples_satisfy_body = self.get_tuples_satisfy_body_EGD(EGD)

        for tuple_ in tuples_satisfy_body:

            self.add_tuple('E', [(tuple_[0][0], tuple_[0][1][variables[0].gauche[0]]), (tuple_[
                           1][0],  tuple_[1][1][variables[0].droite[0]])])

        print(self.get_table('E'))

        for tuple_ in self.tables['E']['rows']:

            if not isinstance(tuple_[variables[0].gauche[0]+"i"][1], UnknownValue):

               # print(tuple_[variables[0].gauche[0]+"i"][1])

                for T in self.tables[variables[0].droite[1]]['rows']:

                  # print("rows",self.tables[variables[0].droite[1]]['rows'])
                  # print( 'hhkjkkj',tuple_[variables[0].droite[0]+"j"])

                    if T[variables[0].droite[0]] == tuple_[variables[0].droite[0]+"j"][1]:

                        T[variables[0].droite[0]] = tuple_[
                            variables[0].gauche[0]+"i"][1]

            elif not isinstance(tuple_[variables[0].droite[0]+"j"][1], UnknownValue):

                for T in self.tables[variables[0].gauche[1]]['rows']:

                    if T[variables[0].gauche[0]] == tuple_[variables[0].gauche[0]+"i"][1]:

                        T[variables[0].gauche[0]] = tuple_[
                            variables[0].droite[0]+"j"][1]

        del self.tables['E']

    def core_chase(self, constraints):

        added_tuples = []
        removed_tuples = []

        for c in constraints:
            n = len(self.tables[c.tete[0].get_nom_relation()]['rows'])
            # là on récupère tous les tuples qui satifassent le corps du TGD
            T = self.get_tuples_satisfy_body_TGD(c)

            for k, v in T.items():

                for tuple_ in v:

                    self.apply_TGD_rules(tuple_, c)

                    added = self.tables[c.tete[0].get_nom_relation()
                                        ]["rows"][n-1]

                    added_tuples.append((added, c.tete[0].get_nom_relation()))

        print('base de donnée avant kernelization',
              self.afficher_toutes_les_tables())

        for tuple_ in added_tuples:
            for index, tuple_1 in enumerate(reversed(self.tables[tuple_[1]]['rows'])):
                print('index-tuple', index, tuple_1)
                if tuple_1 == tuple_[0]:
                    print('!!')
                    # ici on le supprime temporairement
                    del self.tables[tuple_[1]]['rows'][index]

                    if self.is_bdd_satisfies_all_constraints(constraints):
                        # la base de donnée satisfait l'ensemble des contraintes donc on supprime définitivement le tuple
                        # donc on le remets pas dans la base de donée
                        # donc on l'inscrit dans liste des tuples éliminés de la base de donnée
                        removed_tuples.append(tuple_1)

                    else:
                        # on le remet à sa place
                        self.tables[tuple_[1]]['rows'].insert(index, tuple_1)

        print('base des données après kernelization',
              self.afficher_toutes_les_tables())
