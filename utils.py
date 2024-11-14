from pygame import Vector2

class Utils:
    @staticmethod
    def point_to_world_space(local_point: Vector2, heading: Vector2, side: Vector2, position: Vector2) -> Vector2:
        transformed_point = Vector2()
        transformed_point.x = (local_point.x * heading.x) + (local_point.y * side.x) + position.x
        transformed_point.y = (local_point.x * heading.y) + (local_point.y * side.y) + position.y
        return transformed_point

    @staticmethod
    def point_to_local_space(world_point, heading: Vector2, side: Vector2, position: Vector2) -> Vector2:
        translated_point = world_point - position

        local_point_x = translated_point * heading
        local_point_y = translated_point * side

        return Vector2(local_point_x, local_point_y)
