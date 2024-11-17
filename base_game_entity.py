import constants

from pygame.math import Vector2

from enum import Enum

class EntityType(Enum):
    eDefault = -1
    ePlayer = 0
    eEnemy = 1,
    eObstacle = 2
    eWall = 3

class BaseGameEntity:
    latest_id = 0

    def __init__(self,
                 entity_type: EntityType,
                 position: Vector2,
                 radius: float):
        self.id = BaseGameEntity.next_valid_id()
        self.type = entity_type
        self.tag = False
        self.tagged = False
        self.position = Vector2(position.x, constants.WINDOW_RESOLUTION[1] - position.y)
        self.scale = constants.DEFAULT_SCALE
        self.radius = radius

    @staticmethod
    def next_valid_id():
        BaseGameEntity.latest_id += 1
        return BaseGameEntity.latest_id

    def get_render_position(self):
        return Vector2(self.position.x, constants.WINDOW_RESOLUTION[1] - self.position.y)

    def tag(self):
        """Mark the entity as tagged (part of a group)."""
        self.tagged = True

    def untag(self):
        """Unmark the entity as tagged (not part of a group)."""
        self.tagged = False

    def is_tagged(self):
        """Check if the entity is tagged."""
        return self.tagged
