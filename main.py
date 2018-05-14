import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


from GlobalFunc import *
import OpenGLControl as DrawRB
from Robot import *

class RobotSimulator(QMainWindow):

	def __init__(self, *args):
		super(RobotSimulator, self).__init__(*args)
		loadUi('main.ui', self)
		self.objRB = Robot()
		self.RB = DrawRB.GLWidget(self, self.objRB)
		# self.objRB.cf = ConfigRobot()
		self.UpdateData()

	def setupUI(self):	
		self.setCentralWidget(self.RB)
		self.sliderQ1.setMinimum(-360)
		self.sliderQ1.setMaximum(360)
		self.sliderQ1.setValue(RadToDeg(self.objRB.cf.q_init[1]))
		self.sliderQ1.setTickInterval(1)
		self.sliderQ1.sliderMoved.connect(lambda: self.valueChangeJVars(1, self.sliderQ1.value()))

		self.sliderQ2.setMinimum(-360)
		self.sliderQ2.setMaximum(360)
		self.sliderQ2.setValue(RadToDeg(self.objRB.cf.q_init[2]))
		self.sliderQ2.setTickInterval(1)
		self.sliderQ2.sliderMoved.connect(lambda: self.valueChangeJVars(2, self.sliderQ2.value()))

		self.sliderQ3.setMinimum(-360)
		self.sliderQ3.setMaximum(360)
		self.sliderQ3.setValue(RadToDeg(self.objRB.cf.q_init[3]))
		self.sliderQ3.setTickInterval(1)
		self.sliderQ3.sliderMoved.connect(lambda: self.valueChangeJVars(3, self.sliderQ3.value()))

		self.sliderQ4.setMinimum(-360)
		self.sliderQ4.setMaximum(360)
		self.sliderQ4.setValue(RadToDeg(self.objRB.cf.q_init[4]))
		self.sliderQ4.setTickInterval(1)
		self.sliderQ4.sliderMoved.connect(lambda: self.valueChangeJVars(4, self.sliderQ4.value()))

		# self.setCentralWidget(self.RB)
		self.sliderX.setMinimum(-1000)
		self.sliderX.setMaximum(1000)
		self.sliderX.setValue(self.objRB.x)
		self.sliderX.setTickInterval(1)
		self.sliderX.sliderMoved.connect(self.valueChangeEVars)

		self.sliderY.setMinimum(-1000)
		self.sliderY.setMaximum(1000)
		self.sliderY.setValue(self.objRB.y)
		self.sliderY.setTickInterval(1)
		self.sliderY.sliderMoved.connect(self.valueChangeEVars)

		self.sliderZ.setMinimum(-1000)
		self.sliderZ.setMaximum(1000)
		self.sliderZ.setValue(self.objRB.z)
		self.sliderZ.setTickInterval(1)
		self.sliderZ.sliderMoved.connect(self.valueChangeEVars)

		self.sliderAngleR.setMinimum(-360)
		self.sliderAngleR.setMaximum(360)
		self.sliderAngleR.setValue(RadToDeg(self.objRB.psi))
		self.sliderAngleR.setTickInterval(1)
		self.sliderAngleR.sliderMoved.connect(self.valueChangeEVars)

		self.sliderAngleP.setMinimum(-360)
		self.sliderAngleP.setMaximum(360)
		self.sliderAngleP.setValue(RadToDeg(self.objRB.theta))
		self.sliderAngleP.setTickInterval(1)
		self.sliderAngleP.sliderMoved.connect(self.valueChangeEVars)

		self.sliderAngleY.setMinimum(-360)
		self.sliderAngleY.setMaximum(360)
		self.sliderAngleY.setValue(RadToDeg(self.objRB.phi))
		self.sliderAngleY.setTickInterval(1)
		self.sliderAngleY.sliderMoved.connect(self.valueChangeEVars)


	def valueChangeJVars(self, index, value):
		self.objRB.q[index] = DegToRad(value)
		self.objRB.CalFwdPostion(*tuple(self.objRB.q[1:]))
		self.RB.updateGL()
		self.UpdateData()

	def valueChangeEVars(self):
		x = self.sliderX.value()
		y = self.sliderY.value()
		z = self.sliderZ.value()
		psi = DegToRad(self.sliderAngleR.value())
		theta = DegToRad(self.sliderAngleP.value())
		phi =  DegToRad(self.sliderAngleY.value())
		# print(x, " ", y)
		self.objRB.CalInvPostion(x, y, z, psi, theta, phi)
		self.RB.updateGL()

		# self.UpdateData()

	def UpdateData(self):
		self.valueQ1.setText(str(int(RadToDeg(self.objRB.q[1]))))
		self.valueQ2.setText(str(int(RadToDeg(self.objRB.q[2]))))
		self.valueQ3.setText(str(int(RadToDeg(self.objRB.q[3]))))
		self.valueQ4.setText(str(int(RadToDeg(self.objRB.q[4]))))
		self.valueX.setText(str(format(self.objRB.x, '.2f')))
		self.valueY.setText(str(format(self.objRB.y, '.2f')))
		self.valueZ.setText(str(format(self.objRB.z, '.2f')))
		self.valueAngleR.setText(str(int(RadToDeg(self.objRB.psi))))
		self.valueAngleP.setText(str(int(RadToDeg(self.objRB.theta))))
		self.valueAngleY.setText(str(int(RadToDeg(self.objRB.phi))))
		self.sliderX.setValue(int(self.objRB.x))
		self.sliderY.setValue(int(self.objRB.y))
		self.sliderZ.setValue(int(self.objRB.x))
		self.sliderAngleR.setValue(int(RadToDeg(self.objRB.psi)))
		self.sliderAngleP.setValue(int(RadToDeg(self.objRB.theta)))
		self.sliderAngleY.setValue(int(RadToDeg(self.objRB.phi)))


app = QApplication(sys.argv)
window = RobotSimulator()
window.setupUI()
window.show()
sys.exit(app.exec_())