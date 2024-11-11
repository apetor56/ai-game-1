from pygame import Vector2
import random

import constants

class SteeringBehaviours:
    def __init__(self, enemy):
        self.agent = enemy
        self.wander_radius = 20
        self.wander_distance = 30
        self.wander_jitter = 1
        self.wander_target = Vector2(self.wander_radius, 0)
        self.wander_weight = 1.0
        self.obstacle_avoidance_weight = 0.1
        self.wall_avoidance_weight = 0.2
        self.max_force = 1500.0

    def calculate_steering_force(self):
        from enemy import Enemy
        self.reset_weights()

        avoid_obstacle = self.avoid_obstacles(self.agent.game_world.obstacles) if isinstance(self.agent,
                                                                                             Enemy) else Vector2(0, 0)
        wander = self.wander()
        avoid_wall = self.avoid_walls() * self.wall_avoidance_weight

        steering_force = (wander * self.wander_weight +
                          avoid_obstacle * self.obstacle_avoidance_weight +
                          avoid_wall * self.wall_avoidance_weight)

        if steering_force.length() > self.max_force:
            steering_force.scale_to_length(self.max_force)

        return steering_force

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

        if (to_evader.dot(self.agent.heading_vec) > 0) and (relative_heading < -0.95):  # acos(0.95) ~ 18 degrees
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
        self.wander_target += Vector2(random.uniform(-1, 1) * self.wander_jitter,
                                      random.uniform(-1, 1) * self.wander_jitter)
        self.wander_target = self.wander_target.normalize() * self.wander_radius
        target_local = self.wander_target + Vector2(self.wander_distance, 0)
        target_world = self.point_to_world_space(target_local,
                                                 self.agent.heading_vec,
                                                 self.agent.side_vec,
                                                 self.agent.position)
        return target_world - self.agent.position

    def point_to_world_space(self, local_point: Vector2, heading: Vector2, side: Vector2, position: Vector2) -> Vector2:
        transformed_point = Vector2()
        transformed_point.x = (local_point.x * heading.x) + (local_point.y * side.x) + position.x
        transformed_point.y = (local_point.x * heading.y) + (local_point.y * side.y) + position.y
        return transformed_point

    def avoid_obstacles(self, obstacles, detection_range = 150):
        from enemy import Enemy
        avoidance_force = Vector2(0, 0)

        if isinstance(self.agent, Enemy):
            for obstacle in obstacles:
                distance = self.agent.position.distance_to(obstacle.position)

                if distance < detection_range + obstacle.radius:
                    self.obstacle_avoidance_weight = 3.5
                    away_from_obstacle = (self.agent.position - obstacle.position).normalize()

                    strength = (detection_range + obstacle.radius - distance) / detection_range
                    avoidance_force += away_from_obstacle * strength * self.agent.max_speed

            return avoidance_force

    def avoid_walls(self, detection_range = 50):
        avoidance_force = Vector2(0, 0)

        left_distance = self.agent.position.x
        right_distance = constants.WINDOW_RESOLUTION[0] - self.agent.position.x
        top_distance = self.agent.position.y
        bottom_distance = constants.WINDOW_RESOLUTION[1] - self.agent.position.y

        if left_distance < detection_range:
            avoidance_force.x += (detection_range - left_distance)
        if right_distance < detection_range:
            avoidance_force.x -= (detection_range - right_distance)
        if top_distance < detection_range:
            avoidance_force.y += (detection_range - top_distance)
        if bottom_distance < detection_range:
            avoidance_force.y -= (detection_range - bottom_distance)

        if avoidance_force.length() > 0:
            self.wall_avoidance_weight = 9.0
            from enemy import Enemy
            avoidance_force = avoidance_force.normalize() * self.agent.max_speed

        return avoidance_force

    def reset_weights(self):
        self.wander_weight = 1.0
        self.obstacle_avoidance_weight = 0.05
        self.wall_avoidance_weight = 0.05
