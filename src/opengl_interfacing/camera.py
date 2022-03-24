import math

from OpenGL import GL

from utils.objectUtils import perspective, scale, normalize, Vector, cross, flatten, look_at, Matrix, rotateY
from utils.objects import Transform


class Camera(Transform):

    def __init__(self):
        super().__init__()
        self.mvMatrix = Matrix()
        self.near = 0.1
        self.far = 500.0
        self.radius = 8.
        self.theta = 0.
        self.phi = 0.
        self.fovy = 90.0
        self.aspect = 1

        self.pMatrix = perspective(self.fovy,
                                   self.aspect,
                                   self.near,
                                   self.far)

        self.eye_position = Matrix()

        self.eye = Vector([1, 1, 0])
        self.up = Vector([0, 1, 0])
        self.at = Vector([0, 0, 0])

        self.ip_normal = normalize(self.at - self.eye)
        self.ip_x_axis = normalize(cross(self.ip_normal, self.up))
        self.ip_y_axis = normalize(cross(self.ip_x_axis, self.ip_normal))

    def set_fovy(self, angle):
        if self.fovy != angle:
            self.fovy = angle
            self.pMatrix = perspective(self.fovy,
                                       self.aspect,
                                       self.near,
                                       self.far)


    def update(self):
        self.mvMatrix = look_at(self.eye, self.at, self.up)
        self.ip_normal = normalize(self.at - self.eye)
        self.ip_x_axis = normalize(cross(self.ip_normal, self.up))
        self.ip_y_axis = cross(self.ip_x_axis, self.ip_normal)

    def updateHorizontal(self, input_h):
        self.phi += input_h
        self.updateEye()

    def updateVertical(self, input_v):
        self.theta += input_v
        self.updateEye()

    def adjustDistance(self, input_d):
        self.radius += input_d * 0.01
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

        vAngleRadians = ((-self.theta + 90) / 180) * math.pi
        hAngleRadians = ((self.phi + 90) / 180) * math.pi

        self.at[0] = zero_pos[0]
        self.at[1] = zero_pos[1]
        self.at[2] = zero_pos[2]

        self.eye[0] = zero_pos[0] + -self.radius * math.sin(vAngleRadians) * math.cos(hAngleRadians)
        self.eye[1] = zero_pos[1] + -self.radius * math.cos(vAngleRadians)
        self.eye[2] = zero_pos[2] + -self.radius * math.sin(vAngleRadians) * math.sin(hAngleRadians)

        self.ip_normal = normalize(self.at - self.eye)
        self.ip_x_axis = normalize(cross(self.ip_normal, self.up))
        self.ip_y_axis = cross(self.ip_x_axis, self.ip_normal)

        self.mvMatrix = look_at(self.eye, self.at, self.up)

    def getTransform(self, useParent=False):
        return self.mvMatrix.m