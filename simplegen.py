import rcube as cb
import random

# some tests
my_cube = cb.RCube()
print(my_cube.calc_fit())
my_list = []
for z in range(0, 5):
    my_list.append(random.randrange(0, 18))
my_cube.run_list(my_list)