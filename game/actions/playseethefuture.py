from .action import ActionResult, announce
from ..cards import seefuture
from .playnope import NopeableAction


class PlaySeeTheFutureOptions:
  def __init__(self, player):
    self.player = player

  def __contains__(self, action):
    return (isinstance(action, PlaySeeTheFuture)
            and action.player == self.player)

  def pick_random_action(self):
    return PlaySeeTheFuture(self.player)


class PlaySeeTheFuture(NopeableAction):
  def __init__(self, player):
    self.player = player
    self.public = self

  def __str__(self):
    return 'play a See the Future card and peek at the top three cards of the draw pile'

  def perform(self, players, discard_pile, draw_pile):
    # Discard it
    self.player.take(seefuture)
    discard_pile.append(seefuture)

    # Announce
    announce(players, self)

    # If not noped, tell player future
    if not self._get_nope_count(players, discard_pile) % 2:
      SeeTheFuture(self.player).perform(players, draw_pile)

    # Still the player's turn
    return ActionResult()


class SeeTheFuture:
  def __init__(self, player):
    self.player = player
    self.future = None
    self.public = self.SeeTheFuturePublic(player)

  class SeeTheFuturePublic:
    def __init__(self, player):
      self.player = player
      self.future = None

  def __str__(self):
    return 'peek at the top three cards of the draw pile'

  def perform(self, players, draw_pile):
    self.future = draw_pile[-3:]

    # Announce
    announce([self.player], self)
    public_players = list(players)
    public_players.remove(self.player)
    announce(public_players, self.public)
