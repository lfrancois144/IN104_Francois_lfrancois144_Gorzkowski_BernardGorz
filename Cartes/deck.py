

class Jeu():
    def melange(self):
        pass

    def pioche(self):
        carte=Carte("R")
        return carte


class Carte():
    def __init__(self, color):
        self.color=color

    def getColor(self):
        return self.color
