# Import statements
import re
import os
from math import pi, radians
import bpy


"""To Run in Blender:
filename = 'C:\\Users\\mFry2\\Google Drive\\PCT\\position_hand.py'
exec(compile(open(filename).read(), filename, 'exec'))
"""

# Function to translate handshape coding to degrees of rotation, adduction, flexion
def translate_finger_code_to_degrees(finger, hand, code, handShapeParams):
    # flexionDictionary parameters: [proximal, medial, distal] joints
    if hand == 'L':
        flexionDict = {'H':[30, 15, 10], 'E':[20, 10, 5], 'e': [10, 5, 0], 'i':[-45, -50, -60], 'F':[-80, -90, -75], '_':[0,0,0]}
        abductDict = {'middle': {'=':0, '<':10}, 'ring': {'=':0, '<':10}, 'pinky': {'=':0, '<':20}}
        rotDict = {'middle': {'=':0, '<':5}, 'ring': {'=':0, '<':-5}, 'pinky': {'=':0, '<':-10}}
    elif hand == 'R':
        flexionDict = {'H':[-30, -15, -10], 'E':[-20, -10, -5], 'e': [-10, -5, 0], 'i':[45, 50, 60], 'F':[80, 90, 75], '_':[0,0,0]}
        abductDict = {'middle': {'=':0, '<':-10}, 'ring': {'=':0, '<':-10}, 'pinky': {'=':0, '<':-20}}
        rotDict = {'middle': {'=':0, '<':5}, 'ring': {'=':0, '<':-5}, 'pinky': {'=':0, '<':-10}}

    if finger == 'thumb':
        if code[1] == '<':
            handShapeParams['thumb.01.' + hand] = [0, 0, 0]

        if code[0] == 'O' and hand == 'L':
            handShapeParams['thumb.01.' + hand + '.001'] = [0, -70, -40]
            handShapeParams['thumb.02.' + hand] = [0, -70, flexionDict[code[2]][0]]
            handShapeParams['thumb.03.' + hand] = [0, 0, flexionDict[code[3]][1]]
        elif code[0] == 'O' and hand == 'R':
            handShapeParams['thumb.01.' + hand + '.001'] = [0, 70, 40]
            handShapeParams['thumb.02.' + hand] = [0, -70, flexionDict[code[2]][0]]
            handShapeParams['thumb.03.' + hand] = [0, 0, flexionDict[code[3]][1]]
    elif finger == 'index':
        handShapeParams['finger_index.01.' + hand] = [0, 0, flexionDict[code[1]][0]]
        handShapeParams['finger_index.02.' + hand] = [0, 0, flexionDict[code[2]][1]]
        handShapeParams['finger_index.03.' + hand] = [0, 0, flexionDict[code[3]][2]]
    else:
        # Parameters: [adduction, rotation, flexion]
        handShapeParams['finger_' + finger + '.01.' + hand] = [abductDict[finger][code[0]], rotDict[finger][code[0]], flexionDict[code[2]][0]]
        handShapeParams['finger_' + finger + '.02.' + hand] = [0, rotDict[finger][code[0]], flexionDict[code[3]][1]]
        handShapeParams['finger_' + finger + '.03.' + hand] = [0, rotDict[finger][code[0]], flexionDict[code[4]][2]]
        if finger == 'middle' and code[0] == '<':
            tempParam = handShapeParams['finger_index.01.' + hand]
            handShapeParams['finger_index.01.' + hand] = [-10, tempParam[1], tempParam[2]]
    return handShapeParams
"""
def translate_thumb_codes_to_position(hand, shapeCode, contactCode, handShapeParams):
    # r = radial, f = friction, d = distal, p =proximal, m = medial
    handShapeParams['thumb.01.' + hand + '.001'] =
    handShapeParams['thumb.01.' + hand] =
    handShapeParams['thumb.02.' + hand] =
    handShapeParams['thumb.03.' + hand] =
    """

def position_hand():
    with open(os.path.join(os.getcwd(), 'handCode.txt'), 'r') as inFile:
        code = inFile.read()
    parseCode = re.split('\]\d\[+', code[1:])
    [armShape, thumbShape, thumbFingerContact, indexShape, middleShape, ringShape, pinkyShape] = parseCode[:]

    # Set hand & generate degrees of rotation, adduction & flexion
    hand = 'L'
    handShapeParams = dict()
    handShapeParams = translate_finger_code_to_degrees('index', hand, indexShape, handShapeParams)
    handShapeParams = translate_finger_code_to_degrees('middle', hand, middleShape, handShapeParams)
    handShapeParams = translate_finger_code_to_degrees('ring', hand, ringShape, handShapeParams)
    handShapeParams = translate_finger_code_to_degrees('pinky', hand, pinkyShape, handShapeParams)
    handShapeParams = translate_finger_code_to_degrees('thumb', hand, thumbShape, handShapeParams)

    # Position model in blender
    bpy.ops.object.posemode_toggle()

    # deactive current bone select
    if not bpy.context.active_pose_bone == None:
        #print("Bone selected: " + str(bpy.context.active_pose_bone.name))
        deactThisBone = bpy.context.active_pose_bone.name
        deactThisBone = bpy.data.objects["Armature"].pose.bones[deactThisBone].bone
        deactThisBone.select = False


    #Cycle through finger bones in handShapeParams to modify the hand model:
    for strBone, param in handShapeParams.items():
        actThisBone = bpy.data.objects["Armature"].pose.bones[strBone].bone
        actThisBone.select = True
        eleVDegree = param[2]
        addVDegree = param[0]
        rotVDegree = param[1]
        eleVRadian = (eleVDegree/360)*2*pi
        addVRadian = (addVDegree/360)*2*pi
        rotVRadian = (rotVDegree/360)*2*pi

        if '001' in strBone:
            # Flexion/Extension occurs by moving joints about the y-axis
            bpy.ops.transform.rotate(value = eleVRadian, constraint_axis=(False, True, False))
            # Rotation of joints to reflect how natural hands adduct by moving joints about the x-axis
            bpy.ops.transform.rotate(value=rotVRadian, axis = (True, False, False))
            # Adduction of fingers occurs by moving the proximal joint (e.g. finger_index.01.L) about the z-axis
            bpy.ops.transform.rotate(value=addVRadian, axis = (False, False, True))
        else:
            # Flexion/Extension occurs by moving joints about the y-axis
            bpy.ops.transform.rotate(value = eleVRadian, constraint_axis=(False, True, False))

            # Rotation of joints to reflect how natural hands adduct by moving joints about the x-axis
            bpy.ops.transform.rotate(value=rotVRadian, axis = (True, False, False))

            # Adduction of fingers occurs by moving the proximal joint (e.g. finger_index.01.L) about the z-axis
            bpy.ops.transform.rotate(value=addVRadian, axis = (False, False, True),)

        #Deactivate bone
        deactThisBone = actThisBone
        deactThisBone.select = False

    #bpy.ops.transform.rotate(value = 0.2, axis=(.305, 0.885, -0.349), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
    deactThisBone.select = True
    bpy.ops.object.posemode_toggle()
    bpy.ops.object.camera_add(view_align = True)
    bpy.context.scene.camera = bpy.data.objects['Camera']
    camera = bpy.context.object
    camera.location = (-0.75, -0.14, 1.75)
    # camera.rotation_euler = (0.0, 0.0, radians(90))


    #Previous code for monitoring progression of algorithm
    #print(bpy.data.objects['Armature'].pose.bones.keys())
    # List of Bones: ['hand.L', 'palm.02.L.001', 'palm.02.L', 'finger_middle.01.L', 'finger_middle.02.L', 'finger_middle.03.L', 'palm.03.L.001', 'palm.03.L', 'finger_ring.01.L', 'finger_ring.02.L', 'finger_ring.03.L', 'palm.04.L.001', 'palm.04.L', 'finger_pinky.01.L', 'finger_pinky.02.L', 'finger_pinky.03.L', 'palm.01.L.001', 'palm.01.L', 'thumb.01.L.001', 'thumb.01.L', 'thumb.02.L', 'thumb.03.L', 'finger_index.01.L', 'finger_index.02.L', 'finger_index.03.L', 'shoulder.R', 'upper_arm.R', 'forearm.R', 'forearm.R.003', 'hand.R', 'palm.01.R.001', 'palm.01.R', 'thumb.01.R.001', 'thumb.01.R', 'thumb.02.R', 'thumb.03.R', 'finger_index.01.R', 'finger_index.02.R', 'finger_index.03.R', 'palm.02.R.001', 'palm.02.R', 'finger_middle.01.R', 'finger_middle.02.R', 'finger_middle.03.R', 'palm.03.R.001', 'palm.03.R', 'finger_ring.01.R', 'finger_ring.02.R', 'finger_ring.03.R', 'palm.04.R.001', 'palm.04.R', 'finger_pinky.01.R', 'finger_pinky.02.R', 'finger_pinky.03.R']
    # Template: finger_index/middle/ring/pinky.joint.L/R


    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG' # set output format to .png
    scene.frame_set(1)
    scene.render.filepath = os.path.join(os.getcwd(), 'hand_output.png')
    bpy.ops.render.render(write_still=True)

    # frames = 5, 9, 17
    #
    # for frame_nr in frames:
    #
    #     # set current frame to frame 5
    #     scene.frame_set(frame_nr)
    #
    #     # set output path so render won't get overwritten
    #     scene.render.filepath = fp + str(frame_nr)
    #     bpy.ops.render.render(write_still=True) # render still
    #
    # # restore the filepath
    # scene.render.filepath = fp

if __name__ == '__main__': #don't import me
    position_hand()
