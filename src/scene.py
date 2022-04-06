from math import floor, ceil

from opengl_interfacing.camera import Camera


class Scene:
    def __init__(self, camera):
        self.camera = camera or Camera()
        self.objects = []
        self.lights = []
        self.cubes = {}


    def get_current_camera(self):
        return self.camera

    def add_lights(self, lightList):
        for light in lightList:
            self.lights.append(light)


cubesize = 10


def squash_pos(pos):
    x = ceil(pos[0] / cubesize)
    y = ceil(pos[1] / cubesize)
    z = ceil(pos[2] / cubesize)
    print(x, y, z)


print(squash_pos([10, -52, 0]))
