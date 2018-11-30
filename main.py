import json
import sys
from math import sqrt

import pygame

from colors import RED, WHITE, BLUE, BLACK
from geometrical_primitives import Dot, Triangle, Line, Circle
from triangulator import triangulate, sqr_side


def read_config():
    with open('config.json', 'r') as file:
        return json.load(file)


def print_instruction(screen, instruction='Press enter to calculate triangulation (minimal points count: 3)'):
    if pygame.font:
        font = pygame.font.Font(None, 24)
        text = font.render(instruction, 1, RED)
        text_position = text.get_rect()
        screen.blit(text, text_position)


def dots_to_points(dots):
    return [dot.p for dot in dots]


def get_center(triangle):
    a, b, c = triangle
    A = b[0] - a[0]
    B = b[1] - a[1]
    C = c[0] - a[0]
    D = c[1] - a[1]
    E = A * (a[0] + b[0]) + B * (a[1] + b[1])
    F = C * (a[0] + c[0]) + D * (a[1] + c[1])
    G = 2 * (A * (c[1] - b[1]) - B * (c[0] - b[0]))
    if G == 0:
        return
    center_x = (D * E - B * F) / G
    center_y = (A * F - C * E) / G
    return int(center_x), int(center_y)


def draw_circle_by_triangles(triangles, surface):
    centers = [get_center(triangle) for triangle in triangles]

    for i in range(len(centers)):
        center = centers[i]
        if center is not None:
            Circle(center, (255, 255, 255, 0.5), int(sqrt(sqr_side(center, triangles[i][0]))), 1).draw(surface)


def main():
    config = read_config()

    width = config['size']['width']
    height = config['size']['height']

    pygame.init()

    screen_info = pygame.display.Info()
    size = (screen_info.current_w, screen_info.current_h)

    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

    dots = []
    triangles = []
    lines = []

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.dict['button'] == 1:
                    dots.append(Dot(event.dict['pos']))
            elif event.type == pygame.KEYUP:
                if event.dict['key'] == 13:
                    triangles = triangulate(dots_to_points(dots))
                    # lines = triangulate(dots_to_points(dots))
                elif event.dict['key'] == pygame.K_r:
                    dots = []
                    triangles = []
                    lines = []
                elif event.dict['key'] == pygame.K_q:
                    sys.exit()

        screen.fill(BLACK)

        for dot in dots:
            dot.draw(screen)

        draw_circle_by_triangles(triangles, screen)

        if triangles is not None:
            for triangle in triangles:
                Triangle(triangle).draw(screen)

        # when there are segments (from greedy triangulation) instead of triangles
        # if lines is not None:
        #     for line in lines:
        #         Line(line[0], line[1]).draw(screen)

        print_instruction(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
