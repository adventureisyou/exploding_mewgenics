import random
from .action import announce
from ..cards import unknown


class GiveCardOptions:
  def __init__(self, player, cards, target_players, secret=(True, False)):
    self.player = player
    self.cards = cards
    self.target_players = target_players
    self.secret = secret

  def __contains__(self, action):
    return (isinstance(action, GiveCard)
            and action.player == self.player
            and action.card in self.cards
            and action.target_player in self.target_players
            and action.secret in self.secret)

  def pick_random_action(self):
    return GiveCard(self.player,
                    random.choice(self.cards),
                    random.choice(self.target_players),
                    random.choice(self.secret))


class GiveCard:
  def __init__(self, player, card, target_player, secret=False):
    self.player = player
    self.card = card
    self.target_player = target_player
    self.secret = secret
    self.public = self.GiveCardPublic(player,
                                      card,
                                      target_player,
                                      secret)

  class GiveCardPublic:
    def __init__(self, player, card, target_player, secret):
      self.player = player
      self.card = unknown if secret else card
      self.target_player = target_player
      self.secret = secret

  def __str__(self):
    return '{} give a {} card to player {}'.format(
           'secretly' if self.secret else 'publically',
           self.card,
           self.target_player.id)

  def perform(self, players):
    # Give it
    self.player.take(self.card)
    self.target_player.give(self.card)

    # Announce
    announce([self.player, self.target_player], self)
    public_players = list(players)
    public_players.remove(self.player)
    public_players.remove(self.target_player)
    announce(public_players, self.public)


class GiveRandomCard:
  def __init__(self, player, target_player):
    self.player = player
    self.card = None
    self.target_player = target_player
    self.public = self.GiveRandomCardPublic(player,
                                            target_player)

  class GiveRandomCardPublic:
    def __init__(self, player, target_player):
      self.player = player
      self.card = None
      self.target_player = target_player

  def __str__(self):
    return 'give a random card to player {}'.format(self.target_player.id)

  def perform(self, players):
    if not self.player.has_any_cards():
      AnnounceDontHaveAnyCards(self.player).perform(players)
    else:
      self.card = self.player.get_random_card()

      # Give it
      self.player.take(self.card)
      self.target_player.give(self.card)

      # Announce
      announce([self.player, self.target_player], self)
      public_players = list(players)
      public_players.remove(self.player)
      public_players.remove(self.target_player)
      announce(public_players, self.public)


class AnnounceDontHaveAnyCards:
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'announce that they don\'t have any cards'

  def perform(self, players):
    # Announce
    announce(players, self)
