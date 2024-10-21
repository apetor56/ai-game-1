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

        # Return a zero vector if the distance is zero (i.e., we are at the target)
        return Vector2(0, 0)