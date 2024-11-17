from pygame.math import Vector2

import constants

class Wall:
    def __init__(self, point_a=None, point_b=None, normal=None):
        self.point_a = point_a or Vector2(0, 0)
        self.point_b = point_b or Vector2(0, 0)
        self.normal = normal or self.calculate_normal()
        self.color = constants.GREEN

    def calculate_normal(self):
        direction = self.point_b - self.point_a
        normalized_direction = direction.normalize()
        return Vector2(-normalized_direction.y, normalized_direction.x)

    def from_(self):
        return self.point_a

    def to(self):
        return self.point_b

    def normal(self):
        return self.normal
