import math
from collections import OrderedDict
from math import floor, ceil, sqrt

from utils.objectUtils import Matrix, Vector, quaternion_to_matrix, Quaternion, \
    dot, matrix_to_quaternion, length, det4
from utils.objects import Joint, Transform

global time_per_frame


class KeyFrame:
    def __init__(self, transforms: OrderedDict, timestamp: int):
        self.transforms = transforms
        self.timestamp = timestamp

    def getJointKeyFrames(self):
        return self.transforms

    def getTimeStamp(self):
        return self.timestamp


class Animation:
    def __init__(self, keyframes: list):
        self.keyframes = keyframes

    def getAllKeyFrames(self):
        return self.keyframes

    def getNextAndPreviousKeyFrames(self, prev, next):
        if prev < 0 or len(self.keyframes) < next:
            raise Exception("next or previous index was outside keyframe numbers")
        else:
            return (self.keyframes[prev], self.keyframes[next])


class Animator:

    def __init__(self, model, animation: Animation):
        self.model = model
        self.animation = animation
        self.animTime = 0
        self.curPoseList = []
        self.truePoseList =[]

    def doAnimation(self, anim):
        self.animTime = 0
        self.animation = anim

    def update(self, tpf):
        self.tpf = tpf
        if self.animation is not None:
            self.increaseAnimationTime()
            self.curPoseList = []
            curPose = calculateCurrentAnimationPose(self)
            applyPoseToJoints(self, curPose, self.model.rootJoint, Matrix())

    def increaseAnimationTime(self, tpf=None):
        self.animTime += tpf or self.tpf
        if self.animTime > len(self.animation.keyframes) - 1:
            self.animTime %= len(self.animation.keyframes) - 1

def getPreviousAndNextFrames(animator):
    previousFrameID = int(floor(animator.animTime))
    nextFrameID = int(ceil(animator.animTime))
    if previousFrameID == 0 and previousFrameID == nextFrameID:
        nextFrameID = 1
    frames = animator.animation.getNextAndPreviousKeyFrames(previousFrameID, nextFrameID)
    return frames

def calculateProgression(animator, keyframes):
    totalTime = keyframes[1].getTimeStamp() - keyframes[0].getTimeStamp()
    currentTime = animator.animTime - keyframes[0].getTimeStamp()

    if totalTime == 0:
        return 0
    else:
        return currentTime / totalTime

def calculateCurrentAnimationPose(animator):
    frames = getPreviousAndNextFrames(animator)
    progression = calculateProgression(animator, frames)
    return interpolatePoses(frames[0], frames[1], progression)

def applyPoseToJoints(animator, curPose: OrderedDict, rootJoint: Joint, parentTransform):
    curLocalTransform = curPose.get(rootJoint.name)
    curTransform = parentTransform * curLocalTransform
    final = curTransform*rootJoint.inverseBindTransform

    rootJoint.set_transform(curTransform)

    animator.curPoseList.append(final)

    for child in rootJoint.children:
        applyPoseToJoints(animator, curPose, child, curTransform)


def interpolatePoses(prevFrame: KeyFrame, nexFrame: KeyFrame, progression: float):
    curPose = OrderedDict()
    for joint in prevFrame.getJointKeyFrames().keys():
        previousTransform = prevFrame.getJointKeyFrames().get(joint)
        nextTransform = nexFrame.getJointKeyFrames().get(joint)
        curTransform = interpolate(previousTransform, nextTransform, progression)
        curPose[joint] = curTransform

    return curPose


def interpolate(prevTransfrom: Transform, nexTransform: Transform, progression):
    trans = Vector([prevTransfrom.m[0][3], prevTransfrom.m[1][3], prevTransfrom.m[2][3]])
    trans2 = Vector([nexTransform.m[0][3], nexTransform.m[1][3], nexTransform.m[2][3]])

    sx, sy, sz = get_scale(prevTransfrom.m)
    sx1, sy1, sz1 = get_scale(nexTransform.m)

    quat1 = matrix_to_quaternion(prevTransfrom)
    quat2 = matrix_to_quaternion(nexTransform)

    quat3 = slerp(quat1, quat2, progression, True)

    t = Matrix()
    final_pos = trans * (1 - progression) + trans2 * progression
    t[0][3] = final_pos[0]
    t[1][3] = final_pos[1]
    t[2][3] = final_pos[2]

    r = quaternion_to_matrix(quat3)
    det = det4(r)
    r /= det

    sca1 = Vector(sx, sy, sz)
    sca2 = Vector(sx1, sy1, sz1)

    final_sca = sca1 * (1 - progression) + sca2 * progression

    s = Matrix()
    s[0][0] = final_sca[0]
    s[1][1] = final_sca[1]
    s[2][2] = final_sca[2]
    res = t * r * s

    return res


def get_scale(m):
    sx = length(Vector([m[0][0], m[1][0], m[0][2]]))
    sy = length(Vector(m[0][1], m[1][1], m[2][1]))
    sz = length(Vector(m[2][0], m[2][1], m[2][2]))
    return sx, sy, sz


def slerp(a, b, weight, allowFlip):
    cosAngle = dot(a, b)

    # Linear interpolation for close orientations
    if ((1.0 - abs(cosAngle)) < 0.01):
        c1 = 1.0 - weight
        c2 = weight
    else:
        # Spherical interpolation
        angle = math.acos(abs(cosAngle))
        sinAngle = math.sin(angle)
        c1 = (math.sin(angle * (1.0 - weight)) / sinAngle)
        c2 = (math.sin(angle * weight) / sinAngle)

    # Use the shortest path
    if (allowFlip and (cosAngle < 0.0)):
        c1 = -c1

    ret = Quaternion()
    ret.i = c1 * a.i + c2 * b.i
    ret.j = c1 * a.j + c2 * b.j
    ret.k = c1 * a.k + c2 * b.k
    ret.w = c1 * a.w + c2 * b.w

    return ret


def conjungture(q):
    return Quaternion(quats=[-q[0], -q[1], -q[2], q[3]])


def magnitude(q):
    return sqrt(q[0] ** 2 + q[1] ** 2 + q[2] ** 2 + q[3] ** 2)


def inverse(q: Quaternion):
    qk = conjungture(q)
    return qk / magnitude(q)


def power(q, t):
    for i in range(len(q)):
        q[i] = q[i] ** t
    return q
