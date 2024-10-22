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

    def process_input(self):
        self.clear_previous_inputs()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.rotation = -self.rotation_speed
        if keys[pygame.K_e]:
            self.rotation = self.rotation_speed
        if keys[pygame.K_w]:
            self.movement_vec += Vector2(0.0, -self.max_speed)

    def update(self, delta_time):
        self.update_rotation(delta_time)
        self.update_movement(delta_time)

    def render(self, render_target : SurfaceType | Surface):
        pygame.draw.circle(render_target, self.color, self.position, self.radius, width = 1)
        pygame.draw.polygon(render_target, constants.GREEN, self.get_triangle_vertices())

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
