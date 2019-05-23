#!/usr/bin/env python3

import hanabi
import matplotlib.pyplot as plt
import numpy as np
import contextlib

iter = 10000

possible_scores = np.array([i for i in range(26)])
occurences = np.array([0 for i in range(26)])

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


avg = 0
for i in possible_scores:
    x = occurences[i]
    avg = avg + x*i
avg = avg/iter

sd = 0
for i in possible_scores:
    x = occurences[i]
    sd = sd + x*((i-avg)**2)
sd = np.sqrt(sd/iter)

median = -1
sum = 0
for i in possible_scores:
    x = occurences[i]
    sum = sum + x
    if median == -1 and sum > iter/2:
        median = i

occurences = occurences/iter

i = 0
max_occurences = 0
while i < 26:
    if max_occurences < occurences[i]:
        max_occurences = occurences[i]
    i+=1

X = np.linspace(0,25,10000)
Y = np.exp(-(1/2)*((X-avg)/sd)**2)/(sd*np.sqrt(2*np.pi))
plt.plot(X,Y, color = [41/255, 163/255, 41/255], linewidth = 2)

def plot_bar_x():
    # this is for plotting purpose
    index = np.arange(len(possible_scores))
    plt.bar(index, occurences, alpha = 0.5, color = [48/255,96/255,255/255], edgecolor = [24/255,48/255,255/255], linewidth = 2)
    plt.xlabel('Scores', fontsize=15)
    plt.ylabel('Occurences (normalized)', fontsize=15)
    plt.xticks(index, possible_scores, fontsize=7, rotation=30)
    plt.text(0, 9*max_occurences/10, 'Games = '+str(iter)+'\nMedian = '+str(median)+'\nAverage = '+str(round(avg,2))+'\nStandard deviation = '+str(round(sd,2))+'\nMin = '+str(min)+'\nMax = '+str(max), fontsize=10, horizontalalignment='left', verticalalignment='top')
    plt.title('Times the AI hit different scores', fontsize=20)
    plt.show()

plot_bar_x()