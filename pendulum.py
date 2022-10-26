import numpy as np


class Pendulum:
    two_pi = 2 * np.pi

    def __init__(self, r, m, a, col, av=0, aa=0):
        self.r = r
        self.m = m
        self.a = a  # Angle
        self.x = self.r * np.sin(a)
        self.y = self.r * np.cos(a)
        self.col = col
        self.av = av
        self.aa = aa

    def update_velocity(self):
        self.av += self.aa
        if abs(self.av) > self.two_pi:
            self.av %= self.two_pi

    def update_angle(self):
        self.a += self.av
        if abs(self.a) > self.two_pi:
            self.a %= self.two_pi

    def to_string(self):
        return f'Angle: {self.a}\nAngular velocity: {self.av}\nAngular acceleration: {self.aa}\n\n'

    def update_position(self):
        self.x = self.r * np.sin(self.a)
        self.y = self.r * np.cos(self.a)
