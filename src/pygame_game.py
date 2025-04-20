"""
Tristan Jordan
4/19/25
A Pygame implementation of our randomly generated game maps. 
"""

import sys
import argparse # for program params
import pygame # for game rendering
from helpers import map_helpers as maps # custom helper functions for generating game maps w/ CAs

# constant for base block width
BLOCK_WIDTH = 32

# helper function to try to rescale images for allowing map resizing in game, this doesn't work very well but keeping in.
def rescale_images():
    # trying smoothscale for rescaling of images per suggestion (it didn't really fix much):
    # https://stackoverflow.com/questions/77439196/pygame-surface-scaling-issue
    dirt = pygame.transform.smoothscale(pygame.image.load("assets/dirt.png"), (BLOCK_WIDTH, BLOCK_WIDTH))   
    stone = pygame.transform.smoothscale(pygame.image.load("assets/stone.png"), (BLOCK_WIDTH, BLOCK_WIDTH))
    gold = pygame.transform.smoothscale(pygame.image.load("assets/gold.png"), (BLOCK_WIDTH, BLOCK_WIDTH)) 
    diamond = pygame.transform.smoothscale(pygame.image.load("assets/diamond.png"), (BLOCK_WIDTH, BLOCK_WIDTH))
    enemy = pygame.transform.smoothscale(pygame.image.load("assets/enemy.png"), (BLOCK_WIDTH, BLOCK_WIDTH)) 
    player = pygame.transform.smoothscale(pygame.image.load("assets/player.png"), (BLOCK_WIDTH, BLOCK_WIDTH))
    level_exit = pygame.transform.smoothscale(pygame.image.load("assets/exit.png"), (BLOCK_WIDTH, BLOCK_WIDTH))
    pygame.display.update() # try to re-update display after rescaling


# ---------------------------------------------------- MAIN ---------------------------------------------------- #
def main():

    # setting variables for block height, screen dimensions for rendering. 
    BLOCK_WIDTH = 32
    SCREEN_WIDTH = 800
    SCREEN_WIDTH_BLOCKS = SCREEN_WIDTH / BLOCK_WIDTH
    SCREEN_HEIGHT = 608
    SCREEN_HEIGHT_BLOCKS = SCREEN_HEIGHT / BLOCK_WIDTH
    WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    # loading my custom sprites from the assets directory
    dirt = pygame.transform.scale(pygame.image.load("assets/dirt.png"), (BLOCK_WIDTH, BLOCK_WIDTH))   
    stone = pygame.transform.scale(pygame.image.load("assets/stone.png"), (BLOCK_WIDTH, BLOCK_WIDTH))
    gold = pygame.transform.scale(pygame.image.load("assets/gold.png"), (BLOCK_WIDTH, BLOCK_WIDTH)) 
    diamond = pygame.transform.scale(pygame.image.load("assets/diamond.png"), (BLOCK_WIDTH, BLOCK_WIDTH))
    enemy = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (BLOCK_WIDTH, BLOCK_WIDTH)) 
    player = pygame.transform.scale(pygame.image.load("assets/player.png"), (BLOCK_WIDTH, BLOCK_WIDTH))
    level_exit = pygame.transform.scale(pygame.image.load("assets/exit.png"), (BLOCK_WIDTH, BLOCK_WIDTH))

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

    # use helper function to randomly generate a map using CAs and other algos, store the map and spawn/exit positions
    starting_map_info = maps.create_complete_map(args.height, args.width, args.density, args.seed, args.iterations, args.prob_item, args.prob_enemy)
    game_map = starting_map_info[0]
    player_pos = starting_map_info[1]
    level_exit_pos = starting_map_info[2]

    # if map is too sparse and the player spawn / level exit are the same position, generate a new map with higher density and try again. 
    i = 1

    while player_pos == level_exit_pos:
        print("Changing map for the i-th time:", i)
        i += 1
        starting_map_info = maps.create_complete_map(args.height, args.width, args.density + 1, args.seed, args.iterations - 1, args.prob_item, args.prob_enemy)
        game_map = starting_map_info[0]
        player_pos = starting_map_info[1]
        level_exit_pos = starting_map_info[2]

    # setup a clock to limit FPS, and then initialize various pygame attributes like screen, captions, etc.
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption(f"Mine On! - Map Density: {starting_map_info[3]}, Seed: {starting_map_info[4]}, Iterations: {starting_map_info[5]}")
    screen = pygame.display.set_mode(WINDOW_SIZE)
    display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # -------------------- game loop runs in infinite loop until run == False -------------------- #
    run = True

    while run:

        # limit to 30 FPS (helps slow player movement)
        clock.tick(30)

        # base screen filled with gray color for outside map bounds
        screen.fill((86, 86, 86))

        # update the width and height in blocks in case they were changed
        SCREEN_WIDTH_BLOCKS = SCREEN_WIDTH / BLOCK_WIDTH
        SCREEN_HEIGHT_BLOCKS = SCREEN_HEIGHT / BLOCK_WIDTH
        
        # get the player's current position
        player_x = player_pos[0]
        player_y = player_pos[1]

        # calculate the min x, y coords in block dimensions that center around the player
        min_row_pos = player_x - int(SCREEN_WIDTH_BLOCKS / 2) 
        min_col_pos = player_y - int(SCREEN_HEIGHT_BLOCKS / 2) 

        # we only want to render the portion of the map centered around the player within view distance
        for i in range(player_pos[0] - int(SCREEN_WIDTH_BLOCKS / 2), player_pos[0] + int(SCREEN_WIDTH_BLOCKS / 2) + 1):
            for j in range(player_pos[1] - int(SCREEN_HEIGHT_BLOCKS / 2), player_pos[1] + int(SCREEN_HEIGHT_BLOCKS / 2) + 1):

                # if any index is out of bounds, skip drawing anything, otherwise, use blit to draw sprites to grid at specified x, y pos
                # NOTE: some transparent sprites (player, enemy) are drawn over a dirt blit so there's no blank background behind sprite
                if (i < 0) or (j < 0) or (i > args.width - 1) or (j > args.height - 1):
                    continue
                elif game_map[i, j] == 0:
                    screen.blit(dirt, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                elif game_map[i, j] == 1:
                    screen.blit(stone, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                elif game_map[i, j] == 2:
                    screen.blit(gold, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                elif game_map[i, j] == 3:
                    screen.blit(dirt, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                    screen.blit(enemy, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                elif game_map[i, j] == 4:
                    screen.blit(diamond, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                elif game_map[i, j] == 69:
                    screen.blit(dirt, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                    screen.blit(player, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                elif game_map[i, j] == 400:
                    screen.blit(dirt, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))
                    screen.blit(level_exit, ((i - min_row_pos) * BLOCK_WIDTH, (j - min_col_pos) * BLOCK_WIDTH))

        # in game loop get keys pressed
        key = pygame.key.get_pressed()

        # WASD movement:
        #   if any key is pressed, we are going to use the game_map matrix to check if
        #   there's a valid move at that position (0 / floor). If so, we will change the
        #   player's location in the matrix so that it will be redrawn next frame
        #   also update player_pos var
        if key[pygame.K_a] == True:
            if (player_x - 1) >= 0:
                if (game_map[player_x - 1, player_y] == 0):
                    game_map[player_x, player_y] = 0
                    game_map[player_x - 1, player_y] = 69
                    player_pos[0] = player_x - 1
        elif key[pygame.K_d] == True:
            if (player_x + 1) <= args.width - 1: 
                if game_map[player_x + 1, player_y] == 0:
                    game_map[player_x, player_y] = 0
                    game_map[player_x + 1, player_y] = 69
                    player_pos[0] = player_x + 1
        elif key[pygame.K_w] == True: 
            if (player_y - 1) >= 0:  
                if game_map[player_x, player_y - 1] == 0:
                    game_map[player_x, player_y] = 0
                    game_map[player_x, player_y - 1] = 69
                    player_pos[1] = player_y - 1
        elif key[pygame.K_s] == True:   
            if (player_y + 1) <= args.height - 1:
                if game_map[player_x, player_y + 1] == 0:
                    game_map[player_x, player_y] = 0
                    game_map[player_x, player_y + 1] = 69
                    player_pos[1] = player_y + 1
      
        # NOTE: was experimenting w/ re-scaling map in game...
        # this screen scaling is buggy and not implemented perfectly, I don't know pygame super well, 
        # although it is kind of janky looking, still does let you zoom out for a sense of larger map w/in game.
        # ... change block width var for scaling out / in, then try to call helper to rescale sprites
        elif key[pygame.K_e]:
            BLOCK_WIDTH += 1
            rescale_images()
        elif key[pygame.K_q]:
            BLOCK_WIDTH -= 1
            rescale_images()
    
        # use pygames pre-written event classes to check for quit, and end game loop if window is closed.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # update display to redraw map in next frame
        pygame.display.update()

    # quit if game loop exited (window closed)
    pygame.quit()


if __name__ == "__main__":
    main()
