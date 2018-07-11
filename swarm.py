import boid
import random
import numpy


obstacle_frame_offset = 10

size = 600  # canvas size
start = 1  # don't modify! synchronization purposes

global_point_of_interest = (random.randint(start + obstacle_frame_offset+1, size -
                                           obstacle_frame_offset), random.randint(start + obstacle_frame_offset+1, size - obstacle_frame_offset))

boid.boid._point_of_interest = global_point_of_interest


class swarm:

    def __init__(self, number_of_boids, obstacles_map):
        self._number_of_boids = number_of_boids
        self._swarm_map = numpy.zeros((size+1, size+1), dtype=int)
        self.boid = []
        self._create_boids(obstacles_map)

    # agent creation
    def _create_boids(self, obstacles_map):
        for i in range(self._number_of_boids):
            spawn_point = (random.randint(start + obstacle_frame_offset+1, size -
                                          obstacle_frame_offset), random.randint(start + obstacle_frame_offset+1, size - obstacle_frame_offset))
            self.boid.append(boid.boid(spawn_point))
            self.boid[i].input_obstacles_info(obstacles_map)

    def _summarize_boids_data(self):
        for i in range(size):
            for j in range(size):
                self._swarm_map[i][j] = 0
        for i in range(self._number_of_boids):
            coordinate, direction = self.boid[i].get_visual_info()
            self._swarm_map[coordinate[0], coordinate[1]] = 1

    def get_swarm_map(self):
        self._summarize_boids_data()
        return self._swarm_map

    def update_status(self):
        for i in range(self._number_of_boids):
            self.boid[i].update_status()


# information exchange
    # boid_1.input_buddy_info(boid_2, boid_3)
    # boid_2.input_buddy_info(boid_1, boid_3)
    # boid_3.input_buddy_info(boid_1, boid_2)
