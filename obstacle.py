from base_game_entity import BaseGameEntity
from base_game_entity import EntityType

import constants

import pygame
from pygame import Vector2

class Obstacle(BaseGameEntity):
    def __init__(self, position: Vector2, radius: float, color: pygame.Color):
        super().__init__(EntityType.eObstacle, position, radius)
        self.color = color
        self.in_range_tag = True

    def render(self, render_target):
        pygame.draw.circle(render_target, self.color, self.position, self.radius)
