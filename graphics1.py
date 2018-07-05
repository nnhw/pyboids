import tkinter as tki
import time as tm
import math as mt
import boid
import numpy
import random


size = 600
obstacles_map = numpy.zeros((size, size), dtype=int)

for i in range(100, 500):
    obstacles_map[100][i] = 1
    obstacles_map[i][100] = 1
    obstacles_map[500][i] = 1
    obstacles_map[i][500] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1
    obstacles_map[random.randint(100, 500)][random.randint(100, 500)] = 1

root = tki.Tk()
canvas = tki.Canvas(root, width=size, height=size, background="white")
canvas.pack()

for i in range(size):
    for j in range(size):
        if obstacles_map[i][j] == 1:
            canvas.create_oval(i, j, i+1, j+1, width=1,
                               fill="black", tag="obs")
root.update()

boid_1 = boid.boid(int(size/2), int(size/2))

boid_1.input_obstacles_info(obstacles_map)


while True:
    x, y, d_x, d_y = boid_1.get_visual_info()
    print(x, y, d_x, d_y)

    if obstacles_map[int(x)][int(y)] == 1:
        del boid_1

    # canvas.create_line(x, y, x+mt.cos(d)*2, y+mt.sin(d)*2,
    #                    fill="red", tag="id1", width=5)
    canvas.create_oval(x, y, x+1, y+1, width=1,
                       fill="red", tag="id1")

    root.update()
    tm.sleep(0.04)
    canvas.delete("id1")
    boid_1.update_status()
    # canvas.getint("id1")


# root.mainloop()

# tk._test()
