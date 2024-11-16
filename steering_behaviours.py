from math import inf
from pygame import Vector2
import random

class SteeringBehaviours:
    def __init__(self, enemy):
        self.agent = enemy
        self.wander_radius = 20
        self.wander_distance = 30
        self.wander_jitter = 1
        self.wander_target = Vector2(self.wander_radius, 0)

    def calculate_resultant_force(self):
        pass

    def seek(self, target: Vector2):
        from enemy import Enemy
        if isinstance(self.agent, Enemy):
            desired_velocity: Vector2 = ( target - self.agent.position).normalize() * self.agent.max_speed
            return desired_velocity - self.agent.velocity

    def flee(self, target: Vector2):
        from enemy import Enemy
        if isinstance(self.agent, Enemy):

            # Only flee if the target is within 'panic distance'.
            panic_distance_sq = 100.0 * 100.0
            distance_sq = (self.agent.position - target).length_squared()

            if distance_sq > panic_distance_sq:
                return Vector2(0, 0)  # No force if the target is too far away

            desired_velocity: Vector2 = (self.agent.position - target).normalize() * self.agent.max_speed
            return desired_velocity - self.agent.velocity

    def arrive(self, target: Vector2, deceleration: float):
        # Calculate the vector to the target
        to_target = target - self.agent.position

        # Calculate the distance to the target
        dist = to_target.length()

        if dist > 0:
            # Deceleration Tweaker is used to tweak the deceleration rate
            deceleration_tweaker = 0.3

            speed = dist / (deceleration * deceleration_tweaker)
            speed = min(speed, self.agent.max_speed)
            desired_velocity = to_target * (speed / dist)

            return desired_velocity - self.agent.velocity

        # Return a zero vector if the distance is zero (we are at the target)
        return Vector2(0, 0)

    def pursuit(self, evader):
        # Pursuit behavior for chasing a moving target
        to_evader = evader.position - self.agent.position
        relative_heading = self.agent.heading_vec.dot(evader.heading_vec)

        # If the evader is ahead and facing the pursuer, directly seek its current position
        if (to_evader.dot(self.agent.heading_vec) > 0) and (relative_heading < -0.95):  # acos(0.95) ~ 18 degrees
            return self.seek(evader.position)

        # Predict where the evader will be in the future and pursue that predicted position
        look_ahead_time = to_evader.length() / (self.agent.max_speed + evader.velocity.length())
        look_ahead_time += self.turn_around_time(evader.position)
        future_position = evader.position + evader.velocity * look_ahead_time
        return self.seek(future_position)

    def turn_around_time(self, target_pos: Vector2) -> float:
        """
        Calculates the time required for the agent to turn around to face the target.
        This is based on the dot product between the agent's heading and the target's direction.
        """
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

        # Convert local target to world space using agent's heading
        target_world = self.point_to_world_space(target_local,
                                                 self.agent.heading_vec,
                                                 self.agent.side_vec,
                                                 self.agent.position)

        # Return the steering force towards the wander target
        return target_world - self.agent.position

    def point_to_world_space(self, local_point: Vector2, heading: Vector2, side: Vector2, position: Vector2) -> Vector2:
        # Transform the local point to world space (apply rotation and translation)
        transformed_point = Vector2()
        transformed_point.x = (local_point.x * heading.x) + (local_point.y * side.x) + position.x
        transformed_point.y = (local_point.x * heading.y) + (local_point.y * side.y) + position.y
        return transformed_point



#Hiding
    def get_hiding_position(self, pos_ob: Vector2, radius_ob: float, pos_target: Vector2) -> Vector2:
        distance_from_boundary = 30.0
        dist_away = radius_ob + distance_from_boundary

        to_ob = (pos_ob - pos_target).normalize()
        hiding_position = to_ob * dist_away + pos_ob
        return hiding_position

    def hide(self, target, obstacles):
        dist_to_closest = inf
        best_hiding_spot = None

        for obstacle in obstacles:
            hiding_spot = self.get_hiding_position(obstacle.position, obstacle.radius, target.position)

            dist = (hiding_spot - self.agent.position).length_squared()

            if dist < dist_to_closest:
                dist_to_closest = dist
                best_hiding_spot = hiding_spot

        if best_hiding_spot is None:
            return self.evade(target)

        return self.arrive(best_hiding_spot,
                           deceleration=1.0)


#Flocking

