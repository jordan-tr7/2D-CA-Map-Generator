
import argparse
from helpers import map_helpers as maps


def main():

    # add arguments for program to parse
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type = int, help = "height of the map")
    parser.add_argument("--width", type = int, help = "width of the map")
    parser.add_argument("--density", type = int, help = "desired noise density (0 - 100)")
    parser.add_argument("--iterations", type = int, help = "number of smoothing iterations to apply.")
    parser.add_argument("--seed", type = int, help = "Seed for random number generation")
    args = parser.parse_args()

    # Note: 1's, black cells, are walls
    #       0's, white cells, are floors
    # create a random noise grid to store map
    grid = maps.create_noise_grid(args.height, args.width, args.density, args.seed)

    # plot this initial noise grid
    maps.plot_grid(grid, f"Density-{args.density}_iteration-0_{args.height}x{args.width}")

    # use function to smooth map with cellular automata
    new_map = maps.create_map_with_ca(grid, args.iterations)

    # plot the resulting map from CA iterations
    maps.plot_grid(new_map, f"Density-{args.density}_iteration-{args.iterations}_{args.height}x{args.width}")


if __name__ == "__main__":
    main()
