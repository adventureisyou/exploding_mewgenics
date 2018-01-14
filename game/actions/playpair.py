import random
from .playnope import NopeableAction
from .action import ActionResult, announce
from .givecard import GiveCard, GiveRandomCard


class PlayPairOptions:
  def __init__(self, player, cards, target_players):
    self.player = player
    self.cards = cards
    self.target_players = target_players

  def __contains__(self, action):
    return (isinstance(action, PlayPair)
            and action.player == self.player
            and action.cards in self.cards
            and action.target_player in self.target_players)

  def pick_random_action(self):
    return PlayPair(self.player,
                    random.choice(self.cards),
                    random.choice(self.target_players))


class PlayPair(NopeableAction):
  def __init__(self, player, cards, target_player):
    self.player = player
    self.cards = cards
    self.target_player = target_player
    self.public = self

  def __str__(self):
    return 'play a pair of {} cards and take a random card from player {}'.format(
           self.cards,
           self.target_player.id)

  def perform(self, players, discard_pile, _):
    # Discard them
    for _ in range(2):
      self.player.take(self.cards)
      discard_pile.append(self.cards)

    # Announce
    announce(players, self)

    # If not noped
    if not self._get_nope_count(players, discard_pile) % 2:
      GiveRandomCard(self.target_player, self.player).perform(players)

    # Still the player's turn
    return ActionResult()
