import random
from ..cards import favor
from .action import ActionResult, announce, OptionsList
from .playnope import NopeableAction
from .givecard import GiveCardOptions, AnnounceDontHaveAnyCards


class PlayFavorOptions:
  def __init__(self, player, target_players):
    self.player = player
    self.target_players = target_players

  def __contains__(self, action):
    return (isinstance(action, PlayFavor)
            and action.player == self.player
            and action.target_player in self.target_players)

  def pick_random_action(self):
    return PlayFavor(self.player,
                     random.choice(self.target_players))


class PlayFavor(NopeableAction):
  def __init__(self, player, target_player):
    self.player = player
    self.target_player = target_player
    self.public = self

  def __str__(self):
    return 'play a Favor card and ask player {} for a card of their choice'.format(self.target_player.id)

  def perform(self, players, discard_pile, _):
    # Discard it
    self.player.take(favor)
    discard_pile.append(favor)

    # Announce
    announce(players, self)

    # If not noped, let player choose card to give
    if not self._get_nope_count(players, discard_pile) % 2:
      if not self.target_player.has_any_cards():
        AnnounceDontHaveAnyCards(self.target_player).perform(players)
      else:
        options = OptionsList([GiveCardOptions(self.target_player, self.target_player.get_distinct_cards(), [self.player])])
        self.target_player.pick_action(options).perform(players)

    # Still player's turn
    return ActionResult()
