import random

from utils import constants

from utils.objectUtils import cross
from utils.objectUtils import dot
from utils.objectUtils import sub
from utils.objectUtils import normalize


class Node:

    def __init__(self, elements=None):
        self.left = None
        self.right = None
        self.elements = elements or []
        self.partition = None


def classify_poly(partition, poly):
    plane_normal = get_plane(partition)
    dotArray = [dot(poly[0], plane_normal),
                dot(poly[1], plane_normal),
                dot(poly[2], plane_normal)]

    front = False
    back = False
    span = False
    plane = False

    for i in range(len(dotArray)):
        if abs(dotArray[i]) <= constants.EPSILON:
            plane = True
            # point is on the same plane as the normal
        elif dotArray[i] > 0:
            back = True
            if front:
                span = True

            # point is behind normal
        elif dotArray[i] < 0:
            front = True
            if back:
                span = True
            # point is in front of normal

    if span:
        return 3
    elif plane and not back and plane and not front:
        return 0
    elif front and not back:
        return 1
    elif back and not front:
        return 2


def get_plane(poly):
    return cross(sub(poly[1], poly[0]), sub(poly[2], poly[0]))


class BSP_tree:

    def build_tree(self, poly_array, node, make_root=False):

        rand_id = random.randrange(0, len(poly_array))

        if make_root:
            pol = poly_array.pop(rand_id)

            self.root = node
            self.root.elements.append(pol)

            node.partition = get_plane(pol)
            if len(poly_array) > 0:
                poly = poly_array.pop()
            else:
                poly = None

        else:
            if len(poly_array) > 0:
                poly = poly_array.pop()
            else:
                poly = None
            node.partition = get_plane(poly)
            node.elements.append(poly)
            if len(poly_array) > 0:
                poly = poly_array.pop()
            else:
                poly = None

        backList = []
        frontList = []

        while poly is not None:
            res = classify_poly(node.elements[0], poly)

            if res == 0:
                node.elements.append(poly)
            elif res == 1:
                backList.append(poly)
            elif res == 2:
                frontList.append(poly)
            elif res == 3:
                polygon_split(poly, node.elements[0], frontList, backList)

            if len(poly_array) > 0:
                poly = poly_array.pop()
            else:
                poly = None

        if len(backList) > 0:
            node.left = Node()
            self.build_tree(backList, node.left)

        if len(frontList) > 0:
            node.right = Node()
            self.build_tree(frontList, node.right)

    def traverse(self, V, N):
        if N == None:
            return N

        # if v infront of N
        # Yield child tree behind N
        # Yield N
        # Yield child tree in front of N

    def add_polygons(self, poly_list):
        pass



def classify_point(planeNorm, point, knownPoint):
    D = planeNorm[0] * knownPoint[0] + planeNorm[1] * knownPoint[1] + planeNorm[2] * knownPoint[2]
    dist = planeNorm[0] * point[0] + planeNorm[1] * point[1] + planeNorm[2] * point[2] - D

    return dist


def polygon_split(poly, plane, front, back):
    ptA = poly[-1]
    ptK = plane[1]
    plane_normal = get_plane(plane)
    sideA = classify_point(plane_normal, ptA, ptK)

    for i in range(len(poly)):

        ptB = poly[i]
        sideB = classify_point(plane_normal, ptB, ptK)

        if sideB > 0:
            if sideA < 0:

                v = normalize(sub(ptB, ptA))
                sect = (-sideA) / (dot(v, plane_normal))
                cutPoint = (v * sect) + ptA
                front.append(cutPoint)
                back.append(cutPoint)
            front.append(ptB)

        elif sideB < 0:
            if sideA > 0:

                v = normalize(sub(ptB, ptA))
                sect = (-sideA) / (dot(v, plane_normal))
                cutPoint = (v * sect) + ptA
                front.append(cutPoint)
                back.append(cutPoint)
            back.append(ptB)

        else:
            front.append(ptB)
            back.append(ptB)

        ptA = ptB
        sideA = sideB



tree = BSP_tree()

tree.build_tree([[[1, 0, 0], [0, 1, 0], [0, 1, 1.29]],
                [[-1, 0, 0], [0, -1, 0], [0, 0, 0.5]],
                [[2, 0, 0], [0, 2, 0], [0, 0, 2]]],
                Node(),
                True)


