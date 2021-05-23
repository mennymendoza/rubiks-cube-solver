# Rubik's Cube Solver



## Documentation

### Getting Started
Importing the Rubik's Cube class

`import rcube`

Creating an instance of a Rubik's Cube

`example_cube = rcube.RCube()`

### Printing the Cube's State

To print the raw 2D array data that represents the cube, you can use the print_cube function.

`example_cube.print_cube()`

You can also print the cube using the alternate print_colors function. This assigns colors to each number, representing the colors as the first letter of each color. It also takes away the commas and brackets, making the output look cleaner.

`example_cube.print_colors()`

You can check the *fitness* of the cube using the calc_fit function. This function simply counts up how many squares are in the correct position and returns the value. This is useful for measuring how close your cube is to being solved.

`fitness = example_cube.calc_fit()`

### Modifying the Cube

To perform a rotation on your cube (meaning to rotate a piece of the cube to change the appearance), use the rotate function. It takes either a number between 0 - 17 or a string containing Rubik's Cube move notation as an argument. However, note that instead of using an apostrophe (such as in U'), the function actually expects -U. The - sign is used in place of the prime and should be in front of the symbol. Here is a link for a site that explains cube notation: http://www.rubiksplace.com/move-notations/

`example_cube.rotate(1)`

or alternatively,

`example_cube.rotate('-U')`

Another useful function is the run_list function. It takes a *list* of operations as a parameter.

`example_cube.run_list([0, 1, 2, 3, 4])`

or alternatively,

`example_cube.run_list(['U', '-U', 'E', '-E', 'D'])`

### Other Useful Functions

If you want to reset quickly back to a solved cube, you can use the reset function.

`example_cube.reset()`

If you are working with lists of numbers that represent cube operations (this is most useful when you want to randomly generate cube operations), you might want to convert those numbers back into cube notation when printing them out. The num_to_op function converts an integer into a string containing cube notation.

`example_string = example_cube.num_to_op(0)`

### Links
Here is a website containing a virtual 3D Rubik's Cube. The code for this project was tested extensively using this website.
Virtual Rubix Cube: https://www.randelshofer.ch/rubik/virtual_cubes/rubik/instructions/instructions_big.html