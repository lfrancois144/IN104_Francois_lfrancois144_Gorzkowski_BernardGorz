#!/usr/bin/env python3

import hanabi
import matplotlib.pyplot as plt
import numpy as np
import contextlib

iter = 10

players=[2,3,4,5]
scores_2p=0
scores_3p=0
scores_4p=0
scores_5p=0

with contextlib.redirect_stdout(None):

    for n in range(iter):
        game2 = hanabi.Game(players=2)
        ai = hanabi.ai.BigBrain(game2)
        game2.ai = ai
        game2.run()
        score = game2.score
        scores_2p += score

        game3 = hanabi.Game(players=3)
        ai = hanabi.ai.BigBrain(game3)
        game3.ai = ai
        game3.run()
        score = game3.score
        scores_3p += score

        game4 = hanabi.Game(players=4)
        ai = hanabi.ai.BigBrain(game4)
        game4.ai = ai
        game4.run()
        score = game4.score
        scores_4p += score

        game5 = hanabi.Game(players=5)
        ai = hanabi.ai.BigBrain(game5)
        game5.ai = ai
        game5.run()
        score = game5.score
        scores_5p += score

scores_2p=scores_2p/iter
scores_3p=scores_3p/iter
scores_4p=scores_4p/iter
scores_5p=scores_5p/iter

scores = [scores_2p, scores_3p, scores_4p, scores_5p]
plt.clf()
plt.bar(players, scores, color = [48/255, 96/255, 255/255], edgecolor = [24/255, 48/255, 255/255])
plt.xlabel("Number of players")
plt.ylabel("Average over 10,000 games")
plt.xticks(players, [2,3,4,5])
plt.title("Performance relative to the number of players")
plt.show()
