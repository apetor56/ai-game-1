import constants

from pygame import Surface, SurfaceType, Vector2
from obstacle import Obstacle
from wall import Wall

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
        self.walls = []
        self.generate_obstacles()
        self.create_walls()

    def generate_obstacles(self):

        obstacle_positions = [
            Vector2(400, 300),
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

        self.handle_entity_collisions()

    def render(self, render_target: Surface | SurfaceType):
        self.player.render(render_target)
        for enemy in self.enemies:
            enemy.render(render_target)
        for obstacle in self.obstacles:
            obstacle.render(render_target)

    @staticmethod
    def handle_wall_collisions(entity):
        screen_width, screen_height = constants.WINDOW_RESOLUTION

        if entity.position.x - entity.radius < 0:
            entity.position.x = entity.radius
            entity.velocity.x *= -1
        elif entity.position.x + entity.radius > screen_width:
            entity.position.x = screen_width - entity.radius
            entity.velocity.x *= -1

        if entity.position.y - entity.radius < 0:
            entity.position.y = entity.radius
            entity.velocity.y *= -1
        elif entity.position.y + entity.radius > screen_height:
            entity.position.y = screen_height - entity.radius
            entity.velocity.y *= -1

    def handle_entity_collisions(self):
        for obstacle in self.obstacles:
            self.handle_circle_collision(self.player, obstacle, stationary=True)

        for enemy in self.enemies:
            self.handle_circle_collision(self.player, enemy)

        for enemy in self.enemies:
            for obstacle in self.obstacles:
                self.handle_circle_collision(enemy, obstacle, stationary=True)

        for i in range(len(self.enemies)):
            for j in range(i + 1, len(self.enemies)):
                self.handle_circle_collision(self.enemies[i], self.enemies[j])

    def handle_circle_collision(self, entity1, entity2, stationary=False):
        entity2_position = entity2.get_render_position() if stationary == False else entity2.position
        distance = entity1.get_render_position().distance_to(entity2_position)
        min_distance = entity1.radius + entity2.radius

        if distance < min_distance:
            overlap = min_distance - distance
            collision_normal = (entity2_position - entity1.get_render_position()).normalize()
            fixed_collision_normal = Vector2(collision_normal.x, -collision_normal.y)
            if stationary:
                entity1.position -= fixed_collision_normal * overlap
            else:
                entity1.position -= fixed_collision_normal * (overlap / 2)
                entity2.position += fixed_collision_normal * (overlap / 2)

            if not stationary and hasattr(entity1, 'velocity') and hasattr(entity2, 'velocity'):
                self.resolve_velocity(entity1, entity2, fixed_collision_normal)
            elif stationary and hasattr(entity1, 'velocity'):
                self.resolve_velocity_against_stationary(entity1, fixed_collision_normal)

    @staticmethod
    def resolve_velocity(entity1, entity2, collision_normal):
        relative_velocity = entity1.velocity - entity2.velocity
        velocity_along_normal = relative_velocity.dot(collision_normal)

        if velocity_along_normal > 0:
            return

        restitution = constants.RESTITUTION_COEFFICIENT

        impulse_magnitude = -(1 + restitution) * velocity_along_normal
        impulse_magnitude /= (1 / entity1.mass) + (1 / entity2.mass)

        impulse = impulse_magnitude * collision_normal
        entity1.velocity += impulse / entity1.mass
        entity2.velocity -= impulse / entity2.mass

    @staticmethod
    def resolve_velocity_against_stationary(entity, collision_normal):
        velocity_along_normal = entity.velocity.dot(collision_normal)

        if velocity_along_normal > 0:
            return

        restitution = constants.RESTITUTION_COEFFICIENT
        entity.velocity -= (1 + restitution) * velocity_along_normal * collision_normal

    def tag_obstacles_within_view_range(self, enemy, box_length):
        for obstacle in self.obstacles:
            if box_length + obstacle.radius < (enemy.position - obstacle.get_render_position()).length():
                obstacle.in_range_tag = False
            else:
                obstacle.in_range_tag = True


    def create_walls(self):
        window_width = constants.WINDOW_RESOLUTION[0]
        window_height = constants.WINDOW_RESOLUTION[1]

        border_size = 20.0
        corner_size = 0.1
        v_dist = window_height - 2 * border_size
        h_dist = window_width - 2 * border_size

        wall_vertices = [
            Vector2(h_dist * corner_size + border_size, border_size),
            Vector2(window_width - border_size - h_dist * corner_size, border_size),
            Vector2(window_width - border_size, border_size + v_dist * corner_size),
            Vector2(window_width - border_size, window_height - border_size - v_dist * corner_size),
            Vector2(window_width - border_size - h_dist * corner_size, window_height - border_size),
            Vector2(h_dist * corner_size + border_size, window_height - border_size),
            Vector2(border_size, window_height - border_size - v_dist * corner_size),
            Vector2(border_size, border_size + v_dist * corner_size),
        ]

        for i in range(len(wall_vertices) - 1):
            self.walls.append(Wall(wall_vertices[i], wall_vertices[i + 1]))

        self.walls.append(Wall(wall_vertices[-1], wall_vertices[0]))
