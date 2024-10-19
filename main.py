from game_world import GameWorld
import constants

import pygame

def main():
    pygame.init()
    render_target = pygame.display.set_mode(constants.WINDOW_RESOLUTION)
    clock = pygame.time.Clock()
    game_world = GameWorld(render_target)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_target.fill(constants.BLACK_CLEAR_COLOR)

        delta_time = clock.tick(60) / 1000
        game_world.update(delta_time)
        game_world.render(render_target)

        pygame.display.flip()

if __name__ == "__main__":
    main()
