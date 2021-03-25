import math

# Rubix Cube class to hold information about cube and perform operations
class RCube:
    # initializes cube variables
    def __init__(self):
        # Cube Matrix:
        # Holds the current state of the cube; the numbers represent faces.
        #    1 - F,   2 - B,   3 - R,   4 - L,   5 - U,   6 - D
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
    def print_cube(self):
        for i in range(0, 3):
            print(self.cube_mat[i])
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
    # Rows are numbered from 0 to 2.
    def copy_row(self, row, face1, face2):
        base1 = (face1 - 1)*3
        base2 = (face2 - 1)*3
        for i in range(0,3):
            self.cube_mat[row][base2+i] = self.cube_mat[row][base1+i]
    # Copy Column: Copies a column from face1 to face2.
    # Columns are numbered from 0 to 2.
    def copy_col(self, col, face1, face2):
        base1 = (face1 - 1)*3
        base2 = (face2 - 1)*3
        for i in range(0,3):
            self.cube_mat[i][base2+col] = self.cube_mat[i][base1+col]
    # Left Horizontal Rotation:
    def left_horiz_rot(self, row):
        front_row = [self.cube_mat[row][0], self.cube_mat[row][1], self.cube_mat[row][2]]
        self.copy_row(row, 3, 1)
        self.copy_row(row, 2, 3)
        self.copy_row(row, 4, 2)
        for i in range(0, 3):
            self.cube_mat[row][9 + i] = front_row[i]
    # Right Horizontal Rotation:
    def right_horiz_rot(self, row):
        front_row = [self.cube_mat[row][0], self.cube_mat[row][1], self.cube_mat[row][2]]
        self.copy_row(row, 4, 1)
        self.copy_row(row, 2, 4)
        self.copy_row(row, 3, 2)
        for i in range(0, 3):
            self.cube_mat[row][6 + i] = front_row[i]
    # Up Vertical Rotation:
    def up_vert_rot(self, col):
        front_col = [self.cube_mat[0][col], self.cube_mat[1][col], self.cube_mat[2][col]]
        self.copy_col(col, 6, 1)
        self.copy_col(col, 2, 6)
        self.copy_col(col, 5, 2)
        for i in range(0, 3):
            self.cube_mat[i][12 + col] = front_col[i]
    # Down Vertical Rotation:
    def down_vert_rot(self, col):
        front_col = [self.cube_mat[0][col], self.cube_mat[1][col], self.cube_mat[2][col]]
        self.copy_col(col, 5, 1)
        self.copy_col(col, 2, 5)
        self.copy_col(col, 6, 2)
        for i in range(0, 3):
            self.cube_mat[i][15 + col] = front_col[i]
    # Clockwise Vertical Rotation:
    def c_vert_rot(self, col):
        right_col = [self.cube_mat[0][6 + col], self.cube_mat[1][6 + col], self.cube_mat[2][6 + col]]
        self.copy_col(col, 5, 3)
        self.copy_col(col, 4, 5)
        self.copy_col(col, 6, 4)
        for i in range(0, 3):
            self.cube_mat[i][15 + col] = right_col[i]
    def cc_vert_rot(self, col):
        right_col = [self.cube_mat[0][6 + col], self.cube_mat[1][6 + col], self.cube_mat[2][6 + col]]
        self.copy_col(col, 6, 3)
        self.copy_col(col, 4, 6)
        self.copy_col(col, 5, 4)
        for i in range(0, 3):
            self.cube_mat[i][12 + col] = right_col[i]
    # Counter-clockwise Vertical Rotation:
    # Full Rotation Function
    # http://www.rubiksplace.com/move-notations/
    def rotate(self, op):
        if op == 'U':
            self.rotatef_c(5)
            self.left_horiz_rot(0)
        elif op == 'U-':
            self.rotatef_cc(5)
            self.right_horiz_rot(0)
        elif op == 'R':
            self.rotatef_c(3)
            self.up_vert_rot(2)
        elif op == 'R-':
            self.rotatef_cc(3)
            self.down_vert_rot(2)
        elif op == 'F':
            self.rotatef_c(1)
            self.c_vert_rot(0)
        elif op == 'F-':
            self.rotatef_cc(1)
            self.cc_vert_rot(0)
        elif op == 'D':
            self.rotatef_c(6)
            self.right_horiz_rot(2)
        elif op == 'D-':
            self.rotatef_cc(6)
            self.left_horiz_rot(2)
        elif op == 'L':
            self.rotatef_c(4)
            self.down_vert_rot(0)
        elif op == 'L-':
            self.rotatef_cc(4)
            self.up_vert_rot(0)
        elif op == 'B':
            self.rotatef_c(2)
            self.cc_vert_rot(2)
        elif op == 'B-':
            self.rotatef_cc(2)
            self.c_vert_rot(2)
        elif op == 'M':
            self.down_vert_rot(1)
        elif op == 'M-':
            self.up_vert_rot(1)
        elif op == 'E':
            self.right_horiz_rot(1)
        elif op == "E-":
            self.left_horiz_rot(1)
        elif op == 'S':
            self.c_vert_rot(1)
        elif op == 'S-':
            self.cc_vert_rot(1)
        else:
            print("Invalid Operation")
    def perform(self, op_list):
        for op in op_list:
            self.rotate(op)
# end class

# some tests
my_cube = RCube()
print(my_cube.calc_fit())
my_cube.rotate('B')
my_cube.print_cube()
print(my_cube.calc_fit())


