
import argparse
from helpers import map_helpers as maps
import numpy as np # can be del once migrated
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



def find_rooms(game_map, adjacency_matrix, index_matrix):

    map_dim = game_map.shape 
    num_rows = map_dim[0]
    num_cols = map_dim[1]

    visited_matrix = np.zeros(shape=(num_rows, num_cols), dtype = int)

    for row in range(num_rows):
        for col in range(num_cols):

            print(f"Reviewing df[{row}, {col}] out of [{num_rows}, {num_cols}]")

            current_cell = index_matrix[row, col]
            cell_value = game_map[row, col]

            print(f"Cell Index: {current_cell}, Cell Value: {cell_value}")

            # if our current cell is either blank, an item, or enemy, we can consider that
            # part of a room, here we want to start a BFS to fully explore the room
            if cell_value in [0, 2, 3]:
                
                q = queue.Queue()
                q.put(current_cell) # add the current cell's index to queue

                print(q)

                while q.qsize() > 0:
                    
                    print(q.qsize())

                    curr = q.get() 

                    print(f"Current in queue: {curr}")
                    # find neighbors of current element
                    neighbors = [i for i, value in enumerate(adjacency_matrix[curr]) if value == 1]
                    print(neighbors)

                    for neighbor in neighbors:

                        # check if visited, only add if not visited AND a valid open cell
                        if (visited_matrix[neighbor // num_rows, neighbor % num_cols] == 0) and (game_map[neighbor // num_rows, neighbor % num_cols] in [0, 2, 3]):
                            q.put(neighbor)

                    # outside of for loop, change value of visited cell
                    game_map[row, col] = 420
                    visited_matrix[row, col] = 1




def main():

    """
    """
    test_no = 0


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

    modified_map = maps.add_detail(new_map, args.prob_item, args.prob_enemy)
    
    #modified_map[0,0] = 69
    #print(modified_map[0, 0])    
    maps.plot_complex_grid(modified_map, f"spawn-points/Test-{test_no}_Base-Map")

    
    results = create_adjacency_matrix(modified_map)

    ind_mat = results[0]
    adj_mat = results[1]
    #print(ind_mat)
    #print(ind_mat.shape)
    #print(adj_mat)
    #print(adj_mat.shape)
    #print([i for i, value in enumerate(adj_mat[101]) if value == 1]) # find the cell values that are linked to given cell
    
    #res = [i for i, value in enumerate(adj_mat[101]) if value == 1]

    #for item in res:
    #    print(f"The cell ({item // 100}, {item % 100}) neighbors 0, 0")



    find_rooms(modified_map, adj_mat, ind_mat)
    maps.plot_complex_grid(modified_map, f"spawn-points/Test-{test_no}_Base-Map_After-Room-Finding")
    
    #print(9999 // 100)
    #print(9999 % 100)
    #print(103 // 100)
    #print(103 % 100)
    #print(9950 // 100)
    #print(9950 % 100)


if __name__ == "__main__":
    main()
