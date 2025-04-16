
import argparse
from helpers import map_helpers as maps
import numpy as np # can be del once migrated
import math
import queue


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

                    if maps.in_bounds(i + row_offset, j + col_offset, table_shape):
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
                            if maps.in_bounds(i, j, grid_shape):
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

        #print(f"x1: {x1}\nx2: {x2}\ny1: {y1}\ny2: {y2}\nroom_area:{room_area}")

        m_dist = abs(x1 - x2) + abs(y1 - y2)

        # add calculated distance to dictionary with that other room's midpoint
        dist_dict[idx] = [x2, y2, room_area, m_dist]
        idx += 1

    # after all distances calculated, sort dictionary by manhattan dist
    # for lambda key, values are the 1st index, and we want manhattan dist, index 3 w/in those
    sorted_dict = dict(sorted(dist_dict.items(), key = lambda i: i[1][3]))

    return sorted_dict


def make_path(grid, room1, room2):

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
    

def connect_map(grid, all_rooms, n_neighbors):

    for i in range(len(all_rooms)):

        # get the room we're currently on
        room = all_rooms[i]

        # make a copy of all_rooms for remaining so that OG isn't modified
        remaining_rooms = all_rooms.copy()

        # get rid of the room we're currently on:
        remaining_rooms.pop(i)

        manhattan_distances = get_manhattan_distance(room, remaining_rooms)

        for j in range(n_neighbors):
            make_path(grid, room, list(manhattan_distances.values())[j])


def main():

    """
    """
    test_no = 5


    # add arguments for program to parse
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type = int, help = "height of the map")
    parser.add_argument("--width", type = int, help = "width of the map")
    parser.add_argument("--density", type = int, help = "desired noise density (0 - 100)")
    parser.add_argument("--iterations", type = int, help = "number of smoothing iterations to apply.")
    parser.add_argument("--seed", type = int, help = "Seed for random number generation")
    parser.add_argument("--prob_item", type = float, help = "probability of spawning an item")
    parser.add_argument("--prob_enemy", type = float, help = "probability of spawning an enemy")
    args = parser.parse_args()


    # make starting grid
    grid = maps.create_noise_grid(args.height, args.width, args.density, args.seed)

    # use function to smooth map with cellular automata
    new_map = maps.create_map_with_ca(grid, args.iterations)

    # add details to the new map
    modified_map = maps.add_detail(new_map, args.prob_item, args.prob_enemy)
     


    #maps.plot_complex_grid(modified_map, f"spawn-points/Test-{test_no}_Base-Map")


    midpoints_dict = get_room_midpoints(find_room_coordinates(modified_map))



    for key, val in midpoints_dict.items():
        modified_map[val[0], val[1]] = 400
        #print(f"Room: ({val[0]}, {val[1]}), area: {val[2]}")

    #maps.plot_complex_grid(modified_map, f"spawn-points/Test-{test_no}_Base-Map_with_room_midpoints")
    #print(modified_map)

    #print(midpoints_dict.keys())
    #print(midpoints_dict.values())
    #print(midpoints_dict.items())
    #print(abs(-1))

    all_rooms = list(midpoints_dict.values())

    #room_1 = all_rooms[0]
    #rest = all_rooms[1:]

    #print(room_1[0])
    #print(rest)

    #for r in rest:
       # print(r[0])

    #test = get_manhattan_distance(room_1, rest)

    #print(room_1)
    #print(list(test.values())[0])

    #make_path(modified_map, room_1, list(test.values())[0])

    connect_map(modified_map, all_rooms, 3)

    maps.plot_complex_grid(modified_map, f"spawn-points/Test-{test_no}_AfterPath")


if __name__ == "__main__":
    main()
