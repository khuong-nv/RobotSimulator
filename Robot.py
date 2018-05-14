from ConfigRobot import *
from Kinematics import *
class Robot(object):
	"""docstring for Robot"""
	def __init__(self):
		super(Robot, self).__init__()
		self.cf = ConfigRobot()
		self.q = self.cf.q_init
		self.d = self.cf.d
		self.a = self.cf.a
		self.alpha = self.cf.alpha
		self.fwd = FwdKinematics()
		self.inv = InvKinematics()
		self.x, self.y, self.z, self.psi, self.theta, self.phi = self.fwd.Cal_Fwd_Position(*tuple(self.q[1:]))
	
	def CalFwdPostion(self, q1, q2, q3, q4):
		self.x, self.y, self.z, self.psi, self.theta, self.phi = self.fwd.Cal_Fwd_Position(q1, q2, q3, q4)

	def CalInvPostion(self, x, y, z, psi, theta, phi):
		self.x = x
		self.y = y
		self.z = z
		self.psi = psi
		self.theta = theta
		self.phi = phi
		result = tuple()
		print(x, " ", y)
		result = self.inv.Cal_Inv_Position(self.x, self.y, self.z, self.psi, self.theta, self.phi)
		self.q[1:] = list(result)


	def GetCurrentPostion(self):
		return self.x, self.y, self.z

	def GetCurrentAngle(self):
		return self.psi, self.theta, self.phi

	def GetCurrentStatus(self):
		return self.GetCurrentPostion() + self.GetCurrentAngle()