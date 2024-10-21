import constants

from pygame import Surface, SurfaceType

class GameWorld:
    def __init__(self,
                 render_target : SurfaceType):
        self.render_target = render_target

        from enemy import Enemy
        self.enemies = []
        for _ in range(constants.ENEMIES_COUNT):
            self.enemies.append(Enemy(self,
                                      constants.DEFAULT_ENEMY_VELOCITY,
                                      constants.DEFAULT_ENEMY_MAX_SPEED,
                                      constants.DEFAULT_ENEMY_RADIUS,
                                      constants.RED))
        from player import Player
        self.player = Player(self,
                             constants.DEFAULT_PLAYER_VELOCITY,
                             constants.DEFAULT_PLAYER_MAX_SPEED,
                             constants.DEFAULT_PLAYER_RADIUS,
                             constants.GREEN)

    def process_input(self):
        self.player.process_input()

    def update(self, delta_time: float):
        self.player.update(delta_time)
        self.wrap_around_screen(self.player)
        for enemy in self.enemies:
            enemy.update(delta_time)
            self.wrap_around_screen(enemy)

    def render(self, render_target: Surface | SurfaceType):
        self.player.render(render_target)
        for enemy in self.enemies:
            enemy.render(render_target)

    def wrap_around_screen(self, entity):
        """Wraps the entity around the screen when it moves beyond the boundaries."""
        screen_width, screen_height = constants.WINDOW_RESOLUTION

        # Wrap horizontally
        if entity.position.x < 0:
            entity.position.x = screen_width
        elif entity.position.x > screen_width:
            entity.position.x = 0

        # Wrap vertically
        if entity.position.y < 0:
            entity.position.y = screen_height
        elif entity.position.y > screen_height:
            entity.position.y = 0
