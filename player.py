import connect4
from connect4 import *
import json    #for serializing/deserializing the dictionary and save/retrieve to the file/program
import random


##Rewards####################################
GAMMA = 1/COL
WIN_REWARD = 1
LOSE_REWARD = -1
DRAW_REWARD = 0
NOTHING_REWARD = 0
ILLEGAL_MOVE = -2
PROB_EXPERIMENT = 0.01
#############################################


class Player:
  def __init__(self, train=False, opponent=None, piece=None):
      self.piece = piece
      if (piece == None):
          self.piece = self.set_piece(opponent)
      self.ishuman = self.set_ishuman(train)
      self.dict_moves = self.set_dict()
      self.last_move = None
      self.last_board_state_where_move_was_made = None

  def set_piece(self, opponent):
      if opponent != None:
          if (opponent.piece == 'B'):
              return 'R'
          else:
              return 'B'

      while 1:
         piece = input("Enter what piece you want to play('R' or 'B'): ").upper()
         if (piece == 'R' or piece == 'B'):
             return piece
         print ("Invalid input!!")

  def set_ishuman(self, train):
      if train:
          return False
      while 1:
          user_input = input("Is this player a human (Y/N): ").upper()
          if (user_input == 'Y'):
              return True
          if (user_input == 'N'):
               return False
          print ("Invalid Input!!")

  def set_dict(self):
      try:
          fp = open("data.json","r")
          list_of_dicts = json.loads(fp.read())
          if (self.piece == 'B'):
              return list_of_dicts[0]
          else:
              return list_of_dicts[1]
          fp.close()
      except:
          return {}

  def make_move(self, game):
      board_state = game.board_string()
      self.last_board_state_where_move_was_made = board_state
      if self.ishuman == True:
          self.select_col(board_state)
          col = int(input("Enter the colomn to insert in: "))
      else:
          col = self.select_col(board_state)
      game.make_move(col)
      self.last_move = game.last_move
      if (self.last_move == None):
          self.correct_illegal_reward(col, board_state)
      return

  def select_col(self, board_state):
      list_rewards = self.get_list_of_rewards(board_state)
      if not connect4.in_training: print (list_rewards)
      if (random.random() <= PROB_EXPERIMENT):
         col = random.randint(0, COL - 1)
      else:
         col = 0
         for c in range(COL):
             if list_rewards[c] > list_rewards[col]:
                 col = c
      return col

  def get_list_of_rewards(self, board_state):
      list_rewards = []
      if board_state in self.dict_moves:
        return self.dict_moves[board_state]
      else:
        for c in range(0, COL):
            list_rewards.append(0)
        self.dict_moves[board_state] = list_rewards
        return list_rewards

  def correct_the_reward(self, game):
      if self.last_move == None:
          return
      expected_reward = self.dict_moves[self.last_board_state_where_move_was_made][self.last_move]
      actual_reward = 0
      if game.game_over:
          if game.winner == None:
              actual_reward = DRAW_REWARD
          elif game.winner == self.piece:
              actual_reward = WIN_REWARD
          else:
              actual_reward = LOSE_REWARD
      else:
          actual_reward = NOTHING_REWARD
      actual_reward += GAMMA * max(self.get_list_of_rewards(game.board_string()))
      self.dict_moves[self.last_board_state_where_move_was_made][self.last_move]  =  (actual_reward + expected_reward)/2
      return

  def correct_illegal_reward(self, col, board_state):
      actual_reward = ILLEGAL_MOVE + GAMMA * max(self.get_list_of_rewards(board_state))
      self.dict_moves[board_state][col] = (self.dict_moves[board_state][col] + actual_reward)/2
      return

def write_in_file(dict_moves_B, dict_moves_R):
    with open("data.json", 'w') as fp:
        fp.write(json.dumps([dict_moves_B, dict_moves_R, ]))
