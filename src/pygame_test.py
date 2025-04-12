


import pygame
import sys

"""
Main Pygame elements:
1) Game Window
2) Game Loop
3) Event handler
"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

def main():

    clock = pygame.time.Clock()

    pygame.init()

    pygame.display.set_caption("Mine On!")


    screen = pygame.display.set_mode(WINDOW_SIZE)

    display = pygame.Surface((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))


    player = pygame.Rect((300, 250, 50, 50))


    # TODO: look up rendering images to screen
    # TODO: pixel set, stone, cave floor, ore
    # TODO: player / enemy pixel?
    # TODO: load CA MAP, then generate to screen

    run = True

    while run:

        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (255, 0, 0), player)

        key = pygame.key.get_pressed()

        if key[pygame.K_a] == True:
            player.move_ip(-1, 0)
        elif key[pygame.K_d] == True:
            player.move_ip(1, 0)
        elif key[pygame.K_w] == True:
            player.move_ip(0, -1)
        elif key[pygame.K_s] == True:
            player.move_ip(0, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        pygame.display.update()

    pygame.quit()






if __name__ == "__main__":
    main()
