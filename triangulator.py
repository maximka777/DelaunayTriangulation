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

    def is_delaunay_triangulation(self):
        return True

    @staticmethod
    def flip(triangle_pair):
        pass

    def get_first_not_delaunay_pair(self):
        tr_a, tr_b = None, None

        return tr_a, tr_b

    def make(self):
        while not self.is_delaunay_triangulation():
            not_delaunay_triangles_pair = self.get_first_not_delaunay_pair()
            self.flip(not_delaunay_triangles_pair)
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
        return
    segments = generate_segments(points)
    triangulation_segments = GreedyTriangulation(segments).make()
    segments_in_points = [(segment.p1, segment.p2) for segment in triangulation_segments]
    # return segments_in_points
    triangles = segments_to_triangles(segments_in_points)
    delaunay_triangles = DelaunayTriangulation(triangles).make()
    return delaunay_triangles
