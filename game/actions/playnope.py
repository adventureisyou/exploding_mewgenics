import random
from ..cards import nope
from .action import OptionsList, announce


def randomly(seq):
  shuffled = list(seq)
  for _ in range(3):
    random.shuffle(shuffled)
  return iter(shuffled)


class NopeableAction:
  def _get_nope_count(self, players, discard_pile, nopes=0):
    for player in randomly(players):
      options = OptionsList((PlayNopeOptions(player), PassOptions(player)))
      if player.has(nope) and player != self.player:
        action = None
        while action not in options:
          action = player.pick_action(options)
        if isinstance(action, PlayNope):
          return action.perform(players, discard_pile, nopes)
    return nopes


class PlayNopeOptions:
  def __init__(self, player):
    self.player = player

  def __contains__(self, action):
    return (isinstance(action, PlayNope)
            and action.player == self.player)

  def pick_random_action(self):
    return PlayNope(self.player)


class PlayNope(NopeableAction):
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'cancel the last action by playing a nope card'

  def perform(self, players, discard_pile, nopes):
    self.player.take(nope)
    discard_pile.append(nope)

    # Announce
    announce(players, self)

    return self._get_nope_count(players, discard_pile, nopes + 1)


class PassOptions:
  def __init__(self, player):
    self.player = player

  def __contains__(self, action):
    return (isinstance(action, Pass)
            and action.player == self.player)

  def pick_random_action(self):
    return Pass(self.player)


class Pass:
  def __init__(self, player):
    self.player = player

  def __str__(self):
    return 'do nothing'

  def perform(self, nopes, *_, **__):
    return nopes
