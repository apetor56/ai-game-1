import constants

from pygame import Surface, SurfaceType, Vector2
from Obstacle import Obstacle

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

        self.obstacles = []
        self.generate_obstacles()

    def generate_obstacles(self):

        obstacle_positions = [
            Vector2(200, 150),
            Vector2(600, 150),
            Vector2(600, 450)
        ]
        for pos in obstacle_positions:
            self.obstacles.append(Obstacle(pos, radius=60, color=constants.GRAY))

    def process_input(self):
        self.player.process_input()

    def update(self, delta_time: float):
        self.player.update(delta_time)
        self.handle_wall_collisions(self.player)
        for enemy in self.enemies:
            enemy.update(delta_time)
            self.handle_wall_collisions(enemy)

    def render(self, render_target: Surface | SurfaceType):
        self.player.render(render_target)
        for enemy in self.enemies:
            enemy.render(render_target)
        for obstacle in self.obstacles:
            obstacle.render(render_target)

    def handle_wall_collisions(self, entity):
        """Handles wall collisions by bouncing the entity off the screen edges."""
        screen_width, screen_height = constants.WINDOW_RESOLUTION

        # Check for collisions with the left and right walls
        if entity.position.x - entity.radius < 0:
            entity.position.x = entity.radius  # Correct position
            entity.velocity.x *= -1  # Invert velocity (bounce off wall)
        elif entity.position.x + entity.radius > screen_width:
            entity.position.x = screen_width - entity.radius
            entity.velocity.x *= -1

        # Check for collisions with the top and bottom walls
        if entity.position.y - entity.radius < 0:
            entity.position.y = entity.radius
            entity.velocity.y *= -1
        elif entity.position.y + entity.radius > screen_height:
            entity.position.y = screen_height - entity.radius
            entity.velocity.y *= -1
