"""
Artificial Intelligence to play Hanabi.
"""
from random import *
import hanabi

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game


class Cheater(AI):
    """
    This player can see his own cards!

    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if blue_coin<8 and an unnecessary card present: discard it.
      * if blue_coin>0: give a clue on precious card (so a human can play with a Cheater)
      * if blue_coin<8: discard the largest one, except if it's the last of its kind or in chop position in his opponent.
    """

    def play(self):
        "Return the best cheater action."
        game = self.game
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]

        if playable:
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print ('Cheater would play:', "p%d"%playable[0][0], end=' ')
            if (len(playable)>1):
                print('but could also pick:', playable[1:])
            else: print()

            return "p%d"%playable[0][0]


        discardable = [ i+1 for (i,card) in
                        enumerate(game.current_hand.cards)
                        if ( (card.number <= game.piles[card.color])
                             or (game.current_hand.cards.count(card)>1)
                        ) ]
        # discard already played cards, doubles in my hand
        # fixme: discard doubles, if I see it in partner's hand
        # fixme: il me manque les cartes sup d'une pile morte

        if discardable and (game.blue_coins<8):
            print ('Cheater would discard:', "d%d"%discardable[0], discardable)
            return "d%d"%discardable[0]

        ## 2nd type of discard: I have a card, and my partner too
        discardable2 = [ i+1 for (i,card) in enumerate(game.current_hand.cards)
                         if card in game.hands[game.other_player].cards
                       ]
        if discardable2 and (game.blue_coins<8):
            print ('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]


        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     game.hands[game.other_player].cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
                   ]
        if precious:
            clue = False
            # this loop is such that we prefer to clue an card close to chop
            # would be nice to clue an unclued first, instead of a already clued
            for p in precious:
                #print (p, p.number_clue, p.color_clue)
                if p.number_clue is False:
                    clue = "c%d"%p.number
                    break
                if p.color_clue is False:
                    clue = "c%s"%p.color
                    break
                # this one was tricky:
                # don't want to give twice the same clue
            if clue:
                print ('Cheater would clue a precious:',
                       clue, precious)
                if game.blue_coins>0:
                    return clue
                print ("... but there's no blue coin left!")


        # if reach here, can't play, can't discard safely, no card to clue-save
        # Let's give a random clue, to see if partner can unblock me
        if game.blue_coins >0:
            print ('Cheater would clue randomly: cW')
            return 'cw'

        # If reach here, can't play, can't discard safely
        # No blue-coin left.
        # Must discard a card. Let's choose a non-precious one (preferably a 4)
        mynotprecious = [ (card.number,i+1) for (i,card) in
                          enumerate(game.current_hand.cards)
                          if not (
                                  (1+game.discard_pile.cards.count(card))
                                  == game.deck.card_count[card.number])
                     ]
        mynotprecious.sort(key=lambda p: (-p[0], p[1]))
        if mynotprecious:
            act = 'd%d'%mynotprecious[0][1]
            print('Cheater is trapped and must discard:', act, mynotprecious)
            return act

        # Oh boy, not even a safe discard, this is gonna hurt!
        # it's a loss. Discard the biggest
        myprecious = [ (card.number,i+1) for (i,card) in enumerate(game.current_hand.cards) ]
        myprecious.sort(key=lambda p: (-p[0], p[1]))
        act = 'd%d'%myprecious[0][1]
        print('Cheater is doomed and must discard:', act, myprecious)
        return act

class Random(AI):
    """
    Plays randomly, but take in account the number of blue coins
    """
    def play(self):
        game=self.game
        coups_possibles = ['d1', 'd2', 'd3', 'd4', 'd5', 'p1', 'p2', 'p3', 'p4', 'p5', 'cR', 'cB', 'cG', 'cW', 'cY', 'c1', 'c2', 'c3', 'c4', 'c5']
        if game.blue_coins==0:
            return(coups_possibles[randint(0,9)])
        elif game.blue_coins==8:
            return(coups_possibles[randint(5,19)])
        else:
            return(coups_possibles[randint(0,19)])

class BigBrain(AI):
    """
<<<<<<< HEAD
    An AI that will beat them all
    """
    def play(self):
        game=self.game
        coups_possibles = ['d1', 'd2', 'd3', 'd4', 'd5', 'p1', 'p2', 'p3', 'p4', 'p5', 'cR', 'cB', 'cG', 'cW', 'cY', 'c1', 'c2', 'c3', 'c4', 'c5'] 
#TODO si on a un 1 et que la pile correspondante ne contient aucune carte
        if 
=======
    A player set to become the best of all
    """
    def play(self):
        game=self.game
        coups_possibles = ['d1', 'd2', 'd3', 'd4', 'd5', 'p1', 'p2', 'p3', 'p4', 'p5', 'cR', 'cB', 'cG', 'cW', 'cY', 'c1', 'c2', 'c3', 'c4', 'c5']
        possible_colors={'R':hanabi.deck.Color.Red, 'B':hanabi.deck.Color.Blue, 'G':hanabi.deck.Color.Green, 'W':hanabi.deck.Color.White, 'Y':hanabi.deck.Color.Yellow}
        one_cards=['R1', 'B1', 'Y1', 'W1', 'G1']
        do_not_discard=[0,0,0,0,0] #Si =1: carte importante à ne pas discard
        discard_list=[0,0,0,0,0]
        #Vérification des cartes en main
        used_piles=0
        #Giving advices if possible
        if game.blue_coins!=0:
            for c in one_cards:
                card_i=1
                for card in game.hands[game.other_player].cards:
                    if card.__eq__(c) and card.number_clue==False:
                        print("Other player have a 1 and doesn't know it, must tell him")
                        return('c1')
                    card_i+=3

            for c in one_cards:
                card_i=1
                for card in game.hands[game.other_player].cards:
                    if card.__eq__(c) and card.color_clue==False:
                        print("Other player knows he have a 1 but doesn't know the color")
                        card_color=str(card.color)[0]
                        return('c'+card_color)
                    card_i+=1

        #Checking if the board is empty, so that a 1 card can be played without knowing its color
        for c in possible_colors:
            if game.piles.get(possible_colors.get(c))!=0:
                used_piles+=1 

        #Playing cards, or including them in discard_list or do_not_discard
        i=1
        for card in game.current_hand.cards:
            if card.number_clue=='1':
                print('Detected a 1')
                if used_piles==0:
                    print('Playing the 1 because the board is empty')
                    return("p"+str(i))
                if card.color_clue != False:
                    print('I know the color')
                    card_color=str(card.color_clue)[0]
                    if game.piles.get(card_color)==0:
                        print('Use case happened')
                        return('p'+str(i))
                    #TODO add card on the discard_list
            elif card.number_clue==5:
                do_not_discard[i-1]=1
            i+=1

        


        print('Plays randomly')
        return(coups_possibles[randint(0,19)])
#TODO si on a un 1 et que la pile correspondante ne contient aucune carte

>>>>>>> 91f13d73bf44e8a7923f0f5cc710da3039ca87c4
#TODO check si les cartes en main peuvent être posées

#TODO créer une liste des cartes jouées -> si on a dans la main une carte déjà posée => Discard

#TODO si le mate a une carte jouable en main -> 2 indices (couleur + num)

#TODO si on a un 5 en main -> pas le drop

<<<<<<< HEAD
#TODO si le mate a un 5 : indice (num)

        if game.blue_coins==0:
            return(coups_possibles[randint(0,9)])
        elif game.blue_coins==8:
            return(coups_possibles[randint(5,19)])
        else:
            return(coups_possibles[randint(0,19)])        
=======
#TODO si le mate a un 5 : indice (num)
>>>>>>> 91f13d73bf44e8a7923f0f5cc710da3039ca87c4
