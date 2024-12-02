from obstacle import Obstacle
from utils import Utils
import constants

from math import inf
from pygame import Vector2

import random
import math

class SteeringBehaviours:
    def __init__(self, enemy):
        self.agent = enemy
        self.wander_radius = 20
        self.wander_jitter_per_sec = 80
        self.wander_distance = 30
        self.wander_jitter = self.wander_jitter_per_sec
        self.wander_target = Vector2(self.wander_jitter_per_sec, 0)
        self.max_force_length = 1000
        self.min_detection_box_length = 100
        self.box_length = 0
        self.wall_detection_feeler_length = 100
        self.accumulated_steering_force = Vector2()
        self.wander_weight = 3.0
        self.obstacle_avoidance_weight = 20.0
        self.wall_avoidance_weight = 40.0
        self.pursuit_weight = 15.0
        self.hide_weight = 15.0
        self.flock_weight = 1.0
        self.hiding_timer = 0
        self.is_hiding = False
        self.hiding_duration = 7.0
        self.rest_duration = 5.0
        self.time_since_last_switch = 0


    def calculate_steering_force(self):
        self.accumulated_steering_force = Vector2()

        wall_avoidance = self.wall_avoidance(self.agent.game_world.walls) * self.wall_avoidance_weight
        obstacle_avoidance = self.obstacle_avoidance() * self.obstacle_avoidance_weight
        pursuit = Vector2(0, 0)
        hide = self.hide_with_timing(self.agent.game_world.player, self.agent.game_world.obstacles) * self.hide_weight
        flock = self.flock() * self.flock_weight

        min_group_size = 4
        group_radius = 100
        if self.check_group(self.agent.game_world.enemies, self.agent.position, min_group_size, group_radius):
            hide = Vector2(0, 0)
            pursuit = self.pursuit(self.agent.game_world.player) * self.pursuit_weight

        self.accumulate_force(wall_avoidance)
        self.accumulate_force(obstacle_avoidance)
        self.accumulate_force(pursuit)
        self.accumulate_force(hide)
        self.accumulate_force(flock)

        return self.accumulated_steering_force

    def accumulate_force(self, single_force):
        current_force_length = self.accumulated_steering_force.length()
        remaining_length = self.max_force_length - current_force_length

        if remaining_length < 0.0:
            return False

        length_to_add = single_force.length()
        if length_to_add < remaining_length:
            self.accumulated_steering_force += single_force
        elif single_force.length() > constants.ALPHA:
            self.accumulated_steering_force += single_force.normalize() * remaining_length

        return True

    def seek(self, target: Vector2):
        desired_velocity = (target - self.agent.position).normalize() * self.agent.max_speed
        return desired_velocity - self.agent.velocity

    def flee(self, target: Vector2):
        panic_distance_sq = 100.0 * 100.0
        distance_sq = (self.agent.position - target).length_squared()

        if distance_sq > panic_distance_sq:
            return Vector2(0, 0)

        desired_velocity = (self.agent.position - target).normalize() * self.agent.max_speed
        return desired_velocity - self.agent.velocity

    def arrive(self, target: Vector2, deceleration: float):
        to_target = target - self.agent.position
        dist = to_target.length()

        if dist > 0:
            deceleration_tweaker = 0.3
            speed = dist / (deceleration * deceleration_tweaker)
            speed = min(speed, self.agent.max_speed)
            desired_velocity = to_target * (speed / dist)
            return desired_velocity - self.agent.velocity

        return Vector2(0, 0)

    def pursuit(self, evader):
        to_evader = evader.position - self.agent.position
        relative_heading = self.agent.heading_vec.dot(evader.heading_vec)

        if (to_evader.dot(self.agent.heading_vec) > 0) and (relative_heading < -0.95):
            return self.seek(evader.position)

        look_ahead_time = to_evader.length() / (self.agent.max_speed + evader.velocity.length())
        look_ahead_time += self.turn_around_time(evader.position)
        future_position = evader.position + evader.velocity * look_ahead_time
        return self.seek(future_position)

    def turn_around_time(self, target_pos: Vector2) -> float:
        to_target = (target_pos - self.agent.position).normalize()
        dot = self.agent.heading_vec.dot(to_target)
        coefficient = 0.1
        return (dot - 1.0) * -coefficient

    def evade(self, pursuer):
        to_pursuer = pursuer.position - self.agent.position
        look_ahead_time = to_pursuer.length() / (self.agent.max_speed + pursuer.velocity.length())
        future_position = pursuer.position + pursuer.velocity * look_ahead_time
        return self.flee(future_position)

    def wander(self):
        jitter_this_time_slice = self.wander_jitter * self.agent.delta_time
        self.wander_target += Vector2(random.uniform(-1, 1) * jitter_this_time_slice,
                                      random.uniform(-1, 1) * jitter_this_time_slice)
        self.wander_target = self.wander_target.normalize() * self.wander_radius
        target_local = self.wander_target + Vector2(self.wander_distance, 0)
        target_world = Utils.point_to_world_space(target_local,
                                                 self.agent.heading_vec,
                                                 self.agent.side_vec,
                                                 self.agent.position)
        return target_world - self.agent.position

    def obstacle_avoidance(self):
        self.box_length = self.min_detection_box_length + (self.agent.velocity.length() / self.agent.max_speed) * self.min_detection_box_length
        self.agent.game_world.tag_obstacles_within_view_range(self.agent, self.box_length)

        closest_intersecting_obstacle = None
        distance_to_closest_intersection_point = float('inf')
        closest_obstacle_local_position = Vector2()

        for obstacle in self.agent.game_world.obstacles:
            if obstacle.in_range_tag:
                local_pos = Utils.point_to_local_space(obstacle.position, self.agent.heading_vec, self.agent.side_vec,
                                                       self.agent.position)
                if local_pos.x >= 0:
                    expanded_radius = obstacle.radius + self.agent.radius
                    if abs(local_pos.y) < expanded_radius:
                        x = local_pos.x
                        y = local_pos.y
                        sqrt_part = math.sqrt(expanded_radius ** 2 - y ** 2)
                        intersection_point_x = x - sqrt_part
                        if intersection_point_x <= 0:
                            intersection_point_x = x + sqrt_part

                        if intersection_point_x < distance_to_closest_intersection_point:
                            distance_to_closest_intersection_point = intersection_point_x
                            closest_intersecting_obstacle = obstacle
                            closest_obstacle_local_position = local_pos


        if isinstance(closest_intersecting_obstacle, Obstacle):
            steering_force = Vector2()

            multiplier = 1.0 + (self.box_length - closest_obstacle_local_position.x) / self.box_length
            steering_force.y = (closest_intersecting_obstacle.radius - closest_obstacle_local_position.y) * multiplier

            braking_weight = 0.2
            steering_force.x = (closest_intersecting_obstacle.radius - closest_obstacle_local_position.x) * braking_weight

            return -Utils.vector_to_world_space(steering_force, self.agent.heading_vec, self.agent.side_vec)

        return Vector2(0, 0)

    def wall_avoidance(self, walls):
        self.agent.create_feelers()
        dist_to_closest_ip = float('inf')
        closest_wall = -1
        steering_force = Vector2(0, 0)
        closest_point = Vector2(0, 0)

        for feeler in self.agent.feelers:
            for wall_id, wall in enumerate(walls):
                intersects, point, dist = Utils.line_intersection_2d(self.agent.position, feeler,
                                                                     wall.from_(), wall.to())

                if intersects and dist < dist_to_closest_ip:
                    dist_to_closest_ip = dist
                    closest_wall = wall_id
                    closest_point = point

            if closest_wall >= 0:
                overshoot = feeler - closest_point
                steering_force = walls[closest_wall].normal * overshoot.length()
                walls[closest_wall].color = constants.RED

        return steering_force

    @staticmethod
    def get_hiding_position(pos_ob: Vector2, radius_ob: float, pos_target: Vector2) -> Vector2:
        distance_from_boundary = 30.0
        dist_away = radius_ob + distance_from_boundary

        to_ob = (pos_ob - pos_target).normalize()
        hiding_position = to_ob * dist_away + pos_ob
        return hiding_position

    def hide(self, target, obstacles):
        to_enemy_from_player = self.agent.position - target.position
        is_in_player_fov = target.heading_vec.dot(to_enemy_from_player.normalize()) > 0.5  # cos(45 degrees)
        if is_in_player_fov:
            dist_to_closest = inf
            best_hiding_spot = None

            for obstacle in obstacles:
                hiding_spot = self.get_hiding_position(obstacle.position, obstacle.radius,
                                                       target.position)

                dist = (hiding_spot - self.agent.position).length_squared()

                if dist < dist_to_closest:
                    dist_to_closest = dist
                    best_hiding_spot = hiding_spot

            if best_hiding_spot is None:
                return self.evade(target)

            return self.arrive(best_hiding_spot,
                               deceleration=1.0)
        return Vector2()

    def hide_with_timing(self, target, obstacles):
        self.time_since_last_switch += self.agent.delta_time

        if self.is_hiding:
            if self.time_since_last_switch >= self.hiding_duration:
                self.is_hiding = False
                self.time_since_last_switch = 0
            else:
                return self.hide(target, obstacles)

        else:
            if self.time_since_last_switch >= self.rest_duration:
                self.is_hiding = True
                self.time_since_last_switch = 0
            else:
                return Vector2(0, 0)

        return Vector2(0, 0)

    # Flocking
    def separation(self, neighbors):
        separation_force = Vector2(0, 0)
        neighbor_count = 0

        for neighbor in neighbors:
            if neighbor != self.agent and neighbor.tag:
                difference = self.agent.position - neighbor.position
                if difference.length() > 0:
                    separation_force += difference.normalize() / difference.length()
                    neighbor_count += 1

        if neighbor_count > 0:
            separation_force /= neighbor_count

        return separation_force

    def alignment(self, neighbors):
        average_heading = Vector2(0, 0)
        neighbor_count = 0

        for neighbor in neighbors:
            if neighbor != self.agent and neighbor.tag:
                average_heading += neighbor.heading_vec
                neighbor_count += 1

        if neighbor_count > 0:
            average_heading /= neighbor_count
            alignment_force = average_heading - self.agent.heading_vec
            return alignment_force

        return Vector2(0, 0)

    def cohesion(self, neighbors):
        center_of_mass = Vector2(0, 0)
        neighbor_count = 0

        for neighbor in neighbors:
            if neighbor != self.agent and neighbor.tag:
                center_of_mass += neighbor.position
                neighbor_count += 1

        if neighbor_count > 0:
            center_of_mass /= neighbor_count
            cohesion_force = center_of_mass - self.agent.position
            return cohesion_force

        return Vector2(0, 0)

    def flock(self):
        self.agent.tag_neighbors(radius = constants.FLOCKING_RADIUS)

        alignment_force = self.alignment(self.agent.game_world.enemies)
        separation_force = self.separation(self.agent.game_world.enemies)
        cohesion_force = self.cohesion(self.agent.game_world.enemies)
        wander_force = self.wander()

        flocking_force = (
                alignment_force * 16.0 +
                separation_force * 1.0 +
                cohesion_force * 1.0 +
                wander_force * 1.0
        )

        return flocking_force

    def check_group(self, enemies, position, desired_number, radius: float = constants.FLOCKING_RADIUS) -> bool:

        count = 0
        for other_entity in enemies:
            if other_entity == self:
                continue

            distance = position.distance_to(other_entity.position)

            if distance <= radius:
                count += 1

        return count >= desired_number

