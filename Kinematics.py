import numpy as np 
import math
from math import *
from ConfigRobot import *
from GlobalFunc import *

class Kinematics(object):
	"""docstring for Kinematics"""
	def __init__(self):
		cf = ConfigRobot()
		self.q = []
		self.d = cf.d
		self.a = cf.a
		self.alpha = cf.alpha
	def Cal_AMatrix(self, q1, q2, q3, q4):
		A10 = DHMatrix(q1, self.d[1], self.a[1], self.alpha[1])
		A21 = DHMatrix(q2, self.d[2], self.a[2], self.alpha[2])
		A32 = DHMatrix(q3, self.d[3], self.a[3], self.alpha[3])
		A43 = DHMatrix(q4, self.d[4], self.a[4], self.alpha[4])
		A40 = A10.dot(A21).dot(A32).dot(A43)

		return A40	
class FwdKinematics(Kinematics):
	"""docstring for FwdKinematics"""
	def __init__(self):
		super(FwdKinematics, self).__init__()
		
	def Cal_Fwd_Position(self, q1, q2, q3, q4):
		AE = self.Cal_AMatrix(q1, q2, q3, q4)
		xE = AE[0][3]
		yE = AE[1][3]
		zE = AE[2][3]
		psi, theta, phi = ConvertMatToRPY(AE[0:3, 0:3])
		return xE, yE, zE, psi, theta, phi 

class InvKinematics(Kinematics):
	"""docstring for InvKinematics"""
	def __init__(self):
		super(InvKinematics, self).__init__()
				
	def Cal_Inv_Position(self, xe, ye, ze, psi, theta, phi):
		cf = ConfigRobot()
		# c3 = cf.c[2]
		a4 = cf.a[4]
		a3 = cf.a[3]
		a2 = cf.a[2]
		a1 = cf.a[1]
		d3 = cf.d[3]
		d2 = cf.d[2]
		d1 = cf.d[1]

		RPYMat = ConvertRPYToMat(psi, theta, phi)		
		nx = RPYMat[0][0]
		ny = RPYMat[1][0]
		nz = RPYMat[2][0]

		sx = RPYMat[0][1]
		sy = RPYMat[1][1]
		sz = RPYMat[2][1]

		ax = RPYMat[0][2]
		ay = RPYMat[1][2]
		az = RPYMat[2][2]

		r = sqrt(xe**2 + ye**2)
		_phi = atan2(xe/r, ye/r) 

		# q1 = acos((d2 + d3)/r) - _phi

		q1 = - acos((d2 + d3)/r) - _phi
		q234 = atan2(-nz, -sz)
		A = -ze + d1 - a4*sin(q234)
		B = cos(q1)*xe + sin(q1)*ye - a4*cos(q234)
		# print((A**2 + B**2 - a2**2 - a3**2)/(2*a2*a3))
		q3 = acos((A**2 + B**2 - a2**2 - a3**2)/(2*a2*a3))
		# q3 = -acos((A**2 + B**2 - a2**2 - a3**2)/(2*a2*a3))


		delta = a3**2 * (sin(q3))**2 + (a3*cos(q3) + a2)**2
		deltas = A * (a3*cos(q3) + a2) - B*a3*sin(q3) 
		deltac = B * (a3*cos(q3) + a2) + A*a3*sin(q3)

		q2 = atan2(deltas/delta, deltac/delta)

		q4 = q234 - q3 - q2
	
		# print("a = ", A, "\nb = ", B)

		return q1, q2, q3, q4