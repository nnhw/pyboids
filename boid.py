import math as mt
import random
import numpy


class boid:
    _size = 5
    _status = 0
    _speed_max = 1
    _speed_current = 1
    _direction = mt.pi
    _obstacles_map_local = numpy.zeros((600, 600), dtype=int)

    _nearest_boid_1_distance = 0
    _nearest_boid_1_angle = 0

    def __init__(self, x, y):
        self.coordinate_x = x
        self.coordinate_y = y

    def _move(self):
        self.coordinate_x = self.coordinate_x + \
            (self._speed_current * mt.cos(self._direction))
        self.coordinate_y = self.coordinate_y + \
            (self._speed_current * mt.sin(self._direction))

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

        # if sight_x > 599:
        #     sight_x = 599
        # if sight_y > 599:
        #     sight_y = 599
        # if sight_x < 0:
        #     sight_x = 0
        # if sight_y < 0:
        #     sight_y = 0
        for i in range(10):
            sight_x = self.coordinate_x + (mt.cos(self._direction) * i)
            sight_y = self.coordinate_y + (mt.sin(self._direction) * i)
            if self._obstacles_map_local[int(sight_x)][int(sight_y)] == 1:
                if i == 1:
                    self._speed_current = 0
                else:
                    self._speed_current = self._speed_max
                return True
            # self._speed_current = self._speed_max - (11-i)
            # self._direction = self._direction + 1
            # NotImplemented

    def _choose_direction(self, obstacle):
        self._direction = 0.9 * self._direction + \
            random.choice((1, -1))*0.1*(random.random() * 2 * mt.pi)
        if obstacle is True:
            self._direction = self._direction + 1

    def update_status(self):
        self._choose_direction(self._execute_vision())
        self._move()

    def get_visual_info(self):
        return self.coordinate_x, self.coordinate_y, self._direction
