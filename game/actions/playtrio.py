import random
from .action import ActionResult, announce
from .playnope import NopeableAction
from .givecard import GiveCard


class PlayTrioOptions:
  def __init__(self, player, cards, target_players, cards_to_request):
    self.player = player
    self.cards = cards
    self.target_players = target_players
    self.cards_to_request = cards_to_request

  def __contains__(self, action):
    return (isinstance(action, PlayTrio)
            and action.player == self.player
            and action.cards in self.cards
            and action.target_player in self.target_players
            and action.card_to_request in self.cards_to_request)

  def pick_random_action(self):
    return PlayTrio(self.player,
                        random.choice(self.cards),
                        random.choice(self.target_players),
                        random.choice(self.cards_to_request))


class PlayTrio(NopeableAction):
  def __init__(self, player, cards, target_player, card_to_request):
    self.player = player
    self.cards = cards
    self.target_player = target_player
    self.card_to_request = card_to_request
    self.public = self

  def __str__(self):
    return 'play a trio of {} cards and request a {} card from player {}'.format(
           self.cards,
           self.card_to_request,
           self.target_player.id)

  def perform(self, players, discard_pile, _):
    # Discard them
    for _ in range(3):
      self.player.take(self.cards)
      discard_pile.append(self.cards)

    # Announce
    announce(players, self)

    # If not noped:
    if not self._get_nope_count(players, discard_pile) % 2:
      if self.target_player.has(self.card_to_request):
        GiveCard(self.target_player, self.card_to_request, self.player, secret=True).perform(players)
      else:
        AnnounceDontHaveCard(self.target_player, self.card_to_request).perform(players)

    # Still the player's turn
    return ActionResult()


class AnnounceDontHaveCard:
  def __init__(self, player, card):
    self.player = player
    self.card = card
    self.public = self

  def __str__(self):
    return 'announce that they don\'t have a {} card'.format(self.card)

  def perform(self, players):
    # Announce
    announce(players, self)
