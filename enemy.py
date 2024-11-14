from game_world import GameWorld
from moving_entity import MovingEntity
from base_game_entity import EntityType
from steering_behaviours import SteeringBehaviours
from generator import Generator
from utils import Utils
import constants

import pygame
from pygame import Vector2, SurfaceType, Surface

class Enemy(MovingEntity):
    def __init__( self,
                  game_world: GameWorld,
                  velocity: Vector2,
                  max_speed: float,
                  radius: float,
                  color: pygame.Color):
        generated_position = Generator.random_position(game_world.render_target, radius)
        super().__init__(EntityType.eEnemy,
                         generated_position,
                         Vector2(1, 1),
                         velocity,
                         radius,
                         constants.DEFAULT_MASS)
        self.game_world = game_world
        self.color = color
        self.steering_behaviours = SteeringBehaviours(self)
        self.max_speed = max_speed
        self.delta_time = 0.0

    def update(self, delta_time):
        self.delta_time = delta_time
        steering_force: Vector2 = self.steering_behaviours.calculate_steering_force()
        acceleration: Vector2 = steering_force / self.mass

        self.velocity += acceleration * delta_time
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if self.velocity.length() > constants.ALPHA:
            self.heading_vec = self.velocity.normalize()
            self.side_vec = self.heading_vec.rotate(constants.COUNTERCLOCKWISE_ROTATION)

        self.position += self.velocity * delta_time

    def render(self, render_target : SurfaceType | Surface):
        pygame.draw.circle(render_target, self.color, self.get_render_position(), self.radius)
