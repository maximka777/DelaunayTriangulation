import math
from math import sqrt

from external.segments_intersection import intersect


class GreedyTriangulation:
    def __init__(self, segments):
        self.segments = segments

    def make(self):
        self.segments.sort(key=lambda x: x.length)
        triangulation_segments = []
        for segment in self.segments:
            intersects = False
            for triangulation_segment in triangulation_segments:
                if segment.intersect(triangulation_segment):
                    intersects = True
                    break
            if intersects:
                continue
            else:
                triangulation_segments.append(segment)
        return triangulation_segments


def sqr_side(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def get_angle(a, b, c):
    if a * b == 0:
        return 0
    cos = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
    if cos > 1:
        cos = 1
    elif cos < 0:
        cos = 0
    return math.acos(cos)


def angles_by_points(a, b, c):
    return [
        get_angle(sqr_side(a, b), sqr_side(a, c), sqr_side(b, c)),
        get_angle(sqr_side(a, b), sqr_side(b, c), sqr_side(a, c)),
        get_angle(sqr_side(b, c), sqr_side(a, c), sqr_side(a, b))
    ]


def get_min_angle(points):
    return min(angles_by_points(points[0], points[1], points[2]))


def sum_min_angles(triangles):
    return get_min_angle(triangles[0]) + get_min_angle(triangles[1])


def replace_a_on_b_in_triangle(a, b, triangle):
    triangle.remove(a)
    triangle.append(b)


def get_not_general_point(a, b, triangle):
    for p in triangle:
        if p != a and p != b:
            return p


class DelaunayTriangulation:
    def __init__(self, triangles):
        self.triangles = triangles

    @staticmethod
    def make_delaunay_triangulation(triangles):
        sum_min_angles_a = sum_min_angles(triangles)
        DelaunayTriangulation.flip(triangles)
        sum_min_angles_b = sum_min_angles(triangles)
        if sum_min_angles_a > sum_min_angles_b:
            DelaunayTriangulation.flip(triangles)

    @staticmethod
    def is_touched_triangles(tr_a, tr_b):
        ax, ay, az = tr_a
        return (ax in tr_b and ay in tr_b) or (ax in tr_b and az in tr_b) or (ay in tr_b and az in tr_b)

    @staticmethod
    def get_touched_points(tr_a, tr_b):
        points = []
        for p in tr_a:
            if p in tr_b:
                points.append(p)
        return points

    @staticmethod
    def flip(triangle_pair):
        tr_a, tr_b = triangle_pair
        # because someway it can have more than 2 items
        a, b = DelaunayTriangulation.get_touched_points(tr_a, tr_b)[:2]
        tr_a_c = get_not_general_point(a, b, tr_a)
        tr_b_c = get_not_general_point(a, b, tr_b)
        replace_a_on_b_in_triangle(b, tr_b_c, tr_a)
        replace_a_on_b_in_triangle(a, tr_a_c, tr_b)

    def fix_first_not_delaunay_pair(self):
        tr_a, tr_b = None, None
        for i in range(len(self.triangles)):
            tr_a = self.triangles[i]
            for j in range(i + 1, len(self.triangles)):
                tr_b = self.triangles[j]
                if self.is_touched_triangles(tr_a, tr_b):
                    self.make_delaunay_triangulation([tr_a, tr_b])
                    return True
        return False

    def make(self):
        if len(self.triangles) == 1:
            return self.triangles
        while not self.fix_first_not_delaunay_pair():
            pass
        return self.triangles


def is_next_segment(segment, triangle):
    p_a, p_b = segment
    triangle_last_segment = triangle[-1]
    return p_a in triangle_last_segment or p_b in triangle_last_segment


def find_triangle_with_point_from_segment(segment, triangles):
    return list(filter(lambda tr: is_next_segment(segment, tr), triangles))


def triangle_from_segments_to_triangle_from_points(triangle):
    points = []
    for segment in triangle:
        if segment[0] not in points:
            points.append(segment[0])
        if segment[1] not in points:
            points.append(segment[1])
        if len(points) == 3:
            break
    return points


def add_third_segment_to_triangle(segments, triangle):
    triangles = []
    for segment in segments:
        if is_next_segment(segment, triangle):
            triangles.append([triangle[0], triangle[1], segment])
    return triangles


def is_correct_triangle(triangle):
    seg_a = triangle[0]
    seg_b = triangle[1]
    seg_c = triangle[2]

    return (seg_a[0] in seg_c and seg_a[0] not in seg_b) or (seg_a[1] in seg_c and seg_a[1] not in seg_b)


def add_second_segment_to_triangle(segments, triangle):
    triangles = []
    for i in range(len(segments)):
        segment = segments[i]
        if is_next_segment(segment, triangle):
            triangles.extend(add_third_segment_to_triangle(segments[i+1:], [triangle[0], segment]))
    return triangles


def segments_to_triangles(segments):
    triangles = []
    for i in range(len(segments)):
        segment = segments[i]
        triangles.extend(add_second_segment_to_triangle(segments[i+1:], [segment]))
    triangles = list(map(triangle_from_segments_to_triangle_from_points, filter(is_correct_triangle, triangles)))
    return triangles


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = self.calculate_length(p1, p2)

    @staticmethod
    def calculate_length(p1, p2):
        return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))

    def intersect(self, segment):
        return intersect(self.p1, self.p2, segment.p1, segment.p2)


def generate_segments(points):  # it generates all variants of lines between all points
    segments = []
    for i in range(len(points)):
        for j in range(i, len(points)):
            if i != j:
                segments.append(Segment(points[i], points[j]))
    return segments


def triangulate(points):
    if len(points) < 3:
        return []
    segments = generate_segments(points)
    triangulation_segments = GreedyTriangulation(segments).make()
    segments_in_points = [(segment.p1, segment.p2) for segment in triangulation_segments]
    # return segments_in_points
    triangles = segments_to_triangles(segments_in_points)
    delaunay_triangles = DelaunayTriangulation(triangles).make()
    return delaunay_triangles
