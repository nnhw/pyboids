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
        def random_point(): return (random.randint(start + obstacle_frame_offset+1, size -
                                                   obstacle_frame_offset), random.randint(start + obstacle_frame_offset+1, size - obstacle_frame_offset))
        for i in range(self._number_of_boids):
            spawn_point = random_point()
            while (obstacles_map[spawn_point[0]][spawn_point[1]]) == 1:
                spawn_point = random_point()
            self.boid.append(boid.boid(spawn_point, self))
            self.boid[i].input_obstacles_info(obstacles_map)

    def set_global_point_of_interest(self, point_of_interest):
        boid.boid._point_of_interest = point_of_interest

    def get_global_point_of_interest(self):
        return boid.boid._point_of_interest

    def update_status(self):
        for boid in self.boid:  # self._number_of_boids:
            boid.update_status()
