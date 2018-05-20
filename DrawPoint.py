from OpenGL import GLU
from OpenGL.GL import *

class DrawPoint(object):
	"""Draw points of trajectory"""
	def __init__(self):
		super(DrawPoint, self).__init__()
		self.x = None
		self.y = None
		self.z = None
		self.color = None
		self.size = None

	def SetProperties(self, x, y, z, color, size):
		self.x = x
		self.y = y
		self.z = z
		self.color = color
		self.size = size

	def Draw(self):
		glPushMatrix()
		glTranslate(self.x, self.y, self.z)
		glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.color);
		glutSolidSphere(self.size, 10, 10)
		glPopMatrix()
