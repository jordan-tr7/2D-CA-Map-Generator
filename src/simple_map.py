"""
Tristan Jordan
4/16/25
Script to create a simple 2D game map from a random noise grid.
"""

import argparse # for parsing arguments
from helpers import map_helpers as maps # load custom helper functions
from helpers import animate_map_creation as anim # custom helpers for animating

def main():
    # add arguments for program to parse
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type = int, help = "height of the map")
    parser.add_argument("--width", type = int, help = "width of the map")
    parser.add_argument("--density", type = int, help = "desired noise density (0 - 100)")
    parser.add_argument("--iterations", type = int, help = "number of smoothing iterations to apply.")
    parser.add_argument("--seed", type = int, help = "Seed for random number generation")
    parser.add_argument("--animate", type = int, help = "Int for whether or not to animate plot: 1 = yes, 0 = no")
    args = parser.parse_args()

    # create a random noise grid to store map
    grid = maps.create_noise_grid(args.height, args.width, args.density, args.seed)

    # based on animation parameter, either save a gif of each step, or an image of final state
    if args.animate == 1:

        anim.clear_anim_directory()

        for i in range(args.iterations):
            new_map = maps.create_map_with_ca(grid, i)
            maps.plot_grid(new_map, f"animation/{i}_iteration", f"time = {i} (Density: {args.density}, Seed: {args.seed})")

        anim.animate_map_creation(f"figs/gifs/Density-{args.density}_Iterations-{args.iterations}_Seed-{args.seed}.gif", 500, args.iterations)
    else:
        # use function to smooth map with cellular automata
        new_map = maps.create_map_with_ca(grid, args.iterations)

        # plot the resulting map from CA iterations
        maps.plot_grid(new_map, f"Density-{args.density}_iteration-{args.iterations}_{args.height}x{args.width}", "")


if __name__ == "__main__":
    main()
