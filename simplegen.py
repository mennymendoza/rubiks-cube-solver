import rcube as cb
import random

# some tests
my_cube = cb.RCube()
my_cube.print_colors()
genotype = [0, 5, 4, 6, 17, 5]
my_cube.run_list(genotype)
my_cube.print_colors()