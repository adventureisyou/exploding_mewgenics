from ..cards import attack
from .action import ActionResult, announce
from .playnope import NopeableAction


class PlayAttackOptions:
  def __init__(self, player):
    self.player = player

  def __contains__(self, action):
    return (isinstance(action, PlayAttack)
            and action.player == self.player)

  def pick_random_action(self):
    return PlayAttack(self.player)


class PlayAttack(NopeableAction):
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'play an Attack card, immediately end the turn, and force the next player to take two turns'

  def perform(self, players, discard_pile, _):
    self.player.take(attack)
    discard_pile.append(attack)

    # Announce
    announce(players, self)

    if self._get_nope_count(players, discard_pile) % 2:
      return ActionResult()
    return ActionResult(True, True, 2)
