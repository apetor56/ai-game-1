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
                  velocity: Vector2,
                  max_speed: float,
                  radius: float,
                  color: pygame.Color):
        generated_position = Generator.random_position(game_world.render_target, radius)
        generated_heading_vec = Generator.random_vec2()
        super().__init__(EntityType.eEnemy,
                         generated_position,
                         generated_heading_vec,
                         velocity,
                         radius,
                         constants.DEFAULT_MASS)
        self.game_world = game_world
        self.color = color
        self.steering_behaviours = SteeringBehaviours(self)
        self.max_speed = max_speed

    def update(self, delta_time: float):
        #---Seek
        #steering_force: Vector2 = self.steering_behaviours.seek(self.game_world.player.position)

        #---Flee
        #steering_force: Vector2 = self.steering_behaviours.flee(self.game_world.player.position)

        # ---Arrive
        #target_position = self.game_world.player.position
       # steering_force: Vector2 = self.steering_behaviours.arrive(target_position, constants.Deceleration.SLOW)

        #---Pursuit
        steering_force: Vector2 = self.steering_behaviours.pursuit(self.game_world.player)

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
