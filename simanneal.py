import rcube as cb
import random
import time
import math
import copy

# CONSTANTS
TEMP_CYCLES = 100000
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 22
# Iterations per Temperature
ITER_PER_TEMP = 1
# List Size
LIST_SIZE = 50
# Number of Swaps
NUM_SWAPS = 2
# Number of Resets
RAND_RESET_PROB = 0.002

# Generate Simulated Annealing Solution
def gen_sa_sol(init_temp):

    # Cube Initialization
    random.seed(time.time())
    my_cube = cb.RCube()

    # Shuffling Cube
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    shuff_state = my_cube.cube_mat

    # Initialize Solution
    op_list = []
    for z in range(0, LIST_SIZE):
        op_list.append(z % 18)
    solution = (my_cube.run_list(op_list), op_list)

    # Main Loop
    for t in range(0, TEMP_CYCLES):
        # Prints t every 1000 cycles
        if t % 1000 == 0:
            print('t =', t)

        # Temp Function
        temp = init_temp - (0.00002*t)
        if (temp <= 0):
            print('Temperature frozen.')
            return

        # Constant Temp Loop
        for _ in (0, ITER_PER_TEMP):
            (f0, old_list) = solution
            new_list = copy.deepcopy(old_list)

            # Generate new solution
            # Swap Mutation
            for _ in range(0, NUM_SWAPS):
                idx = random.randrange(0, LIST_SIZE - 1)
                temp_val = new_list[idx]
                new_list[idx] = new_list[idx + 1]
                new_list[idx + 1] = temp_val
            
            # Random Reset Mutation
            for z in range(0, LIST_SIZE):
                if (random.random() < RAND_RESET_PROB):
                    new_list[z] = random.randrange(0, 18)
            
            # Calculates new fitness
            my_cube.cube_mat = shuff_state
            f1 = my_cube.run_list(new_list)

            # Check to see if found solution
            if (f1 == 54):
                print('SOLUTION FOUND at T =', init_temp)
                return
            
            # Decides whether to accept new solution
            delta = f0 - f1
            prob_acc = (math.e)**(-delta/temp)
            if (f0 <= f1 or random.random() < prob_acc):
                print(f1, 'accepted!')
                solution = (f1, new_list)
    print('No solution found at T =', init_temp)
# end


gen_sa_sol(2)
