from game_world import GameWorld
from moving_entity import MovingEntity
from base_game_entity import EntityType
from steering_behaviours import SteeringBehaviours
from generator import Generator
import constants

import pygame
from pygame import Vector2, SurfaceType, Surface

class Enemy(MovingEntity):
    def __init__( self,
                  game_world: GameWorld,
                  radius: int = constants.DEFAULT_RADIUS,
                  color: pygame.Color = constants.RED,
                  max_speed: int = constants.DEFAULT_MAX_SPEED):
        generated_position = Generator.random_position(game_world.render_target, radius)
        generated_heading_vec = Generator.random_vec2()
        super().__init__(EntityType.eEnemy,
                         generated_position,
                         generated_heading_vec,
                         constants.DEFAULT_VELOCITY,
                         constants.DEFAULT_MASS,
                         radius)
        self.game_world = game_world
        self.color = color
        self.steering_behaviours = SteeringBehaviours(self)
        self.max_speed = max_speed

    def update(self, delta_time: float):
        steering_force: Vector2 = self.steering_behaviours.calculate_resultant_force()
        acceleration: Vector2 = steering_force / self.mass

        self.velocity += acceleration * delta_time
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if self.velocity.length() > constants.ALPHA:
            self.heading_vec = self.velocity.normalize()
            self.side_vec = self.heading_vec.rotate(constants.CLOCKWISE_ROTATION)

        self.position += self.velocity * delta_time

    def render(self, render_target : SurfaceType | Surface):
        pygame.draw.circle(render_target, self.color, self.position, self.radius)
