from game_world import GameWorld

import pygame

WINDOW_RESOLUTION = (800.0, 600.0)
BLACK_CLEAR_COLOR = (0, 0, 0)

def main():
    pygame.init()
    render_target = pygame.display.set_mode(WINDOW_RESOLUTION)
    clock = pygame.time.Clock()
    game_world = GameWorld(render_target)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_target.fill(BLACK_CLEAR_COLOR)

        delta_time = clock.tick(60) / 1000
        game_world.update(delta_time)
        game_world.render(render_target)

        pygame.display.flip()

if __name__ == "__main__":
    main()
