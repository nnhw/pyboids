import math as mt
import random
import numpy


class boid:
    _size = 5
    _status = 0
    _speed_max = 1
    _speed_current = 1
    _direction_x = 1
    _direction_y = 1
    _obstacles_map_local = numpy.zeros((600, 600), dtype=int)

    _nearest_boid_1_distance = 0
    _nearest_boid_1_angle = 0

    def __init__(self, x, y):
        self.coordinate_x = x
        self.coordinate_y = y

    def _move(self):
        self.coordinate_x = self.coordinate_x + \
            (self._speed_current * self._direction_x)
        self.coordinate_y = self.coordinate_y + \
            (self._speed_current * self._direction_y)

        if self.coordinate_x > 600:
            self.coordinate_x = 0
        if self.coordinate_y > 600:
            self.coordinate_y = 0

        if self.coordinate_x < 0:
            self.coordinate_x = 600
        if self.coordinate_y < 0:
            self.coordinate_y = 600

    def _update_nearest_boids_info(self):
        NotImplemented

    def input_obstacles_info(self, obstacles_info):
        self._obstacles_map_local = obstacles_info

    def _execute_vision(self):
        for i in range(10):
            sight_x = self.coordinate_x + self._direction_x * i
            sight_y = self.coordinate_y + self._direction_y * i
            if self._obstacles_map_local[sight_x][sight_y] == 1:
                print("I see an obstacle at", sight_x,
                      sight_y, "distance is", i, ",stopping")
                self._speed_current = 0
                return True, i, sight_x, sight_y
        print("It's clear, let's go!")
        self._speed_current = self._speed_max
        return False, 0, 0, 0

    def _choose_direction(self, obstacle, distance, x, y):
        if self._direction_x == 0 and self._direction_y == 0:
            print("I don't wanna go, choosing another directrion and stopping")
            self._direction_x = random.randint(-1, 1)
            self._direction_y = random.randint(-1, 1)
            self._speed_current = 0
            return
        if obstacle is True:
            self._direction_x = random.randint(-1, 1)
            self._direction_y = random.randint(-1, 1)
        else:
            self._speed_current = self._speed_max

    def update_status(self):
        obstacle, distance, x, y = self._execute_vision()
        self._choose_direction(obstacle, distance, x, y)
        self._move()

    def get_visual_info(self):
        return self.coordinate_x, self.coordinate_y, self._direction_x, self._direction_y
