import math

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

    @staticmethod
    def line_intersection_2d(A, B, C, D):
        r_top = (A.y - C.y) * (D.x - C.x) - (A.x - C.x) * (D.y - C.y)
        r_bot = (B.x - A.x) * (D.y - C.y) - (B.y - A.y) * (D.x - C.x)

        s_top = (A.y - C.y) * (B.x - A.x) - (A.x - C.x) * (B.y - A.y)
        s_bot = (B.x - A.x) * (D.y - C.y) - (B.y - A.y) * (D.x - C.x)

        if r_bot == 0 or s_bot == 0:
            return False, None, 0.0

        r = r_top / r_bot
        s = s_top / s_bot

        if 0 < r < 1 and 0 < s < 1:
            dist = A.distance_to(B) * r
            point = A + r * (B - A)
            return True, point, dist
        else:
            return False, None, 0.0

    @staticmethod
    def vector_to_world_space(vec, agent_heading, agent_side):
        trans_vec = vec.copy()

        mat_transform = C2DMatrix()
        mat_transform.rotate(agent_heading, agent_side)

        transformed_vec = mat_transform.transform_vector_2d(trans_vec)
        return transformed_vec

class C2DMatrix:
    def __init__(self):
        self.matrix = [[1, 0], [0, 1]]

    def rotate(self, heading, side):
        angle = heading.angle_to(Vector2(1, 0))
        rotation_matrix = [
            [math.cos(math.radians(angle)), math.sin(math.radians(angle))],
            [math.sin(math.radians(angle)), math.cos(math.radians(angle))]
        ]
        self.matrix = rotation_matrix

    def transform_vector_2d(self, vec):
        x = vec.x * self.matrix[0][0] + vec.y * self.matrix[0][1]
        y = vec.x * self.matrix[1][0] + vec.y * self.matrix[1][1]
        return Vector2(x, y)
