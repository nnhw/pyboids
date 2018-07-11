import tkinter as tki
import time as tm
import math as mt
# import boid
import numpy
import random
import swarm


def draw_actors(_canvas, _actors_map):
    for i in range(size):
        for j in range(size):
            if _actors_map[i][j] == 1:
                # print(x, y, d_x, d_y)
                _canvas.create_rectangle(i-1, j-1, i, j, width=5,
                                         fill="red", tag="actors")


# def handle_collision(_obstacles_map, _boid):
#     x, y, d_x, d_y = _boid.get_visual_info()
#     if _obstacles_map[int(x)][int(y)] == 1:
#         print("MAYDAY!")
#         del _boid  # Oh, how rude


size = 600  # canvas size
start = 1  # don't modify! synchronization purposes

obstacle_frame_offset = 10


obstacle_number = 10000
# size+1 is for synchronization with the canvas
obstacles_map = numpy.zeros((size+1, size+1), dtype=int)
# frame construction
for i in range(start + obstacle_frame_offset, size - (obstacle_frame_offset - 2)):
    obstacles_map[start + obstacle_frame_offset][i] = 1
    obstacles_map[i][start + obstacle_frame_offset] = 1
    obstacles_map[size - (obstacle_frame_offset-1)][i] = 1
    obstacles_map[i][size - (obstacle_frame_offset-1)] = 1
# obstacle construction
for i in range(obstacle_number):
    obstacle_x = random.randint(
        start + obstacle_frame_offset+1, size - obstacle_frame_offset)
    obstacle_y = random.randint(
        start + obstacle_frame_offset+1, size - obstacle_frame_offset)
    obstacles_map[obstacle_x][obstacle_y] = 1

# graphics init
root = tki.Tk()
canvas = tki.Canvas(root, width=size, height=size, background="white")
canvas.pack()

# eye candy
canvas.create_line(1, 1, 1, 600, fill="red", width="5")
canvas.create_line(1, 1, 600, 1, fill="red", width="5")
canvas.create_line(600, 1, 600, 600, fill="red", width="5")
canvas.create_line(1, 600, 600, 600, fill="red", width="5")

# obstacles visualization
for i in range(size):
    for j in range(size):
        if obstacles_map[i][j] == 1:
            canvas.create_rectangle(i-1, j-1, i, j, width=0,
                                    fill="green", tag="obs")
root.update()

swarm = swarm.swarm(30, obstacles_map)

while True:

    draw_actors(canvas, swarm.get_swarm_map())

    # drawing
    root.update()
    tm.sleep(0.04)  # 25 fps
    canvas.delete("actors")

    swarm.update_status()
# root.mainloop()
