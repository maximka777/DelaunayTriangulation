import pygame

from colors import GREEN, RED


class Line:
    def __init__(self, p1, p2, color=GREEN, width=1):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.width = width

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.p1, self.p2, self.width)


class Triangle:
    def __init__(self, points, color=GREEN, width=1):
        self.points = points
        self.color = color
        self.width = width

    def draw(self, surface):
        Line(self.points[0], self.points[1], self.color, self.width).draw(surface)
        Line(self.points[1], self.points[2], self.color, self.width).draw(surface)
        Line(self.points[2], self.points[0], self.color, self.width).draw(surface)


class Dot:
    def __init__(self, p, color=RED, radius=2, width=2):
        self.p = p
        self.color = color
        self.radius = radius
        self.width = width

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.p, self.radius, self.width)


class Circle(Dot):
    pass
