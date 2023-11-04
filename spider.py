from enum import Enum

class Card:
  value: int
  """ 1=>Ace ... 13=>King  """
  suit: int
  """ 0=>Clubs, 1=>Spades, 2=>Hearts, 3=>Diamonds"""

  flipped: bool

class State:
  stacks:list[list[Card]]

class Move:
  from_stack:int
  to_stack:int
  num_cards:int

def get_next_moves(s:State)->list[Move]:
  for from_stack_idx,from_stack in enumerate(s):
    for to_stack_idx,to_stack in enumerate(s):
      if from_stack_idx==to_stack_idx: continue
      for num_cards in range(1,len(from_stack)+1):
        if from_stack[-num_cards].

def do_move(s:State,m:Move)->State:
  return s

def print_state(s:State):
  for row in zip(s):
    print(row)