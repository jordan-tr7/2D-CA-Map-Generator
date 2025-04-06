import argparse
from helpers import map_helpers as maps
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt


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
                    if maps.in_bounds(m, n, table_shape):
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

    color_map = colors.ListedColormap(['white', 'black', 'gold', 'red', 'blue'])
    bounds = [0, 1, 2, 3, 4, 5]
    norm = colors.BoundaryNorm(bounds, color_map.N)

    plot = plt.imshow(
        grid, interpolation = 'nearest', origin = 'lower',
        cmap = color_map, norm = norm
    )

    # this may be uncommented for color scale, but not relevant for binary
    #plt.colorbar(plot)
    
    # save image then display plot
    plt.savefig(f'figs/2d-maps-w-items/{filename}.png')
    plt.show()


def main():

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

    # plot this initial noise grid
    maps.plot_grid(grid, f"Density-{args.density}_iteration-0_{args.height}x{args.width}")

    # use function to smooth map with cellular automata
    new_map = maps.create_map_with_ca(grid, args.iterations)

    modified_map = add_detail(new_map, args.prob_item, args.prob_enemy)

    plot_complex_grid(modified_map, f"Enhanced_Density-{args.density}_iteration-{args.iterations}_p-enem-{args.prob_enemy}_p-item-{args.prob_item}_{args.height}x{args.width}")

    print(modified_map)

    # plot the resulting map from CA iterations
    #maps.plot_grid(new_map, f"Density-{args.density}_iteration-{args.iterations}_{args.height}x{args.width}")
    # add items / enemies




if __name__ == "__main__":
    main()
