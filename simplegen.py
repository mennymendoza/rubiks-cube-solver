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
        population.append(genotype)
    
    # Helper Functions

    # Main Loop
    for z in population:
        print(z)
    my_cube.run_list(population[0])
    my_cube.print_colors()
    my_cube.reset()
    my_cube.print_colors()
    
    for it in range(0, 500):
        print('Iteration:', it)

gen_sga_sol()