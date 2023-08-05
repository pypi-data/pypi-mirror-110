from coopstructs.vectors import Vector2
from typing import List
import math

class Rectangle:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def points_tuple(self):
        return ((self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), (self.x, self.y + self.height))

    @property
    def center(self) -> Vector2:
        return Vector2(self.x + self.width / 2, self.y + self.height / 2)

    def __str__(self):
        return f"TopLeft: <{self.x}, {self.y}>, Size: H{self.height} x W{self.width}"


class Line:
    def __init__(self, origin: Vector2, destination: Vector2):

        if origin == destination:
            raise ValueError(f"origin and destination cannot be equal: {origin}")

        self.origin = origin
        self.destination = destination
        # self.length = self.length()

    @property
    def length(self):
        try:
            return (self.destination - self.origin).length()
        except Exception as e:
            print(f"Destination: {self.destination}\n"
                  f"Origin: {self.origin}\n"
                  f"{e}")
            raise

    def intersection(self, other_line) -> Vector2:
        if not type(other_line) == Line:
            raise TypeError(f"can only intersect with objects of type <Line> but type {type(other_line)} was provided")

        xdiff = (self.origin.x - self.destination.x, other_line.origin.x - other_line.destination.x)
        ydiff = (self.origin.y - self.destination.y, other_line.origin.y - other_line.destination.y)

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (   det(self.origin.as_tuple(), self.destination.as_tuple()),
                det(other_line.origin.as_tuple(), other_line.destination.as_tuple())
            )
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Vector2(x, y)


class Circle:

    @classmethod
    def from_boundary_points(cls, point1: Vector2, point2: Vector2, point3: Vector2):
        lst = [point1, point2, point3]
        if not len(lst) == len(set(lst)):
            raise ValueError(f"All the points must be different for a circle to be created. {point1}, {point2}, {point3} were provided")

        #calculate midpoints
        m1 = point1 + (point2 - point1) / 2
        m2 = point2 + (point3 - point2) / 2

        # Generate perpendicular vectors
        perp_vector_m1 = Vector2(m1.x - point1.y + point2.y, m1.y + point1.x - point2.x)
        perp_line_m1 = Line(origin=Vector2(m1.x, m1.y), destination=perp_vector_m1)

        perp_vector_m2 = Vector2(m2.x - point2.y + point3.y, m2.y + point2.x - point3.x)
        perp_line_m2 = Line(origin=Vector2(m2.x, m2.y), destination=perp_vector_m2)

        #Circle center is where perpendicular vectors intersect
        circ_center = perp_line_m1.intersection(perp_line_m2)

        # Radius is distance from center to one of the boundary points
        rad = (circ_center - point1).length()
        return Circle(circ_center, rad, known_boundary_points=[point1, point2, point3])

    def __init__(self, center: Vector2, radius: float, known_boundary_points: List[Vector2] = None):
        if type(radius) != float:
            raise TypeError(f"Radius must be of type float, but type {type(radius)} was provided")

        self.center = center
        self.radius = radius
        self.known_boundary_points = known_boundary_points if known_boundary_points else []

    def point_at_angle(self, radians: float) -> Vector2:
        x = (self.radius * math.cos(radians) + self.center.x)
        y = (self.radius * math.sin(radians) + self.center.y)
        return Vector2(x, y)

    def rads_of_point(self, point: Vector2):
        rads = math.atan2(point.y - self.center.y, point.x - self.center.x)

        if rads > 0:
            ret = rads
        else:
            ret = 2 * math.pi + rads

        return ret

    def rads_between_points(self, a: Vector2, b: Vector2):
        """Assumes a counter-clockwise orientation between the two points"""
        rad_d = self.rads_of_point(b)
        rad_o = self.rads_of_point(a)

        delta = rad_d - rad_o

        if rad_d > rad_o:
            return delta
        else:
            return 2 * math.pi + delta

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Circle of radius {round(self.radius, 2)} centered at {self.center}"

class Triangle:
    def __init__(self, a: Vector2, b: Vector2, c: Vector2):
        self.points = [a, b, c]
    @property
    def a(self):
        return self.points[0]

    @property
    def b(self):
        return self.points[1]

    @property
    def c(self):
        return self.points[2]

    def incentre(self):
        len_ab = (self.a - self.b).length()
        len_bc = (self.b - self.c).length()
        len_ca = (self.c - self.a).length()

        return (len_bc * self.a + len_ab * self.c + len_ca * self.b) / (len_bc + len_ca + len_ab)

if __name__ == "__main__":
    rect = Rectangle(100, 10, 25, 50)

    print(rect.center)