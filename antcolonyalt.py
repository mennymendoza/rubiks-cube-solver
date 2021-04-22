import rcube as cb
import random
import time
import copy

# CONSTANTS
NUM_ANTS = 1000
LIST_SIZE = 50
NUM_SHUFFLES = 22
NUM_STEPS = 5000
RAND_RESET_PROB = 0.01
NUM_SWAPS = 2
ALPHA = 2
BETA = 5
RHO = 0.7

def gen_aco_sol():
    # Cube Initialization
    my_cube = cb.RCube()
    random.seed(time.time())
    for _ in range(0, NUM_SHUFFLES):
        my_cube.rotate(random.randrange(0, 18))
    shuff_state = my_cube.cube_mat

    # Initialize pheremones
    pher = [[1]*LIST_SIZE]*18

    # Generate Colony
    colony = []
    for _ in range(0, NUM_ANTS):
        pos_sol = []
        for _ in range(0, LIST_SIZE):
            pos_sol.append(random.randrange(0, 18))
        my_cube.cube_mat = shuff_state
        f = my_cube.run_list(pos_sol)
        colony.append((f, copy.deepcopy(pos_sol)))
    
    for _ in range(0, NUM_STEPS):
        all_trans = []
        for ant in colony:
            neighbor = copy.deepcopy(ant)
            (f0, op_list) = neighbor

            transitions = []

            # Random Reset Mutation
            for c in range(0, len(op_list)):
                if random.random() < RAND_RESET_PROB:
                    op_list[c] = random.randrange(0, 18)
                    transitions.append((op_list[c], c))
            
            # Swap Mutation
            for _ in range(0, NUM_SWAPS):
                idx = random.randrange(0, LIST_SIZE - 1)
                temp_val = op_list[idx]
                op_list[idx] = op_list[idx + 1]
                op_list[idx + 1] = temp_val
                transitions.append((op_list[idx], idx))
                transitions.append((op_list[idx + 1],idx + 1))
            
            # Find Neighbor's Fitness
            my_cube.cube_mat = shuff_state
            fitness = my_cube.run_list(op_list)
            if fitness == 54:
                print('Solution found!')
                return (fitness, op_list)
            
            # Calculate Probability
            tao = 0
            for tran in transitions:
                (op, pos) = tran
                tao += pher[op][pos]
            eta = fitness - f0
            sum_tao = 0
            for i in range(0, 18):
                for j in range(0, LIST_SIZE):
                    sum_tao += pher[i][j]
            prob_acc = ((tao**ALPHA)*(eta**BETA))/((sum_tao**ALPHA)*(54**BETA))

            # Checks for Ant Acceptance
            if random.random() < prob_acc:
                ant = neighbor
                all_trans.extend(transitions)
        # Pheremone Update
        for i in range(0, 18):
            for j in range(0, LIST_SIZE):
                pher[op][pos] = (1 - RHO)*pher[op][pos]
        for trans in all_trans:
            (op, pos) = trans
            pher[op][pos] += RHO
    return colony





colony = gen_aco_sol()
colony.sort()
for ant in colony:
    print(ant)