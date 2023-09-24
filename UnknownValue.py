""" 
Ci-dessous on définit une class UnknownValue qui permet de créer un null marqué qui va servir par la suite.
Il est à noter que les null sont representés sous frome : null_1, null_10, null_23, null_13 etc... . 
A noter qu'à chaque fois qu'on instancie un UnknownValue c'est à dire un null marqué l'entier x de null_x sera incrémenté de 1 . 
Ceci nous permet de différencier les nulls marqués
"""


class UnknownValue:
    _counter = 0

    def __init__(self):
        self.id = UnknownValue._counter
        UnknownValue._counter += 1

    def __eq__(self, other):
        return isinstance(other, UnknownValue) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"null{self.id}"

    def __format__(self, format_spec):
        return f"null{self.id}"
