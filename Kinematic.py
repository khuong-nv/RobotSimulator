# tinh toan thiet ke robot - viet class tinh toan dong hoc thuan, dong hoc nguoc cua robot 4 bac tu do:
# 	BasicClass: tinh toan bang DH, vi tri khau tac dong cuoi
# 	ForwardClass: Tinh toan dong hoc thuan robot
# 	ReverseClass: Tinh toan dong hoc nguoc robot

import numpy as np 
# import scipy
# import matplotlib.pyplot as plt 
import math

class ConfigRobot(object):
	"""docstring for ConfigRobot"""
	def __init__(self):
		self.q = [0, 0, 0, 0]
		self.d = [256, 150, 150, 0]
		self.a = [0, 832, 876, 185]
		self.alpha = [math.pi/2, 0, 0, 0]

		self.qmin = np.array([-180, -180, -180, -180])*math.pi/180.0
		self.qmax = np.array([180, 180, 180, 180])*math.pi/180.0
	def setDHparameter(self, q, d, a, alpha):
		self.q = q
		self.d = d
		self.a = a
		self.alpha = alpha

class Kinematics(object):
	"""Kinematics"""
	def __init__(self):
		config = ConfigRobot()
		self.q = []
		self.d = config.d
		self.a = config.a
		self.alpha = config.alpha

	def setJoint(self, q):
		self.q = q

	def DH_matrix(self, q, d, a, alpha):
		return np.array([[math.cos(q), -math.cos(alpha)*math.sin(q), math.sin(alpha)*math.sin(q), a*math.cos(q)],
						[math.sin(q), math.cos(alpha)*math.cos(q), -math.sin(alpha)*math.cos(q), a*math.sin(q)],
						[0, math.sin(alpha), math.cos(alpha), d],
						[0,0,0,1]])

class ForwardKinematics(Kinematics):
	"""docstring for ForwardKinematics"""
	def __init__(self):
		super(ForwardKinematics, self).__init__()
	def ComputeEEPositon(self):
		A10 = self.DH_matrix(self.q[0], self.d[0], self.a[0], self.alpha[0])
		A21 = self.DH_matrix(self.q[1], self.d[1], self.a[1], self.alpha[1])
		A32 = self.DH_matrix(self.q[2], self.d[2], self.a[2], self.alpha[2])
		A43 = self.DH_matrix(self.q[3], self.d[3], self.a[3], self.alpha[3])
		A40 = A10.dot(A21).dot(A32).dot(A43)
		return [A40[0, 3], A40[1, 3], A40[2, 3]]
	def ComputeEEVel(self):
		pass 

def main():
	q1 = math.pi/2
	q2 = math.pi/(-3)
	q3 = math.pi/(6)
	q4 = math.pi/(-6)
	Fwd = ForwardKinematics()
	Fwd.setJoint([q1, q2, q3, q4])
	EEMatrix = Fwd.ComputeEEPositon()
	print EEMatrix[0], EEMatrix[1], EEMatrix[2]

		
if __name__ == '__main__':
	main()

# class FwdKinematics():
# 	def __init__(self, EE_Matrix):
# 	 	self.EE_Matrix = EE_Matrix
# 	def Fwd(self, EE_Matrix):
# 		EE = list(EE_Matrix)
# 		for i in EE_Matrix:
# 			EE.append(i)

#Ma tran goc cardan:
# CDM = np.array([[cos(beta)*cos(eta), -cos(beta)*sin(eta), sin(beta)],
# 				[sin(gama)*sin(beta)*cos(eta)+cos(gama)*sin(eta), -sin(gama)*sin(beta)*sin(eta)+cos(gama)*cos(eta), -sin(gama)*cos(beta)],
# 				[-cos(gama)*sin(beta)*cos(eta) + sin(gama)*sin(eta), cos(gama)*sin(beta)*sin(eta) + sin(gama)*cos(eta), cos(gama)*cos(beta)]])

#Ma tran quay khau tac dong cuoi:
# Aee = np.array([[]])

# if __name__ == "__main__":
# 	q1 = math.pi/2
# 	q2 = math.pi/(-3)
# 	q3 = math.pi/(6)
# 	q4 = math.pi/(-6)
# 	A01 = Kinematics(q1, 256, 0, math.pi/2)
# 	A12 = Kinematics(q2, 150, 832, 0)
# 	A23 = Kinematics(q3, 150, 876, 0)
# 	A34 = Kinematics(q4, 0, 185, 0)
# 	A0 = A01.DH_table(q1, 256, 0, math.pi/2)
# 	A1 = A12.DH_table(q2, 150, 832, 0)
# 	A2 = A23.DH_table(q3, 150, 876, 0)
# 	A3 = A34.DH_table(q4, 0, 185, 0)
# 	A02 = A0.dot(A1)
# 	A03 = A02.dot(A2)
# 	A04 = A03.dot(A3)
# 	print('\n\nA01 = \n',A0,'\n\n A12 = \n',A1,'\n\n A23 = \n',A2,'\n\n A34 = \n',A3, '\n\n A04 = \n',A04)
# 	#Vi tri khau thao tac cuoi
# 	# EE1 = FwdKinematics(A04)
# 	# EE = EE1.Fwd(A04)
# 	# xE = EE[0]
# 	# yE = EE[1]
# 	# zE = EE[2]
# 	# print(EE)
# 	xE = A04[0,3]
# 	yE = A04[1,3]
# 	zE = A04[2,3]
# 	print('\nVi tri khau thao tac cuoi:','\nxE = ',xE, '\nyE = ',yE, '\nzE = ',zE)
# 	#Cac goc quay cua khau cuoi
# 	gama = math.pi
# 	beta = q1
# 	eta = q2 + q3 + q4
