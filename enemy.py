import time
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
        target = self.game_world.player
        obstacles = self.game_world.obstacles


        #---Seek
        #steering_force: Vector2 = self.steering_behaviours.seek(self.game_world.player.position)

        #---Flee
        #steering_force: Vector2 = self.steering_behaviours.flee(self.game_world.player.position)

        # ---Arrive
        #target_position = self.game_world.player.position
       # steering_force: Vector2 = self.steering_behaviours.arrive(target_position, constants.Deceleration.SLOW)

        #---Pursuit
        #steering_force: Vector2 = self.steering_behaviours.pursuit(self.game_world.player)

        #---Evade
        #steering_force: Vector2 = self.steering_behaviours.evade(self.game_world.player)

        # ---Wander


        self.position += self.velocity * delta_time



        #Hide
        to_enemy_from_player = self.position - target.position
        is_in_player_fov = target.heading_vec.dot(to_enemy_from_player.normalize()) > 0.5  # cos(45 degrees)

        should_hide = is_in_player_fov



        self.tag_neighbors(radius=constants.FLOCKING_RADIUS)

        # Calculate flocking forces
        alignment_force = self.steering_behaviours.alignment(self.game_world.enemies)
        separation_force = self.steering_behaviours.separation(self.game_world.enemies)
        cohesion_force = self.steering_behaviours.cohesion(self.game_world.enemies)
        wander_force = self.steering_behaviours.wander()

        flocking_force = (
                alignment_force * 16.0 +
                separation_force * 1.0 +
                cohesion_force * 1.0 +
                wander_force * 1.0
        )

        if self.steering_behaviours.check_group(self.game_world.enemies, self.position,8,  30):
            print("Grupa przeciwników jest wystarczająco duża")
           # steering_force: Vector2 = self.steering_behaviours.seek(self.game_world.player.position)
            #steering_force: Vector2 = self.steering_behaviours.pursuit(self.game_world.player)
            steering_force: Vector2 = flocking_force
            pass


        elif should_hide:
            steering_force = self.steering_behaviours.hide(target, obstacles)
        else:
            #steering_force: Vector2 = self.steering_behaviours.wander()
            steering_force: Vector2 =  flocking_force

        acceleration: Vector2 = steering_force / self.mass

        self.velocity += acceleration * delta_time
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if self.velocity.length() > constants.ALPHA:
            self.heading_vec = self.velocity.normalize()
            self.side_vec = self.heading_vec.rotate(constants.CLOCKWISE_ROTATION)

    def tag_neighbors(self, radius: float):
        for other_entity in self.game_world.enemies + [self.game_world.player]:  # Include all enemies and the player
            # First, untag each entity
            other_entity.untag()
            if other_entity == self:
             continue


    def render(self, render_target : SurfaceType | Surface):
        #enemy
       pygame.draw.circle(render_target, self.color, self.position, self.radius)


        # circle of Wander
       # wander_center = self.position + self.heading_vec * self.steering_behaviours.wander_distance


       # pygame.draw.circle(render_target, (0, 255, 0), (int(wander_center.x),
        #                                                            int(wander_center.y)),
         #                                                           int(self.steering_behaviours.wander_radius), 1)

       # wander_target_world = self.steering_behaviours.point_to_world_space(self.steering_behaviours.wander_target,
                                                                        #    self.heading_vec,
                                                                         #   self.side_vec,
                                                                          #  wander_center)

       # pygame.draw.circle(render_target, (255, 255, 255), (int(wander_target_world.x), int(wander_target_world.y)), 5)