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
        self._vector_to_target = [0, 0]
        self._cohesion_vector = [0, 0]
        self._alignment_vector = [0, 0]
        self._avoidance_vector = [0, 0]

        self._swarm = swarm

        self._buddy_1_coordinate = [0, 0]
        self._buddy_2_coordinate = [0, 0]
        self._buddy_3_coordinate = [0, 0]
        self._buddy_1_direction = 0
        self._buddy_2_direction = 0
        self._buddy_3_direction = 0

    def get_visual_info(self):
        return self._coordinate, self._direction

    def set_point_of_interest(self, point_of_interest):
        self._point_of_interest = point_of_interest

    def input_obstacles_info(self, obstacles_info):
        self._obstacles_map_local = obstacles_info

    def _wrap_direction(self):
        print("direction = ", self._direction)
        self._direction = self._direction % (mt.pi * 2)
        print("direction wrapped = ", self._direction)

    def _move(self):
        # self._wrap_direction()
        self._coordinate[0] = self._coordinate[0] + \
            (self._speed_current * self._direction[0])
        self._coordinate[1] = self._coordinate[1] + \
            (self._speed_current * self._direction[1])

    def _execute_vision(self):
        for i in range(1, 11):
            sight_x = self._coordinate[0] + (self._direction[0] * i)
            sight_y = self._coordinate[1] + (self._direction[1] * i)
            if self._obstacles_map_local[int(sight_x)][int(sight_y)] == 1:
                print("I see an obstacle at", sight_x,
                      sight_y, "distance is", i, ",stopping")
                self._speed_current = 0
                return True, i, sight_x, sight_y
            if self._check_buddy_position([sight_x, sight_y]) is True:
                print("I see a buddy at", sight_x,
                      sight_y, "distance is", i, ",stopping")
                self._speed_current = 0
                return True, i, sight_x, sight_y
        # print("It's clear, let's go!")
        self._speed_current = self._speed_max
        return False, 0, 0, 0

    def _avoid_obstacles(self, obstacle, distance, x, y):
        # TODO: Implement "smart" avoidance algorithm
        self._avoidance_vector = [1, 1]]

    def _calculate_distances_in_swarm(self):
        difference= []
        for boid in self._swarm.boid:
            coordinates, direction= boid.get_visual_info()
            difference.append(abs(
                self._coordinate[0] - coordinates[0]) + abs(self._coordinate[1] - coordinates[1]))
        return list(enumerate(difference))

    def _range_difference(self):
        difference= self._calculate_distances_in_swarm()
        for i in range(len(difference)):
            for j in range(len(difference)):
                if difference[i][1] > difference[j][1]:
                    temp= difference[i]
                    difference[i]= difference[j]
                    difference[j]= temp
        return difference

    def _find_nearest_boids(self):
        difference= self._range_difference()
        self._buddy_1_coordinate, self._buddy_1_direction= self._swarm.boid[difference[self._swarm._number_of_boids - 2][0]].get_visual_info(
        )
        self._buddy_2_coordinate, self._buddy_2_direction=self._swarm.boid[difference[self._swarm._number_of_boids - 3][0]].get_visual_info(
        )
        self._buddy_3_coordinate, self._buddy_3_direction=self._swarm.boid[difference[self._swarm._number_of_boids - 4][0]].get_visual_info(
        )

    def _check_buddy_position(self, _coordinates):
        if (_coordinates == self._buddy_1_coordinate) or (_coordinates == self._buddy_2_coordinate) or (_coordinates == self._buddy_3_coordinate):
            return True
        else:
            return False

    def _add_random_noise_to_direction(self):
        self._direction=0.99 * self._direction[0] +
            random.choice((1, -1))*0.01*(random.random() * 2 * mt.pi)

    def _set_direction_to_point(self, _setpoint, _threshold):
        location_error_x=_setpoint[0] - self._coordinate[0]
        location_error_y=_setpoint[1] - self._coordinate[1]
        hippo=mt.sqrt(mt.pow(location_error_x, 2) +
                        mt.pow(location_error_y, 2))
        sin=(location_error_y / hippo)
        cos=(location_error_x / hippo)
        return cos, sin

    def _cohesion(self):
        central_point_x=(
            (self._buddy_1_coordinate[0]+self._buddy_2_coordinate[0]+self._buddy_3_coordinate[0])/3)
        central_point_y = (
            (self._buddy_1_coordinate[1]+self._buddy_2_coordinate[1]+self._buddy_3_coordinate[1])/3)
        central_point = [central_point_x, central_point_y]
        self._cohesion_vector = self._set_direction_to_point(central_point, 10)

    def _alignment(self):
        self._alignment_vector = [(self._buddy_1_direction[0] + self._buddy_2_direction[0] + self._buddy_3_direction[0])/3,
                                  (self._buddy_1_direction[1] + self._buddy_2_direction[1] + self._buddy_3_direction[1])/3]

    def update_status(self):
        self._find_nearest_boids()
        obstacle = True
        self._vector_to_target = self._set_direction_to_point(
            boid._point_of_interest, 0)
        self._alignment()
        self._cohesion()

        while obstacle is True:
            obstacle, distance, x, y = self._execute_vision()
            if obstacle is True:
                self._avoid_obstacles(obstacle, distance, x, y)

        # k1 = k2 = k3 = k4 = 1
        # self._direction = (k1 * self._vector_to_target + k2 * self._alignment_vector + k3 * self._cohesion_vector + k4 * self._avoidance_vector)/2

        self._direction = [(self._vector_to_target[0] + self._cohesion_vector[0] + self._alignment_vector[0])/3,
                           (self._vector_to_target[1] + self._cohesion_vector[1] + self._alignment_vector[1])/3]
        # self._direction = self._alignment_vector
        # self._add_random_noise_to_direction()
        self._move()
