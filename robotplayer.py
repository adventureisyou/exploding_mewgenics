from collections import Counter

from exploding_kittens.player import Player
from exploding_kittens.cards import *
from exploding_kittens.actions.draw import Draw, PlayDefuse, Explode, PutCardInDrawPile
from exploding_kittens.actions.givecard import GiveCard
from exploding_kittens.actions.playattack import PlayAttack
from exploding_kittens.actions.playfavor import PlayFavor
from exploding_kittens.actions.playfivedifferentcards import PlayFiveDifferentCards, TakeCardFromDiscardPile
from exploding_kittens.actions.playnope import PlayNope, PlayNopeOptions, PassOptions
from exploding_kittens.actions.playpair import PlayPair
from exploding_kittens.actions.playseethefuture import PlaySeeTheFuture, SeeTheFuture
from exploding_kittens.actions.playshuffle import PlayShuffle
from exploding_kittens.actions.playskip import PlaySkip
from exploding_kittens.actions.playtrio import PlayTrio, AnnounceDontHaveCard
from exploding_kittens.player import Hand


class RobotPlayer(Player):
  def __init__(self, id_, net):
    self.id = id_
    self.hand = Hand()
    self.net = net

  def tell_game_ready_to_begin(self, players):
    self.__players = players
    self.__discard_pile_knowledge = Hand()
    self.__draw_pile_knowledge = [unknown]*43
    self.__hand_knowledge = {}
    self.__other_player = players[0] if players[0] != self else players[1]
    for player in self.__players:
      self.__hand_knowledge[player] = Hand([unknown]*4 + [defuse])

    self.actions = (
      Draw(self),
      PlayNope(self),
      PlayAttack(self),
      PlaySkip(self),
      PlayFavor(self, self.__other_player),
      PlayShuffle(self),
      PlaySeeTheFuture(self),
      GiveCard(self, nope, self.__other_player),
      GiveCard(self, attack, self.__other_player),
      GiveCard(self, skip, self.__other_player),
      GiveCard(self, favor, self.__other_player),
      GiveCard(self, shuffle, self.__other_player),
      GiveCard(self, seefuture, self.__other_player),
      GiveCard(self, beard, self.__other_player),
      GiveCard(self, rainbow, self.__other_player),
      GiveCard(self, potato, self.__other_player),
      GiveCard(self, melon, self.__other_player),
      GiveCard(self, taco, self.__other_player),
      PlayPair(self, defuse, self.__other_player),
      PlayPair(self, nope, self.__other_player),
      PlayPair(self, attack, self.__other_player),
      PlayPair(self, favor, self.__other_player),
      PlayPair(self, shuffle, self.__other_player),
      PlayPair(self, seefuture, self.__other_player),
      PlayPair(self, beard, self.__other_player),
      PlayPair(self, rainbow, self.__other_player),
      PlayPair(self, potato, self.__other_player),
      PlayPair(self, melon, self.__other_player),
      PlayPair(self, taco, self.__other_player)
    )

  def pick_action(self, options):
    play_type_nope = False
    play_type_give = False
    play_type_discard = True

    if isinstance(options[0], PlayNopeOptions) or isinstance(options[0], PassOptions):
      play_type_nope = True
      play_type_discard = False
    elif isinstance(options[0], GiveCard):
      play_type_give = True
      play_type_discard = False

    inputs = (
      int(play_type_discard),    # play_type_discard
      int(play_type_nope),       # play_type_nope
      int(play_type_give),       # play_type_give
      self.has_count(defuse),    # my_defuse_count
      self.has_count(nope),      # my_nope_count
      self.has_count(attack),    # my_attack_count
      self.has_count(skip),      # my_skip_count
      self.has_count(favor),     # my_favor_count
      self.has_count(shuffle),   # my_shuffle_count
      self.has_count(seefuture), # my_seefuture_count
      self.has_count(beard),     # my_beard_count
      self.has_count(rainbow),   # my_rainbow_count
      self.has_count(potato),    # my_potato_count
      self.has_count(melon),     # my_melon_count
      self.has_count(taco),      # my_taco_count
      self.__discard_pile_knowledge.count(defuse),                 # discarded_defuse_count
      self.__discard_pile_knowledge.count(nope),                   # discarded_nope_count
      self.__discard_pile_knowledge.count(attack),                 # discarded_attack_count
      self.__discard_pile_knowledge.count(skip),                   # discarded_skip_count
      self.__discard_pile_knowledge.count(favor),                  # discarded_favor_count
      self.__discard_pile_knowledge.count(shuffle),                # discarded_shuffle_count
      self.__discard_pile_knowledge.count(seefuture),              # discarded_seefuture_count
      self.__discard_pile_knowledge.count(beard),                  # discarded_beard_count
      self.__discard_pile_knowledge.count(rainbow),                # discarded_rainbow_count
      self.__discard_pile_knowledge.count(potato),                 # discarded_potato_count
      self.__discard_pile_knowledge.count(melon),                  # discarded_melon_count
      self.__discard_pile_knowledge.count(taco),                   # discarded_tacos_count
      self.__hand_knowledge[self.__other_player].count(unknown),   # charlie_unknown_count
      self.__hand_knowledge[self.__other_player].count(defuse),    # charlie_defuse_count
      self.__hand_knowledge[self.__other_player].count(nope),      # charlie_nope_count
      self.__hand_knowledge[self.__other_player].count(attack),    # charlie_attack_count
      self.__hand_knowledge[self.__other_player].count(skip),      # charlie_skip_count
      self.__hand_knowledge[self.__other_player].count(favor),     # charlie_favor_count
      self.__hand_knowledge[self.__other_player].count(shuffle),   # charlie_shuffle_count
      self.__hand_knowledge[self.__other_player].count(seefuture), # charlie_seefuture_count
      self.__hand_knowledge[self.__other_player].count(beard),     # charlie_beard_count
      self.__hand_knowledge[self.__other_player].count(rainbow),   # charlie_rainbow_count
      self.__hand_knowledge[self.__other_player].count(potato),    # charlie_potato_count
      self.__hand_knowledge[self.__other_player].count(melon),     # charlie_melon_count
      self.__hand_knowledge[self.__other_player].count(taco),      # charlie_taco_count
      len(self.__draw_pile_knowledge),                             # deck_count
      len(self.__draw_pile_knowledge) == 1 or self.__draw_pile_knowledge[-1] == exploding,                 # deck_card_1_is_exploding_ind
      len(self.__draw_pile_knowledge) > 1 and self.__draw_pile_knowledge[-1] not in (unknown, exploding),  # deck_card_1_is_not_exploding_ind
      len(self.__draw_pile_knowledge) > 1 and self.__draw_pile_knowledge[-2] == exploding,                 # deck_card_2_is_exploding_ind
      len(self.__draw_pile_knowledge) > 1 and self.__draw_pile_knowledge[-2] not in (unknown, exploding),  # deck_card_2_is_not_exploding_ind
      len(self.__draw_pile_knowledge) > 2 and self.__draw_pile_knowledge[-3] == exploding,                 # deck_card_3_is_exploding_ind
      len(self.__draw_pile_knowledge) > 2 and self.__draw_pile_knowledge[-3] not in (unknown, exploding),  # deck_card_3_is_not_exploding_ind
    )

    #print('Player' + str(self.id))
    #print(inputs)

    outputs = self.net.activate(inputs)

    #print(outputs)

    preferred_actions = list(zip(*sorted(zip(self.actions, outputs), key=lambda x: x[1], reverse=True)))[0]
    for action in preferred_actions:
      if action in options:
        return action

    #print('NO MATCHING ACTIONS')
    return options.pick_random_action()

  def tell_action(self, action):
    name = '_process_{}'.format(action.__class__.__name__.lower().replace('public', ''))
    try:
      function = getattr(self, name)
      function(action)
    except AttributeError as e:
      print(e)

  def _process_draw(self, action):
    self.__hand_knowledge[action.player].add(self.__draw_pile_knowledge.pop())

  def _process_playdefuse(self, action):
    card = defuse if defuse in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    self.__discard_pile_knowledge.add(defuse)

  def _process_explode(self, action):
    pass

  def _process_putcardindrawpile(self, action):
    card = action.card if action.card in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    if action.position:
      self.__draw_pile_knowledge.insert(action.position, action.card)
    else:
      self.__draw_pile_knowledge = [unknown]*len(self.__draw_pile_knowledge)

  def _process_givecard(self, action):
    if not action.card:
      self.__hand_knowledge[action.player] = [unknown]*len(self.__hand_knowledge[action.player].elements())
      self.__hand_knowledge[action.player].remove(unknown)
      self.__hand_knowledge[action.player].add(unknown)
    else:
      card = action.card if action.card in self.__hand_knowledge[action.player] else unknown
      self.__hand_knowledge[action.player].remove(card)
      self.__hand_knowledge[action.player].add(action.card)

  def _process_giverandomcard(self, action):
    if not action.card:
      self.__hand_knowledge[action.player] = [unknown]*len(self.__hand_knowledge[action.player].elements())
      self.__hand_knowledge[action.player].remove(unknown)
      self.__hand_knowledge[action.player].add(unknown)
    else:
      card = action.card if action.card in self.__hand_knowledge[action.player] else unknown
      self.__hand_knowledge[action.player].remove(card)
      self.__hand_knowledge[action.player].add(action.card)

  def _process_playattack(self, action):
    card = attack if attack in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    self.__discard_pile_knowledge.add(attack)

  def _process_playfavor(self, action):
    card = favor if favor in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    self.__discard_pile_knowledge.add(favor)

  def _process_playfivedifferentcards(self, action):
    for card in action.cards:
      card_to_remove = card if card in self.__hand_knowledge[action.player] else unknown
      self.__hand_knowledge[action.player].remove(card_to_remove)
      self.__discard_pile_knowledge.add(card)

  def _process_takecardfromdiscardpile(self, action):
    self.__discard_pile_knowledge.remove(action.card)
    self.__hand_knowledge[action.player].add(action.card)

  def _process_playnope(self, action):
    card = nope if nope in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    self.__discard_pile_knowledge.add(nope)

  def _process_playpair(self, action):
    for _ in range(2):
      card_to_remove = action.cards if action.cards in self.__hand_knowledge[action.player] else unknown
      self.__hand_knowledge[action.player].remove(card_to_remove)
      self.__discard_pile_knowledge.add(action.cards)

  def _process_playshuffle(self, action):
    card = shuffle if shuffle in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    self.__discard_pile_knowledge.add(shuffle)

  def _process_shuffledrawpile(self, action):
    self.__draw_pile_knowledge = [unknown]*len(self.__draw_pile_knowledge)

  def _process_playseethefuture(self, action):
    card = seefuture if seefuture in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    self.__discard_pile_knowledge.add(seefuture)

  def _process_seethefuture(self, action):
    if action.future:
      for idx, card in enumerate(reversed(action.future)):
        self.__draw_pile_knowledge[-idx] = card

  def _process_playskip(self, action):
    card = skip if skip in self.__hand_knowledge[action.player] else unknown
    self.__hand_knowledge[action.player].remove(card)
    self.__discard_pile_knowledge.add(skip)

  def _process_playtrio(self, action):
    for _ in range(3):
      card_to_remove = action.cards if action.cards in self.__hand_knowledge[action.player] else unknown
      self.__hand_knowledge[action.player].remove(card_to_remove)
      self.__discard_pile_knowledge.add(action.cards)

  def _process_announcedonthavecard(self, action):
    pass
    #for _ in range(self.__hand_knowledge[action.player][action.card]):
    #  self.__hand_knowledge[action.player].remove(action.card)

  def _process_announcedonthaveanycards(self, action):
    pass
    #self.__hand_knowledge[action.player] = Hand()
