import constants

from pygame import Surface, SurfaceType

class GameWorld:
    def __init__(self,
                 render_target : SurfaceType):
        self.render_target = render_target

        from enemy import Enemy
        self.enemies = []
        for _ in range(constants.ENEMIES_COUNT):
            self.enemies.append(Enemy(self))

    def update(self, delta_time: float):
        for enemy in self.enemies:
            enemy.update(delta_time)

    def render(self, render_target: Surface | SurfaceType):
        for enemy in self.enemies:
            enemy.render(render_target)
