import rcube as cb
import random
import time

# TODO: add a check when fitness = 54
# TODO: add crossovers

# CONSTANTS
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 700
# List Size: Number of operations in each genotype
LIST_SIZE = 50
# Population Size: Number of genes in fixed population
POPULATION_SIZE = 100
# Number of Iterations: Number of generations
NUM_ITER = 5000
# Random Resest Probability: Probability of flipping an operation to another random operation
RAND_RESET_PROB = 0.2
# Proportionality Constant: Value multiplied to selection probability to increase/decrease
# chance of a genotype getting picked to be a parent
PROP_CONSTANT = POPULATION_SIZE / 10

# Cube Object Initialization
my_cube = cb.RCube()

def gen_sga_sol():
    # Cube Initialization
    random.seed(time.time())
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    shuff_state = my_cube.cube_mat
    my_cube.print_colors()

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
    for _ in range(0, NUM_ITER):
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
            (_, child) = p
            for c in range(0, len(child)):
                if random.random() < RAND_RESET_PROB:
                    child[c] = random.randrange(0, 18)
            my_cube.cube_mat = shuff_state
            children.append((my_cube.run_list(child), child))

        # Update Population
        population.sort()
        children.sort(reverse=True)
        for _ in range(0, int(len(children) / 2)):
            population.pop(0)
            population.append(children[0])
            children.pop(0)
        
        for gene in population:
            (f, _) = gene
            if f == 54:
                print('Solution found!')
                return population
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




