import random


def announce(players, action):
  #if hasattr(action, 'public'):
  #  print('Player {} decides to {}'.format(action.player.id, action))
  for player in players:
    player.tell_action(action)


class ActionResult:
  def __init__(self, end_turn=False, immediate=False, next_player_turns=1):
    self.end_turn = end_turn
    self.immediate = immediate
    self.next_player_turns = next_player_turns


class OptionsList(list):
  def __init__(self, *args):
    list.__init__(self, *args)

  def __contains__(self, action):
    for options in self:
      if action in options:
        return True
    return False

  def pick_random_action(self):
    return random.choice(self).pick_random_action()
