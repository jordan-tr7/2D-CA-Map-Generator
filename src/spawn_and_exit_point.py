
import argparse
from helpers import map_helpers as maps
import numpy as np # can be del once migrated


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
    
    modified_map[0,0] = 69
    print(modified_map[0, 0])    
    maps.plot_complex_grid(modified_map, f"spawn-points/Test-{test_no}_Base-Map")

    
    results = create_adjacency_matrix(modified_map)

    ind_mat = results[0]
    adj_mat = results[1]
    print(ind_mat)
    print(adj_mat)



if __name__ == "__main__":
    main()
