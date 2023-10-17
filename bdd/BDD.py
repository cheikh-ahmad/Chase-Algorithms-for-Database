
class AtomeRelationel :
    def __init__(self, nom_relation, variables):
        self.nom_relation = nom_relation
        self.variables = variables
    
    def get_nom_relation(self):
        return self.nom_relation
class AtomeEgalite :
    def __init__(self,gauche,droite):
        self.gauche = gauche
        self.droite = droite
class EGD :
    def __init__(self, corps, tete):
        self.corps = corps   # une cojonction d'atomes relationnels et/ou d'égalités
        self.tete = tete     # une conjonction d'atomes d'agalité
class TGD :
    def __init__(self, corps, tete):
        self.corps = corps   # une cojonction d'atomes relationnel
        self.tete = tete     # une conjonction d'atomes d'atomes relationnels
class BDD :
    
    def __init__(self):
        self.tables = {}
    
    def add_table(self,nom, colonnes):
        
        self.tables[nom] ={"columns": colonnes, "rows" :[] }
                            
    def add_tuple(self,table,values):
        
        if table  not in self.tables :
            raise ValueError(f" La ralation {table} n'existe pas dans la base de donées") 
        if len(values) != len(self.tables[table]['columns']):
            raise ValueError(f"Nombre de valeurs incorrect pour la table {table}.")
        self.tables[table]['rows'].append(dict(zip(self.tables[table]['columns'], values)))
    
    def get_table(self, table):
        return self.tables[table]
        
    
    def get_tuples_satisfy_body_EGD(self , EGD):
        relational_atom = [atom for atom in  EGD.body if isinstance(atom, AtomeRelationnel)]
        equality_atom = [eq for eq in EGD.body if isinstance(eq, AtomeEgalite)]
        
        rows = {atom.get_nom_relation(): self.get_table(atom.get_nom_relation())["rows"] for atom in relational_atom}
        
        def verify_egality_EGD(tuples, equality_atom):
            tuples_satisfies_body={}
            n= len(equality_atom)
            if len(equality_atom)==1 :
                for equality in equality_atom:
                    for row_1 in rows[equality.gauche[1]]:
                        for row_2 in rows[equality.droite[1]]:
                            if row_1[equality.gauche(0)] == row_2[equality.gauche(0)]:
                                this_tuple_verify_body = set( (set(equality.gauche[1], row_1), set(equality.droite[1], row_2)))
                                tuples_satisfies_body.add(this_tuple_verify_body)
                                
                            if not (row_1[equality.gauche(0)] == row_2[equality.gauche(0)]):
                                this_tuple_verify_body = set( (set(equality.gauche[1], row_1), set(equality.droite[1], row_2)))
                                if this_tuple_verify_body in tuples_satisfies_body:
                                    tuples_satisfies_body.remove(this_tuple_verify_body)
            return tuples_satisfies_body

    def is_EGD_head_is_satisfied(self,T,EGD):
        variables = EGD.tete
        tuple = list(T)
        if variables[0].gauche in T[0].keys():
            if T[0][gauche] == T[1][droite]:
                return True
        
        else:
            if T[0][droite] == T[1][gauche]:
                return True
        
        return False

# pour voir quoi ressemble la structure de la base de donnée
database = BDD()
database.add_table('employees', ['id', 'name', 'salary'])
database.add_tuple('employees', [1, 'Alice', 50000])
database.add_tuple('employees', [2, 'Bob', 60000])
database.add_tuple('employees', [3, 'Charlie', 70000])

database.add_table('departments', ['id', 'name'])
database.add_tuple('departments', [1, 'Sales'])
database.add_tuple('departments', [2, 'Marketing'])

print(database.tables)