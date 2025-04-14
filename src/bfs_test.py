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



def find_rooms(grid):

    res = create_adjacency_matrix(grid)
    ind_mat = res[0]
    adj_mat = res[1]

    grid_shape = grid.shape 
    num_rows = grid_shape[0]
    num_cols = grid_shape[1]

    vis_mat = np.zeros(shape=(num_rows, num_cols), dtype = int)

    for row in range(num_rows):
        for col in range(num_cols):

            cell_val = grid[row, col]
            cell_idx = ind_mat[row, col]

            # if blank space, start bfs
            if cell_val == 0:

                q = queue.Queue()
                q.put(cell_idx) # add the current cell's index to queue

                while q.qsize() > 0:
                    
                    u = q.get()

                    # update visited
                    vis_mat[u // num_rows, u % num_cols] = 1

                    # update symbol in game grid
                    grid[u // num_rows, u % num_cols] = 9

                    neighbors = [i for i, value in enumerate(adj_mat[u]) if value == 1]

                    for neighbor in neighbors:
                        if grid[neighbor // num_rows, neighbor % num_cols] == 0:
                            q.put(neighbor)

                    #print(f"At cell: {u}: ({u // num_rows}, {u % num_cols})")
                    #print(f"\tNeighbors: {[i for i, value in enumerate(adj_mat[u]) if value == 1]}")
                    #print(q.qsize())





def main():
    

    grid = np.array([
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ])

    res = create_adjacency_matrix(grid)
    ind_mat = res[0]
    adj_mat = res[1]

    #print(ind_mat)
    #print(adj_mat)
    #print(24 // 5)
    #print(24 % 5)

    print(grid)

    find_rooms(grid)


    print(grid)
    #for i in range(5):
    #    for j in range(5):
    #        print(grid[i, j])


if __name__ == "__main__":
    main()
