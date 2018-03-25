from PyQt4 import QtCore, QtGui
from PyQt4 import QtOpenGL
from OpenGL import GLU
from OpenGL.GL import *
from numpy import array

class GLWidget(QtOpenGL.QGLWidget):
	xRotationChanged = QtCore.pyqtSignal(int)
	yRotationChanged = QtCore.pyqtSignal(int)
	zRotationChanged = QtCore.pyqtSignal(int)

	def __init__(self, parent=None):
		super(GLWidget, self).__init__(parent)

		self.gear1 = 0
		self.gear2 = 0
		self.gear3 = 0
		self.xRot = 0
		self.yRot = 0
		self.zRot = 0
		self.z_zoom = -30

	def setXRotation(self, angle):
		self.normalizeAngle(angle)

		if angle != self.xRot:
			self.xRot = angle
			self.xRotationChanged.emit(angle)
			self.updateGL()

	def setYRotation(self, angle):
		self.normalizeAngle(angle)

		if angle != self.yRot:
			self.yRot = angle
			self.yRotationChanged.emit(angle)
			self.updateGL()

	def setZRotation(self, angle):
		self.normalizeAngle(angle)

		if angle != self.zRot:
			self.zRot = angle
			self.zRotationChanged.emit(angle)
			self.updateGL()

	def setZoom(self, zoom):
		self.z_zoom = zoom
		self.updateGL()

	def initializeGL(self):
		lightPos = (5.0, 5.0, 10.0, 1.0)
		reflectance1 = (0.8, 0.1, 0.0, 1.0)
		reflectance2 = (0.0, 0.8, 0.2, 1.0)
		reflectance3 = (0.2, 0.2, 1.0, 1.0)

		glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_NORMALIZE)
		glClearColor(0.0, 0.0, 0.0, 1.0)

	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glPushMatrix()
		glTranslate(0, 0, self.z_zoom)
		glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
		glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
		glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
		glRotated(+90.0, 1.0, 0.0, 0.0)
		self.drawGrid()

		glPopMatrix()

	def resizeGL(self, width, height):
		side = min(width, height)
		if side < 0:
			return
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		GLU.gluPerspective(35.0, width / float(height), 0.01, 2000.0)

		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glTranslated(0.0, 0.0, -40.0)

	def mousePressEvent(self, event):
		self.lastPos = event.pos()

	def drawGrid(self):
		glPushMatrix()
		color = [0.0, 1.0, 1.0]
		glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color);
		step = 1
		num = 24
		for i in xrange(-num, num+1):
			glBegin(GL_LINES)
			glVertex3f(i*step, -num * step, 0)
			glVertex3f(i*step, num*step, 0)
			glVertex3f(-num * step, i*step, 0)
			glVertex3f(num*step, i*step, 0)
			glEnd()
		glPopMatrix()

	def mouseMoveEvent(self, event):
		dx = event.x() - self.lastPos.x()
		dy = event.y() - self.lastPos.y()

		if event.buttons() & QtCore.Qt.LeftButton:
			self.setXRotation(self.xRot + 8 * dy)
			self.setYRotation(self.yRot + 8 * dx)
		elif event.buttons() & QtCore.Qt.RightButton:
			self.setZoom(self.z_zoom + 0.5*dy)
		elif event.buttons() & QtCore.Qt.MidButton:
			self.setXRotation(self.xRot + 8 * dy)
			self.setZRotation(self.zRot + 8 * dx)

		self.lastPos = event.pos()

	def xRotation(self):
		return self.xRot

	def yRotation(self):
		return self.yRot

	def zRotation(self):
		return self.zRot  

	def normalizeAngle(self, angle):
		while (angle < 0):
			angle += 360 * 16

		while (angle > 360 * 16):
			angle -= 360 * 16