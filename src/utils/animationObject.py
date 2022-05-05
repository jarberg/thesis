from collections import OrderedDict

from OpenGL.raw.GL.VERSION.GL_1_0 import GL_TRIANGLE_STRIP

from opengl_interfacing.sceneObjects import IndicedModel, Animated_model, Joint
from utils.animator import KeyFrame, Animation, Animator
from utils.objectUtils import Matrix


def get_transformDict(joints):
    odict = OrderedDict()
    for i in range(len(joints)):
        odict[joints[i].name] = joints[i].getTransform()

    return odict



def setup_test_anim_CPU(bones, model):
    key1 = KeyFrame(get_transformDict(bones), 0)

    bones[0].set_position([1, 0, 0])
    bones[0].set_rotation([0, -45, 0])
    bones[1].set_rotation([0, -45, 0])
    bones[2].set_rotation([0, -45, 0])
    bones[3].set_rotation([0, -45, 0])
    key2 = KeyFrame(get_transformDict(bones), 1)

    bones[0].set_position([-1, 0, 0])
    bones[0].set_rotation([90, 0, 0])
    bones[1].set_rotation([90, 0, 0])
    bones[2].set_rotation([90, 0, 0])
    bones[3].set_rotation([90, 0, 0])
    key3 = KeyFrame(get_transformDict(bones), 2)

    bones[0].set_position([0, 0, 1])
    bones[0].set_rotation([0, 45, 0])
    bones[1].set_rotation([0, 45, 0])
    bones[2].set_rotation([0, 45, 0])
    bones[3].set_rotation([0, 45, 0])
    key4 = KeyFrame(get_transformDict(bones), 3)

    bones[0].set_position([0, 0, -1])
    bones[0].set_rotation([0, 0, 90])
    bones[1].set_rotation([0, 0, 90])
    bones[2].set_rotation([0, 0, 90])
    bones[3].set_rotation([0, 0, 90])
    key5 = KeyFrame(get_transformDict(bones), 4)

    bones[0].set_position([0, 0, 0])
    bones[0].set_rotation([0, 0, 0])
    bones[1].set_rotation([0, 0, 0])
    bones[2].set_rotation([0, 0, 0])
    bones[3].set_rotation([0, 0, 0])
    key6 = KeyFrame(get_transformDict(bones), 5)


    anim = Animation([key1, key2, key3, key4, key5, key6])

    animator_obj = Animator(model=model, animation=anim)

    return animator_obj

def init_geo_anim():
    j1 = Joint(0, "joint1", None)
    j2 = Joint(1, "joint2", j1)
    j3 = Joint(2, "joint3", j2)
    j4 = Joint(3, "joint4", j3)
    joint_list = [j1, j2, j3, j4]
    jointPosList = [[-2, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0]]

    j1.set_position(jointPosList[0])
    j2.set_position(jointPosList[1])
    j3.set_position(jointPosList[2])
    j4.set_position(jointPosList[3])

    j1.set_local_bind_transform()
    j2.set_local_bind_transform()
    j3.set_local_bind_transform()
    j4.set_local_bind_transform()

    for key in joint_list:
        for child in key.children:
            key.vertexArray[1] = child.get_position()
            key.initDataToBuffers()
            break

    j1.calcInverseBindTransform(Matrix())

    vertexList = [[-2.0, -0.5, 0.0],
                  [-2.0, 0.5, 0.0],
                  [-1.0, 0.5, 0.0],
                  [-1.0, -0.5, 0.0],
                  [0.0, 0.5, 0.0],
                  [0.0, -0.5, 0.0],
                  [1.0, 0.5, 0.0],
                  [1.0, -0.5, 0.0],
                  [2.0, -0.5, 0.0],
                  [2.0, 0.5, 0.0]]
    indiceList = [0, 1, 3, 2, 5, 4, 7, 6, 8, 9]
    normalList = [[0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1],
                  [0, 0, -1], ]
    weightList = [[1, 0, 0, 0],
                  [1, 0, 0, 0],
                  [1, 0, 0, 0],
                  [1, 0, 0, 0],
                  [1, 0, 0, 0],
                  [1, 0, 0, 0],
                  [0.5, 0.5, 0, 0],
                  [0.5, 0.5, 0, 0],
                  [1, 0, 0, 0],
                  [1, 0, 0, 0]]
    windices = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [1, 0, 0, 0],
                [1, 0, 0, 0],
                [2, 0, 0, 0],
                [2, 0, 0, 0],
                [2, 3, 0, 0],
                [2, 3, 0, 0],
                [3, 0, 0, 0],
                [3, 0, 0, 0]]

    model = IndicedModel(vertexlist=vertexList,
                         indices=indiceList,
                         n_array=normalList,
                         windices=windices,
                         weights=weightList,
                         renderType=GL_TRIANGLE_STRIP)

    model.set_position([0, 2, 0])
    animated = Animated_model(model, j1, 4)

    animator = setup_test_anim_CPU(joint_list, animated)
    return animator, animated, joint_list
