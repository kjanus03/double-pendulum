import math
import numpy as np
import pygame as pg
from pendulum import Pendulum
from functions import truncate


def update_accelerations(pendulum1, pendulum2, g):
    two_pi = 2 * np.pi
    num1_1 = -g * (2 * pendulum1.m + pendulum2.m) * np.sin(pendulum1.a, dtype=np.float64)
    num1_2 = -pendulum2.m * g * np.sin(pendulum1.a - 2 * pendulum2.a, dtype=np.float64)
    num1_3 = -2 * np.sin(pendulum1.a - pendulum2.a, dtype=np.float64) * pendulum2.m
    num1_4 = pendulum2.av ** 2 * pendulum2.r + pendulum1.av ** 2 * pendulum1.r * np.cos(pendulum1.a - pendulum2.a,
                                                                                        dtype=np.float64)
    num1 = num1_1 + num1_2 + num1_3 * num1_4
    den = pendulum1.r * (2 * pendulum1.m + pendulum2.m - pendulum2.m * np.cos(2 * pendulum1.a - 2 * pendulum2.a,
                                                                              dtype=np.float64))

    num2_1 = 2 * np.sin(pendulum1.a - pendulum2.a, dtype=np.float64)
    num2_2 = pendulum1.av ** 2 * pendulum1.r * (pendulum1.m + pendulum2.m) + g * (
            pendulum1.m + pendulum2.m) * np.cos(
        pendulum1.a, dtype=np.float64) + pendulum2.av ** 2 * pendulum2.r * pendulum2.m * np.cos(
        pendulum1.a - pendulum2.a, dtype=np.float64)

    pendulum1.aa = float(truncate(num1 / den, 5))
    pendulum2.aa = float(truncate((num2_1 * num2_2) / den, 5))
    if abs(pendulum1.aa) > two_pi:
        pendulum1.aa %= two_pi
    if abs(pendulum2.aa) > two_pi:
        pendulum2.aa %= two_pi


def game_loop(pendulum1, pendulum2, size, screen_colour, y_offset, fps, g=1, trail_point_size=1):
    pg.init()
    screen = pg.display.set_mode(size, pg.RESIZABLE)
    background = pg.Surface(size, pg.SRCALPHA, 32)
    background = background.convert_alpha()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        w, h = pg.display.get_surface().get_size()
        screen.fill(screen_colour)

        middle = w / 2
        # background = pg.transform.scale(background, (w, h))

        pg.draw.circle(background, pendulum2.col,
                       (pendulum1.x + pendulum2.x + middle, pendulum1.y + pendulum2.y + y_offset), trail_point_size)

        pg.draw.line(screen, pendulum1.col, (middle, y_offset), (pendulum1.x + middle, pendulum1.y + y_offset))
        pg.draw.circle(screen, pendulum1.col, (pendulum1.x + middle, pendulum1.y + y_offset),
                       math.pow(pendulum1.m, 1 / 3) * 3)

        pg.draw.line(screen, pendulum2.col, (pendulum1.x + middle, pendulum1.y + y_offset),
                     (pendulum1.x + pendulum2.x + middle, pendulum1.y + pendulum2.y + y_offset))
        pg.draw.circle(screen, pendulum2.col,
                       (pendulum1.x + pendulum2.x + middle, pendulum1.y + pendulum2.y + y_offset),
                       math.pow(pendulum2.m, 1 / 3) * 3)

        update_accelerations(pendulum1, pendulum2, g)

        pendulum1.update_velocity()
        pendulum1.update_angle()
        pendulum1.update_position()

        pendulum2.update_velocity()
        pendulum2.update_angle()
        pendulum2.update_position()

        pg.time.wait(1000 // fps)
        screen.blit(background, (0, 0))
        pg.display.flip()

    pg.quit()


def main():
    starting_angle1 = np.random.choice(np.linspace(0, 2 * np.pi, 40))
    starting_angle2 = np.random.choice(np.linspace(0, 2 * np.pi, 40))
    r1, m1, a1, col1 = 120, 40, starting_angle1, (255, 255, 255)
    r2, m2, a2, col2 = 120, 40, starting_angle2, (221, 66, 232)

    pendulum1 = Pendulum(r1, m1, a1, col1)
    pendulum2 = Pendulum(r2, m2, a2, col2)

    x, y = 800, 600
    size = (x, y)
    screen_colour = (34, 34, 34)
    y_offset = (y-r1/2)/2
    fps = 40

    game_loop(pendulum1, pendulum2, size, screen_colour, y_offset, fps, g=1)


if __name__ == '__main__':
    main()
