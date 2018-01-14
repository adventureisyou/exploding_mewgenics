import random
from .action import ActionResult, OptionsList, announce
from ..cards import exploding, defuse, unknown


class DrawOptions:
  def __init__(self, player):
    self.player = player

  def __contains__(self, action):
    return (isinstance(action, Draw)
            and action.player == self.player)

  def pick_random_action(self):
    return Draw(self.player)


class Draw:
  def __init__(self, player):
    self.player = player
    self.card = None
    self.public = self.DrawPublic(self.player)

  class DrawPublic:
    def __init__(self, player):
      self.player = player
      self.card = unknown

  def __str__(self):
    return 'draw a card'

  def perform(self, players, discard_pile, draw_pile):
    self.card = draw_pile.pop()
    if self.card == exploding:
      if self.player.has(defuse):
        PlayDefuse(self.player).perform(players, discard_pile)
        options = OptionsList([PutCardInDrawPileOptions(self.player, (exploding,), list(range(len(draw_pile)+1)), (True,))])
        self.player.pick_action(options).perform(players, draw_pile)
      else:
        Explode(self.player).perform(players)
        return ActionResult(True, True)
    else:
      self.player.give(self.card)

      # Announce
      announce([self.player], self)
      public_players = list(players)
      public_players.remove(self.player)
      announce(public_players, self.public)

    return ActionResult(True)


class PlayDefuse:
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'play a Defuse card, avoiding death by exploding kitten'

  def perform(self, players, discard_pile):
    # Apply
    self.player.take(defuse)
    discard_pile.append(defuse)

    # Announce
    for player in players:
      player.tell_action(self)


class Explode:
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'succumb to the exploding kitten due to lack of a Defuse card'

  def perform(self, players):
    # Apply
    players.remove(self.player)

    # Announce
    announce(players, self)


class PutCardInDrawPileOptions:
  def __init__(self, player, cards, positions, secret=(True, False)):
    self.player = player
    self.cards = cards
    self.positions = positions
    self.secret = secret

  def __contains__(self, action):
    return (isinstance(action, PutCardInDrawPile)
            and action.player == self.player
            and action.card in self.cards
            and action.position in self.positions
            and action.secret in self.secret)

  def pick_random_action(self):
    return PutCardInDrawPile(self.player,
                             random.choice(self.cards),
                             random.choice(self.positions),
                             random.choice(self.secret))


class PutCardInDrawPile:
  def __init__(self, player, card, position, secret=False):
    self.player = player
    self.card = card
    self.position = position
    self.secret = secret
    self.public = self.PutCardInDrawPilePublic(player,
                                               card,
                                               position,
                                               secret)

  class PutCardInDrawPilePublic:
    def __init__(self, player, card, position, secret):
      self.player = player
      self.card = card
      self.position = None if secret else position
      self.secret = secret

  def __str__(self):
    return '{} put a {} card into the deck at position {}'.format(
            'secretly' if self.secret else 'publically',
            self.card,
            self.position)

  def perform(self, players, draw_pile):
    draw_pile.insert(self.position, self.card)

    # Announce
    announce([self.player], self)
    public_players = list(players)
    public_players.remove(self.player)
    announce(public_players, self.public)
