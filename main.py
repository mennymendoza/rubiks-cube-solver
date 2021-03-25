import math

# Rubix Cube class to hold information about cube and perform operations
class RCube:
    # initializes cube variables
    def __init__(self):
        # Cube Matrix:
        # Holds the current state of the cube; the numbers represent colors.
        self.cube_mat = [
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
        ]
        # Fitness Matrix: Holds the current fitness of each square on the cube.
        # If correct, holds 1; if not correct, holds 0. 
        self.fit_mat = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    # Fills the fitness matrix and returns the sum of all values in the matrix.
    def calc_fit(self):
        fitness = 0
        for i in range(0, 3):
            for j in range(0, 18):
                self.fit_mat[i][j] = (self.cube_mat[i][j] == math.ceil((j + 1) / 3))
                fitness += self.fit_mat[i][j]
        return fitness
# end class

# some tests
my_cube = RCube()
print(my_cube.calc_fit())