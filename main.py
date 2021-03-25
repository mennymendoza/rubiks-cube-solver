import math

# Rubix Cube class to hold information about cube and perform operations
class RCube:
    # initializes cube variables
    def __init__(self):
        # Cube Matrix:
        # Holds the current state of the cube; the numbers represent colors/faces.
        #    1 - F,   2 - B,   3 - R,   4 - L,   5 - U,   6 - D
        self.cube_mat = [
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1, 2, 3, 1, 2, 3],
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
    # Rotate Face Counter-clockwise
    def rotatef_cc(self, face):
        if face < 1 or face > 6:
            print("invalid face")
            return
        base = (face - 1)*3
        temp1 = self.cube_mat[0][base]
        temp2 = self.cube_mat[0][base + 1]
        self.cube_mat[0][base] = self.cube_mat[0][base + 2]
        self.cube_mat[0][base + 1] = self.cube_mat[1][base + 2]
        self.cube_mat[0][base + 2] = self.cube_mat[2][base + 2]
        self.cube_mat[1][base + 2] = self.cube_mat[2][base + 1]
        self.cube_mat[2][base + 2] = self.cube_mat[2][base]
        self.cube_mat[2][base + 1] = self.cube_mat[1][base]
        self.cube_mat[2][base] = temp1
        self.cube_mat[1][base] = temp2
    # Rotate Face Clockwise
    def rotatef_c(self, face):
        if face < 1 or face > 6:
            print("invalid face")
            return
        base = (face - 1)*3
        temp1 = self.cube_mat[0][base]
        temp2 = self.cube_mat[1][base]
        self.cube_mat[0][base] = self.cube_mat[2][base]
        self.cube_mat[1][base] = self.cube_mat[2][base + 1]
        self.cube_mat[2][base] = self.cube_mat[2][base + 2]
        self.cube_mat[2][base + 1] = self.cube_mat[1][base + 2]
        self.cube_mat[2][base + 2] = self.cube_mat[0][base + 2]
        self.cube_mat[1][base + 2] = self.cube_mat[0][base + 1]
        self.cube_mat[0][base + 2] = temp1
        self.cube_mat[0][base + 1] = temp2
    # Copy Row: Copies a row from face1 to face2
    def copy_row(self, row, face1, face2):
        base1 = (face1 - 1)*3
        base2 = (face2 - 1)*3
        for i in range(0,3):
            self.cube_mat[row][base2+i] = self.cube_mat[row][base1+i]
    # Left Horizontal Rotation: 
    def left_horiz_rot(self, row):
        top_front_row = [self.cube_mat[row][0], self.cube_mat[row][1], self.cube_mat[row][2]]
        self.copy_row(row, 3, 1)
        self.copy_row(row, 2, 3)
        self.copy_row(row, 4, 2)
        for i in range(0, 3):
            self.cube_mat[row][9 + i] = top_front_row[i]
    def left_horiz_rot(self, row):
        pass # fuck
    # Full Rotation Function
    def rotate(self, op):
        if op == 'U':
            self.rotatef_c(5)
            self.left_horiz_rot(0)
        elif op == 'D-':
            self.rotatef_cc(6)
            self.left_horiz_rot(2)
        elif op == "E-":
            self.left_horiz_rot(1)
# end class

# some tests
my_cube = RCube()
print(my_cube.calc_fit())
my_cube.rotate('D-')
print(my_cube.cube_mat)

# [[1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1, 2, 3, 3, 6, 6],
# [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 2, 6, 6],
# [3, 3, 3, 4, 4, 4, 2, 2, 2, 1, 1, 1, 5, 5, 5, 1, 6, 6]]