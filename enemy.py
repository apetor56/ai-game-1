from game_world import GameWorld
from moving_entity import MovingEntity
from base_game_entity import EntityType

import pygame
from pygame import Vector2, SurfaceType, Surface

import random

RED = pygame.Color(255, 0, 0)
FIXED_MASS: float = 1.0
FIXED_VELOCITY = Vector2(10.0, 10.0)

class Enemy(MovingEntity):
    def __init__( self, game_world: GameWorld, radius: int = 10, color: pygame.Color = RED ):
        generated_position = self.generate_random_position( game_world.render_target, radius )
        super().__init__( EntityType.eEnemy, generated_position, FIXED_VELOCITY, FIXED_MASS, radius )
        self.game_world = game_world
        self.color = color

    def update(self, delta_time: float):
        pass

    def render(self, render_target : SurfaceType):
        pygame.draw.circle(render_target, self.color, self.position, self.radius)

    def generate_random_position(self, render_target : SurfaceType, radius: int):
        width, height = render_target.get_size()
        x: float = random.uniform(radius, width - radius)
        y: float = random.uniform(radius, height - radius)
        return Vector2(x, y)
