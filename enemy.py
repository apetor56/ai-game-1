import time
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
        self.feelers = []
        self.feeler_length = 50

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

        # # Hide
        # to_enemy_from_player = self.position - target.position
        # is_in_player_fov = target.heading_vec.dot(to_enemy_from_player.normalize()) > 0.5  # cos(45 degrees)
        #
        # should_hide = is_in_player_fov
        #
        # self.tag_neighbors(radius=constants.FLOCKING_RADIUS)
        #
        # # Calculate flocking forces
        # alignment_force = self.steering_behaviours.alignment(self.game_world.enemies)
        # separation_force = self.steering_behaviours.separation(self.game_world.enemies)
        # cohesion_force = self.steering_behaviours.cohesion(self.game_world.enemies)
        # wander_force = self.steering_behaviours.wander()
        #
        # flocking_force = (
        #         alignment_force * 6.0 +
        #         separation_force * 1.0 +
        #         cohesion_force * 2.0 +
        #         wander_force * 5.0
        # )
        #
        # if should_hide:
        #     steering_force = self.steering_behaviours.hide(target, obstacles)
        # else:
        #     # steering_force: Vector2 = self.steering_behaviours.wander()
        #     steering_force: Vector2 = flocking_force

    def tag_neighbors(self, radius: float):
        for other_entity in self.game_world.enemies + [self.game_world.player]:  # Include all enemies and the player
            # First, untag each entity
            other_entity.untag()
            if other_entity == self:
             continue

    def render(self, render_target : SurfaceType | Surface):
        pygame.draw.circle(render_target, self.color, self.get_render_position(), self.radius)

    def create_feelers(self):
        fixed_position = self.get_render_position()
        fixed_heading_vec = Vector2(self.heading_vec.x, -self.heading_vec.y)

        front = fixed_position + self.feeler_length * fixed_heading_vec

        left_local = Utils.point_to_local_space(front, self.heading_vec, self.side_vec, fixed_position)
        left_local.rotate_ip(-30)
        left_local.scale_to_length(self.feeler_length / 1.5)
        left = Utils.point_to_world_space(left_local, self.heading_vec, self.side_vec, fixed_position)

        right_local = Utils.point_to_local_space(front, self.heading_vec, self.side_vec, fixed_position)
        right_local.rotate_ip(30)
        right_local.scale_to_length(self.feeler_length / 1.5)
        right = Utils.point_to_world_space(right_local, self.heading_vec, self.side_vec, fixed_position)

        self.feelers = [front, left, right]
