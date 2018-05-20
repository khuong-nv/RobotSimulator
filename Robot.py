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
		self.JVars = self.cf.q_init[1:]
		self.q1P = self.JVars
		self.q2P = self.JVars
		self.EVars = []
		self.EVars = self.fwd.Cal_Fwd_Position(self.JVars)
	
	def CalFwdPostion(self, JVars):
		self.JVars = JVars
		self.q1P = self.q2P = JVars
		self.EVars = self.fwd.Cal_Fwd_Position(JVars)

	def CalInvPostion(self, EVars):
		sol = self.inv.FindTheBestSolution(EVars, self.q1P, self.q2P)
		if sol != None:
			result = self.inv.Cal_Inv_Position(EVars, sol)
			if result[0] != False:
				self.x = EVars[0]
				self.y = EVars[1]
				self.z = EVars[2]
				self.psi = EVars[3]
				self.theta = EVars[4]
				self.phi = EVars[5]
				self.JVars= result[1]
				self.q2P = self.q1P
				self.q1P = self.JVars
			else:
				print("error while calculate")
				
	def CalInvPositionEx(self, EVars, q1p, q2p):
		sol = self.inv.FindTheBestSolution(EVars, q1p, q2p)
		if sol != None:
			result = self.inv.Cal_Inv_Position(EVars, sol)
			if result[0] != False:
				JVars= result[1]
				return JVars
			else:
				print("error while calculate")
				return None
		else:
			return None

	def GetCurrentStatus(self):
		return self.EVars