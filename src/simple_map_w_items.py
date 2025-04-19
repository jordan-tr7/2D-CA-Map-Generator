"""
Tristan Jordan
4/19/25
This script demonstrates the stage of the algorithm to add items and enemies,
after the connected map is created
"""

import argparse # program args
from helpers import map_helpers as maps # helpers for map gen
from helpers import animate_map_creation as anim # helpers for gif creation


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

    # case we want to animate a GIF
    if args.animate == 1:
        # clear outstanding pngs from prior runs
        anim.clear_anim_directory()

        # create frames for initial map creation
        animation_index = 0

        while animation_index < args.iterations:
            new_map = maps.create_map_with_ca(grid, animation_index)
            maps.plot_grid(new_map, f"animation/{animation_index}_iteration", f"time = {animation_index} (Density: {args.density}, Seed: {args.seed})")
            animation_index += 1

        # at this point the room is created, needs to be connected
        find_room_results = maps.find_room_coordinates(new_map, animation_index, args.density, args.seed)
        room_dict = find_room_results[0]
        animation_index = find_room_results[1]

        # get room midpoints
        midpoints_dict = maps.get_room_midpoints(room_dict)
        all_rooms = list(midpoints_dict.values())

        # call room connection function w/ animation args
        animation_index = maps.connect_map(new_map, all_rooms, 3, animation_index, args.density, args.seed)

        # call detail addition function w/ animation args
        add_detail_results = maps.add_detail(new_map, args.prob_item, args.prob_enemy, animation_index, args.density, args.seed)

        # get map and animation index in case needed
        modified_map = add_detail_results[0]
        animation_index = add_detail_results[1]

        # animate gif, then clear directory
        anim.animate_map_creation(f"figs/gifs/Items-Enemies_Density-{args.density}_Iterations-{args.iterations}_Seed-{args.seed}.gif", 69, args.iterations)
        anim.clear_anim_directory()

    else:
        # use function to smooth map with cellular automata
        new_map = maps.create_map_with_ca(grid, args.iterations)

        # get room midpoints
        midpoints_dict = maps.get_room_midpoints(maps.find_room_coordinates(new_map, -1, args.density, args.seed, animate_flag = False)[0])
        all_rooms = list(midpoints_dict.values())

        # connect rooms
        maps.connect_map(new_map, all_rooms, 3, -1, args.density, args.seed, animate_flag = False)

        # add items, enemies
        modified_map = maps.add_detail(new_map, args.prob_item, args.prob_enemy, 0, args.density, args.seed, animate_flag=False)

        # save PNG with final result
        maps.plot_complex_grid(modified_map[0], f"2d-maps-w-items/Enhanced_Density-{args.density}_iteration-{args.iterations}_p-enem-{args.prob_enemy}_p-item-{args.prob_item}", "")


if __name__ == "__main__":
    main()
