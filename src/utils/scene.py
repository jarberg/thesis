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

    def get_current_camera(self):
        return self.camera

    def add_lights(self, lightList):
        for i, light in enumerate(lightList):
            self.lights.append(light)

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


