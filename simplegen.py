import rcube as cb
import random

# Constants
LIST_SIZE = 50
POPULATION_SIZE = 100
NUM_ITER = 500

def gen_sga_sol():
    # Initialization
    my_cube = cb.RCube()

    population = []
    genotype = []
    for _ in range(0, POPULATION_SIZE):
        genotype = []
        for _ in range(0, LIST_SIZE):
            genotype.append(random.randrange(0, 18))
        my_cube.run_list(genotype)
        population.append((my_cube.run_list(genotype), genotype))

    # Helper Functions

    # Main Loop
    for z in population:
        print(z)

    for it in range(0, 500):
        print('Iteration:', it)
# end def

gen_sga_sol()