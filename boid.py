import math as mt
import random
import numpy


class boid:
    # _size = 5
    # _status = 0
    _speed_max = 1
    # local visibility map
    _obstacles_map_local = numpy.zeros((600+1, 600+1), dtype=int)
    # TODO: replace global map on small local one (10 x 10)
    # mastermind attribute
    _point_of_interest = [0, 0]

    def __init__(self, x, y):
        self._coordinate = [x, y]
        self._point_of_interest = [x, y]
        self._speed_current = 1
        self._direction = [0, 0]

        self._buddy_1_coordinate = [0, 0]
        self._buddy_2_coordinate = [0, 0]
        self._buddy_1_direction = [0, 0]
        self._buddy_2_direction = [0, 0]

    def get_visual_info(self):
        return self._coordinate[0], self._coordinate[1], self._direction[0], self._direction[1]

    def set_point_of_interest(self, point_of_interest):
        self._point_of_interest = point_of_interest

    def input_obstacles_info(self, obstacles_info):
        self._obstacles_map_local = obstacles_info

    def input_buddy_info(self, _buddy_1, _buddy_2):
        self._buddy_1_coordinate = _buddy_1._coordinate
        self._buddy_2_coordinate = _buddy_2._coordinate
        self._buddy_1_direction = _buddy_1._direction
        self._buddy_2_direction = _buddy_2._direction

    def _move(self):
        self._coordinate[0] = self._coordinate[0] + \
            (self._speed_current * self._direction[0])
        self._coordinate[1] = self._coordinate[1] + \
            (self._speed_current * self._direction[1])

    def _execute_vision(self):
        for i in range(10):
            sight_x = self._coordinate[0] + self._direction[0] * i
            sight_y = self._coordinate[1] + self._direction[1] * i
            if self._obstacles_map_local[sight_x][sight_y] == 1:
                print("I see an obstacle at", sight_x,
                      sight_y, "distance is", i, ",stopping")
                self._speed_current = 0
                return True, i, sight_x, sight_y
            if self._check_buddy_position([sight_x, sight_y]) is True:
                print("I see a buddy at", sight_x,
                      sight_y, "distance is", i, ",stopping")
                return True, i, sight_x, sight_y
        # print("It's clear, let's go!")
        self._speed_current = self._speed_max
        return False, 0, 0, 0

    def _avoid_obstacles(self, obstacle, distance, x, y):
        self._direction[0] = random.randint(-1, 1)
        self._direction[1] = random.randint(-1, 1)

    def _synchronize_directions(self):
        direction_x = self._buddy_1_direction[0] + \
            self._buddy_2_direction[0] + self._direction[0]
        direction_y = self._buddy_1_direction[1] + \
            self._buddy_2_direction[1] + self._direction[1]
        if direction_x > 1:
            direction_x = 1
        if direction_x < -1:
            direction_x = -1
        if direction_y > 1:
            direction_y = 1
        if direction_y < -1:
            direction_y = -1
        self._direction = [direction_x, direction_y]
        # print("New synch direction is", self._direction)

    def _check_buddy_position(self, _coordinates):
        if (_coordinates == self._buddy_1_coordinate) or (_coordinates == self._buddy_2_coordinate):
            return True
        else:
            return False

    def _centralize(self):
        cental_point_x = int(
            (self._coordinate[0]+self._buddy_1_coordinate[0]+self._buddy_2_coordinate[0])/3)
        cental_point_y = int(
            (self._coordinate[1]+self._buddy_1_coordinate[1]+self._buddy_2_coordinate[1])/3)
        cental_point = [cental_point_x, cental_point_y]
        self._set_direction_to_point(cental_point, 10)
        # print("Central point is", cental_point)

    def _choose_random_direction(self):
        self._direction = [random.randint(-1, 1), random.randint(-1, 1)]
        # print("New random direction is", self._direction)

    def _set_direction_to_point(self, _setpoint, _threshold):
        location_error_x = self._coordinate[0] - _setpoint[0]
        location_error_y = self._coordinate[1] - _setpoint[1]
        if location_error_x > _threshold:
            self._direction[0] = -1
        if location_error_x < -_threshold:
            self._direction[0] = 1
        if location_error_x == 0:
            self._direction[0] = 0
        if location_error_y > _threshold:
            self._direction[1] = -1
        if location_error_y < -_threshold:
            self._direction[1] = 1
        if location_error_y == 0:
            self._direction[1] = 0

    def update_status(self):
        obstacle = True
        # self._set_direction_to_point(boid._point_of_interest, 0)
        self._choose_random_direction()
        self._synchronize_directions()
        self._centralize()
        while obstacle is True:
            obstacle, distance, x, y = self._execute_vision()
            if obstacle is True:
                self._avoid_obstacles(obstacle, distance, x, y)
        self._move()
