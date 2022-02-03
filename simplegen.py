from audioop import avg
from cgi import test
import rcube
import random
import time
import copy
import numpy as np
import matplotlib.pyplot as plt

# Initializing cube
test_cube = rcube.RCube()

# Simple Genetic Algorithm function
def sga(input_cube, chrom_size=70, pop_size=100, num_iter=6000, rr_prob=0.4, num_resets=5, num_swaps=5, cross_prob=0.8, parent_prop=0.01):
    
    # Saves the original state of the cube. This helps with resetting the cube after checking the fitness
    shuffled_state = input_cube.cube_mat

    # Seeding random number generator
    random.seed(time.time())

    # Checks if first argument is a cube
    if not isinstance(input_cube, rcube.RCube):
        print("That's not a cube :C")
        return
    
    # Initializing initial population
    population = []
    for _ in range(pop_size):
        chromosome = [random.randrange(0, 18) for _ in range(chrom_size)]
        for idx in range(1, chrom_size - 1):
            if chromosome[idx] % 2 == 0 and (chromosome[idx] + 1 == chromosome[idx - 1] or chromosome[idx] + 1 == chromosome[idx + 1]):
                chromosome[idx] = random.randrange(0, 18)
            if chromosome[idx] % 2 == 1 and (chromosome[idx] - 1 == chromosome[idx - 1] or chromosome[idx] - 1 == chromosome[idx + 1]):
                chromosome[idx] = random.randrange(0, 18)
        input_cube.cube_mat = shuffled_state
        population.append((input_cube.run_list(chromosome), chromosome))

    # Simple Genetic Algorithm Implementation
    all_avg_fit = []
    all_max_fit = []
    for iter in range(num_iter):

        # Roulette Wheel Selection
        sum_f = np.sum([f for f, _ in population])
        prob_dist = [float(c[0] / sum_f) for c in population]
        indices = np.random.choice(pop_size, pop_size, p=prob_dist)
        mating_pool = [copy.deepcopy(population[idx]) for idx in indices]

        # Generating children from parents
        for idx in range(int(pop_size / 2)):
            # Copying parents to children
            _, p1_list = mating_pool[2 * idx]
            _, p2_list = mating_pool[2 * idx + 1]
            c1_chrom = copy.deepcopy(p1_list)
            c2_chrom = copy.deepcopy(p2_list)

            # Crossover Recombination
            for z in range(chrom_size):
                if random.random() < cross_prob:
                    c1_chrom[z], c2_chrom[z] = c2_chrom[z], c1_chrom[z]

            # Random Reset Mutation
            if random.random() < rr_prob:
                for _ in range(num_resets):
                    c1_chrom[random.randrange(chrom_size)] = random.randrange(0, 18)
            if random.random() < rr_prob:
                for _ in range(num_resets):
                    c2_chrom[random.randrange(chrom_size)] = random.randrange(0, 18)

            # Swap Mutation
            for _ in range(0, num_swaps):
                idx = random.randrange(chrom_size - 1)
                c1_chrom[idx], c1_chrom[idx + 1] = c1_chrom[idx + 1], c1_chrom[idx]
            for _ in range(0, num_swaps):
                idx = random.randrange(chrom_size - 1)
                c2_chrom[idx], c2_chrom[idx + 1] = c2_chrom[idx + 1], c2_chrom[idx]

            # Checking for pointless swaps
            for j in range(1, chrom_size - 1):
                if c1_chrom[j] % 2 == 0 and (c1_chrom[j] + 1 == c1_chrom[j - 1] or c1_chrom[j] + 1 == c1_chrom[j + 1]):
                    c1_chrom[j] = random.randrange(0, 18)
                if c1_chrom[j] % 2 == 1 and (c1_chrom[j] - 1 == c1_chrom[j - 1] or c1_chrom[j] - 1 == c1_chrom[j + 1]):
                    c1_chrom[j] = random.randrange(0, 18)
            for j in range(1, chrom_size - 1):
                if c2_chrom[j] % 2 == 0 and (c2_chrom[j] + 1 == c2_chrom[j - 1] or c2_chrom[j] + 1 == c2_chrom[j + 1]):
                    c2_chrom[j] = random.randrange(0, 18)
                if c2_chrom[j] % 2 == 1 and (c2_chrom[j] - 1 == c2_chrom[j - 1] or c2_chrom[j] - 1 == c2_chrom[j + 1]):
                    c2_chrom[j] = random.randrange(0, 18)

            # Updating the fitness of each child to match their new mutated chromosome
            input_cube.cube_mat = shuffled_state
            c1_fit = input_cube.run_list(c1_chrom)
            if c1_fit == 54:
                print("Rubik's Cube Solved!")
                print("Solution:", c1_chrom)
                return c1_chrom, all_avg_fit, all_max_fit
            input_cube.cube_mat = shuffled_state
            c2_fit = input_cube.run_list(c2_chrom)
            if c2_fit == 54:
                print("Rubik's Cube Solved!")
                print("Solution:", c2_chrom)
                return c2_chrom, all_avg_fit, all_max_fit

            child_1 = (c1_fit, c1_chrom)
            child_2 = (c2_fit, c2_chrom)

            # Determining whether child makes it to the mating pool
            # Original condition: if (child_1[0] >= parent_1[0] and child_1[0] >= parent_2[0]) and (not child_1 in mating_pool):
            if not child_1 in mating_pool:
                mating_pool.append(child_1)
            if not child_2 in mating_pool:
                mating_pool.append(child_2)

            # Adding top % of the population to the mating pool. Adds a bit of greediness to the algorithm.
            # Percentage is determined by the parent_prop argument.
            population.sort(reverse=True)
            mating_pool.extend([copy.deepcopy(p) for p in population[:int(parent_prop*pop_size)]])
        
        # Randomizing mating pool and adding just enough to the population
        np.random.shuffle(mating_pool)

        # Replacing population with a random selection from the mating pool
        population = mating_pool[:pop_size]

        # Calculating fitness metrics
        avg_f = np.average([f for f, _ in population])
        max_f = np.max([f for f, _ in population])
        all_avg_fit.append(avg_f)
        all_max_fit.append(max_f)

        # Prints out the iteration number.
        output_step = int(num_iter / 1000)
        if not output_step:
            output_step = 10
        if iter % output_step == 0:
            print(f"Iter: {iter} | Avg. Fitness: {avg_f}")
    return [], all_avg_fit, all_max_fit

all_chrom_size = [50, 100]
all_pop_size = [100, 200]
all_num_iter = [2000, 4000, 6000]
all_rr_prob = [0.5, 0.7, 0.9]
all_cross_prob = [0.5, 0.7, 0.9]
all_num_resets = [5, 50, 100]
all_num_swaps = [5, 50, 100]
all_parent_prop = [0.01, 0.02, 0.05, 0.10]

all_parameters = [{'cs': cs, 'ps': ps, 'ni': ni, 'rr': rr, 'cp': cp, 'nr': nr, 'ns': ns, 'pp': pp} \
    for cs in all_chrom_size \
    for ps in all_pop_size \
    for ni in all_num_iter
    for rr in all_rr_prob
    for cp in all_cross_prob \
    for nr in all_num_resets \
    for ns in all_num_swaps \
    for pp in all_parent_prop
    ]

for param in all_parameters:
    # Shuffling cube with 22 moves
    random.seed(time.time())
    for _ in range(22):
        op = random.randrange(0, 18)
        test_cube.rotate(op)
    
    # Outputting cube state and params
    test_cube.print_colors()
    print("Params:", param)
    
    # Running sga algorithm
    solution, all_avg_fit, all_max_fit = sga(test_cube, chrom_size=param['cs'], pop_size=param['ps'], num_iter=param['ni'], rr_prob=param['rr'], num_resets=param['nr'], num_swaps=param['ns'], cross_prob=param['cp'], parent_prop=param['pp'])
    
    # Saving avg graph fitness
    plt.plot(range(len(all_avg_fit)), all_avg_fit, label='avg fitness')
    plt.savefig('graphs/avg/sga-average-{}-{}-{}-{}-{}-{}-{}-{}.png'.format(param['cs'], param['ps'], param['ni'], param['rr'], param['nr'], param['ns'], param['cp'], param['pp']))
    plt.close()

    # Saving max graph fitness
    plt.plot(range(len(all_max_fit)), all_max_fit, label='max fitness')
    plt.savefig('graphs/max/sga-max-{}-{}-{}-{}-{}-{}-{}-{}.png'.format(param['cs'], param['ps'], param['ni'], param['rr'], param['nr'], param['ns'], param['cp'], param['pp']))
    plt.close()

