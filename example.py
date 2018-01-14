import os
import neat
# import trueskill
from game.game import Game
import random
from collections import Counter
import pprint
import multiprocessing as mp
pp = pprint.PrettyPrinter(indent=2)
import pickle
from datetime import datetime
from elo import Rating, rate_1vs1

prev_gen = {}
ways_parallel = 4
first_to = 4


def worker(in_q, out_q):
  while True:
    work_unit = in_q.get()
    if not work_unit:
      break
    out_q.put(work_unit.do_work())


class WorkUnit(object):
  def __init__(self, game):
    self.game = game

  def do_work(self):
    p1 = self.game[0]
    p2 = self.game[1]
    p1wins = 0
    p2wins = 0
    while True:
      winner = Game((p1[1], p2[1])).play()
      p1wins += 1 - winner
      p2wins += winner
      if p1wins == first_to:
        return list(zip((p1[0], p2[0]), rate_1vs1(p1[2], p2[2])))
      if p2wins == first_to:
        return list(zip((p2[0], p1[0]), rate_1vs1(p2[2], p1[2])))


def eval_genomes(genomes, config):
  nets = {}
  ratings = {}

  for genome_id, genome in genomes:
    ratings[genome_id] = genome.fitness or Rating()
    nets[genome_id] = neat.nn.FeedForwardNetwork.create(genome, config)

  in_q = mp.Queue()
  out_q = mp.Queue()
  processes = [mp.Process(target=worker, args=(in_q, out_q)) for i in range(ways_parallel)]
  for proc in processes:
    proc.start()

  random_order = [x[0] for x in genomes]

  for _ in range(20):
    random.shuffle(random_order)

    counter = 0
    while counter < len(genomes)-1:
      p1, p2 = random_order[counter:counter+2]
      game = ((p1, nets[p1], ratings[p1]), (p2, nets[p2], ratings[p2]))
      in_q.put(WorkUnit(game))
      counter += 2

    responses = 0
    while responses < len(genomes)-1:
      result = out_q.get()
      for player in result:
        ratings[player[0]] = player[1]
      responses += 2

  for _ in range(ways_parallel):
    in_q.put(None)

  pp.pprint(sorted([(k, v) for k, v in ratings.items()], key=lambda x: int(x[1]), reverse=True))

  prev_gen.clear()

  for genome_id, genome in genomes:
    genome.fitness = ratings[genome_id]
    file_Name = '{}.net'.format(genome_id)
    with open(file_Name, 'wb') as fileObject:
      pickle.dump(nets[genome_id], fileObject)
    prev_gen[genome_id] = (ratings[genome_id], nets[genome_id])

  #avg_mu = sum([x.mu for x in ratings.values()])/len(ratings)


def run(config_file):
  # Load configuration.
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                       neat.DefaultSpeciesSet, neat.DefaultStagnation,
                       config_file)

  # Create the population, which is the top-level object for a NEAT run.
  p = neat.Population(config)

  # Add a stdout reporter to show progress in the terminal.
  p.add_reporter(neat.StdOutReporter(True))
  stats = neat.StatisticsReporter()
  p.add_reporter(stats)
  p.add_reporter(neat.Checkpointer(25))

  # Run for up to 300 generations.
  winner = p.run(eval_genomes, 1000000)

  # Display the winning genome.
  print('\nBest genome:\n{!s}'.format(winner))

  # Show output of the most fit genome against training data.
  print('\nOutput:')
  winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
  for xi, xo in zip(xor_inputs, xor_outputs):
    output = winner_net.activate(xi)
    print("input {!r}, expected output {!r}, got {!r}".format(xi, xo, output))

  node_names = {-1:'A', -2: 'B', 0:'A XOR B'}

  p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
  p.run(eval_genomes, 10)


if __name__ == '__main__':
  # Determine path to configuration file. This path manipulation is
  # here so that the script will run successfully regardless of the
  # current working directory.
  # trueskill.setup(tau=0.833, draw_probability=0)
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'config.conf')
  run(config_path)
