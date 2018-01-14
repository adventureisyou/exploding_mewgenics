class Card:
  def __init__(self, name):
    self._name = name

  def __str__(self):
    return self._name

  def __hash__(self):
    return hash(self._name)

  def __eq__(self, other):
    return (isinstance(other, Card)
            and self._name == other._name)


attack = Card('Attack')
beard = Card('Beard Cat')
defuse = Card('Defuse')
favor = Card('Favor')
melon = Card('Melon')
nope = Card('Nope')
potato = Card('Hairy Potato Cat')
rainbow = Card('Rainbow Ralphing Cat')
seefuture = Card('See the Future')
shuffle = Card('Shuffle')
skip = Card('Skip')
taco = Card('Tacocat')
exploding = Card('Exploding Kitten')
unknown = Card('Unknown')

ownable_cards = (attack, beard, defuse, favor, melon, nope, potato, rainbow, seefuture, shuffle, skip, taco)
