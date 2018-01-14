import random
from .robotplayer import RobotPlayer
from .cards import *
from .actions.action import OptionsList
from .actions.draw import DrawOptions
from .actions.playattack import PlayAttackOptions
from .actions.playfavor import PlayFavorOptions
from .actions.playseethefuture import PlaySeeTheFutureOptions
from .actions.playshuffle import PlayShuffleOptions
from .actions.playskip import PlaySkipOptions
from .actions.playpair import PlayPairOptions
from .actions.playtrio import PlayTrioOptions
from .actions.playfivedifferentcards import PlayFiveDifferentCardsOptions


class Game:
  def __init__(self, nets):
    # Initial deck, with no defuses or exploding kittens
    deck = ([attack]*4 +
            [beard]*4 +
            [favor]*4 +
            [melon]*4 +
            [nope]*5 +
            [potato]*4 +
            [rainbow]*4 +
            [seefuture]*5 +
            [shuffle]*4 +
            [skip]*4 +
            [taco]*4)

    # Shuffle deck
    for _ in range(3):
      random.shuffle(deck)

    # Declare players with one defuse and 4 random cards.
    self.players = []
    for id_, net in enumerate(nets):
      starting_cards = [defuse] + [deck.pop() for _ in range(4)]
      self.players.append(RobotPlayer(id_, starting_cards, net))

    # Add extra defuses and exploding kittens into the deck.
    deck.extend([exploding]*(len(self.players)-1) +
                [defuse]*(6-len(self.players)))

    # Shuffle deck again
    for _ in range(3):
      random.shuffle(deck)

    # Declare draw and discard pile
    self.draw_pile = deck
    self.discard_pile = []

    # Tell players we're good to go
    for player in self.players:
      player.tell_game_ready_to_begin(self.players)

  def _generate_options(self, player):
    options = OptionsList([DrawOptions(player)])

    if player.has_any_cards():
      if player.has(attack):
        options.append(PlayAttackOptions(player))

      if player.has(seefuture):
        options.append(PlaySeeTheFutureOptions(player))

      if player.has(shuffle):
        options.append(PlayShuffleOptions(player))

      if player.has(skip):
        options.append(PlaySkipOptions(player))

      pairs = player.get_pairs()
      if player.has(favor) or player.has_any_pair():
        targets = [x for x in self.players if x != player and x.has_any_cards()]
        if targets:
          if player.has(favor):
            options.append(PlayFavorOptions(player, targets))
          if player.has_any_pair():
            options.append(PlayPairOptions(player, player.get_pairs(), targets))
          if player.has_any_trio():
            options.append(PlayTrioOptions(player, player.get_trios(), targets, ownable_cards))

      if player.has_five_different_cards():
        cards_to_take = [x for x in set(self.discard_pile) if x != exploding]
        if cards_to_take:
          cards = player.get_five_card_combos()
          options.append(PlayFiveDifferentCardsOptions(player, cards, cards_to_take))

    return options

  def take_turns(self, player, turns):
    for turn in range(turns):
      while True:
        options = self._generate_options(player)
        result = player.pick_action(options).perform(self.players,
                                                     self.discard_pile,
                                                     self.draw_pile)
        if result.end_turn:
          if result.immediate or turn == turns - 1:
            return result.next_player_turns
          else:
            break

  def play(self):
    nextplayer = self.players[0]
    turns = 1
    while True:
      player = nextplayer
      nextplayernum = (self.players.index(player) + 1) % len(self.players)
      nextplayer = self.players[nextplayernum]
      turns = self.take_turns(player, turns)
      if len(self.players) == 1:
        break

    #print('Player {} is a winrar!'.format(self.players[0].id))
    return self.players[0].id

