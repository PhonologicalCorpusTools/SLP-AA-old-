# Import statements
import re
from collections import OrderedDict
from copy import deepcopy
import mathutils
import math
import numpy as numpy
from numpy.linalg import norm
from numpy import dot
from math import pi ,sin, cos
import os

"""To Run in Blender:
filename = 'C:\\Users\\Michael\\Google Drive\\PCT\\position_hand.py'
exec(compile(open(filename).read(), filename, 'exec'))
"""

def unit_vector(data, axis=None, out=None):
    """Return ndarray normalized by length, i.e. Euclidean norm, along axis.

    >>> v0 = numpy.random.random(3)
    >>> v1 = unit_vector(v0)
    >>> numpy.allclose(v1, v0 / numpy.linalg.norm(v0))
    True
    >>> v0 = numpy.random.rand(5, 4, 3)
    >>> v1 = unit_vector(v0, axis=-1)
    >>> v2 = v0 / numpy.expand_dims(numpy.sqrt(numpy.sum(v0*v0, axis=2)), 2)
    >>> numpy.allclose(v1, v2)
    True
    >>> v1 = unit_vector(v0, axis=1)
    >>> v2 = v0 / numpy.expand_dims(numpy.sqrt(numpy.sum(v0*v0, axis=1)), 1)
    >>> numpy.allclose(v1, v2)
    True
    >>> v1 = numpy.empty((5, 4, 3))
    >>> unit_vector(v0, axis=1, out=v1)
    >>> numpy.allclose(v1, v2)
    True
    >>> list(unit_vector([]))
    []
    >>> list(unit_vector([1]))
    [1.0]

    """
    if out is None:
        data = numpy.array(data, dtype=numpy.float64, copy=True)
        if data.ndim == 1:
            data /= math.sqrt(numpy.dot(data, data))
            return data
    else:
        if out is not data:
            out[:] = numpy.array(data, copy=False)
        data = out
    length = numpy.atleast_1d(numpy.sum(data*data, axis))
    numpy.sqrt(length, length)
    if axis is not None:
        length = numpy.expand_dims(length, axis)
    data /= length
    if out is None:
        return data

def vector_product(v0, v1, axis=0):
    """Return vector perpendicular to vectors.

    >>> v = vector_product([2, 0, 0], [0, 3, 0])
    >>> numpy.allclose(v, [0, 0, 6])
    True
    >>> v0 = [[2, 0, 0, 2], [0, 2, 0, 2], [0, 0, 2, 2]]
    >>> v1 = [[3], [0], [0]]
    >>> v = vector_product(v0, v1)
    >>> numpy.allclose(v, [[0, 0, 0, 0], [0, 0, 6, 6], [0, -6, 0, -6]])
    True
    >>> v0 = [[2, 0, 0], [2, 0, 0], [0, 2, 0], [2, 0, 0]]
    >>> v1 = [[0, 3, 0], [0, 0, 3], [0, 0, 3], [3, 3, 3]]
    >>> v = vector_product(v0, v1, axis=1)
    >>> numpy.allclose(v, [[0, 0, 6], [0, -6, 0], [6, 0, 0], [0, -6, 6]])
    True

    """
    return numpy.cross(v0, v1, axis=axis)

def vector_norm(data, axis=None, out=None):
    """Return length, i.e. Euclidean norm, of ndarray along axis.

    >>> v = numpy.random.random(3)
    >>> n = vector_norm(v)
    >>> numpy.allclose(n, numpy.linalg.norm(v))
    True
    >>> v = numpy.random.rand(6, 5, 3)
    >>> n = vector_norm(v, axis=-1)
    >>> numpy.allclose(n, numpy.sqrt(numpy.sum(v*v, axis=2)))
    True
    >>> n = vector_norm(v, axis=1)
    >>> numpy.allclose(n, numpy.sqrt(numpy.sum(v*v, axis=1)))
    True
    >>> v = numpy.random.rand(5, 4, 3)
    >>> n = numpy.empty((5, 3))
    >>> vector_norm(v, axis=1, out=n)
    >>> numpy.allclose(n, numpy.sqrt(numpy.sum(v*v, axis=1)))
    True
    >>> vector_norm([])
    0.0
    >>> vector_norm([1])
    1.0

    """
    data = numpy.array(data, dtype=numpy.float64, copy=True)
    if out is None:
        if data.ndim == 1:
            return math.sqrt(numpy.dot(data, data))
        data *= data
        out = numpy.atleast_1d(numpy.sum(data, axis=axis))
        numpy.sqrt(out, out)
        return out
    else:
        data *= data
        numpy.sum(data, axis=axis, out=out)
        numpy.sqrt(out, out)

def angle_between_vectors(v0, v1, directed=True, axis=0):
    """Return angle between vectors.

    If directed is False, the inumpyut vectors are interpreted as undirected axes,
    i.e. the maximum angle is pi/2.

    >>> a = angle_between_vectors([1, -2, 3], [-1, 2, -3])
    >>> numpy.allclose(a, math.pi)
    True
    >>> a = angle_between_vectors([1, -2, 3], [-1, 2, -3], directed=False)
    >>> numpy.allclose(a, 0)
    True
    >>> v0 = [[2, 0, 0, 2], [0, 2, 0, 2], [0, 0, 2, 2]]
    >>> v1 = [[3], [0], [0]]
    >>> a = angle_between_vectors(v0, v1)
    >>> numpy.allclose(a, [0, 1.5708, 1.5708, 0.95532])
    True
    >>> v0 = [[2, 0, 0], [2, 0, 0], [0, 2, 0], [2, 0, 0]]
    >>> v1 = [[0, 3, 0], [0, 0, 3], [0, 0, 3], [3, 3, 3]]
    >>> a = angle_between_vectors(v0, v1, axis=1)
    >>> numpy.allclose(a, [1.5708, 1.5708, 1.5708, 0.95532])
    True

    """
    v0 = numpy.array(v0, dtype=numpy.float64, copy=False)
    v1 = numpy.array(v1, dtype=numpy.float64, copy=False)
    dot = numpy.sum(v0 * v1, axis=axis)
    dot /= vector_norm(v0, axis=axis) * vector_norm(v1, axis=axis)
    return numpy.arccos(dot if directed else numpy.fabs(dot))

def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = numpy.asarray(axis)
    axis = axis/math.sqrt(numpy.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return numpy.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])

def rotation_matrix2(angle, direction, point=None):
    """Return matrix to rotate about axis defined by point and direction.

    >>> R = rotation_matrix(math.pi/2, [0, 0, 1], [1, 0, 0])
    >>> numpy.allclose(numpy.dot(R, [0, 0, 0, 1]), [1, -1, 0, 1])
    True
    >>> angle = (random.random() - 0.5) * (2*math.pi)
    >>> direc = numpy.random.random(3) - 0.5
    >>> point = numpy.random.random(3) - 0.5
    >>> R0 = rotation_matrix(angle, direc, point)
    >>> R1 = rotation_matrix(angle-2*math.pi, direc, point)
    >>> is_same_transform(R0, R1)
    True
    >>> R0 = rotation_matrix(angle, direc, point)
    >>> R1 = rotation_matrix(-angle, -direc, point)
    >>> is_same_transform(R0, R1)
    True
    >>> I = numpy.identity(4, numpy.float64)
    >>> numpy.allclose(I, rotation_matrix(math.pi*2, direc))
    True
    >>> numpy.allclose(2, numpy.trace(rotation_matrix(math.pi/2,
    ...                                               direc, point)))
    True

    """
    sina = math.sin(angle)
    cosa = math.cos(angle)
    direction = unit_vector(direction[:3])
    # rotation matrix around unit vector
    R = numpy.diag([cosa, cosa, cosa])
    R += numpy.outer(direction, direction) * (1.0 - cosa)
    direction *= sina
    R += numpy.array([[ 0.0,         -direction[2],  direction[1]],
                      [ direction[2], 0.0,          -direction[0]],
                      [-direction[1], direction[0],  0.0]])
    M = numpy.identity(4)
    M[:3, :3] = R
    if point is not None:
        # rotation not around origin
        point = numpy.array(point[:3], dtype=numpy.float64, copy=False)
        M[:3, 3] = point - numpy.dot(R, point)
    return M

def rotation_from_matrix(matrix):
    """Return rotation angle and axis from rotation matrix.

    >>> angle = (random.random() - 0.5) * (2*math.pi)
    >>> direc = numpy.random.random(3) - 0.5
    >>> point = numpy.random.random(3) - 0.5
    >>> R0 = rotation_matrix(angle, direc, point)
    >>> angle, direc, point = rotation_from_matrix(R0)
    >>> R1 = rotation_matrix(angle, direc, point)
    >>> is_same_transform(R0, R1)
    True

    """
    R = numpy.array(matrix, dtype=numpy.float64, copy=False)
    R33 = R[:3, :3]
    # direction: unit eigenvector of R33 corresponding to eigenvalue of 1
    w, W = numpy.linalg.eig(R33.T)
    i = numpy.where(abs(numpy.real(w) - 1.0) < 1e-8)[0]
    if not len(i):
        raise ValueError("no unit eigenvector corresponding to eigenvalue 1")
    direction = numpy.real(W[:, i[-1]]).squeeze()
    # point: unit eigenvector of R33 corresponding to eigenvalue of 1
    w, Q = numpy.linalg.eig(R)
    i = numpy.where(abs(numpy.real(w) - 1.0) < 1e-8)[0]
    if not len(i):
        raise ValueError("no unit eigenvector corresponding to eigenvalue 1")
    point = numpy.real(Q[:, i[-1]]).squeeze()
    point /= point[3]
    # rotation angle depending on direction
    cosa = (numpy.trace(R33) - 1.0) / 2.0
    if abs(direction[2]) > 1e-8:
        sina = (R[1, 0] + (cosa-1.0)*direction[0]*direction[1]) / direction[2]
    elif abs(direction[1]) > 1e-8:
        sina = (R[0, 2] + (cosa-1.0)*direction[0]*direction[2]) / direction[1]
    else:
        sina = (R[2, 1] + (cosa-1.0)*direction[1]*direction[2]) / direction[0]
    angle = math.atan2(sina, cosa)
    return angle, direction, point

# Function to translate handshape coding to degrees of rotation, adduction, flexion
def translate_finger_code_to_degrees(finger, hand, Fshape, handShapeParams):
	# flexionDictionary parameters: [proximal, medial, distal] joints
	if hand == 'L':
		flexionDict = {'H':[30, 15, 10], 'E':[20, 10, 5], 'e': [10, 5, 0], 'i':[-45, -50, -60], 'F':[-80, -90, -75], '_':[0, 0, 0]}
		abductDict = {'middle': {'=':0, '<':10, '_':0}, 'ring': {'=':0, '<':10, '_':0}, 'pinky': {'=':0, '<':20, '_':0}}
		rotDict = {'middle': {'=':0, '<':5, '_':0}, 'ring': {'=':0, '<':-5, '_':0}, 'pinky': {'=':0, '<':-10, '_':0}}
	else:
		flexionDict = {'H':[-30, -15, -10], 'E':[-20, -10, -5], 'e': [-10, -5, 0], 'i':[45, 50, 60], 'F':[80, 90, 75], '_':[0, 0, 0]}
		abductDict = {'middle': {'=':0, '<':-10, '_':0}, 'ring': {'=':0, '<':-10, '_':0}, 'pinky': {'=':0, '<':-20, '_':0}}
		rotDict = {'middle': {'=':0, '<':5, '_':0}, 	'ring': {'=':0, '<':-5, '_':0}, 'pinky': {'=':0, '<':-10, '_':0}}
	
	if finger == 'index':
		handShapeParams['finger_index.01.' + hand] = [0, 0, flexionDict[Fshape[1]][0]]
		handShapeParams['finger_index.02.' + hand] = [0, 0, flexionDict[Fshape[2]][1]]
		handShapeParams['finger_index.03.' + hand] = [0, 0, flexionDict[Fshape[3]][2]]
	else:
		# Parameters: [adduction, rotation, flexion]
		handShapeParams['finger_' + finger + '.01.' + hand] = [abductDict[finger][Fshape[0]], rotDict[finger][Fshape[0]], flexionDict[Fshape[2]][0]]
		handShapeParams['finger_' + finger + '.02.' + hand] = [0, rotDict[finger][Fshape[0]], flexionDict[Fshape[3]][1]]
		handShapeParams['finger_' + finger + '.03.' + hand] = [0, rotDict[finger][Fshape[0]], flexionDict[Fshape[4]][2]]
	return handShapeParams

def translate_thumb_code_to_degrees(hand, Tshape, handShapeParams, outf):
	if Tshape[0] == 'O':
		flexionDict = {'H':[-20, -10], 'E':[-10, -5], 'e': [15, 15], 'i':[30, 25], 'F':[80, 25], '_':[0, 0]}
	elif Tshape[0] == 'L':
		flexionDict = {'H':[-20, -10], 'E':[-10, -5], 'e': [15, 15], 'i':[30, 25], 'F':[85, 35], '_':[0, 0]}
	else:
		flexionDict = {'H':[0, 0], 'E':[50, 0], 'e': [0, 0], 'i':[60, 0], 'F':[80, 0], '_':[0, 0]}

	# Sample Code: Tshape:[L=EH]  
	if Tshape[0] == 'O' and Tshape[1] == '=':
		handShapeParams['thumb.02.' + hand] = [flexionDict[Tshape[2]][1], 0, 0]
		handShapeParams['thumb.03.' + hand] = [flexionDict[Tshape[3]][0], 0, 0]	
		handShapeParams['thumb.01.' + hand + '.001'] = [0, 0, -50] 
	elif Tshape[0] == 'O' and Tshape[1] == '<':
		handShapeParams['thumb.01.' + hand + '.001'] = [0, -20, -50] 
	elif Tshape[0] == 'L' and Tshape[1] == '=':
		handShapeParams['thumb.01.' + hand + '.001'] = [0, 20, 0] 
	elif Tshape[0] == 'L' and Tshape[1] == '<':
		handShapeParams['thumb.01.' + hand + '.001'] = [-20, 20, 0] 
	return handShapeParams

## Start Script

# Read handshape coding and parse into thumb/fingers
with open(os.path.join(os.getcwd(), 'handCode.txt'), 'r') as inFile:
	code = inFile.read()
	parseCode = re.split('\]\d\[+', code[1:])
	[armShape, thumbShape, thumbFingerContact, indexShape, middleShape, ringShape, pinkyShape] = parseCode[:]

# Set hand & generate degrees of rotation, adduction & flexion
with open(os.path.join(os.getcwd(), 'debug.txt'), 'w') as outf:
	hand = 'L'
	handShapeParams = OrderedDict()
	handShapeParams = translate_finger_code_to_degrees('index', hand, indexShape, handShapeParams)
	handShapeParams = translate_finger_code_to_degrees('middle', hand, middleShape, handShapeParams)
	handShapeParams = translate_finger_code_to_degrees('ring', hand, ringShape, handShapeParams)
	handShapeParams = translate_finger_code_to_degrees('pinky', hand, pinkyShape, handShapeParams)
	handShapeParams = translate_thumb_code_to_degrees(hand, thumbShape, handShapeParams, outf)

	#Write to debugging file
	outf.write(str(handShapeParams) + '\r\n')

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
		#Ensure all bones deactivated
		if bpy.context.active_pose_bone is not None:
			deactThisBone = bpy.context.active_pose_bone.name
			deactThisBone = bpy.data.objects["Armature"].pose.bones[deactThisBone].bone
			deactThisBone.select = False

		actThisBone = bpy.data.objects["Armature"].pose.bones[strBone].bone
		actThisBone.select = True

		addVDegree = param[0]
		rotVDegree = param[1]
		eleVDegree = param[2]
		eleVRadian = (eleVDegree/360)*2*pi
		addVRadian = (addVDegree/360)*2*pi
		rotVRadian = (rotVDegree/360)*2*pi
		
		#Apply transformations
		# Flexion/Extension occurs by moving joints about the y-axis
		bpy.ops.transform.rotate(value = eleVRadian, constraint_axis=(False, True, False))	
		# Rotation of joints to reflect how natural hands adduct by moving joints about the x-axis
		bpy.ops.transform.rotate(value=rotVRadian, axis = (True, False, False))
		# Adduction of fingers occurs by moving the proximal joint (e.g. finger_index.01.L) about the z-axis
		bpy.ops.transform.rotate(value=addVRadian, axis = (False, False, True))	
	
		#Deactivate bone
		deactThisBone = actThisBone
		deactThisBone.select = False
	
	
	# Now use world matrix location to do thumb-finger contact
	outf.write(thumbFingerContact)

	thumbBaseBone = 'thumb.01.L.001'
	thumbEndBone = 'thumb.03.L'
	fingBone = 'finger_ring.03.L'

	thumbMat = bpy.data.objects["Armature"].pose.bones[thumbBaseBone].matrix
	thumbLoc, thumbRot, thumbSca = bpy.data.objects["Armature"].pose.bones[thumbBaseBone].matrix.decompose()
	thumbEndLoc, thumbEndRot, thumbEndSca = bpy.data.objects["Armature"].pose.bones[thumbEndBone].matrix.decompose()
	fingMat = bpy.data.objects["Armature"].pose.bones[fingBone].matrix
	fingLoc, fingRot, fingSca = bpy.data.objects["Armature"].pose.bones[fingBone].matrix.decompose()
	
	thumbLocMat = mathutils.Matrix.Translation(thumbLoc)
	thumbRotMat = thumbRot.to_matrix()


	outf.write('\n' + str(thumbLoc) + '\n')
	outf.write('\n' + str(thumbRot) + '\n')
	outf.write('\n' + str(thumbEndLoc) + '\n')
	outf.write('\n' + str(fingLoc) + '\n')

	

	#axisT = thumbLoc-fingLoc
	axisT = Vector((0.9, -0.33, -0.26))
	qq = rotation_matrix(axisT, -0.5)
	mm = rotation_matrix2(0.5, axisT)
	outf.write('\n' + str(qq) + '\n')
	outf.write('\n' + str(mm) + '\n')

	#for ii in range(3):
	#	for jj in range(3):
	#		mm[ii][jj] = manMat[ii][jj]
	manRot = deepcopy(thumbRot)
	manRot.x = 0.9
	manRot.y = -0.33
	manRot.z = -0.26
	manRot.w = -0.5
	
	outf.write('\n' + str(manRot) + '\n')

	manRotMat = manRot.to_matrix()
	newThumbMat = deepcopy(thumbMat)
	for ii in range(3):
		for jj in range(3):
			newThumbMat[ii][jj] = manRotMat[ii][jj]

	bpy.data.objects["Armature"].pose.bones[thumbBaseBone].matrix = newThumbMat
	

bpy.ops.object.posemode_toggle()

#bpy.ops.object.camera_add(view_align = True)
#bpy.context.scene.camera = bpy.data.objects['Camera']

#Code for monitoring progression of algorithm
#print(bpy.data.objects['Armature'].pose.bones.keys())
"""
List of Bones: 	['shoulder.R', 'upper_arm.R', 'forearm.R', 'forearm.R.003', 'hand.R', 'hand.L', 
					'palm.01.L.001', 'palm.01.L', 'palm.02.L.001', 'palm.02.L', 'palm.03.L.001', 'palm.03.L', 'palm.04.L.001', 'palm.04.L', 
					'thumb.01.L.001', 'thumb.01.L', 'thumb.02.L', 'thumb.03.L',
				   	'finger_index.01.L', 'finger_index.02.L', 'finger_index.03.L',  
				   	'finger_middle.01.L', 'finger_middle.02.L', 'finger_middle.03.L', 
				   	'finger_ring.01.L', 'finger_ring.02.L', 'finger_ring.03.L', 
					'finger_pinky.01.L', 'finger_pinky.02.L', 'finger_pinky.03.L',

					'palm.01.R.001', 'palm.01.R', 'palm.02.R.001', 'palm.02.R', 'palm.03.R.001', 'palm.03.R', 'palm.04.R.001', 'palm.04.R', 
					'thumb.01.R.001', 'thumb.01.R', 'thumb.02.R', 'thumb.03.R',  
					'finger_index.01.R', 'finger_index.02.R', 'finger_index.03.R', 
					'finger_middle.01.R', 'finger_middle.02.R', 'finger_middle.03.R', 
					'finger_ring.01.R', 'finger_ring.02.R', 'finger_ring.03.R', 
					'finger_pinky.01.R', 'finger_pinky.02.R', 'finger_pinky.03.R']
"""

# Template: finger_index/middle/ring/pinky.joint.L/R
# bpy.ops.ed.undo_history(item=0)	
#bpy.ops.transform.resize(value=(0.85, 0.85, 0.85), constraint_axis=(False,False,False),constraint_orientation='GLOBAL',mirror=False,proportional='DISABLED',proportional_edit_falloff='SMOOTH',proportional_size=1)
#bpy.ops.transform.trackball(value=(1.05,1.15),mirror=False,proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)