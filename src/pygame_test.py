import sys
import argparse
import pygame
from helpers import map_helpers as maps

"""
Main Pygame elements:
1) Game Window
2) Game Loop
3) Event handler
"""

BLOCK_WIDTH = 32
SCREEN_WIDTH = 800
SCREEN_WIDTH_BLOCKS = SCREEN_WIDTH / BLOCK_WIDTH
SCREEN_HEIGHT = 608
SCREEN_HEIGHT_BLOCKS = SCREEN_HEIGHT / BLOCK_WIDTH
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

dirt = pygame.transform.scale(pygame.image.load("assets/dirt.png"), (32, 32))   
stone = pygame.transform.scale(pygame.image.load("assets/stone.png"), (32, 32))
gold = pygame.transform.scale(pygame.image.load("assets/gold.png"), (32, 32)) 
diamond = pygame.transform.scale(pygame.image.load("assets/diamond.png"), (32, 32))
enemy = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (32, 32)) 
player = pygame.transform.scale(pygame.image.load("assets/player.png"), (32, 32))
level_exit = pygame.transform.scale(pygame.image.load("assets/exit.png"), (32, 32))

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


    starting_map_info = maps.create_complete_map(args.height, args.width, args.density, args.seed, args.iterations, args.prob_item, args.prob_enemy)
    game_map = starting_map_info[0]
    player_pos = starting_map_info[1]
    level_exit_pos = starting_map_info[2]

    print(player_pos)
    print(level_exit_pos)
    print(player_pos == level_exit_pos)

    i = 1

    while player_pos == level_exit_pos:
        print("Changing time", i)
        i += 1
        starting_map_info = maps.create_complete_map(args.height, args.width, args.density + 1, args.seed, args.iterations - 1, args.prob_item, args.prob_enemy)
        game_map = starting_map_info[0]
        player_pos = starting_map_info[1]
        level_exit_pos = starting_map_info[2]

    clock = pygame.time.Clock()

    pygame.init()

    pygame.display.set_caption(f"Mine On! - Map Density: {starting_map_info[3]}, Seed: {starting_map_info[4]}, Iterations: {starting_map_info[5]}")


    screen = pygame.display.set_mode(WINDOW_SIZE)

    display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    print(player_pos[0] - int(SCREEN_WIDTH_BLOCKS / 2), player_pos[0], player_pos[0] + int(SCREEN_WIDTH_BLOCKS / 2))
    print(player_pos[1] - int(SCREEN_HEIGHT_BLOCKS / 2), player_pos[1], player_pos[1] + int(SCREEN_HEIGHT_BLOCKS / 2))

    run = True

    while run:

        clock.tick(30)

        screen.fill((86, 86, 86))


        player_x = player_pos[0]
        player_y = player_pos[1]

        min_row_pos = player_x - int(SCREEN_WIDTH_BLOCKS / 2) 
        min_col_pos = player_y - int(SCREEN_HEIGHT_BLOCKS / 2) 


        for i in range(player_pos[0] - int(SCREEN_WIDTH_BLOCKS / 2), player_pos[0] + int(SCREEN_WIDTH_BLOCKS / 2)):
            for j in range(player_pos[1] - int(SCREEN_HEIGHT_BLOCKS / 2), player_pos[1] + int(SCREEN_HEIGHT_BLOCKS / 2)):

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

        key = pygame.key.get_pressed()

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




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()






if __name__ == "__main__":
    main()
