# creating Occupancy grid using LIDAR sensor
# Its non cascading model i.e. dimensions of actual map will be almost equal to resultant
# That's actually a poor way - more size, slower computation

# TODO Stopping condition
# TODO Increase cell size of resultant map
# TODO Set botL = botW = 60 and edit move_bot()
# TODO Edit move_bot() to move to centroid of unvisited cells
# TODO Get Readings

import numpy
from PIL import Image
from pygame_arena import BLACK, WHITE
import pygame
import pygame.locals
from math import sin, cos, radians

specs = (500, 3, 1, 1, 4000)
# specs[0] - Frequency of LIDAR in Hz
# specs[1] - Time taken for servo motor to complete 1 revolution
# specs[2] - Bot Length (Y Axis, using standard cartesian Coordinates)
# specs[3] - Bot Width (X Axis)
# specs[4] - Max Distance LIDAR can measure, in cm

actual_map = []
coordinates = []

# bot's coordinates
x = 0
y = 0
firstTime = True


# Turns 'jpg' to actual_map array
# Initializes x,y,result_map to some values
def init():
    global actual_map, x, y
    im = Image.open('map.jpg')
    actual_map = numpy.array(im)
    x = actual_map.shape[1] / 2
    y = actual_map.shape[0] / 2


def move_bot():
    global x, y, actual_map, firstTime

    if not firstTime:
        try:
            while x < actual_map.shape[1] and actual_map[y][x] == 255:
                x += 1
            while y < actual_map.shape[0] and actual_map[y][x] == 255:
                y += 1
        except IndexError:
            print "Moved to", x, ",", y
    else:
        firstTime = False


def get_readings():
    global x, y, actual_map
    readings = []
    n = specs[0] * specs[1]

    for i in range(0, n):
        r = 1
        _x = x - int(cos(radians(i * 360 / n)) * r)
        _y = y - int(sin(radians(i * 360 / n)) * r)

        readings.append(0)
        while 0 <= _x < actual_map.shape[1] and 0 <= _y < actual_map.shape[0]:
            if actual_map[_y][_x] != 255:
                readings[i] = r
                break
            r += 1
            _x = x - int(cos(radians(i * 360 / n)) * r)
            _y = y - int(sin(radians(i * 360 / n)) * r)

        # comment these 2 lines to avoid edges.
        # '5' is just for offset
        if _x >= actual_map.shape[1] or _y >= actual_map.shape[0] or _x < 0 or _y < 0:
            readings[i] = r - 1
    return readings


def save_image():
    global coordinates
    pygame.init()
    screen = pygame.display.set_mode((actual_map.shape[1], actual_map.shape[0]))
    screen.fill(BLACK)
    pygame.draw.polygon(screen, WHITE, coordinates)
    pygame.image.save(screen, 'result.jpg')
    pygame.quit()

    im = Image.open('result.jpg')
    im = im.convert('1')
    im.save('result.jpg')  # saving it as  pure BW


def main():
    init()
    done = True

    while done:
        move_bot()

        # This will be actual RasPi Part
        # MOTOR(HIGH)
        # LIDAR(HIGH)
        # WAIT(specs[3]*1000)
        readings = get_readings()
        # MOTOR(LOW)
        # LIDAR(LOW)

        n = len(readings)
        for i in range(0, n):
            if readings[i] < specs[4]:
                a = int(readings[i] * sin(radians(i * 360 / n)))
                b = int(readings[i] * cos(radians(i * 360 / n)))
                coordinates.append((x - b, y - a))

        done = raw_input("Press 'y' to continue").startswith('y')
        save_image()


if __name__ == '__main__':
    main()
