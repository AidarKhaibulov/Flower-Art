import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


def rot_matr(ang):
    mtr = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return mtr


def diag_matr(a, b, c):
    mtr = np.array([[a, 0, 0], [0, b, 0], [0, 0, c]])
    return mtr


def draw_petal(img, p):
    e1 = bezier_curve(img, p[0][0], p[1][0], p[0][1], p[1][1], p[0][2], p[1][2])
    e2 = bezier_curve(img, p[0][0], p[1][0], p[0][3], p[1][3], p[0][2], p[1][2])

    #filling petals logic

    left = min(min(e1[0]), min(e2[0]))
    right = max(max(e1[0]), max(e2[0]))
    up = max(max(e1[1]), max(e2[1])) - 1
    down = min(min(e1[1]), min(e2[1])) + 1

    # petals out of image case
    if right >= width:
        right = width - 1
    if left < 0:
        left = 1
        left, right = right, left
    if up >= height:
        up = height - 1
    if down < 0:
        down = 1
    count = 0
    if down - 1 < height:
        if right == 1:
            for j in range(left, right, -1):
                if img[j, down - 1, 0] == img[j, down - 1, 1] == img[j, down - 1, 2] == 255:
                    count += 1
            if count == 1:
                down += 2
            for y in range(down, up):
                flag_first = False
                flag_second = False
                flag_third = False
                for x in range(left, right, -1):
                    if img[x, y, 0] == img[x, y, 1] == img[x, y, 2] == 255 and not flag_third :
                        flag_first = True
                    if flag_first and img[x, y, 0] == 255 and img[x, y, 1] == 10 and img[x, y, 2] == 130:
                        flag_second = True
                    if flag_second and flag_first and img[x, y, 0] == img[x, y, 1] == img[x, y, 2] == 255:
                        flag_first = False
                        flag_third = True
                        flag_second = False
                    if flag_second and flag_first and img[x, y, 0] == 255 and img[x, y, 1] == 10 and img[
                        x, y, 2] == 130:
                        img[x, y, :3] = [255, 255, 255]
        elif left>0:
            for j in range(left, right):
                if  img[j, down - 1, 0] == img[j, down - 1, 1] == img[j, down - 1, 2] == 255:
                    count += 1
            if count == 1:
                down += 2
            for y in range(down, up):
                flag_first = False
                flag_second = False
                flag_third = False
                for x in range(left, right):
                    if img[x, y, 0] == img[x, y, 1] == img[x, y, 2] == 255 and not flag_third:
                        flag_first = True
                    if flag_first and img[x, y, 0] == 255 and img[x, y, 1] == 10 and img[x, y, 2] == 130:
                        flag_second = True
                    if flag_second and flag_first and img[x, y, 0] == img[x, y, 1] == img[x, y, 2] == 255:
                        flag_first = False
                        flag_third = True
                        flag_second = False
                    if flag_second and flag_first and img[x, y, 0] == 255 and img[x, y, 1] == 10 and img[
                        x, y, 2] == 130:
                        img[x, y, :3] = [255, 255, 255]


def bezier_curve(img, x0, y0, x1, y1, x2, y2,flag=0):
    t = np.linspace(0, 1, petal_quality)
    x_coordinates = np.int32(np.round(x0 * (1 - t) ** 2 + 2 * x1 * (1 - t) * t + x2 * t ** 2))
    y_coordinates = np.int32(np.round(y0 * (1 - t) ** 2 + 2 * y1 * (1 - t) * t + y2 * t ** 2))
    for i in range(petal_quality):
        if flag==1:
            if img[y_coordinates[i], x_coordinates[i], 0] == 255 and img[y_coordinates[i], x_coordinates[i], 1] == 10 and img[y_coordinates[i], x_coordinates[i], 2] == 130:
                img[y_coordinates[i], x_coordinates[i], :3] = [0, 100,0 ]
        else:
            if 0 <= x_coordinates[i] < width and 0 <= y_coordinates[i] < height:
                img[y_coordinates[i], x_coordinates[i], :3] = [255, 255, 255]
    return [y_coordinates, x_coordinates]

width, height = 1000, 1000

petal_quality = 420 # affects points amount in curves. if < 420 may cause holes in curves due to lack of density
img = np.zeros((width, height, 3), dtype=np.uint8)
img[:, :, 0], img[:, :, 1], img[:, :, 2] = 255, 10, 130

radius = height // 8

petals_amount = 8

center_shifting_matrix = diag_matr(1, 1, 1)
center_shifting_matrix[:2, -1] = np.array([-width / 2, -height / 2])

alpha = math.radians(360 / petals_amount)
rotation_matrix = np.zeros((3, 3))
rotation_matrix[:2, :2] = rot_matr(alpha)
rotation_matrix[:2, -1] = np.array([width / 2, height / 2])
rotation_matrix[-1, -1] = 1

tearing_off_matrix = diag_matr(1, 1, 1)

frames_amount = 60
frames = []
fig = plt.figure()

for frame in range(frames_amount):
    img[:, :, 0], img[:, :, 1], img[:, :, 2] = 255, 10, 130
    point1 = np.array([width // 2, height // 2 + radius, 1])
    point2 = np.array([width // 2 - 140, height // 2 + radius + 300 // 2, 1])
    point3 = np.array([width // 2, height // 2 + radius + 300, 1])
    point4 = np.array([width // 2 + 140, height // 2 + radius + 300 // 2, 1])
    points = np.array([point1, point2, point3, point4]).T
    for petal in range(petals_amount):
        tearing_off_flag = frame - petal * 2
        speed = 6
        if tearing_off_flag > 0:
            tearing_off_matrix[:2, -1] = np.array([-tearing_off_flag * speed * math.sin(petal * alpha), tearing_off_flag * speed * math.cos(petal * alpha)])
            points = tearing_off_matrix @ points
            draw_petal(img, points)
            tearing_off_matrix[:2, -1] = np.array([tearing_off_flag * speed * math.sin(petal * alpha), -tearing_off_flag * speed * math.cos(petal * alpha)])
            points = tearing_off_matrix @ points
        else:
            draw_petal(img, points)
        points = center_shifting_matrix @ points
        points = rotation_matrix @ points

    for i in range(0,height//2-radius):
        for petal in range(width // 2 - 10, width // 2 + 10):
            if img[petal, i, 0] == 255 and img[petal, i, 1] == 10 and img[petal, i, 2] == 130:
                img[petal, i] = [0, 100, 0]

    if frame%8==0:
        p3_x = height - height // 4
        p3_y = width // 6-5
    else:
        p3_x=height -height//4
        p3_y=width //6+5
    for petal in range(70, -1, -1):
        point1 = np.array([width // 8, height // 2 , 1])
        point2 = np.array([width // 8 - 70, height // 2+(point3[1]-point1[1])//2, 1])
        point3 = np.array([p3_y, p3_x, 1])
        point4 = np.array([width // 8 + petal, height // 2 + (point3[1] - point1[1]) // 2, 1])
        p = np.array([point1, point2, point3, point4]).T
        bezier_curve(img, p[0][0], p[1][0], p[0][3], p[1][3], p[0][2], p[1][2],1)

    for i in range(height // 2 - radius, height // 2 + radius):
        for petal in range(width // 2 - radius, width // 2 + radius):
            if ((height / 2 - i) ** 2 + (width / 2 - petal) ** 2) ** 0.5 < radius:
                img[petal, i] = [255, 255, 0]


    img = np.transpose(img, axes=(1, 0, 2))
    img = np.flipud(img)
    im = plt.imshow(img)
    plt.show()
    #frames.append([im])
ani = animation.ArtistAnimation(fig, frames, interval=4, blit=True, repeat_delay=0)
writer = PillowWriter(fps=24)
ani.save("flower1.gif", writer=writer)
plt.show()
