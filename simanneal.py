import rcube as cb
import random
import time
import math

# CONSTANTS
TEMP_CYCLES = 500000
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 700
# Iterations per Temperature
ITER_PER_TEMP = 1
# List Size
LIST_SIZE = 100

# Generate Simulated Annealing Solution
def gen_sa_sol(init_temp):

    # Cube Initialization
    random.seed(time.time())
    my_cube = cb.RCube()
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    shuff_state = my_cube.cube_mat

    # Initialize Solution
    solution = (my_cube.calc_fit(), [])

    # Main Loop
    for t in range(0, TEMP_CYCLES):
        # Temp Function
        temp = init_temp * (0.99997**t)
        if (temp <= 0):
            break

        # Constant Temp Loop
        for _ in (0, ITER_PER_TEMP):
            (f0, _) = solution
            new_list = []
            
            # Generate New Solution
            for _ in range(0, LIST_SIZE):
                new_list.append(random.randrange(0, 18))
            my_cube.cube_mat = shuff_state
            my_cube.run_list(new_list)
            f1 = my_cube.calc_fit()

            if (f1 == 54):
                print('SOLUTION FOUND at T =', init_temp)
                return
            delta = f0 - f1
            prob_acc = (math.e)**(-delta/temp)
            if (f0 <= f1 or random.random() < prob_acc):
                print(f1, 'accepted!')
                solution = (f1, new_list)
    print('No solution found at T =', init_temp)
# end

gen_sa_sol(5)
