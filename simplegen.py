import rcube as cb
import random

# Constants
LIST_SIZE = 50
POPULATION_SIZE = 100
NUM_ITER = 500
RAND_RESET_PROB = 0.3

# Select Parents
def select_p(population):
    parents = []
    sum_f = 0
    for g in population:
        (f, _) = g
        sum_f += f
    for g in population:
        (f, li) = g
        prob = float(f / sum_f)
        print(prob)
        if (random.random() < prob):
            parents.append(g)
    return parents

# Update Population
def update_pop(population, childen):
    new_pop = []
    return new_pop

def gen_sga_sol():
    # Initialization
    my_cube = cb.RCube()

    # Generates Initial Population
    population = []
    genotype = []
    for _ in range(0, POPULATION_SIZE):
        genotype = []
        for _ in range(0, LIST_SIZE):
            genotype.append(random.randrange(0, 18))
        population.append((my_cube.run_list(genotype), genotype))

    # Select Parents
    parents = select_p(population)
    print(parents)

    # Generate Children from Parents
    children = []
    for p in parents:
        (_, child) = p
        for c in range(0, len(child)):
            if random.random() < RAND_RESET_PROB:
                child[c] = random.randrange(0, 18)
        children.append((my_cube.run_list(child), child))
    print(children)
# end def

gen_sga_sol()