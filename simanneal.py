from hashlib import new
import rcube as cb
import random
import time
import math

# CONSTANTS
TEMP_CYCLES = 1000
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 700
# Iterations per Temperature
ITER_PER_TEMP = 5
# Max Temperature
INIT_TEMP = 5000

# Generate Simulated Annealing Solution
def gen_sa_sol():
    # Cube Initialization
    random.seed(time.time())
    my_cube = cb.RCube()
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    my_cube.print_colors()

    for k in range(0, TEMP_CYCLES):
        temp = INIT_TEMP / (1 + math.log10(k+1))
        if (temp <= 0):
            break
        for _ in (0, ITER_PER_TEMP):
            old_state = my_cube.cube_mat
            old_fitness = my_cube.calc_fit()
            my_cube.rotate(random.randrange(0, 18))
            new_fitness = my_cube.calc_fit()
            if (new_fitness == 54):
                print('solution found!')
                return
            delta = old_fitness - new_fitness
            prob_acc = (math.e)**(delta/temp)
            if (new_fitness <= old_fitness or random.random() < prob_acc):
                print(new_fitness, ' accepted')
            else:
                my_cube.cube_mat = old_state
                print('no changes made')
            print('---------------')
# end

gen_sa_sol()