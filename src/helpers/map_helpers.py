"""
Tristan Jordan
4/19/25
This file contains various helper functions used to generate 
game maps with Cellular Automata.
"""


import numpy as np # for various matrix functions, and random number generation.
import math # for floor() method.
import queue # using queue data structure in BFS.
import matplotlib.pyplot as plt # for plotting before map moved into Pygame.
from matplotlib import colors # used in plotting custom pixel color scales.


# --------------------------------------------- FINAL FUNCTION TO CREATE COMPLETE MAP FOR PYGAME ---------------------------------------------- #


def create_complete_map(height, width, density, seed, iterations, prob_item, prob_enemy):
    """
    This function creates a complete game map with floors, walls, items, and enemies. 
    Modified forms of Breadth First Search (BFS) are used to classify rooms, connect rooms
    across the map, and then verify that a valid path from the chosen spawn point to the 
    level exit point exists. This calls various helper functions which will be defined below.

    Args:
        height: int, the height of the desired map 
        width: int, the width of the desired map
        density: int, between 0 - 100 for density of black pixels / walls. 
        seed: int, to control random number generation
        iterations: int, number of iterations over which to apply Cellular Automata (CA) rules.
        prob_item: float, probability of spawning a gold-node
        prob_enemy: float, probability of spawning an enemy. 
    
    Returns:
        List, a python list containing the following elements:
            [
            modified_map (idx 0): the np matrix of the final map, 
            spawn_point (idx 1): a List containing [x coord, y coord] of the spawn point,
            exit_point (idx 2): a List containing [x coord, y coord] of the level exit,
            density (idx 3): int, density of final map,
            seed (idx 4): int, seed used in RNG of final map,
            iterations (idx 5): final number of iterations used for CA rules
        ]
    """
    # get base noise grid as starting point
    grid = create_noise_grid(height, width, density, seed)

    # smooth map with cellular automata
    new_map = create_map_with_ca(grid, iterations)

    # find and store the rooms
    midpoints_dict = get_room_midpoints(find_room_coordinates(new_map, -1, density, seed, animate_flag = False)[0])
    all_rooms = list(midpoints_dict.values())

    # connect the rooms on the map
    connect_map(new_map, all_rooms, 3, -1, density, seed, animate_flag = False)

    # add items and enemies to map
    modified_map = add_detail(new_map, prob_item, prob_enemy, 0, density, seed, animate_flag=False)

    # find and add spawn and exit point
    spawn_point = find_specific_room(all_rooms, 35, new_map.shape, "high", "low")
    exit_point = find_specific_room(all_rooms, 35, new_map.shape, "low", "high")

    # check if valid path from spawn to level exit using BFS
    valid_points = verify_path(modified_map[0], [spawn_point[0], spawn_point[1]], [exit_point[0], exit_point[1]])

    # if there's no valid path on this set of params, recursively call w/ new density, seed, and iteration amount
    if valid_points == False:
        return create_complete_map(height, width, density - 1, seed + 1, iterations - 1, prob_item, prob_enemy)

    # once we are sure there's a valid path, set the states for spawn and exit point on the map
    modified_map[0][spawn_point[0], spawn_point[1]] = 69
    modified_map[0][exit_point[0], exit_point[1]] = 400

    # return map and other info. for PyGame
    return [modified_map[0], [spawn_point[0], spawn_point[1]], [exit_point[0], exit_point[1]], density, seed, iterations]


# ------------------------------------------ GRID AND MAP CREATION FUNCTIONS, WITH CELLULAR AUTOMATA ------------------------------------------ #

# function to create a blank matrix of 0s
def create_blank_grid(num_rows, num_cols):
    """
    This function creates matrix of specified dimentions populated with 0s.

    Args: 
        num_rows: int, how many rows to include in matrix
        num_cols: int, how many columns to include in matrix
    
    Returns: 
        np matrix of specified dimensions, populated with 0s
    """
    return np.zeros(shape=(num_rows, num_cols), dtype = float)


# function to create a random noise grid that the CA will use to make a map
def create_noise_grid(num_rows, num_cols, desired_density, rng_seed):
    """
    This function makes a random noise grid with the specified
    dimensions and density of black pixels / walls. 

    Args:
        num_rows: int, how many rows to include in matrix
        num_cols: int, how many columns to include in matrix
        desired_density: int, a number between 0 - 100, how densely
            filled with walls the map should be. E.g., 50 would result in 50% black, 50% white pixels.
        rng_seed: int, controls random number generation.
    
    Returns:
        np matrix randomly populated w/ 0s and 1s according to parameters.
    """
    # quick check to make density between 0 - 100
    if desired_density > 100:
        desired_density = 100

    if desired_density < 0:
        desired_density = 0

    # convert specified density into probabilities 
    prob_one = desired_density / 100
    prob_zero = 1 - prob_one

    # set seed for random number generation
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


# helper function to check whether a matrix position is in bounds.
def in_bounds(row, col, shape):
    """
    This function determines whether or not the given row
    and column index positions of a table are in bounds. 

    Args:
        row: int, the row index of the position being checked
        col: int, the col index of the position being checked
        shape: tuple (num_rows, num_cols), the shape of the current matrix.
    
    Returns:
        bool, True if table[row, col] is in bounds, else False.
    
    Examples:
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


# function to use Cellular Automata to make our matrix more map like
def create_map_with_ca(starting_grid, num_iterations):
    """
    This function uses Cellular Atomata (CA) rules to create a
    more natural looking game map. 

    Args:
        starting_grid: np matrix, with 0s / 1s to represent floors / walls.
        num_iterations: int, how many time steps over which to apply the CA rules.
    
    Returns:
        modified_grid, np matrix with cells changed after CA rules applied over iterations.
    """

    # get num rows and cols
    table_shape = starting_grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]

    # create a new copy to store the changed grid
    modified_grid = starting_grid.copy()

    # loop through specified number of iterations
    for i in range(1, num_iterations + 1):
        
        # create a temporary grid for this iteration
        temp_grid = modified_grid.copy()

        print(f"Starting iteration {i}...")

        # double loop for rows, then cols, equivalent to map width, height
        for row in range(num_rows):
            for col in range(num_cols):
                
                # for each cell, we need to find number of neighbors that are walls
                num_neighboring_walls = 0

                # double loop through this cell's Moore neighborhood
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
                            # if out of bounds, we will automatically consider it a wall
                            num_neighboring_walls += 1
                
                # once outside of loop to check neighbors, apply CA rule
                if num_neighboring_walls > 4:
                    modified_grid[row, col] = 1
                else:
                    modified_grid[row, col] = 0
    
    return modified_grid


# function to add more details to game map, including items and enemies
def add_detail(starting_grid, prob_item, prob_enemy, animation_index, density, seed, animate_flag=True):
    """
    This function adds detail to our game map, including items and enemies. Currently matrix states
    are represented as: 
        0: white / floors
        1: black / walls
    
    This function will add the states:
        2: yellow / gold-nodes
        3: red / enemies
        4: blue / diamonds

    There is additional code that enables animating the generation, which does take some space for
    storing png images. This can be disabled by setting the arg animate_flag to False

    Args:
        starting_grid: np matrix, which should have already been setup with create_map_with_ca()
        prob_item: float, desired probability of spawning gold nodes
        prob_enemy: float, desired probability of spawning enemies
        animation_index: int, passed in from function calls to keep track of order of animation frames.
        density: int, density of map being generated.. only used for plot title if animating
        seed: int, seed for random number generation, only used for plot title if animating
        animate_flag: bool, defaults to True, set to false to avoid full animation. 
    
    Returns:
        List: a list containing the following elements:
            [
            temp_grid (idx 0): np matrix with changed cells after item and enemy addition
            animation_index (idx 1): int, returns the animation index after fn is run for future fns that need it.
        ]
    """
    # make a copy of the grid that will store our new items and enemies, then get row/col dims
    temp_grid = starting_grid.copy()
    table_shape = temp_grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]

    # double loop to check every cell in the table
    for row in range(num_rows):
        for col in range(num_cols):

            # once again for each cell, we need to find number of neighboring walls (will control how items / enemies set)
            num_neighboring_walls = 0

            # double loop over this cell's Moore neighborhood
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

            # once outside of loop to check neighbors, we can apply CA like rules for items and enemies
            if num_neighboring_walls > 4:

                # if > 4 but < 6 neighboring walls, pick a random int according to probabilities, if
                # this check passes, we'll add a gold node at this position (state 2)
                if num_neighboring_walls < 6:
                    spawn_item = np.random.choice([0, 1], p = [1 - prob_item, prob_item])
                    if spawn_item == 1:
                        temp_grid[row, col] = 2

                        # if we successfully added a gold node and animating, increment idx and plot a new snapshot
                        if animate_flag:
                            animation_index += 1
                            plot_complex_grid(
                                temp_grid, 
                                f"animation/{animation_index}_iteration",
                                f"time = {animation_index} (Density: {density}, Seed: {seed})"
                            )
                
                # we only want to spawn diamonds in places all surrounded by walls
                # diamond probability hard coded to 1%
                if num_neighboring_walls > 7:
                    spawn_diamond = np.random.choice([0, 1], p = [0.99, 0.01])
                    if spawn_diamond == 1:
                        temp_grid[row, col] = 4

                        # if diamond added and animating, increment then plot snapshot
                        if animate_flag:
                            animation_index += 1
                            plot_complex_grid(
                                temp_grid, 
                                f"animation/{animation_index}_iteration",
                                f"time = {animation_index} (Density: {density}, Seed: {seed})"
                            )

            # we only want to spawn enemies in open space w/ no walls
            if num_neighboring_walls == 0:

                # make a check against prob of spawning an enemy
                spawn_enemy = np.random.choice([0, 1], p = [1 - prob_enemy, prob_enemy])

                if spawn_enemy == 1:
                    temp_grid[row, col] = 3

                    # if we successfully added enemy, handle animation
                    if animate_flag:
                        animation_index += 1
                        plot_complex_grid(
                            temp_grid, 
                            f"animation/{animation_index}_iteration",
                            f"time = {animation_index} (Density: {density}, Seed: {seed})"
                        )
    
    # return final modified grid and the updated animation index
    return [temp_grid, animation_index]



# -------------------------------------------- PATHING FUNCTIONS FOR ROOM FINDING, CONNECTION, ETC -------------------------------------------- #


# function to create an index matrix for the map
def create_index_matrix(grid):
    """
    This function creates an index matrix of our map matrix, where each cell's value corresponds to its index
    For example, For a 100 x 100 matrix grid, grid[99, 99] would have the index value index_matrix[99, 99] = 999, 
    because it is the last / 1000th element in the matrix.

    Args:
        grid: np matrix from which to create a corresponding index matrix
    
    Returns:
        new_mat: np matrix where cell values correspond with the indices of the original matrix
    """
    # get grid's dimensions, then initialize a new matrix of 0s w/ same dims
    table_shape = grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]
    new_mat = np.zeros(shape=(num_rows, num_cols), dtype = int)

    # loop over, setting cell value in new matrix as index
    index = 0
    for i in range(num_rows):
        for j in range(num_cols):
            new_mat[i, j] = index 
            index += 1

    return(new_mat)


# function to create an adjacency matrix from our map grid
def create_adjacency_matrix(grid):
    """
    This function creates an adjacency matrix for our map matrix.

    Args:
        grid: np matrix to create an adjacency matrix for
    
    Returns:
        List, containing [
            np matrix (idx 0): index matrix corresponding w/ grid,
            np matrix (idx 1): adjacency matrix corresponding w/ grid
        ]
    
    Note:
        I wrote this function while experimenting & learning about pathfinding algorithms, 
        but the adjacency matrix is horribly space inefficient. Even for 
        a small game map (100 x 100), the corresponding adjacency matrix is 
        (1000, 1000).

        The original idea was that for row 0 of the matrix, the 1000 columns
        would tell every neighbor of cell 0. E.g., if adj_mat[0, 999] = 1, this
        would mean that the cell at idx 999 was a neighbor w/ 1. However, we don't
        need to do this because we can just indices with boundary checking to find the neighbors. 
    """
    # get grid's dimensions
    table_shape = grid.shape
    num_rows = table_shape[0]
    num_cols = table_shape[1]
    num_cells = num_rows * num_cols

    # get ind matrix, then create new dim grid for adjacency matrix
    index_mat = create_index_matrix(grid)
    adj_mat = np.zeros(shape=(num_cells, num_cells), dtype = int)

    # double loop over every cell in grid
    for i in range(num_rows):
        for j in range(num_cols):
            
            # get cell, then loop over Moore neighborhood
            cell = index_mat[i, j]

            for row_offset in range(-1, 2):
                for col_offset in range(-1, 2):

                    # don't need to consider a cell adjacent w/ itself
                    if row_offset == 0 and col_offset == 0:
                        continue

                    # if in bounds, then update adjacency matrix
                    if in_bounds(i + row_offset, j + col_offset, table_shape):
                        neighbor = index_mat[i + row_offset, j + col_offset]
                        adj_mat[cell, neighbor] = 1

    return [index_mat, adj_mat]


# function to search for and categorize rooms within the map
def find_room_coordinates(grid, animation_index, density, seed, animate_flag=True):
    """
    This function uses a modified version of breadth first search (BFS) to search the
    map and identify rooms. It additional keeps track of the min and max x, y coords
    found within rooms, so that we can create and return a list of room midpoints. 
    Additional args allow for animation of this room finding process. 

    Args:
        grid: np matrix, map to search for rooms
        animation_index: int, used for tracking and saving images to animate
        density: int, used in animation plot to display param
        seed; int, used in animation plot to display param
        animate_flag: bool, defaults True, whether or not to animate progress w/ images
    
    Returns:
        List: with elements [
            dict (idx 0): room_dict containing midpoint coords and area of rooms,
            animation_index: int, returned for future functions to animate in correct order
        ]
    
    Note:
        Writing this function is where I learned a handy trick about cell indices. We can 
        find the row and column index from a given cell index using floor division and modulo. 

        E.g., the cell in row 95, 4th col (idx 3) would have the index 9503. Given just 9503, we can find 
        the row and col using:
        row = 9503 // num_rows (100) = 95
        col = 9503 % num_cols (100) = 3
    """
    # make a copy of input grid so we can modify it for animation, then
    # get index matrix and dimension details. Create a new vis_mat 
    # that will indicate whether or not cells have been visited, all start at 0 not seen.
    grid_to_mod = grid.copy()
    ind_mat = create_index_matrix(grid_to_mod)
    grid_shape = grid_to_mod.shape 
    num_rows = grid_shape[0]
    num_cols = grid_shape[1]
    vis_mat = np.zeros(shape=(num_rows, num_cols), dtype = int)

    # create a dictionary w/ idx to store encountered rooms. 
    room_dict = {}
    idx = 0

    # double loop over every cell in our modified grid
    for row in range(num_rows):
        for col in range(num_cols):

            # get the current cell's value and index
            cell_val = grid_to_mod[row, col]
            cell_idx = ind_mat[row, col]

            # if we encounter an unvisited blank floor space, start modified BFS to classify this room
            if cell_val == 0 and vis_mat[cell_idx // num_rows, cell_idx % num_cols] == 0:

                # because we are using BFS, initialize a queue to store cells that need to be visited
                q = queue.Queue()
                q.put(cell_idx) # add the current cell's index to queue

                # initialize vars that will be used to track the min/max x, y encountered, and this room's area
                min_x = row 
                max_x = row 
                min_y = col 
                max_y = col
                area = 0

                # if animating, set this separate index
                if animate_flag:
                    m = 0

                # next BFS step, as long as there are unvisited nodes in the queue...
                while q.qsize() > 0:
                    
                    # dequeue the first cell
                    u = q.get()

                    # update vis_mat to show that we have visited this cell
                    vis_mat[u // num_rows, u % num_cols] = 1

                    # update symbol in grid for drawing as new color
                    grid_to_mod[u // num_rows, u % num_cols] = 9

                    # if animating, only plot state after each 50 additions to save on png space
                    if animate_flag:
                        m += 1
                        if m % 50 == 0:
                            animation_index += 1
                            plot_complex_grid(
                                grid_to_mod, 
                                f"animation/{animation_index}_iteration",
                                f"time = {animation_index} (Density: {density}, Seed: {seed})"
                            )

                    # check Moore neighborhood of this cell:
                    for i in range((u // num_rows) - 1, (u // num_rows) + 2):
                        for j in range((u % num_cols) - 1, (u % num_cols) + 2):

                            # if the current cell is in bounds, and not equal to our starting cell
                            if in_bounds(i, j, grid_shape):
                                if (i != u // num_rows) or (j != u % num_cols):
                                    # if open space, and not in the queue, add it to the queue
                                    if (grid_to_mod[i, j] == 0) and (ind_mat[i, j] not in q.queue):
                                        q.put(ind_mat[i, j])

                    # increment the area, then use logical checks to update max and min 
                    # if the current cell is above or below our previously seen max/min
                    area += 1

                    if (u // num_rows) < min_x:
                        min_x = u // num_rows
                    
                    if (u // num_rows) > max_x:
                        max_x = u // num_rows

                    if (u % num_cols) < min_y: 
                        min_y = u % num_cols

                    if (u % num_cols) > max_y:
                        max_y = u % num_cols

                # once all neighbors have been visited and room classified, add info. about coords to room dict
                room_dict[idx] = [min_x, max_x, min_y, max_y, area]
                idx += 1

    # after all rooms classified, return dictionary of rooms and the animation index for future fns that animate
    return [room_dict, animation_index]


# function to calculate the midpoints of given rooms
def get_room_midpoints(room_dict):
    """
    This function calculates the room midpoints given a dictionary of rooms with
    info. about the min and max x, y coords. 

    Args:
        room_dict: dictionary, each index key contains values that are a list with
            [min_x, max_x, min_y, max_y, area]
    
    Returns:
        A new dictionary, where each index key contains values for the room:
            [midpoint_x, midpoint_y, area]
    """
    # create a new dictionary to store the room midpoints
    midpoints_dict = {}
    idx = 0

    # loop over every key, val pair in the room dictionary
    for key, val in room_dict.items():

        # get all info about the current room using list comprehension
        int_list = [int(i) for i in val]

        # find the middle x coord
        avg_x = math.floor((int_list[0] + int_list[1]) / 2)

        # find the middle y coord
        avg_y = math.floor((int_list[2] + int_list[3]) / 2)

        # add to dictionary the midpoint x, y, and area of room
        midpoints_dict[idx] = [avg_x, avg_y, int_list[4]]
        idx += 1

    return midpoints_dict


# function to create a path between two rooms
def make_path(grid, room1, room2, animation_index, density, seed, animate_flag):
    """
    This function makes a path between two rooms on the map. The path width
    will be varied randomly between 1 - 2 pixels.

    Args:
        grid: np matrix of map
        room1: list with coord info. of first room
        room2: list with coord info. of second room
        animation_index: int, for keeping track of anim. order
        density: int, for plotting in animation frame
        seed: int, for plotting in animation frame
        animate_flag: bool, whether or not to animate, passed from connect_map()
    
    Returns:
        animation_index: int, for keeping track of anim progress. Otherwise map 
            path is modified in place.
    """
    # hard-coding min/max range for path width
    min_range = 0
    max_range = 2

    # store room coords in variables
    start_x = room1[0]
    start_y = room1[1]
    end_x = room2[0]
    end_y = room2[1]

    # if animating, setup this idx
    if animate_flag:
        m = 0

    # loop for as long as the starting point is not at end point, on x OR y dim. 
    while (start_x != end_x) or (start_y != end_y):
        
        # randomly select the width of path for this position
        clear_width = np.random.randint(min_range, max_range)

        # loop over the square in specified width, setting each spot on map to floor
        for i in range(start_x - clear_width, start_x + clear_width + 1):
            for j in range(start_y - clear_width, start_y + clear_width + 1):
                grid[i, j] = 0

        # increment if start_x <> end_x, or if start_y <> end_y
        if start_x < end_x:
            start_x += 1
        
        if start_x > end_x:
            start_x -= 1
        
        if start_y < end_y:
            start_y += 1
        
        if start_y > end_y:
            start_y -= 1
    
        # path creating takes less steps, so we'll animate the update every 5 frames
        if animate_flag:
            m += 1
            if m % 5 == 0:
                plot_grid(grid, f"animation/{animation_index}_iteration", f"time = {animation_index} (Density: {density}, Seed: {seed})")
                animation_index += 1

    return animation_index


# function to connect rooms across the map
def connect_map(grid, all_rooms, n_neighbors, animation_index, density, seed, animate_flag=True):
    """
    This function looks at all the rooms on the map, and connects each one to its n nearest
    neighbors, which is specified as an argument. 

    Args:
        grid: np matrix of map to connect rooms within
        all_rooms: list containing the midpoints of each room on the map
        n_neighbors: int, will set how many nearest neighbors each room creates a path to
        animation_index: int, for keeping track of anim. order
        density: int, for plotting in animation frame
        seed: int, for plotting in animation frame
        animate_flag: bool, whether or not to animate
    
    Returns:
        animation_index: int, for keeping track of anim progress. Otherwise map 
            connections are modified in place.
    """
    # for each room...
    for i in range(len(all_rooms)):
        
        # get the room we're currently on
        room = all_rooms[i]

        # make a copy of all_rooms for remaining so that OG isn't modified
        remaining_rooms = all_rooms.copy()

        # get rid of the room we're currently on:
        remaining_rooms.pop(i)

        # get the manhattan distances from this room to all remaining rooms. 
        # NOTE: this will be returned by get_manhattan_distance() in order of nearest neighbors earliest in dict
        manhattan_distances = get_manhattan_distance(room, remaining_rooms)

        # loop over the n nearest neighbors, and make a path between this room and each nearest neighbor. 
        for j in range(n_neighbors):
            animation_index = make_path(grid, room, list(manhattan_distances.values())[j], animation_index, density, seed, animate_flag)
    
    return animation_index


# function to find a specific corner room
def find_specific_room(rooms_list, min_area, grid_shape, target_x="low", target_y="low"):
    """
    This function finds a specified corner room. We want to do this so that the spawn
    and level exit can be on opposite corners of the map, incentivizing exploration. 

    Args:
        rooms_list: a list of all rooms on the map. 
        min_area: int, the minimum area acceptable for the spawn and level exit points
        grid_shape: tuple, dimensions of game map
        target_x: string, x coord corner of the map to search for, defaults to "low", also accepts "high"
        target_y: string, y coord corner of the map to search for, defaults to "low", also accepts "high"
    
    Returns:
        list: the room coordinates of the room closest to the specified corner of the map
    
    Notes: 
        We have both a target x & y parameter so that you can reach all 4 corners. 
        E.g., target_x = "low" and target_y = "low" will find the bottom-left corner of the map
              target_x = "low" and target_y = "high" will find the top-left corner of the map. 
    """
    # use list comprehension to filter out rooms which aren't above the min allowable area
    valid_rooms_list = [i for i in rooms_list if i[2] > min_area]

    # if there are no valid rooms above set area, raise an exception.
    if len(valid_rooms_list) == 0:
        raise Exception("Unable to find rooms: for this map there were no rooms above the specified min_area. Try lowering the map density or the min_area.")
    
    # max indices for x & y 
    max_x = grid_shape[0] - 1
    max_y = grid_shape[1] - 1

    # create vars to keep track of which room has the lowest distance, and room midpoint coords
    room_index = 0
    room_x = valid_rooms_list[room_index][0]
    room_y = valid_rooms_list[room_index][1]
    lowest_distance = -1

    # depending on desired parameters, get euclidean distance from first room to corner
    if (target_x == "low") and (target_y == "low"):
        lowest_distance = find_euclidean_distance((0, 0), (room_x, room_y))
    elif (target_x == "low") and (target_y == "high"):
        lowest_distance = find_euclidean_distance((0, max_y), (room_x, room_y))
    elif (target_x == "high") and (target_y == "low"):
        lowest_distance = find_euclidean_distance((max_x, 0), (room_x, room_y))
    elif (target_x == "high") and (target_y == "high"):
        lowest_distance = find_euclidean_distance((max_x, max_y), (room_x, room_y))

    # loop over all valid rooms
    for i in range(len(valid_rooms_list)):

        # get midpoint of current room
        this_x = valid_rooms_list[i][0]
        this_y = valid_rooms_list[i][1]

        # find euclidean dist to corner based on params
        if (target_x == "low") and (target_y == "low"):
            dist_from_goal = find_euclidean_distance((0, 0), (this_x, this_y))
        elif (target_x == "low") and (target_y == "high"):
            dist_from_goal = find_euclidean_distance((0, max_y), (this_x, this_y))
        elif (target_x == "high") and (target_y == "low"):
            dist_from_goal = find_euclidean_distance((max_x, 0), (this_x, this_y))
        elif (target_x == "high") and (target_y == "high"):
            dist_from_goal = find_euclidean_distance((max_x, max_y), (this_x, this_y))
        
        # if any of the rooms have a lower dist to corner, update our lowest and idx
        if dist_from_goal < lowest_distance:
            room_index = i 
            lowest_distance = dist_from_goal
    
    # after checking all rooms, room_index will store the room closest to desired corner
    return valid_rooms_list[room_index]


# function that uses BFS to verify whether or not a path exists from start point to end point
def verify_path(grid, start, finish):
    """
    This function verifies whether or not there is a path from a specified start point
    to a specified end point. 

    Params:
        grid: np matrix w/ game map
        start: a list containing the [x, y] coordinates of the start point (player spawn)
        finish: a list containing the [x, y] coordinates of the end point (level exit)
    
    Returns:
        bool: True if a valid path exists from start to finish, False otherwise
    """
    # create an index matrix for the grid
    ind_mat = create_index_matrix(grid)

    # get dimensions of the grid, and create a vis_mat to keep track of 
    # which cells have been visited in the BFS
    grid_shape = grid.shape
    num_rows = grid_shape[0]
    num_cols = grid_shape[1]
    vis_mat = np.zeros(shape = (num_rows, num_cols), dtype = int)

    # get starting cell index
    cell_idx = ind_mat[start[0], start[1]]

    # start BFS
    q = queue.Queue()
    q.put(cell_idx) # starting cell is 1st in queue

    # as long as unvisited cells remain in the queue...
    while q.qsize() > 0:

        # dequeue first cell in queue
        u = q.get()

        # get its current indices
        current_x = u // num_rows 
        current_y = u % num_cols 

        # note in vis_mat that this cell has been visited
        vis_mat[current_x, current_y] = 1

        # if we are at the desired end point, return True because we have found a valid path
        if (current_x == finish[0]) and (current_y == finish[1]):
            return True

        # ------------------------ Check von Neumann neighborhood to avoid blocking corner wall ------------------------ #
        """
        For each cell in von Neumann neighborhood, we will first check if it is in bounds, and unvisited. 
        If so, if the grid's state is 0 for floor, or 3 for enemy, we will consider it a valid cell in
        the room and enqueue it, else it will not be enqueued because it is a blocking wall or other kind of ore. 
        """
        # left (x - 1, y)
        if in_bounds(current_x - 1, current_y, grid_shape) and vis_mat[current_x - 1, current_y] == 0:
            if (grid[current_x - 1, current_y] in [0, 3]) and (ind_mat[current_x - 1, current_y] not in q.queue):
                q.put(ind_mat[current_x - 1, current_y])

        # right (x + 1, y)
        if in_bounds(current_x + 1, current_y, grid_shape) and vis_mat[current_x + 1, current_y] == 0:
            if (grid[current_x + 1, current_y] in [0, 3]) and (ind_mat[current_x + 1, current_y] not in q.queue):
                q.put(ind_mat[current_x + 1, current_y])

        # up (x, y + 1)
        if in_bounds(current_x, current_y + 1, grid_shape) and vis_mat[current_x, current_y + 1] == 0:
            if (grid[current_x, current_y + 1] in [0, 3]) and (ind_mat[current_x, current_y + 1] not in q.queue):
                q.put(ind_mat[current_x, current_y + 1])

        # down (x, y - 1)
        if in_bounds(current_x, current_y - 1, grid_shape) and vis_mat[current_x, current_y - 1] == 0:
            if (grid[current_x, current_y - 1] in [0, 3]) and (ind_mat[current_x, current_y - 1] not in q.queue):
                q.put(ind_mat[current_x, current_y - 1])

    # if BFS explored as far as possible without returning True, return False as no valid path exists.
    return False



# ------------------------------------------------------------- DISTANCE FUNCTIONS ------------------------------------------------------------ #


# function to get the manhattan distince between one room and a set of other rooms
def get_manhattan_distance(room, other_rooms):
    """
    This function will calculate the manhattan distance between one room's centerpoint, 
    to the centerpoint of all other rooms. 

    Args:
        room: a List containing the midpoint-coordinates and area of the room [x, y, area]
        other_rooms: a List of Lists, each element containing info. about another room
            [[x1, y1, area1], [x2, y2, area2], etc...]
    
    Returns:
        A List of Lists, containing all other_room coordinates with their manhattan distance from
        origin room. Additionally, this list will be ordered by the closest rooms to origin first.
    
    Note:
        formula for manhattan distance is: |x1 - x2| + |y1 - y2|
    """
    # create a dictionary that will store room info about the other rooms
    dist_dict = {}
    
    # for adding new elements to dist_dict
    idx = 0

    # loop over each room in the other rooms
    for r in other_rooms:

        # get x, y coordinates of origin room's midpoint
        x1 = room[0]
        y1 = room[1]

        # get x, y coordinates of current other room's midpoint
        x2 = r[0]
        y2 = r[1]
        room_area = r[2] # also get area of the other room

        # calculate manhattan distance according to formula
        m_dist = abs(x1 - x2) + abs(y1 - y2)

        # add calculated distance to dictionary with that other room's midpoint
        dist_dict[idx] = [x2, y2, room_area, m_dist]
        idx += 1

    # after all distances calculated, sort dictionary by manhattan dist
    # for lambda key, values are the 1st index, and we want manhattan dist, index 3 w/in those
    sorted_dict = dict(sorted(dist_dict.items(), key = lambda i: i[1][3]))

    return sorted_dict


# helper function to calculate the euclidean distance between two points
def find_euclidean_distance(p1, p2):
    """
    This function calculates the euclidean distance between two points. 

    Args:
        p1: a tuple containing the x and y coordinate of the first point (x1, y1)
        p2: a tuple containing the x and y coordinate of the second point (x2, y2)
    
    Note:
        formula for euclidean distance is: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """
    # calc and return euclidean distance
    inner_part = ((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2)
    euclidean_distance = inner_part ** 0.5
    return euclidean_distance



# ------------------------------------------------------------- PLOTTING FUNCTIONS ------------------------------------------------------------ #


# function to plot a simple grid with black and white pixels only
def plot_grid(grid, filename, custom_title, display=False):
    """
    This function creates a simple plot of a grid with black and white pixels.
    0s will be colored as white, and 1s as black.

    Args:
        grid: np matrix to plot
        filename: string, name of the output file to save in the figs directory
        custom_title: string, title to set on the plot
        display: bool, defaults to false, if true will display in a window as well as save file.
    
    Returns:
        None, but png image will be saved to figs directory
    """
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


# function to plot a more complex grid with multiple colors
def plot_complex_grid(grid, filename, custom_title, display=False):
    """
    This function creates a complex plot with multiple pixels. Color states will include:
        - 0: white
        - 1: black:
        - 2: gold
        - 3: red
        - 4: blue
        - > 5: green
        - > 70: pink

    Args:
        grid: np matrix to plot
        filename: string, name of the output file to save in the figs directory
        custom_title: string, title to set on the plot
        display: bool, defaults to false, if true will display in a window as well as save file.
    
    Returns:
        None, but png image will be saved to figs directory
    """
    # create a plot to hold the figure
    plot = plt.figure()

    color_map = colors.ListedColormap(['white', 'black', 'gold', 'red', 'blue', 'green', 'pink'])
    bounds = [0, 0.99, 2, 3, 4, 5, 70, 419]
    norm = colors.BoundaryNorm(bounds, color_map.N)

    plt.title(custom_title)
    plot = plt.imshow(
        grid, interpolation = 'nearest', origin = 'lower',
        cmap = color_map, norm = norm
    )

    # this may be uncommented for color scale, but gets in the way so I leave out
    #plt.colorbar(plot)
    
    # save image then display plot
    plt.savefig(f'figs/{filename}.png')

    if display:
        plt.show()
