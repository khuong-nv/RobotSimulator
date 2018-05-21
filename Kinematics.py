import numpy as np 
import math
from math import *
from ConfigRobot import *
from GlobalFunc import *

class Kinematics(object):
	"""docstring for Kinematics"""
	def __init__(self):
		self.cf = ConfigRobot()
		self.q = []
		self.d = self.cf.d
		self.a = self.cf.a
		self.a[4] = self.a[4]
		self.alpha = self.cf.alpha

	def Cal_AMatrix(self, q1, q2, q3, q4):
		A10 = DHMatrix(q1, self.d[1], self.a[1], self.alpha[1])
		A21 = DHMatrix(q2, self.d[2], self.a[2], self.alpha[2])
		A32 = DHMatrix(q3, self.d[3], self.a[3], self.alpha[3])
		A43 = DHMatrix(q4, self.d[4], self.a[4]+33, self.alpha[4])
		A40 = A10.dot(A21).dot(A32).dot(A43)

		return A40	
class FwdKinematics(Kinematics):
	"""docstring for FwdKinematics"""
	def __init__(self):
		super(FwdKinematics, self).__init__()
		
	def Cal_Fwd_Position(self, JVars):
		q1 = JVars[0]
		q2 = JVars[1]
		q3 = JVars[2]
		q4 = JVars[3]
		AE = self.Cal_AMatrix(q1, q2, q3, q4)
		xE = AE[0][3]
		yE = AE[1][3]
		zE = AE[2][3]
		psi, theta, phi = ConvertMatToRPY(AE[0:3, 0:3])
		EVars = [xE, yE, zE, psi, theta, phi]
		return np.asarray(EVars)

class InvKinematics(Kinematics):
	"""docstring for InvKinematics"""
	def __init__(self):
		super(InvKinematics, self).__init__()

	def Cal_Sol(self, sol):
		result = [1]*2
		if sol % 2:
			result[0] = 1
		else:
			result[0] = -1
		if sol > 1 and sol < 4:
			result[1] = -1
		return result

	def FindTheBestSolution(self, EVars, q1P, q2P):
		k1 = 0.9
		k2 = 0.1
		sp_time = 0.5
		W = [0] * 4
		for i in np.arange(4):
			result = self.Cal_Inv_Position(EVars, i+1)
			if result[0] == False:
				return None
			q = result[1]
			t1 = SmartDegSubstraction(q, q1P)
			tmp = SmartDegSubstraction(q1P, q2P)
			t2 = SmartDegSubstraction(q, q1P + sp_time * tmp)
			W[i] = k1 * np.sum(np.square(t1)) + k2 * np.sum(np.square(t2))
		Wmin = min(W)
		return W.index(Wmin) + 1

	def Cal_Inv_Position(self, EVars, sol):
		xe = EVars[0]
		ye = EVars[1]
		ze = EVars[2]
		psi = EVars[3]
		theta = EVars[4]
		phi = EVars[5]
		s = self.Cal_Sol(sol)
		a4 = self.a[4]+33
		a3 = self.a[3]
		a2 = self.a[2]
		a1 = self.a[1]
		d3 = self.d[3]
		d2 = self.d[2]
		d1 = self.d[1]

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
		try:
			r = sqrt(xe**2 + ye**2)
			_phi = atan2(xe/r, ye/r) 
			q1 = s[0] * acos((d2 + d3)/r) - _phi
			q234 = atan2(-nz, -sz)
			A = -ze + d1 - a4*sin(q234)
			B = cos(q1)*xe + sin(q1)*ye - a4*cos(q234)
			q3 = s[1] * acos((A**2 + B**2 - a2**2 - a3**2)/(2*a2*a3))

			delta = a3**2 * (sin(q3))**2 + (a3*cos(q3) + a2)**2
			deltas = A * (a3*cos(q3) + a2) - B*a3*sin(q3) 
			deltac = B * (a3*cos(q3) + a2) + A*a3*sin(q3)

			q2 = atan2(deltas/delta, deltac/delta)
			q4 = q234 - q3 - q2
			return True,  np.array([q1, q2, q3, q4])
		except Exception as e:
			return False, 

	def function():
		pass