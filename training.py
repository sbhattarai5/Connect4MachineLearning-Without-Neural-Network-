import player
from player import *

def play_game(p1, p2):
    g1 = Game()
    while not g1.game_over:
        if (g1.turn == p1.piece):
            if (p1.ishuman):
                print (g1)
            p1.make_move(g1)
            p2.correct_the_reward(g1)
        else:
            if (p2.ishuman):
                print (g1)
            p2.make_move(g1)
            p1.correct_the_reward(g1)
    return g1

how_many_games_to_train = int(input("How many games do you want to train automatically?: "))
hold_prob_experiment = player.PROB_EXPERIMENT
connect4.in_training = True
p1 = Player(train=True, opponent=None, piece='B')
p2 = Player(train=True, opponent=p1)
for i in range(how_many_games_to_train):
    player.PROB_EXPERIMENT = 0.5
    play_game(p1, p2)
write_in_file(p1.dict_moves, p2.dict_moves)
connect4.in_training = False
player.PROB_EXPERIMENT = hold_prob_experiment
print ("Player 1 Initializing......")
p1 = Player()
print ("Initialized.....")
print ("Player 2 Initializing......")
p2 = Player(opponent=p1)
print ("Initialized......")

dict_players = {}
if p1.piece == 'B':
    dict_players = {'B':'Player 1', 'R':'Player 2'}
else:
    dict_players = {'R':'Player 1', 'B':'Player 2'}

g1 = play_game (p1, p2)
print (g1)
if (g1.winner==None):
    print ("It's draw!!")
else:
    print (dict_players[g1.winner], "is the Winner!!")
write_in_file(p1.dict_moves, p2.dict_moves)
