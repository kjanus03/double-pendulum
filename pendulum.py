import numpy as np

class Pendulum:
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

    def update_angle(self):
        self.a += self.av

    def update_position(self):
        self.x = self.r * np.sin(self.a)
        self.y = self.r * np.cos(self.a)