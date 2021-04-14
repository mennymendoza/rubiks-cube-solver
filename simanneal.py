from hashlib import new
import rcube as cb
import random
import time
import math

# CONSTANTS
TEMP_CYCLES = 100000
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 700
# Iterations per Temperature
ITER_PER_TEMP = 5
# Max Temperature
INIT_TEMP = 10

# Generate Simulated Annealing Solution
def gen_sa_sol():
    # Cube Initialization
    random.seed(time.time())
    my_cube = cb.RCube()
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    my_cube.print_colors()

    # Temp Initialization
    temp = INIT_TEMP

    for k in range(0, TEMP_CYCLES):
        temp = temp / (1 + math.log10(k+1))
        if (temp <= 0):
            break
        for _ in (0, ITER_PER_TEMP):
            old_state = my_cube.cube_mat
            old_fitness = my_cube.calc_fit()
            my_cube.rotate(random.randrange(0, 18))
            new_fitness = my_cube.calc_fit()
            delta = old_fitness - new_fitness
            if (new_fitness <= old_fitness):
                print(new_fitness, ' accepted')
            elif (random.random() < ((math.e)**(delta/temp))):
                print(new_fitness, ' accepted anyway')
            else:
                my_cube.cube_mat = old_state
                print('no changes made')
            print('---------------')
# end

gen_sa_sol()