from helpers import map_helpers as maps
import matplotlib.pyplot as plt
from matplotlib import colors
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


def initialize_corners(starting_size, heights):
    
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

    return grid 



def diamond_square_recur(grid, top_LX, bot_RX, top_LY, bot_RY, depth, random_range):


    current_length = bot_RX - top_LX

    # if short enough for no defined point on next diamond step, return
    if current_length < 2:
        return

    modify_X = int((top_LX + bot_RX) / 2)
    modify_Y = int((top_LY + bot_RY) / 2) 

    # diamond part
    avg = (grid[top_LX, top_LY] + grid[top_LX, bot_RY] + grid[bot_RX, bot_RY] + grid[bot_RX, top_LY]) / 4
    grid[modify_X, modify_Y] = avg + np.random.randint(random_range[0], random_range[1])

    # --------------------- square part ---------------------
    
    # left square side midpoint TODO: add random
    grid[top_LX, modify_Y] = ((grid[top_LX, top_LY] + grid[top_LX, bot_RY] + grid[modify_X, modify_Y]) / 3) + np.random.randint(random_range[0], random_range[1])

    # top square side midpoint TODO: add random
    grid[modify_X, top_LY] = ((grid[top_LX, top_LY] + grid[bot_RX, top_LY] + grid[modify_X, modify_Y]) / 3) + np.random.randint(random_range[0], random_range[1])

    # right square side midpoint TODO: add random
    grid[bot_RX, modify_Y] = ((grid[modify_X, modify_Y] + grid[bot_RX, top_LY] + grid[bot_RX, bot_RY]) / 3) + np.random.randint(random_range[0], random_range[1])

    # bottom square side midpoint TODO: add random
    grid[modify_X, bot_RY] = ((grid[modify_X, modify_Y] + grid[top_LX, bot_RY] + grid[bot_RX, bot_RY]) / 3) + np.random.randint(random_range[0], random_range[1])


    # update random range var
    random_range = [i * 0.95 for i in random_range]

    # ---------------- make recursive calls ---------------- 
    # top-left quadrant
    diamond_square_recur(grid, top_LX, modify_X, top_LY, modify_Y, depth + 1, random_range)
   
    # bottom-right quadrant
    diamond_square_recur(grid, modify_X, bot_RX, modify_Y, bot_RY, depth + 1, random_range)
    
    # top-right quadrant
    diamond_square_recur(grid, modify_X, bot_RX, top_LY, modify_Y, depth + 1, random_range)
    
    # bottom-left quadrant
    diamond_square_recur(grid, top_LX, modify_X, modify_Y, bot_RY, depth + 1, random_range)



def plot_heightmap(grid, filename):

    # create a plot to hold the figure
    plot = plt.figure()

    color_map = colors.ListedColormap(['blue', '#E9DFC3', 'green', 'gray', 'white'])
    bounds = [0, 6, 8, 12, 16, 20]
    norm = colors.BoundaryNorm(bounds, color_map.N)

    plot = plt.imshow(
        grid, interpolation = 'nearest', origin = 'lower',
        cmap = color_map, norm = norm
    )

    # this may be uncommented for color scale, but not relevant for binary
    plt.colorbar(plot)
    
    # save image then display plot
    plt.savefig(f'figs/height-maps/{filename}.png')
    plt.show()


#def diamond_square(grid, topLX, botRX, topLY):
#    print("hi")

def main():

    heights = [0, 20]
    rand_range = [-4, 4]


    test = initialize_corners(7, heights)
    #print(test)

    diamond_square_recur(test, 0, test.shape[0]-1, 0, test.shape[1]-1, 1, rand_range)

    plot_heightmap(test, "Test-1")

    #print(np.min(test))
    #print(np.max(test))




if __name__ == "__main__":
    main()
