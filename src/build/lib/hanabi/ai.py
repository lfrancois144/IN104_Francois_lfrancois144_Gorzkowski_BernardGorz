"""
Artificial Intelligence to play Hanabi.
"""
from random import *
import hanabi

import itertools

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game

    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        #return sum([x.cards for x in self.other_hands], [])
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))

        
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
                         if card in self.other_players_cards
                       ]
        if discardable2 and (game.blue_coins<8):
            print ('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]


        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     self.other_players_cards
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
                    clue = clue[:2]   # quick fix, with 3+ players, can't clue cRed anymore, only cR
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
    A player set to become the best of all
    """
    def play(self):
        game=self.game
        coups_possibles = ['d1', 'd2', 'd3', 'd4', 'd5', 'p1', 'p2', 'p3', 'p4', 'p5', 'cR', 'cB', 'cG', 'cW', 'cY', 'c1', 'c2', 'c3', 'c4', 'c5']
        possible_colors={'R':hanabi.deck.Color.Red, 'B':hanabi.deck.Color.Blue, 'G':hanabi.deck.Color.Green, 'W':hanabi.deck.Color.White, 'Y':hanabi.deck.Color.Yellow}
        one_cards=['R1', 'B1', 'Y1', 'W1', 'G1']
        color_list=['R','B','G','W','Y']
        random_list = ['1','2','3','4','5','R','B','G','W','Y']
        do_not_discard=[0,0,0,0,0] #Si =1: carte importante à ne pas discard
        possible_clue=[]
        playable_plus1={'R':0, 'B':0, 'G':0, 'W':0, 'Y':0}      #RBGWY
        #Vérification des cartes en main
        used_pile_1=0
        used_pile_2=0
        used_pile_3=0
        used_pile_4=0
        used_pile_5=0
        
        for card in game.current_hand.cards:
            if (card.number_clue != False) and (card.color_clue != False):
                card_color=str(card.color_clue)[0]
                if game.piles.get(possible_colors.get(card_color)) == (int(card.number_clue) - 2):
                    playable_plus1[card_color]=1

        
        for c in possible_colors:
            if game.piles.get(possible_colors.get(c))>=1:
                used_pile_1+=1
            if game.piles.get(possible_colors.get(c))>=2:
                used_pile_2+=1
            if game.piles.get(possible_colors.get(c))>=3:
                used_pile_3+=1
            if game.piles.get(possible_colors.get(c))>=4:
                used_pile_4+=1
            if game.piles.get(possible_colors.get(c))==5:
                used_pile_5+=1
        
        #list of piles :

        used_piles_colors = []
        for c in possible_colors:
            used_piles_colors.append(game.piles.get(possible_colors.get(c)))
        
        #Check what types of cards have been discarded
        
        color_lines={'R':0, 'B':1, 'G':2, 'W':3, 'Y':4}
        colors_in_game = [10]*5
        numbers_in_game = [ 15, 10, 10, 10, 5]
        deck_matrix = [[ 3, 2, 2, 2, 1],[ 3, 2, 2, 2, 1],[ 3, 2, 2, 2, 1],[ 3, 2, 2, 2, 1],[ 3, 2, 2, 2, 1]]
        for disc_card in game.discard_pile.cards:
            card_color_ind = color_lines.get(str(disc_card.color)[0])
            card_number_ind = int(disc_card.number)-1
            colors_in_game[card_color_ind] -=1
            numbers_in_game[card_number_ind] -=1
            deck_matrix[card_color_ind][card_number_ind] -=1


        #Check what cards are on the table

        color_count = 0
        for c in possible_colors:
            if game.piles.get(possible_colors.get(c))>=1:
                colors_in_game[color_count] -=1
                numbers_in_game[0] -=1
                deck_matrix[color_count][0] -=1

            if game.piles.get(possible_colors.get(c))>=2:
                colors_in_game[color_count] -=1
                numbers_in_game[1] -=1
                deck_matrix[color_count][1] -=1

            if game.piles.get(possible_colors.get(c))>=3:
                colors_in_game[color_count] -=1
                numbers_in_game[2] -=1
                deck_matrix[color_count][2] -=1

            if game.piles.get(possible_colors.get(c))>=4:
                colors_in_game[color_count] -=1
                numbers_in_game[3] -=1
                deck_matrix[color_count][3] -=1

            if game.piles.get(possible_colors.get(c))==5:
                colors_in_game[color_count] -=1
                numbers_in_game[4] -=1
                deck_matrix[color_count][4] -=1

            color_count += 1

        #Check what types of cards are in other player's hand

        for other_card in self.other_players_cards:
                card_color_ind = color_lines.get(str(other_card.color)[0])
                card_number_ind = int(other_card.number)-1
                colors_in_game[card_color_ind] -=1
                numbers_in_game[card_number_ind] -=1
                deck_matrix[card_color_ind][card_number_ind] -=1

        #Playing cards, or including them in discard_list or do_not_discard
        i=1
        for card in game.current_hand.cards:
            
            #Playing a 1 if nothing has been played
            if card.number_clue=='1' and used_pile_1==0:
                print('Playing the 1 because the board is empty')
                return("p"+str(i))
                        
            elif card.number_clue==5:
                do_not_discard[i-1]=1
            i+=1

        #Plays 5 in priority
        i=1
        for card in game.current_hand.cards:
            if (card.color_clue != False) and (card.number_clue == '5'):
                card_color=str(card.color_clue)[0]
                if (game.piles.get(possible_colors.get(card_color)) == 4) :
                    print('Plays a safe card')
                    return("p"+str(i))
            i+=1

        #Playing a card you know works
        i=1
        for card in game.current_hand.cards:
            if (card.color_clue != False) and (card.number_clue != False):
                card_color=str(card.color_clue)[0]

                if game.piles.get(possible_colors.get(card_color)) == (int(card.number_clue) - 1) :
                    print('Plays a safe card')
                    return("p"+str(i))
                
            i+=1



        #Clues
        if game.blue_coins!=0:
            for card in self.other_players_cards:
                card_color=str(card.color)[0]
                if (playable_plus1[card_color] == 1) and game.piles.get(possible_colors.get(card_color)) == card.number - 1:
                    if card.number_clue == False:
                        print("Planning clue")
                        return('c'+str(card.number))

                    if card.color_clue == False:
                        print("Planning clue")
                        return('c'+str(card_color))




            for card in self.other_players_cards:
                card_color=str(card.color)[0]
                top_card_number=game.piles.get(possible_colors.get(card_color))
                if card.number==top_card_number+1:
                    if card.number_clue==False:
                        print("Giving a number clue about the "+str(card.color)+str(card.number)+", which can be played")
                        return('c'+str(card.number))

                    if card.color_clue==False:
                        print("Giving a color clue about the "+str(card.color)+str(card.number)+", which can be played")
                        return('c'+card_color)
                
                #Lines removed because too expensive, discarding is handled randomly at the end
                #
                #elif card.number<top_card_number+1:
                #    if card.number_clue==False:
                #        print("Giving a number clue about the "+str(card.color)+str(card.number)+", which can be discarded")
                #        return('c'+str(card.number))
                #
                #    if card.color_clue==False:
                #        print(card.color)
                #        print("Giving a color clue about the "+str(card.color)+str(card.number)+", which can be discarded")
                #        return('c'+card_color)

                if card.number_clue==False:
                    possible_clue.append(str(card.number))
                if card.color_clue==False:
                    possible_clue.append(card_color)


        #Smart yolo : for instance plays a 3 if it sees piles of 2's


        if game.red_coins<2:
            playable_count = [0, 0, 0, 0, 0]
            play_order = [1, 2, 3, 4, 5]
            i = 0
            for card_count in used_piles_colors:
                if card_count != 5:
                    playable_count[card_count] = playable_count[card_count] + deck_matrix[i][card_count]
                i+=1
            
            #Estimating chance of getting a card right

            for card_number_ind in range(5):
                if numbers_in_game[card_number_ind] != 0:
                    playable_count[card_number_ind] = playable_count[card_number_ind]/numbers_in_game[card_number_ind]
                
            #Sort algorithm (sorting probabilities from best to worst)
            for j in range(5):
                cursor = playable_count[j]
                cursor2 = play_order[j]
                pos = j
                while pos > 0 and playable_count[pos - 1] < cursor:
                    playable_count[pos] = playable_count[pos - 1]
                    play_order[pos] = play_order[pos - 1]
                    pos = pos - 1
                playable_count[pos] = cursor
                play_order[pos] = cursor2
            
            nb_of_cards = len(game.deck.cards)

            k=0
            while k<5 and playable_count[k] != 0:
                l = 1
                for card in game.current_hand.cards:
                    #The more the game goes on, the more risk is taken
                    if (card.color_clue == False) and (int(card.number_clue) == play_order[k]) and (playable_count[k]>(0.3+((0.6-0.3)/40)*nb_of_cards)):
                        print("Yolo")
                        return("p"+str(l))
                    l+=1
                k+=1

        #Discard
        if game.blue_coins<8:   
            i=1
            for card in game.current_hand.cards:
                if (card.color_clue != False) and (card.number_clue != False):
                    if game.piles.get(possible_colors.get(card_color)) > (int(card.number_clue) - 1) :
                        print('Discards a safe card')
                        return("d"+str(i))

                if used_pile_1==5 and card.number_clue==1:
                    print("All piles have at least a 1")
                    return("d"+str(i))

                if used_pile_2==5 and card.number_clue==2:
                    print("All piles have at least a 2")
                    return("d"+str(i))

                if used_pile_3==5 and card.number_clue==3:
                    print("All piles have at least a 3")
                    return("d"+str(i))

                if used_pile_4==5 and card.number_clue==4:
                    print("All piles have at least a 4")
                    return("d"+str(i))

                if game.piles.get(hanabi.deck.Color.Red)==5 and str(card.color_clue)=='Red':
                    print("Red pile is complete")
                    return("d"+str(i))

                if game.piles.get(hanabi.deck.Color.Blue)==5 and str(card.color_clue)=='Blue':
                    print("Blue pile is complete")
                    return("d"+str(i))
            
                if game.piles.get(hanabi.deck.Color.Green)==5 and str(card.color_clue)=='Green':
                    print("Green pile is complete")
                    return("d"+str(i))

                if game.piles.get(hanabi.deck.Color.White)==5 and str(card.color_clue)=='White':
                    print("White pile is complete")
                    return("d"+str(i))

                if game.piles.get(hanabi.deck.Color.Yellow)==5 and str(card.color_clue)=='Yellow':
                    print("Yellow pile is complete")
                    return("d"+str(i))

                i+=1
            
#            for card in game.current_hand.cards:
#                if (card.color_clue != False) and (card.number_clue == False):

#        if game.red_coins<2 and game.blue_coins==8:
#            print("Yolo")
#            return('p'+random_list[randint(0,4)])
            i = 0
            for card in game.current_hand.cards:
                if (card.color_clue != False) and (card.number_clue != False):
                    card_color=str(card.color_clue)[0]
                    if deck_matrix[color_lines.get(card_color)][int(card.number_clue)-1] == 1:
                        do_not_discard[i] = 1
                i += 1


        
        #If there are many blue coins, give a clue about something they don't know      
        #Deactivated because useless

        if game.blue_coins>8:
            optmizing_clues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #colors then numbers
            for card in self.other_players_cards:
                if game.piles.get(hanabi.deck.Color.Red)==5 and str(card.color_clue)=='Red':
                    optmizing_clues[0] += 1

                if game.piles.get(hanabi.deck.Color.Blue)==5 and str(card.color_clue)=='Blue':
                    optmizing_clues[1] += 1
            
                if game.piles.get(hanabi.deck.Color.Green)==5 and str(card.color_clue)=='Green':
                    optmizing_clues[2] += 1

                if game.piles.get(hanabi.deck.Color.White)==5 and str(card.color_clue)=='White':
                    optmizing_clues[3] += 1

                if game.piles.get(hanabi.deck.Color.Yellow)==5 and str(card.color_clue)=='Yellow':
                    optmizing_clues[4] += 1
                
                if card.number_clue==1:
                    optmizing_clues[5] += 1

                if card.number_clue==2:
                    optmizing_clues[6] += 1

                if card.number_clue==3:
                    optmizing_clues[7] += 1

                if card.number_clue==4:
                    optmizing_clues[8] += 1
                
                if card.number_clue==5:
                    optmizing_clues[9] += 1
            
            i = 1
            max = 0
            while i < 10:
                if optmizing_clues[i] > optmizing_clues[max]:
                    max = i
                i += 1
            
            if max <5 :
                print("Clever clue")
                return('c'+color_list[max])
            
            if max > 4 :
                print("Clever clue")
                return('c'+max-4)


        if game.blue_coins<8:

            choose_from = []
            i = 1
            for card in game.current_hand.cards:
                if (card.color_clue == False) and (card.number_clue == False):
                    choose_from.append(str(i))
                i += 1
            if len(choose_from)!=0:
                print("Discards card with no clue")
                return("d"+choose_from[-1])
            
            #choose_from = []
            #i = 1
            #for card in game.current_hand.cards:
            #    if (card.color_clue == False) or (card.number_clue == False):
            #        choose_from.append(str(i))
            #    i += 1
            #if len(choose_from)!=0:
            #    print("Discards card with one clue")
            #    return("d"+choose_from[-1))


        if game.blue_coins<8:
            discard_list=[]
            i = 1
            for j in do_not_discard:
                if j == 0:
                    discard_list.append(i)
                i += 1
            
            if len(discard_list)!=0:
                print("Discard random but avoid do_not_discard")
                return('d'+str(discard_list[randint(0,len(discard_list) - 1)]))

            print("All or no cards are precious, discards a random card")
            return("d"+str(randint(1,5)))


        #TODO Ne pas donner un clue que l'on connait deja !
        if game.blue_coins!=0:
            print("Giving a random clue")
            if len(possible_clue)==0:
                return('c'+random_list[randint(0,9)])
            return('c'+possible_clue[randint(0,len(possible_clue)-1)])



        print('Plays randomly')
        return(coups_possibles[randint(0,19)])

#TODO definir des priorites entre les cartes au lieu de l'ordre de la main