#!/usr/bin/env python3

import hanabi
import matplotlib.pyplot as plt
import numpy as np
import contextlib

iter = 500

possible_scores = [i for i in range(26)]
occurences = [0 for i in range(26)]

with contextlib.redirect_stdout(None):

    for n in range(iter):
        game = hanabi.Game()
        ai = hanabi.ai.BigBrain(game)
        game.ai = ai
        game.run()
        score = game.score

        occurences[score] += 1

i = 0
min = 0
while i < 26 and occurences[i] == 0:
    i += 1
    min = i

i = 25
max = 25
while i >= 0 and occurences[i] == 0:
    i -= 1
    max = i

possible_scores = possible_scores[min:max+1]
occurences = occurences[min:max+1]

def plot_bar_x():
    # this is for plotting purpose
    index = np.arange(len(possible_scores))
    plt.bar(index, occurences)
    plt.xlabel('Scores', fontsize=15)
    plt.ylabel('Occurences', fontsize=15)
    plt.xticks(index, possible_scores, fontsize=10, rotation=30)
    plt.title('Times the AI hit different scores', fontsize=20)
    plt.show()

plot_bar_x()