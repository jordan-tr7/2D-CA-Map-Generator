"""
Tristan Jordan
4/19/25
This script creates a complete map with connected rooms, items, enemies, and spawn / level exit points. 
"""


import argparse # for program args
from helpers import map_helpers as maps # helpers for map gen


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
    parser.add_argument("--animate", type = int, help = "Int for whether or not to animate plot: 1 = yes, 0 = no")
    args = parser.parse_args()

    # make starting grid
    grid = maps.create_noise_grid(args.height, args.width, args.density, args.seed)

    # use function to smooth map with cellular automata
    new_map = maps.create_map_with_ca(grid, args.iterations)

    # get all room midpoints
    midpoints_dict = maps.get_room_midpoints(maps.find_room_coordinates(new_map, -1, args.density, args.seed, animate_flag = False)[0])
    all_rooms = list(midpoints_dict.values())

    # connect all rooms
    maps.connect_map(new_map, all_rooms, 3, -1, args.density, args.seed, animate_flag = False)

    # add items, enemies
    modified_map = maps.add_detail(new_map, args.prob_item, args.prob_enemy, 0, args.density, args.seed, animate_flag=False)

    # find rooms closest to separate corners for spawn / exit points
    spawn_point = maps.find_specific_room(all_rooms, 35, new_map.shape, "high", "low")
    exit_point = maps.find_specific_room(all_rooms, 35, new_map.shape, "low", "high")

    # check whether or not there is a valid path from start to end, print
    # in this script not enforcing this be true so you can see examples of ones where pathing fails. 
    # this however will be handled by the function that creates maps for the pygame implementation. 
    valid_points = maps.verify_path(modified_map[0], [spawn_point[0], spawn_point[1]], [exit_point[0], exit_point[1]])
    print(valid_points)

    # although spawn/exit points only need to be one cell, changing colors of a larger swath so they're easier to see
    for i in range(spawn_point[0] - 1, spawn_point[0] + 2):
        for j in range(spawn_point[1] - 1, spawn_point[1] + 2):
            modified_map[0][i, j] = 69
    for i in range(exit_point[0] - 1, exit_point[0] + 2):
        for j in range(exit_point[1] - 1, exit_point[1] + 2):
            modified_map[0][i, j] = 400

    # save png of final result
    maps.plot_complex_grid(modified_map[0], f"spawn-points/Density-{args.density}_iteration-{args.iterations}_p-enem-{args.prob_enemy}_p-item-{args.prob_item}_seed-{args.seed}", "")


if __name__ == "__main__":
    main()
