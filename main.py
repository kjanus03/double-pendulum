import numpy as np
import pygame as pg
from pendulum import Pendulum


def update_accelerations(Pendulum1, Pendulum2):
    g = 1
    num1_1 = -g * (2 * Pendulum1.m + Pendulum2.m) * np.sin(Pendulum1.a)
    num1_2 = -Pendulum2.m * g * np.sin(Pendulum1.a - 2 * Pendulum2.a)
    num1_3 = -2 * np.sin(Pendulum1.a - Pendulum2.a) * Pendulum2.m
    num1_4 = Pendulum2.av ** 2 * Pendulum2.r + Pendulum1.av ** 2 * Pendulum1.r * np.cos(Pendulum1.a - Pendulum2.a)
    num1 = num1_1 + num1_2 + num1_3 * num1_4
    den = Pendulum1.r * (2 * Pendulum1.m + Pendulum2.m - Pendulum2.m * np.cos(2 * Pendulum1.a - 2 * Pendulum2.a))

    num2_1 = 2 * np.sin(Pendulum1.a - Pendulum2.a)
    num2_2 = Pendulum1.av ** 2 * Pendulum1.r * (Pendulum1.m + Pendulum2.m) + g * (
            Pendulum1.m + Pendulum2.m) * np.cos(
        Pendulum1.a) + Pendulum2.av ** 2 * Pendulum2.r * Pendulum2.m * np.cos(Pendulum1.a - Pendulum2.a)

    Pendulum1.aa = num1 / den
    Pendulum2.aa = (num2_1 * num2_2) / den


def game_loop(Pendulum1, Pendulum2, size, screen_colour, y_offset, fps):
    middle = size[0] / 2
    pg.init()
    screen = pg.display.set_mode(size)
    background = pg.Surface(size, pg.SRCALPHA, 32)
    background = background.convert_alpha()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        screen.fill(screen_colour)

        pg.draw.circle(background, Pendulum2.col,
                       (Pendulum1.x + Pendulum2.x + middle, Pendulum1.y + Pendulum2.y + y_offset), 2)

        pg.draw.line(screen, Pendulum1.col, (middle, y_offset), (Pendulum1.x + middle, Pendulum1.y + y_offset))
        pg.draw.circle(screen, Pendulum1.col, (Pendulum1.x + middle, Pendulum1.y + y_offset), Pendulum1.m)

        pg.draw.line(screen, Pendulum2.col, (Pendulum1.x + middle, Pendulum1.y + y_offset),
                     (Pendulum1.x + Pendulum2.x + middle, Pendulum1.y + Pendulum2.y + y_offset))
        pg.draw.circle(screen, Pendulum2.col,
                       (Pendulum1.x + Pendulum2.x + middle, Pendulum1.y + Pendulum2.y + y_offset), Pendulum2.m)



        update_accelerations(Pendulum1, Pendulum2)

        Pendulum1.update_velocity()
        Pendulum1.update_angle()
        Pendulum1.update_position()

        Pendulum2.update_velocity()
        Pendulum2.update_angle()
        Pendulum2.update_position()

        pg.time.wait(1000 // fps)
        screen.blit(background, (0, 0))
        pg.display.flip()
        screen.blit(background, (0, 0))
    pg.quit()


def main():
    starting_angle1 = np.random.choice(np.linspace(0, 2 * np.pi, 40))
    starting_angle2 = np.random.choice(np.linspace(0, 2 * np.pi, 40))
    r1, m1, a1, col1 = 120, 20, starting_angle1, (255, 255, 255)
    r2, m2, a2, col2 = 120, 20, starting_angle2, (221, 66, 232)

    Pendulum1 = Pendulum(r1, m1, a1, col1)
    Pendulum2 = Pendulum(r2, m2, a2, col2)

    size = (800, 600)
    screen_colour = (20, 20, 20)
    y_offset = 210
    fps = 31

    game_loop(Pendulum1, Pendulum2, size, screen_colour, y_offset, fps)


if __name__ == '__main__':
    main()
