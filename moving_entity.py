from base_game_entity import BaseGameEntity
from base_game_entity import EntityType

from pygame import Vector2

class MovingEntity(BaseGameEntity):
    def __init__(self, entity_type: EntityType, position: Vector2, velocity: Vector2, mass: float, radius: int):
        super().__init__(entity_type, position, radius)
        self.velocity = velocity
        self.mass = mass
