import math as mt
import random
import numpy


class boid:
    _size = 5
    _status = 0
    _speed_max = 1
    _speed_current = 1
    _direction_x = 0
    _direction_y = 0
    _coordinate_x = 0
    _coordinate_y = 0
    _obstacles_map_local = numpy.zeros((600+1, 600+1), dtype=int)

    _nearest_boid_1_distance = 0
    _nearest_boid_1_angle = 0

    _point_of_interest = [0, 0]

    def __init__(self, x, y):
        self.coordinate_x = x
        self.coordinate_y = y
        self._point_of_interest = [x, y]

    def set_point_of_interest(self, point_of_interest):
        self._point_of_interest = point_of_interest

    def _move(self):
        self.coordinate_x = self.coordinate_x + \
            (self._speed_current * self._direction_x)
        self.coordinate_y = self.coordinate_y + \
            (self._speed_current * self._direction_y)

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

    def _avoid_obstacles(self, obstacle, distance, x, y):
        self._direction_x = random.randint(-1, 1)
        self._direction_y = random.randint(-1, 1)

    def _set_direction_to_point(self):
        location_error_x = self.coordinate_x - self._point_of_interest[0]
        location_error_y = self.coordinate_y - self._point_of_interest[1]
        if location_error_x > 0:
            self._direction_x = -1
        if location_error_x < 0:
            self._direction_x = 1
        if location_error_x == 0:
            self._direction_x = 0
        if location_error_y > 0:
            self._direction_y = -1
        if location_error_y < 0:
            self._direction_y = 1
        if location_error_y == 0:
            self._direction_y = 0

    def update_status(self):
        obstacle = True
        self._set_direction_to_point()
        while obstacle is True:
            obstacle, distance, x, y = self._execute_vision()
            if obstacle is True:
                self._avoid_obstacles(obstacle, distance, x, y)
        self._move()

    def get_visual_info(self):
        return self.coordinate_x, self.coordinate_y, self._direction_x, self._direction_y
