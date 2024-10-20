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
