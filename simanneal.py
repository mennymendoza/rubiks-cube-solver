import rcube as cb
import random
import time
import math
import copy

# CONSTANTS
TEMP_CYCLES = 100000
# Number of Shuffles: Number of random operations done on cube in initial shuffling
NUM_SHUFFLES = 700
# Iterations per Temperature
ITER_PER_TEMP = 1
# List Size
LIST_SIZE = 100
# Number of Swaps
NUM_SWAPS = 5
# Number of Resets
RAND_RESET_PROB = 0.05

# Generate Simulated Annealing Solution
def gen_sa_sol(init_temp):

    # Cube Initialization
    random.seed(time.time())
    my_cube = cb.RCube()
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    shuff_state = my_cube.cube_mat

    # Initialize Solution
    op_list = []
    for _ in range(0, LIST_SIZE):
        op_list.append(random.randrange(0, 18))
    solution = (my_cube.run_list(op_list), op_list)

    # Main Loop
    for t in range(0, TEMP_CYCLES):

        if t % 1000 == 0:
            print(t)

        # Temp Function
        temp = init_temp - (0.00004*t)
        if (temp <= 0):
            print('Temperature frozen.')
            return

        # Constant Temp Loop
        for _ in (0, ITER_PER_TEMP):
            (f0, old_list) = solution
            new_list = copy.deepcopy(old_list)

            # Generate New Solution
            # Swap Mutation
            for _ in range(0, NUM_SWAPS):
                idx1 = random.randrange(0, LIST_SIZE)
                idx2 = random.randrange(0, LIST_SIZE)
                tempo = new_list[idx1]
                new_list[idx1] = new_list[idx2]
                new_list[idx2] = tempo
            
            # Random Reset Mutation
            for z in range(0, LIST_SIZE):
                if (random.random() < RAND_RESET_PROB):
                    new_list[z] = random.randrange(0, 18)
            
            # Calculates New Fitness
            my_cube.cube_mat = shuff_state
            f1 = my_cube.run_list(new_list)

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
