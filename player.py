from operator import truth

from game_world import GameWorld
from moving_entity import MovingEntity
from base_game_entity import EntityType
from steering_behaviours import SteeringBehaviours
from generator import Generator
import constants

import pygame
from pygame import Vector2, SurfaceType, Surface


class Player(MovingEntity):
    def __init__(self,
                 game_world: GameWorld,
                 velocity: Vector2,
                 max_speed: float,
                 radius: float,
                 color: pygame.Color):
        generated_position = Generator.random_position(game_world.render_target, radius)
        super().__init__(EntityType.ePlayer,
                         generated_position,
                         velocity,
                         constants.DEFAULT_PLAYER_HEADING_VEC,
                         radius,
                         constants.DEFAULT_MASS)
        self.game_world = game_world
        self.color = color
        self.steering_behaviours = SteeringBehaviours(self)
        self.max_speed = max_speed
        #self.vertices = self.get_triangle_vertices()
        self.rotation = 0.0
        self.rotation_speed = 180.0
        self.movement_vec = Vector2(0.0, 0.0)
        self.front = Vector2(0.0, -self.radius)

        self.shoot_cooldown = 0  # Cooldown timer in seconds
        self.shooting = False
        self.shot_end = None

    def process_input(self):
        self.clear_previous_inputs()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.rotation = -self.rotation_speed
        if keys[pygame.K_e]:
            self.rotation = self.rotation_speed
        if keys[pygame.K_w]:
            self.movement_vec += Vector2(0.0, -self.max_speed)
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shooting = True
            self.shoot()
            self.shoot_cooldown = 0.5  # Cooldown of 0.5 seconds
        else:
            self.shooting = False

    def shoot(self):
        shot_start = self.position
        shot_direction = self.heading_vec.normalize()  # Ensure the direction is normalized
        max_shot_length = 800  # Max shot range
        shot_end = shot_start + shot_direction * max_shot_length

        # Check for obstacle blocks
        blocked, intersection_point = self.steering_behaviours.is_shot_blocked(shot_start, shot_direction,self.game_world.obstacles)
        if blocked:
            shot_end = intersection_point
        else:
            blocked, intersection_point = self.steering_behaviours.is_shot_blocked(shot_start, shot_direction,
                                                                                   self.game_world.enemies)
            if blocked:
                shot_end = intersection_point
                print("enemy shot")
                for enemy in self.game_world.enemies:
                    # Upewnij się, że enemy.position i intersection_point to obiekty Vector2
                    # To jest dlatego bo z jakiegos powodu czasem ich nie widzi i crashuje
                    if isinstance(enemy.position, Vector2) and isinstance(intersection_point, Vector2):
                        if enemy.position.distance_to(intersection_point) <= enemy.radius:
                            print(f"Enemy at {enemy.position} killed!")
                            self.game_world.enemies.remove(enemy)
                            break
                    else:
                        print(f"Warning: Invalid position type for enemy or intersection point.")


        self.shot_end = shot_end# Save the shot end point for rendering

    def update(self, delta_time):
        self.update_rotation(delta_time)
        self.update_movement(delta_time)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= delta_time

    def render(self, render_target : SurfaceType | Surface):
        pygame.draw.circle(render_target, self.color, self.position, self.radius, width = 1)
        pygame.draw.polygon(render_target, constants.GREEN, self.get_triangle_vertices())

        if self.shooting and self.shot_end:
            pygame.draw.line(render_target, constants.GREEN, self.position, self.shot_end, width=1)

    def update_rotation(self, delta_time: float):
        if self.rotation != 0:
            self.heading_vec = self.heading_vec.rotate(self.rotation * delta_time).normalize()
            translated_vertex = self.front

            rotated_vertex = translated_vertex.rotate(self.rotation * delta_time)
            self.front = rotated_vertex

    def update_movement(self, delta_time: float):
        if self.movement_vec != Vector2(0.0, 0.0):
            self.velocity = self.heading_vec * self.velocity.length()
            self.movement_vec = self.heading_vec * self.movement_vec.length()
            self.velocity += self.movement_vec * delta_time

            if self.velocity.length() > constants.DEFAULT_PLAYER_MAX_SPEED:
                self.velocity.scale_to_length(constants.DEFAULT_PLAYER_MAX_SPEED)

            self.position += self.velocity * delta_time
            self.vertices = self.get_triangle_vertices()

    def clear_previous_inputs(self):
        self.rotation = 0.0
        self.movement_vec = Vector2(0.0, 0.0)

    def get_triangle_vertices(self):
        left = self.front.rotate(120)
        right = self.front.rotate(240)

        return [self.front + self.position, left + self.position, right + self.position]
