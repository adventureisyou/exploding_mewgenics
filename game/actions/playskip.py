from ..cards import skip
from .action import ActionResult, announce
from .playnope import NopeableAction


class PlaySkipOptions:
  def __init__(self, player):
    self.player = player

  def __contains__(self, action):
    return (isinstance(action, PlaySkip)
            and action.player == self.player)

  def pick_random_action(self):
    return PlaySkip(self.player)


class PlaySkip(NopeableAction):
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'play a Skip card and immediately end the turn'

  def perform(self, players, discard_pile, _):
    # Discard it
    self.player.take(skip)
    discard_pile.append(skip)

    # Announce
    announce(players, self)

    # If noped, still the player's turn
    if self._get_nope_count(players, discard_pile) % 2:
      return ActionResult()

    # Skip to the next player
    return ActionResult(True)
