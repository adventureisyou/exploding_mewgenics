import random
from .action import ActionResult, announce
from ..cards import shuffle
from .playnope import NopeableAction


class PlayShuffleOptions:
  def __init__(self, player):
    self.player = player

  def __contains__(self, action):
    return (isinstance(action, PlayShuffle)
            and action.player == self.player)

  def pick_random_action(self):
    return PlayShuffle(self.player)


class PlayShuffle(NopeableAction):
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'play a Shuffle card'

  def perform(self, players, discard_pile, draw_pile):
    # Discard it
    self.player.take(shuffle)
    discard_pile.append(shuffle)

    # Announce
    announce(players, self)

    # If not noped, shuffle the draw pile
    if not self._get_nope_count(players, discard_pile) % 2:
      ShuffleDrawPile(self.player).perform(players, draw_pile)

    # Still the player's turn
    return ActionResult()


class ShuffleDrawPile:
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'shuffle the draw pile'

  def perform(self, players, draw_pile):
    # Multiple shuffles to ensure randomness
    for _ in range(3):
      random.shuffle(draw_pile)

    # Announce
    announce(players, self)
