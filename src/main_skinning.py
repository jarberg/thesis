import math
import time
from collections import OrderedDict
import json
import numpy
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image, ImageOps

from opengl_interfacing.animator import Animator, Animation, KeyFrame
from opengl_interfacing.camera import Camera
from opengl_interfacing.framebuffer import G_Buffer
from opengl_interfacing.initshader import initShaders
from opengl_interfacing.renderer import ImagePlane, Renderer, Cube
from utils.objectUtils import flatten, Matrix, Vector, det4
from utils.objects import Joint, Animated_model, Transform, Model, IndicedModel, set_bind_transform_from_self, \
    calcInverseBindTransform

width, height = 200, 200
aspectRatio = width / height
program = None
postProgram = None
window = None

global renderer
global t2
global blit
global target
global count, cube, animator
count = 0


def make_charlie(jointDict):
    f = open("res/models/charlie.txt")
    data = json.load(f)

    lists = [[], [], [], [], []]

    for i in data["indices"]:
        lists[1].append(int(data["indices"][i]))

    for i, k in enumerate(data["vertex"]):

        if (i + 1) % 3 == 0 and i != 0:
            ret = []
            ret.append(float(data["vertex"][str(int(k) - 2)]))
            ret.append(float(data["vertex"][str(int(k) - 1)]))
            ret.append(float(data["vertex"][k]))
            lists[0].append(ret)

    for i, k in enumerate(data["normals"]):

        if (i + 1) % 3 == 0 and i != 0:
            ret = []
            ret.append(float(data["normals"][str(int(k) - 2)]))
            ret.append(float(data["normals"][str(int(k) - 1)]))
            ret.append(float(data["normals"][k]))
            lists[2].append(ret)

    for i, k in enumerate(data["weights"]):
        res = []
        res2 = []
        for d in data["weights"][k]:
            res.append(float(data["weights"][k][d]))
            bone = jointDict.get(d)
            if bone:
                res2.append(bone.id)

        for i in range(4 - len(res2)):
            res2.append(-1)

        for i in range(4 - len(res)):
            res.append(-1)
        lists[3].append(res)
        lists[4].append(res2)

    return IndicedModel(vertexlist=lists[0], indices=lists[1], n_array=lists[2], weights=lists[3], windices=lists[4],
                        renderType=GL_TRIANGLES)


def update_persp_event(w, h):
    global renderer, buffer, cam
    glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
    cam.update_pMatrix()
    # buffer.resize(w, h)

    clear_framebuffer()


def buttons(key, x, y):
    # print(key, x, y)
    if key == b'd':
        global debug
        debug = not debug


def on_click(button, state, x, y):
    global buttonPressed, cam, dragx_start, dragy_start, dragx_mid_start, dragy_mid_start
    buttonPressed = -1
    print(button)
    if button == 0:
        buttonPressed = 0
        if state == 0:
            dragx_start = x
            dragy_start = y
    elif (button == 1):
        buttonPressed = 1
        if state == 0:
            dragx_mid_start = x
            dragy_mid_start = y
    elif button == 3:
        cam.adjustDistance(-3)
    elif button == 4:
        cam.adjustDistance(3)
        # scrool backward


def mouseControl(mx, my):
    global cam, dragx_start, dragy_start, buttonPressed, dragy_mid_start, dragx_mid_start
    if buttonPressed == 0:
        ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)

        deltax = ((mx - dragx_start) * ratio) / glutGet(GLUT_WINDOW_WIDTH)
        deltay = (my - dragy_start) / glutGet(GLUT_WINDOW_HEIGHT)

        cam.updateHorizontal(-deltax * 100)
        cam.updateVertical(-deltay * 100)

        dragx_start = mx
        dragy_start = my

    if buttonPressed == 1:
        ratio = glutGet(GLUT_WINDOW_WIDTH) / glutGet(GLUT_WINDOW_HEIGHT)
        deltax = ((mx - dragx_mid_start) * ratio) / glutGet(GLUT_WINDOW_WIDTH)
        deltay = (my - dragy_mid_start) / glutGet(GLUT_WINDOW_HEIGHT)
        campos = cam.get_position()

        camDirx = cam.ip_x_axis
        camDiry = cam.ip_y_axis

        diry = camDiry * deltay * -100

        dir = camDirx * deltax * 100
        pos = Vector(campos) + dir + diry

        newpos = [pos[0], pos[1], pos[2]]
        cam.set_position(newpos)

        dragx_mid_start = mx
        dragy_mid_start = my


def joint_setup():
    global mod
    joint_list = []
    joint_pos_dict = {"hips_bind": [0.0, 32.750671463853806, 0.12837982177734375],
                      "spine_bind": [-1.6684639585398346e-33, 3.932319061167931, -4.440892098500626e-16],
                      "torso_bind": [-4.065110481311791e-15, 4.576907512213921, -2.0261570199409107e-15],
                      "neck_bind": [-1.0116990564111588e-14, 11.390718733660947, -5.051514762044462e-15],
                      "head_bind": [-2.7733661207514518e-15, 3.1229999999999976, -1.3877787807814457e-15],
                      "L_eyeBallholder_bind": [-9.827746212482468, 19.046114030360776, -10.123785257339488],
                      "L_eyeBall_bind": [0.0, 0.0, 0.0],
                      "L_lo_eyeLid_bind": [0.0, 0.0, 0.0],
                      "L_lo_eyeLidEnd_bind": [-6.154634371570738, -0.1805786973121002, -6.011081638677995],
                      "L_up_eyeLid_bind": [0.0, 0.0, 0.0],
                      "L_up_eyeLidEnd_bind": [-6.154137418399465, -0.06449671295440851, -6.011556327146041],
                      "nose_base_bind": [4.376228694457804e-15, 21.251864500342357, -19.708781917648228],
                      "nose_mid_bind": [1.6702765584326323e-14, -8.650566531378786, -1.3079150081340671],
                      "nose_tip_bind": [1.5990002469944898e-14, -8.982434347689107, -1.1112982178487627],
                      "hair01_base_bind": [-5.64954203296829, 32.04880256889815, -6.550948176199717],
                      "hair01_mid_bind": [-2.705442593294525, 4.1731256295357895, -4.88919816323379],
                      "hair01_tip_bind": [-3.5607206158148355, -0.5098526576320239, -6.906157665956043],
                      "hair03_base_bind": [7.334651990320951, 31.26162735154268, -8.135527001327462],
                      "hair03_mid_bind": [1.992392179129931, 3.7475059247209543, -3.7600273042432146],
                      "hair03_tip_bind": [2.23763057624598, -0.2864475044211332, -3.777952027838209],
                      "hair02_base_bind": [1.788482072050835, 32.57450861325648, 1.0414075093037873],
                      "hair02_mid_bind": [0.9882062827644031, 5.576935029511745, -0.8740821435613294],
                      "hair02_tip_bind": [2.5303088839852736, 3.2756207505880326, -2.7200822156558844],
                      "R_eyeBallholder_bind": [9.827750000000016, 19.046150572108836, -10.12378982177734],
                      "R_eyeBall_bind": [0.0, 0.0, 1.7763568394002505e-15],
                      "R_lo_eyeLid_bind": [0.0, 0.0, 1.7763568394002505e-15],
                      "R_lo_eyeLidEnd_bind": [6.15465, -0.18059999999999832, -6.011089999999999],
                      "R_up_eyeLid_bind": [0.0, 0.0, 1.7763568394002505e-15],
                      "R_up_eyeLidEnd_bind": [6.154149999999998, -0.06449999999999534, -6.011590000000002],
                      "L_eyebrow01_bind": [-18.444005966186506, 28.39803511190376, -8.602426052093502],
                      "L_eyebrow02_bind": [3.814584732055664, 0.0, -3.2660746574401838],
                      "L_eyebrow03_bind": [4.550272464752197, 0.0, -3.895988941192625],
                      "L_eyebrow04_bind": [3.814584732055664, 0.0, -3.2660756111145],
                      "R_eyebrow01_bind": [18.444000000000017, 28.398050572108836, -8.602429821777342],
                      "R_eyebrow02_bind": [-3.814599999999997, -1.4210854715202004e-14, -3.2660500000000017],
                      "R_eyebrow03_bind": [-4.550300000000002, 1.4210854715202004e-14, -3.8959999999999972],
                      "R_eyebrow04_bind": [-3.814539999999999, -1.4210854715202004e-14, -3.2661000000000016],
                      "lo_jaw_bind": [0.252361774444576, -5.105976067837844, -13.685051554266597],
                      "lo_teeth_bind": [5.551115123125783e-17, -1.5256660791973786, 1.8778952925205505],
                      "lo_teeth_end_bind": [-1.1657341758564144e-15, 5.256999999999998, 0.0],
                      "R_loLip02_bind": [10.067609786987322, 6.13340060782361, 0.9411388574282249],
                      "R_loLip01_bind": [5.243923664093037, 6.499824756948598, -1.6090458692868594],
                      "loLip_bind": [-0.2523617744445608, 6.499824756948598, -3.008666879113518],
                      "L_loLip01_bind": [-5.748651774444561, 6.499824756948598, -1.6090282675105048],
                      "L_loLip02_bind": [-10.572361774444568, 6.13340060782361, 0.9411717324893996],
                      "up_jaw_bind": [0.2523617744445743, 5.943997269853725, -16.315869509344214],
                      "up_teeth_bind": [3.9968028886505635e-15, 1.1302159902993552, 4.508713247598163],
                      "up_teeth_end_bind": [-1.7763568394002505e-15, -5.25655502254439, 1.7763568394002505e-15],
                      "R_upLip03_bind": [11.553838253021263, -4.778134212869453, 5.122050940160872],
                      "R_upLip02_bind": [8.39050912857058, -4.811983929055984, 2.017318426733137],
                      "R_upLip01_bind": [3.9616878032684553, -4.811983929055984, 0.5587403169919298],
                      "upLip_bind": [-0.2523617744445698, -4.652727947610671, -0.4148858197878553],
                      "L_upLip01_bind": [-4.466411774444558, -4.812014040750306, 0.5587896875668772],
                      "L_upLip02_bind": [-8.895231774444557, -4.812014040750306, 2.017289687566885],
                      "L_upLip03_bind": [-12.058561774444557, -4.812014040750306, 5.122089687566881],
                      "L_lipEdge_grp_bind": [2.1371793224034263e-15, 0.0, 1.7763568394002505e-15],
                      "L_lipEdge_bind": [-13.592408180236808, 1.317181553296777, -9.244866371154759],
                      "R_lipEdge_grp_bind": [2.1371793224034263e-15, 0.0, 1.7763568394002505e-15],
                      "R_lipEdge_bind": [14.09710000000001, 1.3170657711198928, -9.244869821777325],
                      "tounge01_bind": [-1.0497865758750666e-14, 9.619400683505603, 8.73255613132332],
                      "tounge02_bind": [1.0729152437861136e-15, 0.09607696533202414, -4.831980692115271],
                      "tounge03_bind": [-1.0745742090238892e-15, -7.105427357601002e-15, -5.098042595090997],
                      "tounge04_bind": [-1.2005695767570486e-15, -7.105427357601002e-15, -5.6957954036860095],
                      "L_clavical_bind": [-0.36676163657193683, 9.316933780391288, 0.0],
                      "L_upArm_bind": [-18.294881133761265, 0.0, 4.45017727738191],
                      "L_loArm_bind": [-13.708669790363619, -1.4210854715202004e-14, 1.9040990786899243],
                      "L_wrist_bind": [-12.642666909437388, 0.0, -1.9040990786899288],
                      "L_index_clav_bind": [-5.085630290128343, 0.4743634273553283, -4.34570411339679],
                      "L_index_base_bind": [-5.100140813857344, 0.011719853023237192, -0.08912469122776517],
                      "L_index_mid_bind": [-3.902183966140484, 0.008967011739848374, -0.06819045861463023],
                      "L_index_tip_bind": [-3.5692965559514604, 0.008202054131210446, -0.06237326871154168],
                      "L_long_clav_bind": [-5.25463387435893, 0.5310865869112007, -1.0848403678218146],
                      "L_long_base_bind": [-5.341922126441872, 0.012275453652833335, -0.09334980688931527],
                      "L_long_mid_bind": [-3.9738457250930708, 0.009131686660190041, -0.06944274406568107],
                      "L_long_tip_bind": [-3.6852262737035204, 0.008468454472414066, -0.06439913440346823],
                      "L_pinky_clav_bind": [-5.181320800048162, 0.592678531376265, 2.494596726386237],
                      "L_pinky_base_bind": [-5.12370499751907, 0.011774002267188166, -0.08953647409210941],
                      "L_pinky_mid_bind": [-3.3838280427618344, 0.007775857327153801, -0.05913221624390008],
                      "L_pinky_tip_bind": [-2.675770020400961, 0.006148777554884077, -0.04675893971732492],
                      "L_thumb_base_bind": [-3.1965429256060744, -1.2487172005072793, -3.1325791369403873],
                      "L_thumb_mid_bind": [-1.024224454095389, -0.09535456789081564, -5.678726748934432],
                      "L_thumb_tip_bind": [-0.2802069976543251, -0.06345869939264759, -3.718748569815288],
                      "L_loArm_twist01_bind": [-3.4195545952852413, -1.4210854715202004e-14, -0.5150156055722821],
                      "L_loArm_twist02_bind": [-6.584244977715265, 0.0, -0.9916463738024994],
                      "L_loArm_twist03_bind": [-9.592003378157322, 7.105427357601002e-15, -1.4446417774011238],
                      "R_clavical_bind": [0.3773116540839474, 9.316933780391288, 0.0],
                      "R_upArm_bind": [18.654388345916054, -3.1817626947372446e-05, 4.358700178222657],
                      "R_loArm_bind": [13.708599999999993, 1.4210854715202004e-14, 1.9041000000000006],
                      "R_wrist_bind": [12.642700000000005, 0.0, -1.9041000000000015],
                      "R_index_clav_bind": [5.0869840063230995, 0.5361000000000047, -4.336981655033128],
                      "R_index_base_bind": [5.100123108235273, 7.105427357601002e-15, -0.08902297930640468],
                      "R_index_mid_bind": [3.902205584665573, 0.0, -0.0681132513158535],
                      "R_index_tip_bind": [3.569256302177706, 7.105427357601002e-15, -0.0623016000172527],
                      "R_long_clav_bind": [5.256028288615674, 0.5361000000000047, -1.0756241639958155],
                      "R_long_base_bind": [5.341886280924662, 7.105427357601002e-15, -0.09324297115025404],
                      "R_long_mid_bind": [3.973894664408462, 0.0, -0.06936458884771435],
                      "R_long_tip_bind": [3.685238634816116, 7.105427357601002e-15, -0.06432607914829669],
                      "R_pinky_clav_bind": [5.182796109468441, 0.5361000000000047, 2.5043391594947124],
                      "R_pinky_base_bind": [5.123719513841031, 7.105427357601002e-15, -0.0894348560951359],
                      "R_pinky_mid_bind": [3.3837845547257572, 0.0, -0.05906417864821201],
                      "R_pinky_tip_bind": [2.675792401783852, 7.105427357601002e-15, -0.04670612974569188],
                      "R_thumb_base_bind": [3.193346151537213, -1.202699999999993, -3.153731903136738],
                      "R_thumb_mid_bind": [1.0241341903137737, 0.0, -5.679548628749497],
                      "R_thumb_tip_bind": [0.2801320102087601, 7.105427357601002e-15, -3.719295444362606],
                      "R_loArm_twist03_bind": [3.419435823494254, 3.181762686210732e-05, -0.5149977174748228],
                      "R_loArm_twist02_bind": [6.584737752645509, 3.1817626840791036e-05, -0.9917205901286383],
                      "R_loArm_twist01_bind": [9.591824027731107, 3.1817626840791036e-05, -1.444614765617632],
                      "pelvis_bind": [1.1093356479670479e-31, -1.4109367456279713, 1.6653345369377348e-16],
                      "L_upLeg_bind": [-10.536461353302, -5.589452430628182, -0.12837982177734367],
                      "L_loLeg_bind": [3.552713678800501e-15, -8.241555213928223, -0.5627865195274334],
                      "L_ankle_bind": [0.0, -8.87046432495117, 0.5627865195274349],
                      "L_foot_bind": [-1.7763568394002505e-15, -7.07848065158314, -8.939351195574032],
                      "L_bigToe_bind": [2.400537736178947, 2.220446049250313e-16, -0.20114514724602373],
                      "L_toes_bind": [-1.645695604861885, -2.220446049250313e-16, 0.1416901535959365],
                      "penis_bind": [-1.7073931939410512e-15, -6.664884254358647, -7.785037517547608],
                      "R_upLeg_bind": [10.5365, -5.5894347182258315, -0.12837982177734367],
                      "R_loLeg_bind": [5.329070518200751e-15, -8.241599999999998, -0.5627869999999997],
                      "R_ankle_bind": [-3.552713678800501e-15, -8.87044, 0.5627869999999994],
                      "R_foot_bind": [3.552713678800501e-15, -7.078480000000002, -8.939349999999997],
                      "R_bigToe_bind": [-2.4005800000000033, -1.5543122344752192e-15, -0.20115000000000371],
                      "R_toes_bind": [1.6456999999999962, -6.661338147750939e-16, 0.1416899999999952]
                      }
    parentdict = {"hips_bind": None,
                  "spine_bind": "hips_bind",
                  "torso_bind": "spine_bind",
                  "neck_bind": "torso_bind",
                  "head_bind": "neck_bind",
                  "L_eyeBallholder_bind": "head_bind",
                  "L_eyeBall_bind": "L_eyeBallholder_bind",
                  "L_lo_eyeLid_bind": "L_eyeBallholder_bind",
                  "L_lo_eyeLidEnd_bind": "L_lo_eyeLid_bind",
                  "L_up_eyeLid_bind": "L_eyeBallholder_bind",
                  "L_up_eyeLidEnd_bind": "L_up_eyeLid_bind",
                  "nose_base_bind": "head_bind",
                  "nose_mid_bind": "nose_base_bind",
                  "nose_tip_bind": "nose_mid_bind",
                  "hair01_base_bind": "head_bind",
                  "hair01_mid_bind": "hair01_base_bind",
                  "hair01_tip_bind": "hair01_mid_bind",
                  "hair03_base_bind": "head_bind",
                  "hair03_mid_bind": "hair03_base_bind",
                  "hair03_tip_bind": "hair03_mid_bind",
                  "hair02_base_bind": "head_bind",
                  "hair02_mid_bind": "hair02_base_bind",
                  "hair02_tip_bind": "hair02_mid_bind",
                  "R_eyeBallholder_bind": "head_bind",
                  "R_eyeBall_bind": "R_eyeBallholder_bind",
                  "R_lo_eyeLid_bind": "R_eyeBallholder_bind",
                  "R_lo_eyeLidEnd_bind": "R_lo_eyeLid_bind",
                  "R_up_eyeLid_bind": "R_eyeBallholder_bind",
                  "R_up_eyeLidEnd_bind": "R_up_eyeLid_bind",
                  "L_eyebrow01_bind": "head_bind",
                  "L_eyebrow02_bind": "L_eyebrow01_bind",
                  "L_eyebrow03_bind": "L_eyebrow02_bind",
                  "L_eyebrow04_bind": "L_eyebrow03_bind",
                  "R_eyebrow01_bind": "head_bind",
                  "R_eyebrow02_bind": "R_eyebrow01_bind",
                  "R_eyebrow03_bind": "R_eyebrow02_bind",
                  "R_eyebrow04_bind": "R_eyebrow03_bind",
                  "lo_jaw_bind": "head_bind",
                  "lo_teeth_bind": "lo_jaw_bind",
                  "lo_teeth_end_bind": "lo_teeth_bind",
                  "R_loLip02_bind": "lo_jaw_bind",
                  "R_loLip01_bind": "lo_jaw_bind",
                  "loLip_bind": "lo_jaw_bind",
                  "L_loLip01_bind": "lo_jaw_bind",
                  "L_loLip02_bind": "lo_jaw_bind",
                  "up_jaw_bind": "head_bind",
                  "up_teeth_bind": "up_jaw_bind",
                  "up_teeth_end_bind": "up_teeth_bind",
                  "R_upLip03_bind": "up_jaw_bind",
                  "R_upLip02_bind": "up_jaw_bind",
                  "R_upLip01_bind": "up_jaw_bind",
                  "upLip_bind": "up_jaw_bind",
                  "L_upLip01_bind": "up_jaw_bind",
                  "L_upLip02_bind": "up_jaw_bind",
                  "L_upLip03_bind": "up_jaw_bind",
                  "L_lipEdge_grp_bind": "head_bind",
                  "L_lipEdge_bind": "L_lipEdge_grp_bind",
                  "R_lipEdge_grp_bind": "head_bind",
                  "R_lipEdge_bind": "R_lipEdge_grp_bind",
                  "tounge01_bind": "torso_bind",
                  "tounge02_bind": "tounge01_bind",
                  "tounge03_bind": "tounge02_bind",
                  "tounge04_bind": "tounge03_bind",
                  "L_clavical_bind": "torso_bind",
                  "L_upArm_bind": "L_clavical_bind",
                  "L_loArm_bind": "L_upArm_bind",
                  "L_wrist_bind": "L_loArm_bind",
                  "L_index_clav_bind": "L_wrist_bind",
                  "L_index_base_bind": "L_index_clav_bind",
                  "L_index_mid_bind": "L_index_base_bind",
                  "L_index_tip_bind": "L_index_mid_bind",
                  "L_long_clav_bind": "L_wrist_bind",
                  "L_long_base_bind": "L_long_clav_bind",
                  "L_long_mid_bind": "L_long_base_bind",
                  "L_long_tip_bind": "L_long_mid_bind",
                  "L_pinky_clav_bind": "L_wrist_bind",
                  "L_pinky_base_bind": "L_pinky_clav_bind",
                  "L_pinky_mid_bind": "L_pinky_base_bind",
                  "L_pinky_tip_bind": "L_pinky_mid_bind",
                  "L_thumb_base_bind": "L_wrist_bind",
                  "L_thumb_mid_bind": "L_thumb_base_bind",
                  "L_thumb_tip_bind": "L_thumb_mid_bind",
                  "L_loArm_twist01_bind": "L_loArm_bind",
                  "L_loArm_twist02_bind": "L_loArm_bind",
                  "L_loArm_twist03_bind": "L_loArm_bind",
                  "R_clavical_bind": "torso_bind",
                  "R_upArm_bind": "R_clavical_bind",
                  "R_loArm_bind": "R_upArm_bind",
                  "R_wrist_bind": "R_loArm_bind",
                  "R_index_clav_bind": "R_wrist_bind",
                  "R_index_base_bind": "R_index_clav_bind",
                  "R_index_mid_bind": "R_index_base_bind",
                  "R_index_tip_bind": "R_index_mid_bind",
                  "R_long_clav_bind": "R_wrist_bind",
                  "R_long_base_bind": "R_long_clav_bind",
                  "R_long_mid_bind": "R_long_base_bind",
                  "R_long_tip_bind": "R_long_mid_bind",
                  "R_pinky_clav_bind": "R_wrist_bind",
                  "R_pinky_base_bind": "R_pinky_clav_bind",
                  "R_pinky_mid_bind": "R_pinky_base_bind",
                  "R_pinky_tip_bind": "R_pinky_mid_bind",
                  "R_thumb_base_bind": "R_wrist_bind",
                  "R_thumb_mid_bind": "R_thumb_base_bind",
                  "R_thumb_tip_bind": "R_thumb_mid_bind",
                  "R_loArm_twist03_bind": "R_loArm_bind",
                  "R_loArm_twist02_bind": "R_loArm_bind",
                  "R_loArm_twist01_bind": "R_loArm_bind",
                  "pelvis_bind": "hips_bind",
                  "L_upLeg_bind": "pelvis_bind",
                  "L_loLeg_bind": "L_upLeg_bind",
                  "L_ankle_bind": "L_loLeg_bind",
                  "L_foot_bind": "L_ankle_bind",
                  "L_bigToe_bind": "L_foot_bind",
                  "L_toes_bind": "L_foot_bind",
                  "penis_bind": "pelvis_bind",
                  "R_upLeg_bind": "pelvis_bind",
                  "R_loLeg_bind": "R_upLeg_bind",
                  "R_ankle_bind": "R_loLeg_bind",
                  "R_foot_bind": "R_ankle_bind",
                  "R_bigToe_bind": "R_foot_bind",
                  "R_toes_bind": "R_foot_bind", }
    joint_dict = OrderedDict()

    # create base joint with parent refference
    for i, key in enumerate(joint_pos_dict.keys()):
        parent = None
        if parentdict[key] is not None:
            parent = parentdict[key]

        realParent = joint_dict.get(parent, None)
        jj = Joint(i, name=key, parent=realParent)
        joint_dict[key] = jj
        joint_dict[key].set_position(joint_pos_dict[key])
        joint_list.append(jj)

    #setup joint visual for debug rendering
    for each in joint_dict:
        for child in joint_dict[each].children:
            joint_dict[each].vertexArray[1] = Vector(child.get_position()).elements
            joint_dict[each].initDataToBuffers()
            break

    # set all joint bindposes
    for each in joint_dict.keys():
        parent = parentdict.get(each,  joint_dict[each].getTransform())
        parent = joint_dict.get(parent, Transform())
        joint_dict[each].set_bind_transform(parent.getTransform())

    mod = make_charlie(joint_dict)

    return joint_dict, joint_list


def init():
    global start_time
    global fps_counter

    global renderer, debug, cube, program, lightProgram, jointProgram, animator, time_per_frame
    global blit
    global target
    global buffer, bbj, joint, joint2
    debug = False

    time_per_frame = 0
    fps_counter = 0
    start_time = time.time()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow("Opengl Window In Python")

    glutReshapeFunc(update_persp_event)
    GL.glLineWidth(1)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    GL.glEnable(GL.GL_BLEND)
    glEnable(GL_DEPTH_TEST)

    glDisable(GL_CULL_FACE)
    glutDisplayFunc(render)
    glutIdleFunc(render)

    program = initShaders("/shader/skinning/skinning_v_cpu_interpolate.glsl", "/shader/skinning/skinning_f.glsl")
    jointProgram = initShaders("/shader/debug/joint_v_shader.glsl", "/shader/debug/joint_f_shader.glsl")
    glUseProgram(program)

    cube = Cube()
    cube2 = Cube()
    t = ImagePlane("/res/images/box.png")
    t2 = ImagePlane("/res/images/box.png")
    cube.material.set_tex_diffuse(t.get_material().tex_diffuse)
    cube.set_position([1, 0, 0])

    glutKeyboardFunc(buttons)
    glutMotionFunc(mouseControl)
    glutMouseFunc(on_click)

    global bj, cam, mod, joint_list
    jointdict, joint_list = joint_setup()
    bj = jointdict["hips_bind"]

    bj.set_bind_transform(Matrix())

    mod.set_position([-50, 0, 0])

    animated = Animated_model(mod, bj, len(jointdict), indices=mod.windices, weights=mod.weights)
    animator = setup_test_anim(joint_list, animated)

    cam = Camera()
    renderer = Renderer()
    renderer.objects = [cube, mod, animated]

    # te1 = Transform()
    # te2 = Transform()
    # te2.set_position([1, 0, 0])
    # data = flatten([flatten(te1.m), flatten(te2.m)], numpy.float32, )
    ## data = flatten(2, data_type=numpy.int8)
    ## data2= flatten(te1.m)
    # global test_ssbo
    # test_ssbo = glGenBuffers(1)
    # glBindBuffer(GL_SHADER_STORAGE_BUFFER, test_ssbo)
    ## glBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, data.nbytes, data)
    ## glBufferSubData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data2.nbytes, data2)
    #
    # glBufferData(GL_SHADER_STORAGE_BUFFER, data.nbytes, data=data, usage=GL_DYNAMIC_COPY)
    # glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, test_ssbo)
    #
    ## pog = glGetBufferSubData(GL_SHADER_STORAGE_BUFFER, 0, data.nbytes, None)
    #
    # glBindBuffer(GL_SHADER_STORAGE_BUFFER, 0)

    glutMainLoop()


def get_transformDict(joints):
    odict = OrderedDict()

    for i in range(len(joints)):
        odict[joints[i].name] = joints[i].getTransform()

    return odict


def setup_test_anim(bones, model):
    bones[86].set_rotation([0, 0, 0])
    bones[87].set_rotation([0, 0, 0])

    key1 = KeyFrame(get_transformDict(bones), 0)

    bones[86].set_rotation([-45, 0, 0])
    bones[87].set_rotation([90,0,0])

    key2 = KeyFrame(get_transformDict(bones), 1)

    # bones[0].set_rotation([180, 0, 0])
    # bones[1].set_position(Vector(pos)+[0,0,3])

    key3 = KeyFrame(get_transformDict(bones), 2)

    # bones[0].set_rotation([0, 0, 0])
    # bones[1].set_position(Vector(pos)+[0,0,3])

    key4 = KeyFrame(get_transformDict(bones), 3)

    # bones[0].set_rotation([0, 0, 0])
    # bones[1].set_position(Vector(pos)+[0,0,3])

    key5 = KeyFrame(get_transformDict(bones), 4)

    anim = Animation([key1, key2, key3, key4, key5])

    animator_obj = Animator(model=model, animation=anim)

    return animator_obj


def save_current_framebuffer_as_png(bufferid):
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    GL.glBindFramebuffer(GL_READ_FRAMEBUFFER, bufferid)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
    image.save('glutout.png', 'PNG')
    GL.glBindFramebuffer(GL_FRAMEBUFFER, 0)


def fps_update():
    global fps_counter
    global start_time
    global time_per_frame
    tim = (time.time() - start_time)

    if tim != 0:
        time_per_frame = tim
        #print("FPS: ", 1 / tim)


def clear_framebuffer():
    glClearColor(0.0, 1.0, 1, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


def render():
    global renderer, debug, buffer, program, lightProgram, cube, bbj, joint, joint2, animator, start_time, cam, test_ssbo, joint_list
    start_time = time.time()

    clear_framebuffer()
    glUseProgram(program)
    renderer.draw(cam, animator=animator)

    if debug:
        glUseProgram(jointProgram)
        renderer.joint_draw(joint_list, cam,  animator=animator)

    animator.update(time_per_frame)
    glFlush()

    fps_update()


init()
