from pygame.math import Vector2

from enum import Enum


class EntityType(Enum):
    eDefault = -1
    ePlayer = 0
    eEnemy = 1

class BaseGameEntity:
    latest_id = 0

    def __init__(self, entity_type: EntityType, position: Vector2, radius: int):
        self.id = BaseGameEntity.next_valid_id()
        self.type = entity_type
        self.tag = False
        self.position = position
        self.scale = Vector2(1, 1)
        self.radius = radius

    @staticmethod
    def next_valid_id():
        BaseGameEntity.latest_id += 1
        return BaseGameEntity.latest_id
