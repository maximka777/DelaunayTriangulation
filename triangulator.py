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
    return [(segment.p1, segment.p2) for segment in triangulation_segments]
