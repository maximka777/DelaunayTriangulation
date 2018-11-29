import json
import sys

import pygame

from colors import RED, WHITE
from geometrical_primitives import Dot, Triangle, Line
from triangulator import triangulate


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


def main():
    config = read_config()

    width = config['size']['width']
    height = config['size']['height']

    size = (width, height)

    pygame.init()

    screen = pygame.display.set_mode(size)

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

        screen.fill(WHITE)

        for dot in dots:
            dot.draw(screen)

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
