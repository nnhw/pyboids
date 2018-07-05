import tkinter as tki
import time as tm
import math as mt
import boid
import numpy
import random


def draw_actor(_canvas, _boid):
    x, y, d_x, d_y = _boid.get_visual_info()
    # print(x, y, d_x, d_y)
    _canvas.create_rectangle(x-1, y-1, x, y, width=5,
                             fill="red", tag="actors")


def handle_collision(_obstacles_map, _boid):
    x, y, d_x, d_y = _boid.get_visual_info()
    if _obstacles_map[int(x)][int(y)] == 1:
        print("MAYDAY!")
        del _boid


size = 600
start = 1

frame_offset = 10
obstacle_number = 10000
obstacles_map = numpy.zeros((size+1, size+1), dtype=int)

for i in range(start + frame_offset, size - (frame_offset - 2)):
    obstacles_map[start + frame_offset][i] = 1
    obstacles_map[i][start + frame_offset] = 1
    obstacles_map[size - (frame_offset-1)][i] = 1
    obstacles_map[i][size - (frame_offset-1)] = 1
for i in range(obstacle_number):
    obstacle_x = random.randint(start + frame_offset+1, size - frame_offset)
    obstacle_y = random.randint(start + frame_offset+1, size - frame_offset)
    obstacles_map[obstacle_x][obstacle_y] = 1

root = tki.Tk()
canvas = tki.Canvas(root, width=size, height=size, background="white")
canvas.pack()

canvas.create_line(1, 1, 1, 600, fill="red", width="5")
canvas.create_line(1, 1, 600, 1, fill="red", width="5")
canvas.create_line(600, 1, 600, 600, fill="red", width="5")
canvas.create_line(1, 600, 600, 600, fill="red", width="5")

for i in range(size):
    for j in range(size):
        if obstacles_map[i][j] == 1:
            canvas.create_rectangle(i-1, j-1, i, j, width=0,
                                    fill="green", tag="obs")
root.update()

spawn_point1 = (random.randint(start + frame_offset+1, size -
                               frame_offset), random.randint(start + frame_offset+1, size - frame_offset))
spawn_point2 = (random.randint(start + frame_offset+1, size -
                               frame_offset), random.randint(start + frame_offset+1, size - frame_offset))
spawn_point3 = (random.randint(start + frame_offset+1, size -
                               frame_offset), random.randint(start + frame_offset+1, size - frame_offset))
boid_1 = boid.boid(spawn_point1[0], spawn_point1[1])
boid_2 = boid.boid(spawn_point1[0]+50, spawn_point1[1]+50)
boid_3 = boid.boid(spawn_point1[0]-50, spawn_point1[1]-50)

boid_1.input_obstacles_info(obstacles_map)
boid_2.input_obstacles_info(obstacles_map)
boid_3.input_obstacles_info(obstacles_map)

global_point_of_interest = (random.randint(start + frame_offset+1, size -
                                           frame_offset), random.randint(start + frame_offset+1, size - frame_offset))

boid.boid._point_of_interest = global_point_of_interest


while True:

    draw_actor(canvas, boid_1)
    handle_collision(obstacles_map, boid_1)

    draw_actor(canvas, boid_2)
    handle_collision(obstacles_map, boid_2)

    draw_actor(canvas, boid_3)
    handle_collision(obstacles_map, boid_3)

    root.update()
    tm.sleep(0.04)
    canvas.delete("actors")
    boid_1.update_status()
    boid_2.update_status()
    boid_3.update_status()

    boid_1.input_buddy_info(boid_2, boid_3)
    boid_2.input_buddy_info(boid_1, boid_3)
    boid_3.input_buddy_info(boid_1, boid_2)

# root.mainloop()
