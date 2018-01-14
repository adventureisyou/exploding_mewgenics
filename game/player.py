import random
from collections import Counter
from itertools import combinations
from .cards import *


class Hand(Counter):
  def add(self, card):
    self.update([card])

  def remove(self, card):
    self[card] -= 1
    if self[card] < 1:
      del self[card]

  def count(self, card):
    return self.get(card, 0)


class Player:
  def __init__(self, id_, starting_cards):
    self.id = id_
    self.hand = Hand(starting_cards)

  def give(self, card):
    self.hand.add(card)

  def take(self, card):
    self.hand.remove(card)

  def has_any_cards(self):
    return len(self.hand) > 0

  def has(self, card):
    return card in self.hand

  def has_count(self, card):
    return self.hand.count(card)

  def has_any_pair(self):
    return len(self.get_pairs()) > 0

  def has_pair_of(self, card):
    return card in self.hand and self.hand[card] > 1

  def get_pairs(self):
    return [card for card, count in self.hand.items() if count > 1]

  def has_any_trio(self):
    return len(self.get_trios()) > 0

  def has_trio_of(self, card):
    return card in self.hand and self.hand[card] > 2

  def get_trios(self):
    return [card for card, count in self.hand.items() if count > 2]

  def get_random_card(self):
    return random.choice(list(self.hand.elements()))

  def pick_action(self, possible_actions):
    return possible_actions.pick_random_action()

  def get_distinct_cards(self):
    return list(self.hand.keys())

  def has_five_different_cards(self):
    return len(self.get_distinct_cards()) > 4

  def get_five_card_combos(self):
    return list(combinations(self.get_distinct_cards(), 5))

  def tell_game_ready_to_begin(self, players):
    self.__players = players

  def tell_action(self, action):
    pass

  def tell_future(self, cards):
    pass
