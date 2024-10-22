from pygame import Vector2

class SteeringBehaviours:
    def __init__(self, enemy):
        self.agent = enemy

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