import deck  # game ? rougenoir ?

jeu = deck.Jeu(4)

jeu.melange()

while jeu.nb_cartes > 0:
    # question
    guess = input('\nQuelle couleur devinez-vous? [R/N] ')

    #TODO vérifier que le format de la carte en input est correct

    #piocher
    jeu.pioche()
    picked_color = jeu.top.color

    # question : elle la pop ou elle la remet ? fixme

    print("Vous avez choisit un(e)", guess)

    print("Vous avez tiré un(e)", picked_color)


    # regarder si la carte tire est rouge ou noire
    if picked_color == guess :
        print('Gagné')
    else:
        print('Perdu')

print("Le jeu de cartes est épuisé !\n")

#TODO ajouter une porte de sortie
