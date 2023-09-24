class EGD:
    def __init__(self, corps, tete):
        self.corps = corps   # une cojonction d'atomes relationnels et/ou d'égalités
        self.tete = tete     # une conjonction d'atomes d'agalité


class TGD:
    def __init__(self, corps, tete):
        self.corps = corps   # une cojonction d'atomes relationnel
        self.tete = tete     # une conjonction d'atomes d'atomes relationnels
