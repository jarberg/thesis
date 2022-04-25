from math import floor, ceil

from opengl_interfacing.camera import Camera
from utils import input_manager


class Scene:

    def __init__(self, camera=None):
        self.camera = camera or Camera()
        self.inputMan = input_manager.Input_manager(self)
        self.entities = []
        self.joints = []
        self.animators = []
        self.lights = []
        self.light_cubes = {}
        self.entity_cubes = {}
        self.debug = False
        self.play = False
        self.GPU = False

    def add_entities(self, entity_list):
        for entity in entity_list:
            self.entities.append(entity)
            cube = self.entity_cubes.get(entity, [])
            cube.append(squash_pos(entity.get_position()))
            self.entity_cubes[entity] = cube


    def get_current_camera(self):
        return self.camera

    def add_lights(self, lightList):
        for i, light in enumerate(lightList):
            self.lights.append(light)
            #cube = squash_pos(light)
            #listobj = self.light_cubes.get(str(cube), [])
            #listobj.append(i)
            #self.light_cubes[str(cube)] = listobj

    def add_animator(self, animator):
        self.animators.append(animator)

    def get_lightCube(self, cubeKey):
        return self.light_cubes.get(str(cubeKey), [])

    def get_lightCubes(self):
        return self.light_cubes

    def get_entity_list(self):
        return self.entities

    def get_entityCube_list(self):
        return self.entity_cubes

    def add_joints(self, joint_list):
        for joint in joint_list:
            self.joints.append(joint)

    def get_joints(self):
        return self.joints

    def set_debug(self):
        self.debug = not self.debug

    def set_GPU(self):
        self.GPU = not self.GPU

    def update(self, time_per_frame):
        if self.play:
            for ani in self.animators:
                ani.update(time_per_frame)


cubesize = 5


def squash_pos(pos):
    if pos[0] > 0:
        x = floor(pos[0] / cubesize)
    else:
        x = ceil(pos[0] / cubesize)
    if pos[1] > 0:
        y = floor(pos[1] / cubesize)
    else:
        y = ceil(pos[1] / cubesize)
    if pos[2] > 0:
        z = floor(pos[2] / cubesize)
    else:
        z = ceil(pos[2] / cubesize)

    return [x, y, z]


def check_adjecents(pos, radius):
    basecube = squash_pos(pos)

    radius = int(ceil(radius / cubesize))

    for i in range(-radius, radius):
        for j in range(-radius, radius + 1):
            for k in range(-radius, radius + 1):
                print([basecube[0] + i, basecube[1] + j, basecube[2] + k])


def is_not_same_cube(cube1, cube2):
    truecount = 0
    for i in range(len(cube1)):
        if cube1[i] == cube2[i]:
            truecount += 1

    return truecount != len(cube1)


check_adjecents([30, 30, 30], 5)
