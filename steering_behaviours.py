from pygame import Vector2

import constants

class SteeringBehaviours:
    def __init__(self, enemy):
        self.agent = enemy

    def calculate_resultant_force(self):
        return self.seek()

    def seek(self):
        from enemy import Enemy
        if isinstance(self.agent, Enemy):
            FIXED_TARGET = Vector2(400, 300)
            desired_velocity: Vector2 = (FIXED_TARGET - self.agent.position).normalize() * self.agent.max_speed
            return desired_velocity - self.agent.velocity
