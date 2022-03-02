import os
import numpy

import constants
from opengl_interfacing.texture import Texture_Manager
from utils.objects import Transform, Model
from PIL import Image


class ImageRenderer:

    def __init__(self):
        pass

    def draw(self):
        pass

    def bind(self):
        pass

    def unbind(self):
        pass


class Plane(Model):
    def __init__(self, program):
        plane = [[0.5, 0.5,   -1],
                 [0.5, -0.5,  -1],
                 [-0.5, 0.5,  -1],
                 [-0.5, -0.5, -1],
                 [-0.5, 0.5,  -1],
                 [0.5, -0.5,  -1],
                 ]
        self.coordArray = [
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [1.0, 0.0],
            [0.0, 1.0],
        ]
        super().__init__(program, plane,  self.coordArray)


class ImagePlane(Plane):

    def __init__(self, path, program):
        super().__init__(program)
        root = constants.ROOT_DIR
        path = os.path.abspath(root + path).replace("\\", "/")
        im = Image.open(fp=path)
        imdata = numpy.array(list(im.getdata()))

        self.texture = Texture_Manager().createNewTexture(size=[im.size[0], im.size[1]], data=imdata, mipmap = True)

