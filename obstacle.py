import pygame
from pygame import Vector2

class Obstacle:
    def __init__(self, position: Vector2, radius: float, color: pygame.Color):
        self.position = position
        self.radius = radius
        self.color = color

    def render(self, render_target):
        pygame.draw.circle(render_target, self.color, self.position, self.radius)