"""
Tristan Jordan 
4/19/25
This script will generate a simple map with connected rooms, with options
to animate the process into a GIF.
"""


import argparse # for program args
from helpers import map_helpers as maps # helper functions for map generation
from helpers import animate_map_creation as anim # helper functions for animating gifs


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

    # make starting random noise grid
    grid = maps.create_noise_grid(args.height, args.width, args.density, args.seed)

    # check if animating or just saving final png
    if args.animate == 1:
        # clear directory in case anything remains from last anim
        anim.clear_anim_directory()

        # first will need to animate the simple map creation before rooms are connected
        animation_index = 0

        while animation_index < args.iterations:
            new_map = maps.create_map_with_ca(grid, animation_index)
            maps.plot_grid(new_map, f"animation/{animation_index}_iteration", f"time = {animation_index} (Density: {args.density}, Seed: {args.seed})")
            animation_index += 1

        # at this point the room is created, needs to be connected
        find_room_results = maps.find_room_coordinates(new_map, animation_index, args.density, args.seed)
        room_dict = find_room_results[0]
        animation_index = find_room_results[1]

        # get the midpoints of each room
        midpoints_dict = maps.get_room_midpoints(room_dict)
        all_rooms = list(midpoints_dict.values())

        # call connection function with animation options
        maps.connect_map(new_map, all_rooms, 3, animation_index, args.density, args.seed)

        # after that is complete, animate the whole sequence then clear directory
        anim.animate_map_creation(f"figs/gifs/Connected_Density-{args.density}_Iterations-{args.iterations}_Seed-{args.seed}.gif", 69, args.iterations)
        anim.clear_anim_directory()

    else:
        # use function to smooth map with cellular automata
        new_map = maps.create_map_with_ca(grid, args.iterations)

        # get all room midpoints
        midpoints_dict = maps.get_room_midpoints(maps.find_room_coordinates(new_map, -1, args.density, args.seed, animate_flag = False)[0])
        all_rooms = list(midpoints_dict.values())

        # call helper to connect rooms
        maps.connect_map(new_map, all_rooms, 3, -1, args.density, args.seed, animate_flag = False)

        # plot final result as a png
        maps.plot_grid(new_map, f"connected/Connected_Seed-{args.seed}_Density-{args.density}_i-{args.iterations}", "")


if __name__ == "__main__":
    main()
