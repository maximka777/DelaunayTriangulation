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


class DelaunayTriangulation:
    def __init__(self, triangles):
        self.triangles = triangles

    def make(self):
        return self.triangles


def triangle_has_point_from_segment(segment, triangle):
    seg_a, seg_b = segment
    for side in triangle:
        side_a, side_b = side
        if side_a == seg_a or side_a == seg_b or side_b == seg_a or side_b == seg_b:
            return True
    return False


def find_triangle_with_point_from_segment(segment, triangles):
    return list(filter(lambda tr: triangle_has_point_from_segment(segment, tr), triangles))


def triangle_from_segments_to_triangle_from_points(triangle):
    points = []
    for segment in triangle:
        if segment[0] not in points:
            points.append(segment[0])
        if segment[1] not in points:
            points.append(segment[1])
    return points


def segments_to_triangles(segments):
    triangles = []
    for segment in segments:
        triangles_with_point_from_segment = find_triangle_with_point_from_segment(segment, triangles)
        for triangle in triangles_with_point_from_segment:
            triangle.append(segment)
        if len(triangles_with_point_from_segment) == 0:
            triangles.append([segment])
    triangles = list(map(triangle_from_segments_to_triangle_from_points, triangles))
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
        return
    segments = generate_segments(points)
    triangulation_segments = GreedyTriangulation(segments).make()
    segments_in_points = [(segment.p1, segment.p2) for segment in triangulation_segments]
    triangles = segments_to_triangles(segments_in_points)
    delaunay_triangles = DelaunayTriangulation(triangles).make()
    return delaunay_triangles
