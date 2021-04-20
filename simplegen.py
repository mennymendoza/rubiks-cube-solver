import rcube as cb
import random
import time
import copy

# TODO: add a check when fitness = 54
# TODO: add crossovers
# TODO: take more children
# What I think I'm doing wrong is taking the fittest parents, not the parents that
# generated the fittest children. I actually don't know if this will work due to the
# nature of the Rubik's Cube.

# CONSTANTS
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 700
# List Size: Number of operations in each genotype
LIST_SIZE = 22
# Population Size: Number of genes in fixed population
POPULATION_SIZE = 1000
# Number of Iterations: Number of generations
NUM_ITER = 25000
# Random Resest Probability: Probability of flipping an operation to another random operation
RAND_RESET_PROB = 0.15
# Number of Swaps
NUM_SWAPS = 3
# Proportionality Constant: Value multiplied to selection probability to increase/decrease
# chance of a genotype getting picked to be a parent
PROP_CONSTANT = POPULATION_SIZE / 10

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
    genotype = []
    for _ in range(0, POPULATION_SIZE):
        genotype = []
        for _ in range(0, LIST_SIZE):
            genotype.append(random.randrange(0, 18))
        my_cube.cube_mat = shuff_state
        population.append((my_cube.run_list(genotype), genotype))
    
    # Main Loop
    for i in range(0, NUM_ITER):
        print('Iter:', i)
        # Select Parents
        parents = []
        sum_f = 0
        for g in population:
            (f, _) = g
            sum_f += f
        for g in population:
            (f, _) = g
            prob = float(f / sum_f)
            if (random.random() < PROP_CONSTANT*prob):
                parents.append(g)

        # Generate Children from Parents
        children = []
        for p in parents:
            (_, p_list) = p
            child_list = copy.deepcopy(p_list)
            # Random Reset Mutation
            for c in range(0, len(child_list)):
                if random.random() < RAND_RESET_PROB:
                    child_list[c] = random.randrange(0, 18)
            # Swap Mutation
            for _ in range(0, NUM_SWAPS):
                idx = random.randrange(0, LIST_SIZE - 1)
                temp_val = child_list[idx]
                child_list[idx] = child_list[idx + 1]
                child_list[idx + 1] = temp_val
            my_cube.cube_mat = shuff_state
            child_fit = my_cube.run_list(child_list)
            if child_fit == 54:
                print('Solution found!')
                return (child_fit, child_list)
            children.append((child_fit, child_list))

        # Update Population
        population.sort()
        children.sort(reverse=True)
        for _ in range(0, len(children)):
            population.pop(0)
            population.append(children[0])
            children.pop(0)
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




