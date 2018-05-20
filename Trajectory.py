import numpy as np 
from math import *

class Trajectory(object):
	def __init__(self, startPoint = None, endPoint = None):
		#startPoint and endPoint are numpy arrays
		self.startPoint = startPoint
		self.endPoint = endPoint
		self.sp_time = 0.5

	def SetPoint(self, startPoint, endPoint):
		self.startPoint = startPoint
		self.endPoint = endPoint

	def SetSpTime(self, time):
		self.sp_time = time

	def Calculate(self):
		distance = np.linalg.norm(self.endPoint - self.startPoint)
		v0 = 0.2
		T = int(distance/v0)
		numT = int(T/self.sp_time)
		s0 = 0; sn = distance
		h = sn - s0
		a0 = s0
		a1 = 0
		a2 = 0
		a3 = 1.0/(2 * T**3) * 20*h
		a4 = 1.0/(2 * T**4) * (-30)*h
		a5 = 1.0/(2 * T**5) * 12*h
		point = np.array([[None, None, None]])
		for i in range(numT+1):
			t = i*T/numT
			s = a0 + a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5
			point = np.append(point, [self.startPoint + ((self.endPoint - self.startPoint)/distance) * s], axis = 0)
		point = np.delete(point, 0, axis = 0)
		return point