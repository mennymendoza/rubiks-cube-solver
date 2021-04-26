import rcube as cb
import random
import time
import copy
import numpy as np
import matplotlib.pyplot as plt

# CONSTANTS
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 22
# List Size: Number of operations in each genotype
LIST_SIZE = 50
# Population Size: Number of genes in fixed population
POPULATION_SIZE = 100
# Number of Iterations: Number of generations
NUM_ITER = 6000
# Random Resest Probability: Probability of chromosome mutating via Random Reset Mutation
RAND_RESET_PROB = 0.4
# Number of Resets
NUM_RESETS = 5
# Number of Swaps
NUM_SWAPS = 5
# Proportionality Constant: Value multiplied to selection probability to increase/decrease
# chance of a genotype getting picked to be a parent
PROP_CONSTANT = 1
# Crossover Probability
CROSSOVER_PROB = 0.8

# Cube Object Initialization
my_cube = cb.RCube()

# Generate Simple Genetic Algorithm Solution
def gen_sga_sol():
    # Cube Initialization
    random.seed(time.time())
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    shuff_state = my_cube.cube_mat

    # Generates Initial Population
    population = []
    for _ in range(0, POPULATION_SIZE):
        genotype = [random.randrange(0, 18) for _ in range(0, POPULATION_SIZE)]
        for idx in range(1, len(genotype) - 1):
            if genotype[idx] % 2 == 0 and (genotype[idx] + 1 == genotype[idx - 1] or genotype[idx] + 1 == genotype[idx + 1]):
                genotype[idx] = random.randrange(0, 18)
            if genotype[idx] % 2 == 1 and (genotype[idx] - 1 == genotype[idx - 1] or genotype[idx] - 1 == genotype[idx + 1]):
                genotype[idx] = random.randrange(0, 18)
        my_cube.cube_mat = shuff_state
        population.append((my_cube.run_list(genotype), genotype))

    fitness_values = []
    # Main Loop
    for i in range(0, NUM_ITER):
        print('Iter:', i)

        # Roulette Wheel Selection
        sum_f = 0
        for g in population:
            (f, _) = g
            sum_f += f
        prob_dist = [float(g[0] / sum_f) for g in population]
        mate_pool_idx = np.random.choice(len(prob_dist), len(prob_dist), p=prob_dist).tolist()
        mate_pool = [copy.deepcopy(population[idx]) for idx in mate_pool_idx]

        # Generate Children from Parents
        for idx in range(int(len(mate_pool)/2)):
            f0 = mate_pool[2 * idx][0]
            f1 = mate_pool[2 * idx + 1][0]
            list_1 = copy.deepcopy(mate_pool[2 * idx])[1]
            list_2 = copy.deepcopy(mate_pool[2 * idx + 1])[1]

            # Mutation / Recombination
            if random.random() < CROSSOVER_PROB:
                # Crossover Recombination
                for z in range(random.randrange(len(list_1))):
                    list_1[z], list_2[z] = list_2[z], list_1[z]
            
            # Random Reset Mutation
            if random.random() < RAND_RESET_PROB:
                for _ in range(NUM_RESETS):
                    list_1[random.randrange(len(list_1))] = random.randrange(0, 18)
            if random.random() < RAND_RESET_PROB:
                for _ in range(NUM_RESETS):
                    list_2[random.randrange(len(list_2))] = random.randrange(0, 18)

            # Swap Mutation
            for _ in range(0, NUM_SWAPS):
                idx = random.randrange(len(list_1) - 1)
                list_1[idx], list_1[idx+1] = list_1[idx+1], list_1[idx]
            for _ in range(0, NUM_SWAPS):
                idx = random.randrange(len(list_2) - 1)
                list_2[idx], list_2[idx+1] = list_2[idx+1], list_2[idx]

            for j in range(1, len(list_1) - 1):
                if list_1[j] % 2 == 0 and (list_1[j] + 1 == list_1[j - 1] or list_1[j] + 1 == list_1[j + 1]):
                    list_1[j] = random.randrange(0, 18)
                if list_1[j] % 2 == 1 and (list_1[j] - 1 == list_1[j - 1] or list_1[j] - 1 == list_1[j + 1]):
                    list_1[j] = random.randrange(0, 18)
            for j in range(1, len(list_2) - 1):
                if list_2[j] % 2 == 0 and (list_2[j] + 1 == list_2[j - 1] or list_2[j] + 1 == list_2[j + 1]):
                    list_2[j] = random.randrange(0, 18)
                if list_2[j] % 2 == 1 and (list_2[j] - 1 == list_2[j - 1] or list_2[j] - 1 == list_2[j + 1]):
                    list_2[j] = random.randrange(0, 18)

            # BETA: trying to just accept different fitness values and let roulette eliminate less fit children
            # Decide whether to add first child to mate pool
            my_cube.cube_mat = shuff_state
            child_f0 = my_cube.run_list(list_1)
            if child_f0 == 54:
                print('Solution Found!')
                return child_f0
            elif child_f0 != f0 and child_f0 != f1:
                mate_pool.append((child_f0, list_1))

            # Decide whether to add second child to mate pool
            my_cube.cube_mat = shuff_state
            child_f1 = my_cube.run_list(list_2)
            if child_f1 == 54:
                print('Solution Found!')
                return child_f1
            elif child_f1 != f0 and child_f1 != f1:
                mate_pool.append((child_f1, list_2))

        # Adding top 10% of the population
        population.sort(reverse=True)
        for p in range(int(0.1 * len(population))):
            mate_pool.append(copy.deepcopy(population[p]))

        # Update Population
        mate_pool.sort()
        (max_fit, _) = mate_pool[-1]
        print(max_fit)
        fitness_values.append(max_fit)
        if len(mate_pool) > POPULATION_SIZE:
            for _ in range(len(mate_pool) - POPULATION_SIZE):
                mate_pool.pop(0)
        population = mate_pool
    plt.plot(list(range(len(fitness_values))), fitness_values)
    plt.show()
    return population
# end def

# Executes SGA algorithm and records execution time
start_time = time.time()
final_pop = gen_sga_sol()
exec_time = time.time() - start_time

# Prints final population output + execution time
print('Population Size:', len(final_pop), '\n----------------')
for geno in final_pop:
    (fit, op_list) = geno
    print('Op List:', end=' ')
    for op in op_list:
        print(my_cube.num_to_op(op), end=' ')
    print('\nFitness:', fit, '\n')
print('Execution Time:', exec_time, 'seconds')




