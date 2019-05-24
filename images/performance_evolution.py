import matplotlib.pyplot as plt

average = [1.27, 2.13, 5.48, 12.06, 12.81, 12.97, 14.01, 13.11, 13.92, 13.71, 14.85, 17.73, 18.57, 18.8]
median = [1, 2, 5, 12, 13, 13, 14, 13, 14, 14, 15, 18, 19, 19]
sd = [1.3, 1.24, 2.56, 2.13, 2.3, 2.32, 1.99, 1.7, 1.88, 1.68, 1.86, 2.06, 2.24, 2.19]
mini = [0, 0, 0, 4, 5, 5, 5, 6, 6, 6, 7, 6, 3, 2]
maxi = [10, 10, 20, 19, 21, 21, 21, 20, 20, 20, 22, 23, 25, 25]
commits = ["Random", "color advice" ,"clues improvement", "discard", "sed pile", "line swap", "2nd line swap", "oups", "disc unknown card", "Planning clue", "disc old card", "Del exp cards", "Probabilities", "Clever clue"]

poss_avg = [1,3,5,7,9,11,13,15,17,19,21,23,25]

plt.plot(commits, average, 'o')
plt.xlabel('Commits', fontsize=15)
plt.ylabel('Average', fontsize=15)
plt.xticks(commits, fontsize=7, rotation=20)
plt.yticks(poss_avg)
plt.title('Evolution of the average score', fontsize=20)
plt.show()

plt.plot(commits, median, 'o')
plt.xlabel('Commits', fontsize=15)
plt.ylabel('Median', fontsize=15)
plt.xticks(commits, fontsize=7, rotation=20)
plt.yticks(poss_avg)
plt.title('Evolution of the median', fontsize=20)
plt.show()

plt.plot(commits, sd, 'o')
plt.xlabel('Commits', fontsize=15)
plt.ylabel('Standard deviation', fontsize=15)
plt.xticks(commits, fontsize=7, rotation=20)
plt.title('Evolution of the standard deviation', fontsize=20)
plt.show()

plt.plot(commits, mini, 'o')
plt.xlabel('Commits', fontsize=15)
plt.ylabel('Minimum score', fontsize=15)
plt.xticks(commits, fontsize=7, rotation=20)
plt.yticks(poss_avg)
plt.title('Evolution of the minimum score', fontsize=20)
plt.show()

plt.plot(commits, maxi, 'o')
plt.xlabel('Commits', fontsize=15)
plt.ylabel('Maximum score', fontsize=15)
plt.xticks(commits, fontsize=7, rotation=20)
plt.yticks(poss_avg)
plt.title('Evolution of the maximum score', fontsize=20)
plt.show()