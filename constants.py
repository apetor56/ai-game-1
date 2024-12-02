import pygame
from pygame import Vector2

ENEMIES_COUNT: int = 4
WINDOW_RESOLUTION = (800.0, 600.0)
BLACK_CLEAR_COLOR = (0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
GRAY = pygame.Color(128, 128, 128)
BLUE = pygame.Color(0, 0, 255)
EPSILON = 1e-9

DEFAULT_PLAYER_VELOCITY = Vector2(150.0, 150.0)
DEFAULT_PLAYER_MAX_SPEED: float = DEFAULT_PLAYER_VELOCITY.length()
DEFAULT_PLAYER_RADIUS: int = 20
DEFAULT_PLAYER_HEADING_VEC = Vector2(0, -1)

DEFAULT_ENEMY_VELOCITY = Vector2(0.0, 0.0)
DEFAULT_ENEMY_MAX_SPEED: float = 150
DEFAULT_ENEMY_RADIUS: float = 10

DEFAULT_MASS: float = 1.0
DEFAULT_SCALE = Vector2(1.0, 1.0)

ALPHA: float = 1e-6
COUNTERCLOCKWISE_ROTATION: float = -90.0
FLOCKING_RADIUS: int = 5

class Deceleration:
    #speed of arrive
    SLOW = 3.0
    NORMAL = 2.0
    FAST = 1.0

RESTITUTION_COEFFICIENT = 0.8
MAX_FLOAT_VEC2 = Vector2(float('inf'), float('inf'))
