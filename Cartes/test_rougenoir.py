import deck  # game ? rougenoir ?

jeu = deck.Jeu()

jeu.melange()

# question
guess = input('Quelle couleur devinez-vous? [R/N]')

#piocher
carte_tiree = jeu.pioche()
# question : elle la pop ou elle la remet ? fixme

print("Vous avez tire un(e) ", carte_tiree)


# regarder si la carte tire est rouge ou noire
if carte_tiree.color == guess :
    print('gagne')
else:
    print('perdu')

# TODO, FIXME: epuiser le jeu de cartes
#    ajouter un eporte de sortie
