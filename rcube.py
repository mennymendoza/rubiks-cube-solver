import math

# Rubix Cube class to hold information about cube and perform operations
class RCube:
    # initializes cube variables
    def __init__(self):
        # Constants:
        self.F = 1
        self.R = 2
        self.B = 3
        self.L = 4
        self.U = 5
        self.D = 6
        # First column of the face
        self.f_start = (self.F-1)*3
        self.r_start = (self.R-1)*3
        self.b_start = (self.B-1)*3
        self.l_start = (self.L-1)*3
        self.u_start = (self.U-1)*3
        self.d_start = (self.D-1)*3
        # Cube Matrix:
        # Holds the current state of the cube; the numbers represent faces.
        #    1 - F,   2 - R,   3 - B,   4 - L,   5 - U,   6 - D
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
    # Reset Cube
    def reset(self):
        self.cube_mat = [
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6],
            [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6]
        ]
        self.fit_mat = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    # Print Cube
    def print_cube(self):
        for i in range(0, 3):
            print(self.cube_mat[i])
        print()
    # Calculate Fitness
    # Fills the fitness matrix and returns the sum of all values in the matrix.
    def calc_fit(self):
        fitness = 0
        for i in range(0, 3):
            for j in range(0, 18):
                self.fit_mat[i][j] = (self.cube_mat[i][j] == math.ceil((j + 1) / 3))
                fitness += self.fit_mat[i][j]
        return fitness
    # Rotate Face Counter-Clockwise
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
    # Copy Row
    # Copies a row from face1 to face2. Rows are numbered from 0 to 2.
    def copy_row(self, row, face1, face2):
        base1 = (face1 - 1)*3
        base2 = (face2 - 1)*3
        for i in range(0,3):
            self.cube_mat[row][base2+i] = self.cube_mat[row][base1+i]
    # Copy Column
    # Copies a column from face1 to face2. Columns are numbered from 0 to 2.
    def copy_col(self, col, face1, face2):
        base1 = (face1 - 1)*3
        base2 = (face2 - 1)*3
        for i in range(0,3):
            self.cube_mat[i][base2+col] = self.cube_mat[i][base1+col]
    # Left Horizontal Rotation
    def left_horiz_rot(self, row):
        front_row = [self.cube_mat[row][0], self.cube_mat[row][1], self.cube_mat[row][2]]
        self.copy_row(row, 2, 1)
        self.copy_row(row, 3, 2)
        self.copy_row(row, 4, 3)
        for i in range(0, 3):
            self.cube_mat[row][9 + i] = front_row[i]
    # Right Horizontal Rotation
    def right_horiz_rot(self, row):
        front_row = [self.cube_mat[row][0], self.cube_mat[row][1], self.cube_mat[row][2]]
        self.copy_row(row, 4, 1)
        self.copy_row(row, 3, 4)
        self.copy_row(row, 2, 3)
        for i in range(0, 3):
            self.cube_mat[row][3 + i] = front_row[i]
    # Up Vertical Rotation
    def up_vert_rot(self, col):
        front_col = [self.cube_mat[0][col], self.cube_mat[1][col], self.cube_mat[2][col]]
        for i in range(0, 3):
            self.cube_mat[i][self.f_start + col] = self.cube_mat[i][self.d_start + col]
        for i in range(0, 3):
            self.cube_mat[i][self.d_start + col] = self.cube_mat[2 - i][self.b_start + (2 - col)]
        for i in range(0, 3):
            self.cube_mat[i][self.b_start + (2 - col)] = self.cube_mat[2 - i][self.u_start + col]
        for i in range(0, 3):
            self.cube_mat[i][self.u_start + col] = front_col[i]
    # Down Vertical Rotation
    def down_vert_rot(self, col):
        front_col = [self.cube_mat[0][col], self.cube_mat[1][col], self.cube_mat[2][col]]
        for i in range(0, 3):
            self.cube_mat[i][self.f_start + col] = self.cube_mat[i][self.u_start + col]
        for i in range(0, 3):
            self.cube_mat[i][self.u_start + col] = self.cube_mat[2 - i][self.b_start + (2 - col)]
        for i in range(0, 3):
            self.cube_mat[i][self.b_start + (2 - col)] = self.cube_mat[2 - i][self.d_start + col]
        for i in range(0, 3):
            self.cube_mat[i][self.d_start + col] = front_col[i]
    # Clockwise Vertical Rotation
    def c_vert_rot(self, col):
        right_col = [self.cube_mat[0][self.r_start + col], self.cube_mat[1][self.r_start + col], self.cube_mat[2][self.r_start + col]]
        for i in range(0, 3):
            self.cube_mat[i][self.r_start + col] = self.cube_mat[2 - col][self.u_start + i]
        for i in range(0, 3):
            self.cube_mat[2 - col][self.u_start + i] = self.cube_mat[2 - i][self.l_start + (2 - col)]
        for i in range(0, 3):
            self.cube_mat[i][self.l_start + (2 - col)] = self.cube_mat[col][self.d_start + i]
        for i in range(0, 3):
            self.cube_mat[col][self.d_start + i] = right_col[2 - i]
    # Counter-clockwise Vertical Rotation
    def cc_vert_rot(self, col):
        right_col = [self.cube_mat[0][self.r_start + col], self.cube_mat[1][self.r_start + col], self.cube_mat[2][self.r_start + col]]
        for i in range(0, 3):
            self.cube_mat[i][self.r_start + col] = self.cube_mat[col][self.d_start + (2 - i)]
        for i in range(0, 3):
            self.cube_mat[col][self.d_start + i] = self.cube_mat[i][self.l_start + (2 - col)]
        for i in range(0, 3): # current
            self.cube_mat[i][self.l_start + (2 - col)] = self.cube_mat[2 - col][self.u_start + (2 - i)]
        for i in range(0, 3):
            self.cube_mat[2 - col][self.u_start + i] = right_col[i]
    # Full Rotation Function
    # This is the function that you should actually use to move the cube around.
    # See move notation link in README.md for how different moves affect the cube.
    def rotate(self, op):
        if op == 'U' or op == 0:
            print('U')
            self.rotatef_c(5)
            self.left_horiz_rot(0)
        elif op == '-U' or op == 1:
            print('-U')
            self.rotatef_cc(5)
            self.right_horiz_rot(0)
        elif op == 'E' or op == 2:
            print('E')
            self.right_horiz_rot(1)
        elif op == '-E' or op == 3:
            print('-E')
            self.left_horiz_rot(1)
        elif op == 'D' or op == 4:
            print('D')
            self.rotatef_c(6)
            self.right_horiz_rot(2)
        elif op == '-D' or op == 5:
            print('-D')
            self.rotatef_cc(6)
            self.left_horiz_rot(2)
        elif op == 'R' or op == 6:
            print('R')
            self.rotatef_c(2)
            self.up_vert_rot(2)
        elif op == '-R' or op == 7:
            print('-R')
            self.rotatef_cc(2)
            self.down_vert_rot(2)
        elif op == 'L' or op == 8:
            print('L')
            self.rotatef_c(4)
            self.down_vert_rot(0)
        elif op == '-L' or op == 9:
            print('-L')
            self.rotatef_cc(4)
            self.up_vert_rot(0)
        elif op == 'M' or op == 10:
            print('M')
            self.down_vert_rot(1)
        elif op == '-M' or op == 11:
            print('-M')
            self.up_vert_rot(1)
        elif op == 'F' or op == 12:
            print('F')
            self.rotatef_c(1)
            self.c_vert_rot(0)
        elif op == '-F' or op == 13:
            print('-F')
            self.rotatef_cc(1)
            self.cc_vert_rot(0)
        elif op == 'B' or op == 14:
            print('B')
            self.rotatef_c(3)
            self.cc_vert_rot(2)
        elif op == '-B' or op == 15:
            print('-B')
            self.rotatef_cc(3)
            self.c_vert_rot(2)
        elif op == 'S' or op == 16:
            print('S')
            self.c_vert_rot(1)
        elif op == '-S' or op == 17:
            print('-S')
            self.cc_vert_rot(1)
        else:
            print(op, "is an invalid operation")
    # Run List
    
    def run_list(self, op_list):
        for op in op_list:
            self.rotate(op)
            self.print_colors()
    # Print Colors
    # Assumes Red = 1, Yellow = 2, Orange = 3, White = 4, Blue = 5, and Green = 6
    def print_colors(self):
        # this function is for testing only
        for i in range(0, 3):
            for j in range(0, 18):
                if (self.cube_mat[i][j] == 1):
                    print('R', end=' ')
                elif (self.cube_mat[i][j] == 2):
                    print('Y', end=' ')
                elif (self.cube_mat[i][j] == 3):
                    print('O', end=' ')
                elif (self.cube_mat[i][j] == 4):
                    print('W', end=' ')
                elif (self.cube_mat[i][j] == 5):
                    print('B', end=' ')
                elif (self.cube_mat[i][j] == 6):
                    print('G', end=' ')
            print()
        print()
# end class



