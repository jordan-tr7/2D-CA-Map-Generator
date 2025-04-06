from helpers import map_helpers as maps
import numpy as np

"""
Notes: 

For this algo, map must be size 2^n + 1

Steps:
1) Assign a height value to each corner of the map (top right, top left, etc.)
2) Run an iteration of square step, e.g., avg 4 corners to set center number
   +/- random number, 
3) Diamond step, four diamonds (technically triangles as one corner missing)
   Similarly, calculate average of corners +/- random number

Once we finish full square and diamond step, we need to augment random range, 
e.g., from [-2, 2] to [-1, 1]
"""


def diamond_square(starting_size, heights, rand_range):
    
    np.random.seed(42) #rng_seed

    # refers to the width of one edge of the map 
    # e.g. given starting size 2, becomes 5 for a 25 cell (5x5) matrix
    height_map_size = (2 ** starting_size) + 1

    # refers to width of each square / diamond in iteration
    chunk_size = max_table_idx = height_map_size - 1


    # create empty grid
    grid = maps.create_blank_grid(height_map_size, height_map_size)

    # randomly set starting corners
    grid[0, 0] = np.random.randint(heights[0], heights[1] + 1)
    grid[chunk_size, 0] = np.random.randint(heights[0], heights[1] + 1)
    grid[0, chunk_size] = np.random.randint(heights[0], heights[1] + 1)
    grid[chunk_size, chunk_size] = np.random.randint(heights[0], heights[1] + 1)

    roughness = 2 # random range

    while chunk_size > 1:
        
        step_size = chunk_size // 2

        for i in range(0, max_table_idx, step_size):
            for j in range(0, max_table_idx, step_size):
                # skip if this cell already has a value
                if grid[i, j] != 0:
                    continue

                grid[i, j] = (grid[i - step_size, j - step_size] + grid[i + step_size, j + step_size] +  grid[i - step_size, j + step_size] +  grid[i + step_size, j - step_size])/4 

        chunk_size //= 2


     #   diamond_step()
     #   chunk_size /= 2
     #   roughness /= 2
    
    return grid # return height_map



def diamond_square_recur(grid, top_LX, bot_RX, top_LY, bot_RY, depth):

    current_length = bot_RX - top_LX

    # if short enough for no defined point on next diamond step, return
    if current_length < 2:
        return

    modify_X = (top_LX + bot_RX) / 2
    modify_Y = (top_LY + bot_RY) / 2

    # diamond part
    avg = int((grid[top_LX, top_LY] + grid[top_LX, bot_RY] + grid[bot_RX, bot_RY] + grid[bot_RX, top_LY]) / 4)
    grid[modify_X, modify_Y] = avg # TODO: add random num here

    # square part
    


def main():

    heights = [1, 8]
    rand_range = [-2, 2]


    test = diamond_square(2, heights, rand_range)
    print(test)






if __name__ == "__main__":
    main()
