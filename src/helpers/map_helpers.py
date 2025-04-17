import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import math
import queue


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


def plot_grid(grid, filename, custom_title, display=False):
    # create a plot to hold the figure
    plot = plt.figure()

    # add a title, then use imshow to add the plot
    plt.title(custom_title)
    plot = plt.imshow(
        grid, cmap = 'Greys', interpolation = 'nearest', origin = 'lower'
    )

    # this may be uncommented for color scale, but not relevant for binary
    #plt.colorbar(plot)
    
    # save image then display plot if selected
    plt.savefig(f'figs/{filename}.png')
    
    if display:
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

    color_map = colors.ListedColormap(['white', 'black', 'gold', 'red', 'blue', 'green', 'pink'])
    bounds = [0, 0.99, 2, 3, 4, 5, 70, 419]
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


def create_index_matrix(grid):
    table_shape = grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]
    new_mat = np.zeros(shape=(num_rows, num_cols), dtype = int)

    index = 0

    for i in range(num_rows):
        for j in range(num_cols):
            new_mat[i, j] = index 
            index += 1

    return(new_mat)


def create_adjacency_matrix(grid):

    table_shape = grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]
    num_cells = num_rows * num_cols

    index_mat = create_index_matrix(grid)
    adj_mat = np.zeros(shape=(num_cells, num_cells), dtype = int)

    for i in range(num_rows):
        for j in range(num_cols):
            
            cell = index_mat[i, j]

            for row_offset in range(-1, 2):
                for col_offset in range(-1, 2):

                    if row_offset == 0 and col_offset == 0:
                        continue

                    if in_bounds(i + row_offset, j + col_offset, table_shape):
                        neighbor = index_mat[i + row_offset, j + col_offset]
                        adj_mat[cell, neighbor] = 1

    return [index_mat, adj_mat]



def find_room_coordinates(grid):

    grid_to_mod = grid.copy()
    ind_mat = create_index_matrix(grid_to_mod)
    grid_shape = grid_to_mod.shape 
    num_rows = grid_shape[0]
    num_cols = grid_shape[1]
    vis_mat = np.zeros(shape=(num_rows, num_cols), dtype = int)

    room_dict = {}
    idx = 0


    for row in range(num_rows):
        for col in range(num_cols):

            cell_val = grid_to_mod[row, col]
            cell_idx = ind_mat[row, col]

            #print(f"In row: {row}, col: {col}")

            # if blank space, and not visited start bfs
            if cell_val == 0 and vis_mat[cell_idx // num_rows, cell_idx // num_cols] == 0:
                
                #print(f"In cell: {row}, {col}... value: {cell_val}... visited {vis_mat[cell_idx // num_rows, cell_idx // num_cols]}")

                q = queue.Queue()
                q.put(cell_idx) # add the current cell's index to queue

                min_x = row 
                max_x = row 
                min_y = col 
                max_y = col
                area = 0

                while q.qsize() > 0:
                    
                    u = q.get()

                    # update visited
                    vis_mat[u // num_rows, u % num_cols] = 1

                    # update symbol in game grid
                    grid_to_mod[u // num_rows, u % num_cols] = 9

                    # check neighbors:
                    for i in range((u // num_rows) - 1, (u // num_rows) + 2):
                        for j in range((u % num_cols) - 1, (u % num_cols) + 2):

                            # check if in bounds
                            if in_bounds(i, j, grid_shape):
                                # don't count current cell
                                if (i != u // num_rows) or (j != u % num_cols):
                                    # if open space
                                    if (grid_to_mod[i, j] == 0) and (ind_mat[i, j] not in q.queue):
                                        q.put(ind_mat[i, j])

                    area += 1

                    if (u // num_rows) < min_x:
                        min_x = u // num_rows
                    
                    if (u // num_rows) > max_x:
                        max_x = u // num_rows

                    if (u % num_cols) < min_y: 
                        min_y = u % num_cols

                    if (u % num_cols) > max_y:
                        max_y = u % num_cols

                room_dict[idx] = [min_x, max_x, min_y, max_y, area]
                idx += 1

    return room_dict



def get_room_midpoints(room_dict):
    # create a new dictionary to store the room midpoints
    midpoints_dict = {}
    idx = 0

    for key, val in room_dict.items():

        int_list = [int(i) for i in val]

        # find the middle x coord
        avg_x = math.floor((int_list[0] + int_list[1]) / 2)

        # find the middle y coord
        avg_y = math.floor((int_list[2] + int_list[3]) / 2)

        # add to dictionary the midpoint x, y, and area of room
        midpoints_dict[idx] = [avg_x, avg_y, int_list[4]]
        idx += 1

    return midpoints_dict



def get_manhattan_distance(room, other_rooms):

    dist_dict = {}
    idx = 0

    #print(room)
    #print(other_rooms)

    """
    formula for manhattan distance is:
        |x1 - x2| + |y1 - y2|
    """
    for r in other_rooms:

        x1 = room[0]
        x2 = r[0]
        y1 = room[1]
        y2 = r[1]
        room_area = r[2]

        m_dist = abs(x1 - x2) + abs(y1 - y2)

        # add calculated distance to dictionary with that other room's midpoint
        dist_dict[idx] = [x2, y2, room_area, m_dist]
        idx += 1

    # after all distances calculated, sort dictionary by manhattan dist
    # for lambda key, values are the 1st index, and we want manhattan dist, index 3 w/in those
    sorted_dict = dict(sorted(dist_dict.items(), key = lambda i: i[1][3]))

    return sorted_dict


def make_path(grid, room1, room2, animation_index, density, seed):

    min_range = 0
    max_range = 2

    start_x = room1[0]
    start_y = room1[1]
    end_x = room2[0]
    end_y = room2[1]

    while (start_x != end_x) or (start_y != end_y):
        clear_width = np.random.randint(min_range, max_range)

        for i in range(start_x - clear_width, start_x + clear_width + 1):
            for j in range(start_y - clear_width, start_y + clear_width + 1):
                grid[i, j] = 0

        if start_x < end_x:
            start_x += 1
        
        if start_x > end_x:
            start_x -= 1
        
        if start_y < end_y:
            start_y += 1
        
        if start_y > end_y:
            start_y -= 1
    
        plot_grid(grid, f"animation/{animation_index}_iteration", f"time = {animation_index} (Density: {density}, Seed: {seed})")
        animation_index += 1

    return animation_index


def connect_map(grid, all_rooms, n_neighbors, animation_index, density, seed):

    for i in range(len(all_rooms)):

        # get the room we're currently on
        room = all_rooms[i]

        # make a copy of all_rooms for remaining so that OG isn't modified
        remaining_rooms = all_rooms.copy()

        # get rid of the room we're currently on:
        remaining_rooms.pop(i)

        manhattan_distances = get_manhattan_distance(room, remaining_rooms)

        for j in range(n_neighbors):
            animation_index = make_path(grid, room, list(manhattan_distances.values())[j], animation_index, density, seed)

