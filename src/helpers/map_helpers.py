import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def create_blank_grid(num_rows, num_cols):
    return np.zeros(shape=(num_rows, num_cols), dtype = float)

def create_noise_grid(num_rows, num_cols, desired_density, rng_seed):
    # quick check to make density between 0 - 100
    if desired_density > 100:
        desired_density = 100
    
    if desired_density < 0:
        desired_density = 0

    # convert specified density into probabilities 
    prob_one = desired_density / 100
    prob_zero = 1 - prob_one


    np.random.seed(rng_seed)

    """
    Note: Originaly used numpy's randomint, but in case we want 
    to change density of the 2D grid, googled the prompt 
        "numpy randint with set probability": 

    Which returned the following code from Google's AI Overview:

    # Generate an array of 10 random integers from the same set and probabilities
    random_ints = np.random.choice([0, 1, 2], size=10, p=[0.2, 0.5, 0.3])

    # Will adapt this to our needs below to set probability of 0/1
    """
    # create and return matrix using numpy's random choice
    # w/ set probabilities for 0's and 1's
    grid = np.random.choice(
        [0, 1], 
        size=(num_rows, num_cols), 
        p = [prob_zero, prob_one]
    )
    return grid


def plot_grid(grid, filename, custom_title):
    # create a plot to hold the figure
    plot = plt.figure()

    # add a title, then use imshow to add the plot
    plt.title(custom_title)
    plot = plt.imshow(
        grid, cmap = 'Greys', interpolation = 'nearest', origin = 'lower'
    )

    # this may be uncommented for color scale, but not relevant for binary
    #plt.colorbar(plot)
    
    # save image then display plot
    plt.savefig(f'figs/{filename}.png')
    plt.show()


def in_bounds(row, col, shape):
    """
    This function determines whether or not the given row
    and column index positions of a table are in bounds. 

    Parameters
    ----------
    row : int
        The row index of the position being checked
    col : int
        The col index of the position being checked
    shape : tuple (num_rows, num_cols)
        The shape of the current matrix.
    
    Returns
    -------
    boolean
        True if table[row, col] is in bounds, else False.
    
    Examples
    --------
    grid = create_noise_grid(100, 100, 45) # shape is (100, 100)
    print(in_bounds(99, 99, grid.shape)) # True
    print(in_bounds(-1, 5, grid.shape))  # False
    """
    row_max = shape[0] - 1
    col_max = shape[1] - 1 

    if (row > row_max) or (row < 0) or (col > col_max) or (col < 0):
        return False 
    else:
        return True






def create_map_with_ca(starting_grid, num_iterations):

    # get num rows and cols
    table_shape = starting_grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]

    # create a new var to store the changed grid
    modified_grid = starting_grid.copy()

    # loop through specified number of iterations
    for i in range(1, num_iterations + 1):
        
        # create a temporary grid for this iteration
        temp_grid = modified_grid.copy()

        print(f"Starting iteration {i}...")

        # double loop for rows, then cols, equivalent to map height, width
        for row in range(num_rows):
            for col in range(num_cols):
                
                # now for each cell, we need to find number of neighbors
                num_neighboring_walls = 0

                for m in range(row - 1, row + 2):
                    for n in range(col - 1, col + 2):

                        # check if grid[m, n] is in bounds
                        if in_bounds(m, n, table_shape):
                            # we don't count the cell itself as a neighbor
                            if (m != row) or (n != col):
                                # if spot == 1, increment num walls
                                if temp_grid[m, n] == 1:
                                    num_neighboring_walls += 1
                        else:
                            # if out of bounds, automatically consider a wall
                            num_neighboring_walls += 1
                
                # once outside of loop to check neighbors, apply CA rule
                if num_neighboring_walls > 4:
                    modified_grid[row, col] = 1
                else:
                    modified_grid[row, col] = 0
    
    return modified_grid



def add_detail(starting_grid, prob_item, prob_enemy):

    temp_grid = starting_grid.copy()

    table_shape = temp_grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]

    for row in range(num_rows):
        for col in range(num_cols):

            # now for each cell, we need to find number of neighbors
            num_neighboring_walls = 0

            for m in range(row - 1, row + 2):
                for n in range(col - 1, col + 2):

                    # check if grid[m, n] is in bounds
                    if in_bounds(m, n, table_shape):
                        # we don't count the cell itself as a neighbor
                        if (m != row) or (n != col):
                            # if spot == 1, increment num walls
                            if temp_grid[m, n] == 1:
                                num_neighboring_walls += 1
                    else:
                        # if out of bounds, automatically consider a wall
                        num_neighboring_walls += 1

            # once outside of loop to check neighbors, apply CA rule
            if num_neighboring_walls > 4:

                if num_neighboring_walls < 6:
                    spawn_item = np.random.choice([0, 1], p = [1 - prob_item, prob_item])
                    if spawn_item == 1:
                        temp_grid[row, col] = 2
                
                if num_neighboring_walls > 7:
                    spawn_diamond = np.random.choice([0, 1], p = [0.99, 0.01])
                    if spawn_diamond == 1:
                        temp_grid[row, col] = 4

            if num_neighboring_walls == 0:

                spawn_enemy = np.random.choice([0, 1], p = [1 - prob_enemy, prob_enemy])

                if spawn_enemy == 1:
                    temp_grid[row, col] = 3
    
    return temp_grid


def plot_complex_grid(grid, filename):
    # create a plot to hold the figure
    plot = plt.figure()

    color_map = colors.ListedColormap(['white', 'black', 'gold', 'red', 'blue', 'green', 'purple'])
    bounds = [0, 1, 2, 3, 4, 5, 70, 419]
    norm = colors.BoundaryNorm(bounds, color_map.N)

    plot = plt.imshow(
        grid, interpolation = 'nearest', origin = 'lower',
        cmap = color_map, norm = norm
    )

    # this may be uncommented for color scale, but not relevant for binary
    plt.colorbar(plot)
    
    # save image then display plot
    plt.savefig(f'figs/{filename}.png')
    plt.show()
