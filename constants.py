import pygame
from pygame import Vector2

ENEMIES_COUNT: int = 5
WINDOW_RESOLUTION = (800.0, 600.0)
BLACK_CLEAR_COLOR = (0, 0, 0)
RED = pygame.Color(255, 0, 0)

DEFAULT_MASS: float = 1.0
DEFAULT_VELOCITY = Vector2(100.0, 100.0)
DEFAULT_MAX_SPEED: float = DEFAULT_VELOCITY.length()
DEFAULT_RADIUS: float = 10
DEFAULT_SCALE = Vector2(1.0, 1.0)

ALPHA: float = 1e-6
CLOCKWISE_ROTATION: float = 90.0
