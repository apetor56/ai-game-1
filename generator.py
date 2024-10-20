from pygame import SurfaceType, Vector2

import random

class Generator:
    @staticmethod
    def random_position(render_target: SurfaceType, radius: float):
        width, height = render_target.get_size()
        x: float = random.uniform(radius, width - radius)
        y: float = random.uniform(radius, height - radius)
        return Vector2(x, y)

    @staticmethod
    def random_vec2():
        x: float = random.uniform(-1, 1)
        y: float = random.uniform(-1, 1)
        return Vector2(x, y).normalize()
