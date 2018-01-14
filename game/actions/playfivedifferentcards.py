import random
from .action import ActionResult, announce
from .playnope import NopeableAction


class PlayFiveDifferentCardsOptions:
  def __init__(self, player, cards, cards_to_take):
    self.player = player
    self.cards = cards
    self.cards_to_take = cards_to_take

  def __contains__(self, action):
    return (isinstance(action, PlayFiveDifferentCards)
            and action.player == self.player
            and action.cards in self.cards
            and action.card_to_take in self.cards_to_take)

  def pick_random_action(self):
    return PlayFiveDifferentCards(self.player,
                                  random.choice(self.cards),
                                  random.choice(self.cards_to_take))


class PlayFiveDifferentCards(NopeableAction):
  def __init__(self, player, cards, card_to_take):
    self.player = player
    self.cards = cards
    self.card_to_take = card_to_take
    self.public = self

  def __str__(self):
    return 'play five different cards ({}) for the chance to take a {} card from the discard pile'.format(
           ', '.join([str(x) for x in self.cards]),
           self.card_to_take)

  def perform(self, players, discard_pile, _):
    for card in self.cards:
      self.player.take(card)
      discard_pile.append(card)

    # Announce
    announce(players, self)

    if not self._get_nope_count(players, discard_pile) % 2:
      TakeCardFromDiscardPile(self.player, self.card_to_take).perform(players, discard_pile)
    return ActionResult()


class TakeCardFromDiscardPile:
  def __init__(self, player, card):
    self.player = player
    self.card = card
    self.public = self

  def __str__(self):
    return 'take a {} card from the discard pile'.format(self.card)

  def perform(self, players, discard_pile):
    discard_pile.remove(self.card)
    self.player.give(self.card)

    # Announce
    announce(players, self)
