import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ConfigRobot import *
from GlobalFunc import *
import OpenGLControl as DrawRB

class RobotSimulator(QMainWindow):

	def __init__(self, *args):
		super(RobotSimulator, self).__init__(*args)
		loadUi('main.ui', self)
		self.RB = DrawRB.GLWidget(self)
		self.cf = ConfigRobot()
		self.UpdateData()

	def setupUI(self):	
		self.setCentralWidget(self.RB)
		self.sliderQ1.setMinimum(-360)
		self.sliderQ1.setMaximum(360)
		self.sliderQ1.setValue(RadToDeg(self.cf.q_init[0]))
		self.sliderQ1.setTickInterval(1)
		self.sliderQ1.valueChanged.connect(lambda: self.valueChangeQVars(0, self.sliderQ1.value()))

		self.sliderQ2.setMinimum(-360)
		self.sliderQ2.setMaximum(360)
		self.sliderQ2.setValue(RadToDeg(self.cf.q_init[1]))
		self.sliderQ2.setTickInterval(1)
		self.sliderQ2.valueChanged.connect(lambda: self.valueChangeQVars(1, self.sliderQ2.value()))

		self.sliderQ3.setMinimum(-360)
		self.sliderQ3.setMaximum(360)
		self.sliderQ3.setValue(RadToDeg(self.cf.q_init[2]))
		self.sliderQ3.setTickInterval(1)
		self.sliderQ3.valueChanged.connect(lambda: self.valueChangeQVars(2, self.sliderQ3.value()))

		self.sliderQ4.setMinimum(-360)
		self.sliderQ4.setMaximum(360)
		self.sliderQ4.setValue(RadToDeg(self.cf.q_init[3]))
		self.sliderQ4.setTickInterval(1)
		self.sliderQ4.valueChanged.connect(lambda: self.valueChangeQVars(3, self.sliderQ4.value()))

	def valueChangeQVars(self, index, value):
		self.RB.q[index] = DegToRad(value)
		self.RB.updateGL()
		self.UpdateData()

	def UpdateData(self):
		self.valueQ1.setText(str(int(RadToDeg(self.RB.q[0]))))
		self.valueQ2.setText(str(int(RadToDeg(self.RB.q[1]))))
		self.valueQ3.setText(str(int(RadToDeg(self.RB.q[2]))))
		self.valueQ4.setText(str(int(RadToDeg(self.RB.q[3]))))

app = QApplication(sys.argv)
window = RobotSimulator()
window.setupUI()
window.show()
sys.exit(app.exec_())