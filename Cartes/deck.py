from random import *

class Carte():
    def __init__(self, color):
        self.color = color

class Jeu(Carte):
    def __init__(self, nb_cartes):
        colors = ['R','N']
        self.nb_cartes = nb_cartes
        self.cartes = []
        for i in range(nb_cartes//2):
            for dif_colors in colors:
                nouvelle_carte = Carte(dif_colors)
                self.cartes.append(nouvelle_carte)
        self.top = self.cartes[-1]                  #top : carte au dessus du deck

    def melange(self):
        for i in range(self.nb_cartes*10):          #10 arbitraire pour s'assurer que les deck est mélangé
            carte_a = randint(0,self.nb_cartes-1)
            carte_b = randint(0,self.nb_cartes-1)
            self.cartes[carte_a],self.cartes[carte_b]=self.cartes[carte_b],self.cartes[carte_a]
        self.top = self.cartes[-1]

    def pioche(self):
        self.top = self.cartes[-1]
        self.nb_cartes -= 1
        self.cartes.pop()




