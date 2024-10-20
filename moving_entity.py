from base_game_entity import BaseGameEntity
from base_game_entity import EntityType
import constants

from pygame import Vector2

class MovingEntity(BaseGameEntity):
    def __init__(self,
                 entity_type: EntityType,
                 position: Vector2,
                 velocity: Vector2,
                 heading_vec: Vector2,
                 radius: float,
                 mass: float):
        super().__init__(entity_type,
                         position,
                         radius)
        self.velocity = velocity
        self.heading_vec = heading_vec
        self.side_vec = self.heading_vec.rotate(constants.CLOCKWISE_ROTATION)
        self.mass = mass
