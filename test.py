from game.game import Game
import pickle

file_Name = '462.net' #1456 1149
with open(file_Name, 'rb') as fileObject:
  net1 = pickle.load(fileObject)

file_Name = '1027.net' #1119 #584
with open(file_Name, 'rb') as fileObject:
  net2 = pickle.load(fileObject)

wins = 0
for _ in range(100):
  game = Game([net1, net2])
  wins += game.play()

print(wins/100)
