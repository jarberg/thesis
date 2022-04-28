import math

from opengl_interfacing.utils import get_aspect_ratio
from utils.objectUtils import perspective, normalize, Vector, cross, flatten, look_at, Matrix, rotateY, radians
from utils.objects import Transform


class Camera(Transform):

    def __init__(self):
        super().__init__()
        self.mvMatrix = Matrix()
        self.near = 0.001
        self.far = 2000.0
        self.radius = 3
        self.theta = 0.
        self.phi = 0.
        self.fovy = 90.0
        self.aspect = get_aspect_ratio()
        self.pMatrix = flatten(perspective(self.fovy, self.aspect, self.near, self.far))

        self.eye = Vector([0, 1, -1])
        self.up = Vector([0, 1, 0])
        self.at = Vector(super(Camera, self).get_position())

        self.updateEye()

    def set_fovy(self, angle):
        if self.fovy != angle:
            self.fovy = angle
            self.pMatrix = flatten(perspective(self.fovy, self.aspect, self.near, self.far))


    def update_pMatrix(self, aspect = None):
        aspect = aspect or get_aspect_ratio()
        if self.aspect != aspect:
            self.aspect = aspect
            self.pMatrix = flatten(perspective(self.fovy, self.aspect, self.near, self.far))

    def update(self):
        print(self.theta)
        print(self.phi)
        print(self.radius)
        self.mvMatrix = look_at(self.eye, self.at, self.up)
        self.ip_normal = normalize(self.at - self.eye)
        self.ip_x_axis = normalize(cross(self.ip_normal, self.up))
        self.ip_y_axis = cross(self.ip_x_axis, self.ip_normal)

    def updateHorizontal(self, input_h):
        self.phi += input_h
        self.phi %= 360
        self.updateEye()

    def updateVertical(self, input_v):
        self.theta += input_v
        self.theta %= 360
        self.updateEye()

    def adjustDistance(self, input_d):
        self.radius += input_d
        self.updateEye()

    def set_position(self, newPos: list or Vector):
        super().set_position(newPos)
        self.updateEye()

    def updateEye(self):
        zero_pos = super().get_position()

        if self.theta < 90 or self.theta > 270:
            self.up[0] = 0
            self.up[1] = 1
            self.up[2] = 0

        elif self.theta == 90:
            trans = rotateY(-self.phi)*Vector([0, 0, -1, 0])
            self.up[0] = trans[0]
            self.up[1] = trans[1]
            self.up[2] = trans[2]

        else:
            self.up[0] = 0
            self.up[1] = -1
            self.up[2] = 0

        vAngleRadians = radians(-self.theta+90)
        hAngleRadians = radians(self.phi+90)

        self.at[0] = zero_pos[0]
        self.at[1] = zero_pos[1]
        self.at[2] = zero_pos[2]

        self.eye = Vector([zero_pos[0]+self.radius * math.sin(vAngleRadians) * math.cos(hAngleRadians),
                           zero_pos[1]+self.radius * math.cos(vAngleRadians),
                           zero_pos[2]+self.radius * math.sin(vAngleRadians) * math.sin(hAngleRadians)
                           ])

        self.update()


    def _getTransform(self, useParent=False):
        return self.mvMatrix