from opengl_interfacing.camera import Camera
from utils import input_manager
from utils.input_manager import Input_manager


class Scene:

    def __init__(self, camera=None):
        self.camera = camera or Camera()
        self.inputMan = Input_manager(self)
        self.entities = []
        self.light_list = []


    def add_entities(self, entity_list):
        for entity in entity_list:
            self.entities.append(entity)

    def get_current_camera(self):
        return self.camera

    def add_lights(self, lightList):
        for i, light in enumerate(lightList):
            self.light_list.append(light)

    def get_lights(self):
        return self.light_list

    def get_entity_list(self):
        return self.entities


