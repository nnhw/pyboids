import math as mt
import random
import numpy


class boid:
    # _size = 5
    # _status = 0
    _speed_max = 1
    # local visibility map
    # FIXME: Magic numbers!
    _obstacles_map_local = numpy.zeros((600+1, 600+1), dtype=int)
    # TODO: replace global map on small local one (10 x 10)
    # mastermind attribute
    _point_of_interest = [0, 0]

    def __init__(self, coordinate, swarm):
        self._coordinate = [coordinate[0], coordinate[1]]
        self._point_of_interest = coordinate
        self._speed_current = 1
        self._direction = [0, 0]

        self._swarm = swarm

        self._buddy_1_coordinate = [0, 0]
        self._buddy_2_coordinate = [0, 0]
        self._buddy_3_coordinate = [0, 0]
        self._buddy_1_direction = [0, 0]
        self._buddy_2_direction = [0, 0]
        self._buddy_3_direction = [0, 0]

    def get_visual_info(self):
        return self._coordinate, self._direction

    def set_point_of_interest(self, point_of_interest):
        self._point_of_interest = point_of_interest

    def input_obstacles_info(self, obstacles_info):
        self._obstacles_map_local = obstacles_info

    def _move(self):
        self._coordinate[0] = self._coordinate[0] + \
            (self._speed_current * self._direction[0])
        self._coordinate[1] = self._coordinate[1] + \
            (self._speed_current * self._direction[1])

    def _execute_vision(self):
        for i in range(1, 11):
            sight_x = self._coordinate[0] + self._direction[0] * i
            sight_y = self._coordinate[1] + self._direction[1] * i
            if self._obstacles_map_local[sight_x][sight_y] == 1:
                # print("I see an obstacle at", sight_x,
                #       sight_y, "distance is", i, ",stopping")
                self._speed_current = 0
                return True, i, sight_x, sight_y
            if self._check_buddy_position([sight_x, sight_y]) is True:
                # print("I see a buddy at", sight_x,
                #       sight_y, "distance is", i, ",stopping")
                self._speed_current = 0
                return True, i, sight_x, sight_y
        # print("It's clear, let's go!")
        self._speed_current = self._speed_max
        return False, 0, 0, 0

    def _avoid_obstacles(self, obstacle, distance, x, y):
        self._direction[0] = random.randint(-1, 1)
        self._direction[1] = random.randint(-1, 1)

    def _synchronize_directions(self):
        direction_x = self._buddy_1_direction[0] + \
            self._buddy_2_direction[0] + \
            self._buddy_3_direction[0] + self._direction[0]
        direction_y = self._buddy_1_direction[1] + \
            self._buddy_2_direction[1] + \
            self._buddy_3_direction[1] + self._direction[1]
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

    def _calculate_distances_in_swarm(self):
        difference = []
        for boid in self._swarm.boid:
            coordinates, direction = boid.get_visual_info()
            difference.append(abs(
                self._coordinate[0] - coordinates[0]) + abs(self._coordinate[1] - coordinates[1]))
            # print(list(enumerate(difference)), "\n")
        return list(enumerate(difference))

    def _range_difference(self):
        difference = self._calculate_distances_in_swarm()
        for i in range(len(difference)):
            for j in range(len(difference)):
                if difference[i][1] > difference[j][1]:
                    temp = difference[i]
                    # print(difference[i], "\n")
                    difference[i] = difference[j]
                    difference[j] = temp
        # print(difference, "\n")
        return difference

    def _find_nearest_boids(self):
        difference = self._range_difference()
        # print(difference, "\n")
        # print(difference[1][1])
        self._buddy_1_coordinate, self._buddy_1_direction = self._swarm.boid[difference[self._swarm._number_of_boids - 2][0]].get_visual_info(
        )
        self._buddy_2_coordinate, self._buddy_2_direction = self._swarm.boid[difference[self._swarm._number_of_boids - 3][0]].get_visual_info(
        )
        self._buddy_3_coordinate, self._buddy_3_direction = self._swarm.boid[difference[self._swarm._number_of_boids - 4][0]].get_visual_info(
        )
        # print(self._buddy_1_coordinate, "\n")
        # print(self._buddy_2_coordinate, "\n")
        # print(self._swarm.boid[difference[0][0]], "\n")

    def _check_buddy_position(self, _coordinates):
        if (_coordinates == self._buddy_1_coordinate) or (_coordinates == self._buddy_2_coordinate) or (_coordinates == self._buddy_3_coordinate):
            return True
        else:
            return False

    def _centralize(self):
        central_point_x = int(
            (self._buddy_1_coordinate[0]+self._buddy_2_coordinate[0]+self._buddy_3_coordinate[0])/3)
        central_point_y = int(
            (self._buddy_1_coordinate[1]+self._buddy_2_coordinate[1]+self._buddy_3_coordinate[1])/3)
        central_point = [central_point_x, central_point_y]
        self._set_direction_to_point(central_point, 10)
        # print("Central point is", central_point)

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
        self._find_nearest_boids()
        obstacle = True
        self._set_direction_to_point(boid._point_of_interest, 0)
        # self._choose_random_direction()
        self._synchronize_directions()
        self._centralize()
        while obstacle is True:
            obstacle, distance, x, y = self._execute_vision()
            if obstacle is True:
                self._avoid_obstacles(obstacle, distance, x, y)
        self._move()
