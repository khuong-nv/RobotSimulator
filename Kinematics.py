import matplotlib.pyplot as plt 
import numpy as np 
import math
from math import *
from ConfigRobot import *

class DH(object):
	"""docstring for Kinematics"""
	def __init__(self, q, d, a, alpha):
		self.q = q
		self.d = d
		self.a = a
		self.alpha = alpha

	def Cal_DHMatrix(self):
		return np.array([[cos(self.q), -cos(self.alpha)*sin(self.q), sin(self.alpha)*sin(self.q), self.a*cos(self.q)],
						[sin(self.q), cos(self.alpha)*cos(self.q), -sin(self.alpha)*cos(self.q), self.a*sin(self.q)],
						[0, sin(self.alpha), cos(self.alpha), self.d],
						[0,0,0,1]])
		
class Kinematics(object):
	"""docstring for Kinematics"""
	def __init__(self):
		cf = ConfigRobot()
		self.q = []
		self.d = cf.d
		self.a = cf.a
		self.alpha = cf.alpha
	def Cal_AMatrix(self, q0, q1, q2, q3):
		_A10 = DH(q0, self.d[0], self.a[0], self.alpha[0])
		_A21 = DH(q1, self.d[1], self.a[1], self.alpha[1])
		_A32 = DH(q2, self.d[2], self.a[2], self.alpha[2])
		_A43 = DH(q3, self.d[3], self.a[3], self.alpha[3])

		A10 = _A10.Cal_DHMatrix()
		A21 = _A21.Cal_DHMatrix()
		A32 = _A32.Cal_DHMatrix()
		A43 = _A43.Cal_DHMatrix()

		# RCD = np.array([[cos(beta)*cos(eta), -cos(beta)*sin(eta), sin(beta)],
		# 				[sin(_alpha)*sin(beta)*cos(eta) + cos(_alpha)*sin(eta), -sin(_alpha)*sin(beta)*sin(eta)+cos(_alpha)*cos(eta), -sin(_alpha)*cos(beta)],
		# 				[-cos(_alpha)*sin(beta)*cos(eta) + sin(_alpha)*sin(eta), cos(_alpha)*sin(beta)*sin(eta) + sin(_alpha)*cos(eta), cos(_alpha)*cos(beta)]])

		return A10.dot(A21).dot(A32).dot(A43)
	
class FwdKinematics(Kinematics):
	"""docstring for FwdKinematics"""
	def __init__(self):
		super(FwdKinematics, self).__init__()
		
	def ComputeFwd(self, q0, q1, q2, q3):
		AE = self.Cal_AMatrix(q0, q1, q2, q3)
		
		xE = AE[0][3]
		yE = AE[1][3]
		zE = AE[2][3]

		_alpha = pi/2
		beta = q0
		eta = q1 + q2 + q3

		return xE, yE, zE, _alpha, beta, eta


		
class InvKinematics(Kinematics):
	"""docstring for InvKinematics"""
	def __init__(self):
		super(InvKinematics, self).__init__()
				
	def Cal_Inv(self, xe, ye, ze, _alpha, beta, eta):
		cf = ConfigRobot()
		# c3 = cf.c[2]
		a4 = cf.a[3]
		a3 = cf.a[2]
		a2 = cf.a[1]
		a1 = cf.a[0]
		d3 = cf.d[2]
		d2 = cf.d[1]
		d1 = cf.d[0]

		A = ze - d1 - a4*sin(eta)
		B = cos(beta)*xe + sin(beta)*ye - a4*cos(eta)
		c3 = (A**2 + B**2 - a2**2 - a3**2)/(2*a2*a3)
		# cc = A*(sqrt((cf.a[2]*c3+cf.a[1])**2+cf.a[2]**2*(1-c3**2)))**-1
		cc = A/sqrt((a3*c3+a2)**2+a3**2*(1-c3**2))
		gama = acos((a3*c3/(2*a2*a3)+a2)/sqrt((a3*c3+a2)**2 + (a3**2)*(1-c3**2)))
		
		q4 = eta - acos(c3) - asin(cc) + gama
		q2 = asin(cc) - gama
		q3 = acos(c3)
		q1 = beta

		return q1, q2, q3, q4

if __name__ == "__main__":
	s = Kinematics()
	print('Matrix of EE:')
	print(s.Cal_AMatrix(0, pi, pi/2, pi/3))

	ss = FwdKinematics()
	print('\nEE position:')
	print(ss.ComputeFwd(0, pi, pi/2, pi/3))

	sss = InvKinematics()
	print('\nInverse Kinematics:')
	print(sss.Cal_Inv(-248.003, -5.3, 502.212, math.pi/2, 0, 5.7596))