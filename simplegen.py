import rcube as cb
import random
import time

# Constants
NUM_SHUFFLES = 700
LIST_SIZE = 50
POPULATION_SIZE = 100
NUM_ITER = 5
RAND_RESET_PROB = 0.8
PROP_CONSTANT = 0.9

def gen_sga_sol():
    # Cube Initialization
    random.seed(time.time())
    my_cube = cb.RCube()
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    og_state = my_cube.cube_mat
    my_cube.print_colors()

    # Generates Initial Population
    population = []
    genotype = []
    for _ in range(0, POPULATION_SIZE):
        genotype = []
        for _ in range(0, LIST_SIZE):
            genotype.append(random.randrange(0, 18))
        my_cube.cube_mat = og_state
        population.append((my_cube.run_list(genotype), genotype))

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
            if (PROP_CONSTANT*random.random() < prob):
                parents.append(g)

        # Generate Children from Parents
        children = []
        for p in parents:
            (_, child) = p
            for c in range(0, len(child)):
                if random.random() < RAND_RESET_PROB:
                    child[c] = random.randrange(0, 18)
            my_cube.cube_mat = og_state
            children.append((my_cube.run_list(child), child))

        # Update Population
        population.sort()
        children.sort(reverse=True)
        for _ in range(0, int(len(children) / 2)):
            population.pop(0)
            population.append(children[0])
            children.pop(0)
    return population
# end def

final_pop = gen_sga_sol()
print(len(final_pop))
for geno in final_pop:
    print(geno)