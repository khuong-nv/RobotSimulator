import numpy as np 
import math
from math import *
from ConfigRobot import *
from GlobalFunc import *
# conf = ConfigRobot()

# global q1P
# global q2P
# q1P = conf.q_init
# q2P = conf.q_init
		

class Kinematics(object):
	"""docstring for Kinematics"""
	def __init__(self):
		cf = ConfigRobot()
		self.q = []
		self.d = cf.d
		self.a = cf.a
		self.alpha = cf.alpha
		self.q1P = cf.q_init
		self.q2P = cf.q_init

	def Cal_AMatrix(self, q1, q2, q3, q4):
		A10 = DHMatrix(q1, self.d[0], self.a[0], self.alpha[0])
		A21 = DHMatrix(q2, self.d[1], self.a[1], self.alpha[1])
		A32 = DHMatrix(q3, self.d[2], self.a[2], self.alpha[2])
		A43 = DHMatrix(q4, self.d[3], self.a[3], self.alpha[3])
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
		a4 = cf.a[3]
		a3 = cf.a[2]
		a2 = cf.a[1]
		a1 = cf.a[0]
		d3 = cf.d[2]
		d2 = cf.d[1]
		d1 = cf.d[0]

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

	def Optimization(self, xe, ye, ze, psi, theta, phi):
		
		cf = ConfigRobot()
		# c3 = cf.c[2]
		a4 = cf.a[3]
		a3 = cf.a[2]
		a2 = cf.a[1]
		a1 = cf.a[0]
		d3 = cf.d[2]
		d2 = cf.d[1]
		d1 = cf.d[0]

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

		############################################################
		q11 = acos((d2 + d3)/r) - _phi
		q234 = atan2(-nz, -sz)
		A = -ze + d1 - a4*sin(q234)
		B11 = cos(q11)*xe + sin(q11)*ye - a4*cos(q234)
		# print((A**2 + B**2 - a2**2 - a3**2)/(2*a2*a3))
		# print((A**2 + B11**2 - a2**2 - a3**2)/(2*a2*a3))
		q31 = acos((A**2 + B11**2 - a2**2 - a3**2)/(2*a2*a3))

		# q3 = -acos((A**2 + B**2 - a2**2 - a3**2)/(2*a2*a3))


		delta11 = a3**2 * (sin(q31))**2 + (a3*cos(q31) + a2)**2
		deltas11 = A * (a3*cos(q31) + a2) - B11*a3*sin(q31) 
		deltac11 = B11 * (a3*cos(q31) + a2) + A*a3*sin(q31)

		q21 = atan2(deltas11/delta11, deltac11/delta11)
		q41 = q234 - q31 - q21


		###########################################################
		q12 = acos((d2 + d3)/r) - _phi
		B12 = cos(q12)*xe + sin(q12)*ye - a4*cos(q234)
		q32 = -acos((A**2 + B12**2 - a2**2 - a3**2)/(2*a2*a3))

		delta12 = a3**2 * (sin(q32))**2 + (a3*cos(q32) + a2)**2
		deltas12 = A * (a3*cos(q32) + a2) - B12*a3*sin(q32) 
		deltac12 = B12 * (a3*cos(q32) + a2) + A*a3*sin(q32)
		
		q22 = atan2(deltas12/delta12, deltac12/delta12)
		q42 = q234 - q32 - q22


		############################################################
		q13 = -acos((d2 + d3)/r) - _phi
		B13 = cos(q13)*xe + sin(q13)*ye - a4*cos(q234)
		q33 = acos((A**2 + B13**2 - a2**2 - a3**2)/(2*a2*a3))

		delta13 = a3**2 * (sin(q33))**2 + (a3*cos(q33) + a2)**2
		deltas13 = A * (a3*cos(q33) + a2) - B13*a3*sin(q33) 
		deltac13 = B13 * (a3*cos(q33) + a2) + A*a3*sin(q33)

		q23 = atan2(deltas13/delta13, deltac13/delta13)
		q43 = q234 - q33 - q23



		############################################################
		q14 = -acos((d2 + d3)/r) - _phi
		B14 = cos(q14)*xe + sin(q14)*ye - a4*cos(q234)
		q34 = -acos((A**2 + B14**2 - a2**2 - a3**2)/(2*a2*a3))

		delta14 = a3**2 * (sin(q34))**2 + (a3*cos(q34) + a2)**2
		deltas14 = A * (a3*cos(q34) + a2) - B14*a3*sin(q34) 
		deltac14 = B14 * (a3*cos(q34) + a2) + A*a3*sin(q34)

		q24 = atan2(deltas14/delta14, deltac14/delta14)
		q44 = q234 - q34 - q24

		############################################################

		k1 = 0.85
		k2 = 0.15
		deltat = 0.1
		Q11 = np.array([q11, q21, q31, q41])
		Q12 = np.array([q12, q22, q32, q42])
		Q13 = np.array([q13, q23, q33, q43])
		Q14 = np.array([q14, q24, q34, q44])

		W11 = k1*(Q11 - self.q1P).dot(Q11 - self.q1P) + k2*(Q11 - (self.q1P + deltat*(self.q1P - self.q2P))).dot(Q11 - (self.q1P + deltat*(self.q1P - self.q2P)))
		W12 = k1*(Q12 - self.q1P).dot(Q12 - self.q1P) + k2*(Q12 - (self.q1P + deltat*(self.q1P - self.q2P))).dot(Q12 - (self.q1P + deltat*(self.q1P - self.q2P)))
		W13 = k1*(Q13 - self.q1P).dot(Q13 - self.q1P) + k2*(Q13 - (self.q1P + deltat*(self.q1P - self.q2P))).dot(Q13 - (self.q1P + deltat*(self.q1P - self.q2P)))
		W14 = k1*(Q14 - self.q1P).dot(Q14 - self.q1P) + k2*(Q14 - (self.q1P + deltat*(self.q1P - self.q2P))).dot(Q14 - (self.q1P + deltat*(self.q1P - self.q2P)))

		############################################################
		w_max = max(W11, W12, W13, W14)
		q_opt = []
		if w_max == W11:
			q_opt = Q11
			print('q11')
			# return Q11
		elif w_max == W12:
			q_opt = Q12
			print('q12')
			# return Q12
		elif w_max == W13:
			q_opt = Q13
			print('q13')
			# return Q13
		elif w_max == W14:
			q_opt = Q14
			print('q14')
			# return Q14

		self.q2P = self.q1P
		self.q1P = q_opt
		# return q_opt
		# print("Test:\n\n")
		# print(q_opt)
		print(Q11)
		print(Q12)
		print(Q13)
		print(Q14)
		# print(W11)
		# print(W12)
		# print(W13)
		# print(W14)
		print("\n\n")
		return ([q11, q21, q31, q41], [q12, q22, q32, q42], [q13, q23, q33, q43], [q14, q24, q34, q44])


if __name__ == '__main__':
	test = Kinematics()
	testt = test.Cal_AMatrix(-0.506, -0.7155, 1.1868, 1.09955)
	print(testt)
	test1 = FwdKinematics()
	test11 = test1.Cal_Fwd_Position(-0.506, -0.7155, 1.1868, 1.09955)
	print(test11)
	test21 = InvKinematics()
	print(test21.Cal_Inv_Position(test11[0], test11[1], test11[2], test11[3], test11[4], test11[5]))
	test22 = test21.Optimization(test11[0], test11[1], test11[2], test11[3], test11[4], test11[5])
	print(test1.Cal_Fwd_Position(*test22[0]))
	print(test1.Cal_Fwd_Position(*test22[1]))
	print(test1.Cal_Fwd_Position(*test22[2]))
	print(test1.Cal_Fwd_Position(*test22[3]))