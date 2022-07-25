import pygame, random
import numpy as np
from copy import deepcopy
from snake import Snake, SCREEN_SIZE, PIXEL_SIZE
from genome import Genome
import pickle

N_POPULATION = 50
N_BEST = 5
N_CHILDREN = 5
PROB_MUTATION = 0.4

pygame.init()
pygame.font.init()
s = pygame.display.set_mode((SCREEN_SIZE * PIXEL_SIZE, SCREEN_SIZE * PIXEL_SIZE))
pygame.display.set_caption('Snake')

with open('N_1/Gen#19_Fit-925.0.p', 'rb') as file:
  GENOME = pickle.load(file)
  
# generate 1st population
genomes = [Genome() for _ in range(N_POPULATION)]
genomes.extend([GENOME])
best_genomes = None

n_gen = 0
while True:
  n_gen += 1

  for i, genome in enumerate(genomes):
    snake = Snake(s, genome1=genome,genome2=GENOME)
    fitness, score = snake.run()

    genome.fitness = fitness

    # print('Generation #%s, Genome #%s, Fitness: %s, Score: %s' % (n_gen, i, fitness, score))

  if best_genomes is not None:
    genomes.extend(best_genomes)
  genomes.sort(key=lambda x: x.fitness, reverse=True)

  print('===== Generaton #%s\tBest Fitness %s =====' % (n_gen, genomes[0].fitness))
  # print(genomes[0].w1, genomes[0].w2)
  with open(f'Gen#{n_gen}_Fit-{genomes[0].fitness}.p','wb') as file :
    pickle.dump(genomes[0], file)

  best_genomes = deepcopy(genomes[:N_BEST])

  # crossover
  for i in range(N_CHILDREN):
    new_genome = deepcopy(best_genomes[0])
    a_genome = random.choice(best_genomes)
    b_genome = random.choice(best_genomes)

    cut = random.randint(0, new_genome.w1.shape[1])
    new_genome.w1[i, :cut] = a_genome.w1[i, :cut]
    new_genome.w1[i, cut:] = b_genome.w1[i, cut:]

    cut = random.randint(0, new_genome.w2.shape[1])
    new_genome.w2[i, :cut] = a_genome.w2[i, :cut]
    new_genome.w2[i, cut:] = b_genome.w2[i, cut:]

    cut = random.randint(0, new_genome.w3.shape[1])
    new_genome.w3[i, :cut] = a_genome.w3[i, :cut]
    new_genome.w3[i, cut:] = b_genome.w3[i, cut:]

    cut = random.randint(0, new_genome.w4.shape[1])
    new_genome.w4[i, :cut] = a_genome.w4[i, :cut]
    new_genome.w4[i, cut:] = b_genome.w4[i, cut:]

    best_genomes.append(new_genome)

  # mutation
  genomes = []
  for i in range(int(N_POPULATION / (N_BEST + N_CHILDREN))):
    for bg in best_genomes:
      new_genome = deepcopy(bg)

      mean = 20
      stddev = 10

      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w1 += new_genome.w1 * np.random.normal(mean, stddev, size=(6, 10)) / 100 * np.random.randint(-1, 2, (6, 10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w2 += new_genome.w2 * np.random.normal(mean, stddev, size=(10, 20)) / 100 * np.random.randint(-1, 2, (10, 20))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w3 += new_genome.w3 * np.random.normal(mean, stddev, size=(20, 10)) / 100 * np.random.randint(-1, 2, (20, 10))
      if random.uniform(0, 1) < PROB_MUTATION:
        new_genome.w4 += new_genome.w4 * np.random.normal(mean, stddev, size=(10, 3)) / 100 * np.random.randint(-1, 2, (10, 3))

      genomes.append(new_genome)
      