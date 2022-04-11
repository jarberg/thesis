from math import floor, ceil

from opengl_interfacing.camera import Camera
from utils import input_manager


class Scene:

    def __init__(self, camera=None):
        self.camera = camera or Camera()
        self.inputMan = input_manager.Input_manager(self)
        self.entities = []
        self.animators = []
        self.lights = []
        self.cubes = {}
        self.debug = False
        self.GPU = False

    def add_entities(self, entity_list):
        for entity in entity_list:
            self.entities.append(entity)

    def get_current_camera(self):
        return self.camera

    def add_lights(self, lightList):
        for light in lightList:
            self.lights.append(light)

    def add_animator(self, animator):
        self.animators.append(animator)

    def get_entity_list(self):
        return self.entities

    def set_debug(self):
        self.debug = not self.debug

    def set_GPU(self):
        self.GPU = not self.GPU

    def update(self, time_per_frame):
        for ani in self.animators:
            ani.update(time_per_frame)


cubesize = 10


def squash_pos(pos):
    x = ceil(pos[0] / cubesize)
    y = ceil(pos[1] / cubesize)
    z = ceil(pos[2] / cubesize)
    print(x, y, z)

