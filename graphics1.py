import tkinter as tki
import time as tm
import math as mt
import boid
import numpy
import random


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

# for i in range(start + frame_offset+50, size - 100 - (frame_offset - 2)):
#     obstacles_map[start + frame_offset+200][i] = 1

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

boid_1 = boid.boid(int(size/2), int(size/2))

boid_1.input_obstacles_info(obstacles_map)


while True:
    x, y, d_x, d_y = boid_1.get_visual_info()
    print(x, y, d_x, d_y)

    if obstacles_map[int(x)][int(y)] == 1:
        print("MAYDAY!")
        del boid_1

    canvas.create_rectangle(x-1, y-1, x, y, width=5,
                            fill="red", tag="id1")

    root.update()
    tm.sleep(0.04)
    canvas.delete("id1")
    boid_1.update_status()
    # canvas.getint("id1")


# root.mainloop()

# tk._test()
