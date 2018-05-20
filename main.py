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
from Trajectory import *
from numpy import arange, append, delete

class RobotSimulator(QMainWindow):

	def __init__(self, *args):
		super(RobotSimulator, self).__init__(*args)
		loadUi('main.ui', self)
		self.objRB = Robot()
		self.RB = DrawRB.GLWidget(self, self.objRB)
		# self.objRB.cf = ConfigRobot()
		self.UpdateData(1)
		self.UpdateData(2)
		self.fileName = None
		self.AllPoints = np.array([[None, None, None]])
		self.AllJVars = np.array([[None, None, None, None]])

	def setupUI(self):	
		self.setCentralWidget(self.RB)
		self.sliderQ1.setMinimum(-360)
		self.sliderQ1.setMaximum(360)
		self.sliderQ1.setValue(RadToDeg(self.objRB.cf.q_init[1]))
		self.sliderQ1.setTickInterval(1)
		self.sliderQ1.sliderMoved.connect(lambda: self.valueChangeJVars(0, self.sliderQ1.value()))

		self.sliderQ2.setMinimum(-360)
		self.sliderQ2.setMaximum(360)
		self.sliderQ2.setValue(RadToDeg(self.objRB.cf.q_init[2]))
		self.sliderQ2.setTickInterval(1)
		self.sliderQ2.sliderMoved.connect(lambda: self.valueChangeJVars(1, self.sliderQ2.value()))

		self.sliderQ3.setMinimum(-360)
		self.sliderQ3.setMaximum(360)
		self.sliderQ3.setValue(RadToDeg(self.objRB.cf.q_init[3]))
		self.sliderQ3.setTickInterval(1)
		self.sliderQ3.sliderMoved.connect(lambda: self.valueChangeJVars(2, self.sliderQ3.value()))

		self.sliderQ4.setMinimum(-360)
		self.sliderQ4.setMaximum(360)
		self.sliderQ4.setValue(RadToDeg(self.objRB.cf.q_init[4]))
		self.sliderQ4.setTickInterval(1)
		self.sliderQ4.sliderMoved.connect(lambda: self.valueChangeJVars(3, self.sliderQ4.value()))

		# self.setCentralWidget(self.RB)
		self.sliderX.setMinimum(-1000)
		self.sliderX.setMaximum(1000)
		self.sliderX.setValue(self.objRB.EVars[0])
		self.sliderX.setTickInterval(1)
		self.sliderX.sliderMoved.connect(self.valueChangeEVars)

		self.sliderY.setMinimum(-1000)
		self.sliderY.setMaximum(1000)
		self.sliderY.setValue(self.objRB.EVars[1])
		self.sliderY.setTickInterval(1)
		self.sliderY.sliderMoved.connect(self.valueChangeEVars)

		self.sliderZ.setMinimum(-1000)
		self.sliderZ.setMaximum(1000)
		self.sliderZ.setValue(self.objRB.EVars[2])
		self.sliderZ.setTickInterval(1)
		self.sliderZ.sliderMoved.connect(self.valueChangeEVars)

		self.sliderAngleR.setMinimum(-360)
		self.sliderAngleR.setMaximum(360)
		self.sliderAngleR.setValue(RadToDeg(self.objRB.EVars[3]))
		self.sliderAngleR.setTickInterval(1)
		self.sliderAngleR.sliderMoved.connect(self.valueChangeEVars)

		self.sliderAngleP.setMinimum(-360)
		self.sliderAngleP.setMaximum(360)
		self.sliderAngleP.setValue(RadToDeg(self.objRB.EVars[4]))
		self.sliderAngleP.setTickInterval(1)
		self.sliderAngleP.sliderMoved.connect(self.valueChangeEVars)

		self.sliderAngleY.setMinimum(-360)
		self.sliderAngleY.setMaximum(360)
		self.sliderAngleY.setValue(RadToDeg(self.objRB.EVars[5]))
		self.sliderAngleY.setTickInterval(1)
		self.sliderAngleY.sliderMoved.connect(self.valueChangeEVars)

		self.sliderAngleR.setEnabled = False
		self.btnOpenFile.clicked.connect(self.openFileNameDialog)
		self.btnLoadFile.clicked.connect(self.LoadFile)
		self.btnRun.clicked.connect(self.Run)

	def valueChangeJVars(self, index, value):
		self.objRB.JVars[index] = DegToRad(value)
		self.objRB.CalFwdPostion(self.objRB.JVars)
		self.RB.updateGL()
		self.UpdateData(1)

	def valueChangeEVars(self):
		x = self.sliderX.value()
		y = self.sliderY.value()
		z = self.sliderZ.value()
		psi = DegToRad(self.sliderAngleR.value())
		theta = DegToRad(self.sliderAngleP.value())
		phi =  DegToRad(self.sliderAngleY.value())
		EVars = [x, y, z, psi, theta, phi]
		self.objRB.CalInvPostion(EVars)
		self.UpdateData(2)
		self.RB.updateGL()

	def openFileNameDialog(self):    
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.fileName, _ = QFileDialog.getOpenFileName(self,"Openfile", "","Gcode Files (*.gcode);;All Files (*)", options=options)
		self.processLoadFile.setValue(0)

	def LoadFile(self):
		listPoint = LoadGCode(self.fileName, self.objRB.EVars[0], self.objRB.EVars[1], self.objRB.EVars[2])
		self.RB.updateGL()
		trj = Trajectory()
		for i in arange(len(listPoint)-1):
			p1 = listPoint[i][:3]
			p2 = listPoint[i+1][:3]
			trj.SetPoint(p1, p2)
			points = trj.Calculate()
			self.AllPoints = np.append(self.AllPoints, points, axis = 0)

		self.AllPoints = np.delete(self.AllPoints, 0, axis = 0)
		self.RB.listPoints = self.AllPoints
		self.processLoadFile.setValue(100)

	def Run(self):
		q1P = self.objRB.q1P
		q2P = self.objRB.q2P
		for p in self.AllPoints:
			EVars = np.append(p, [self.objRB.EVars[3], self.objRB.EVars[4], self.objRB.EVars[5]])
			JVar = self.objRB.CalInvPositionEx(EVars, q1P, q2P)
			if JVar == None:
				break
			self.AllJVars = np.append(self.AllJVars, [JVar], axis = 0)
			q2P = q1P
			q1P = JVar
			
		print(self.AllJVars)


			

	def UpdateData(self, tabsel):
		if tabsel == 1:
			self.sliderX.setValue(int(self.objRB.EVars[0]))
			self.sliderY.setValue(int(self.objRB.EVars[1]))
			self.sliderZ.setValue(int(self.objRB.EVars[2]))
			self.sliderAngleR.setValue(int(RadToDeg(self.objRB.EVars[3])))
			self.sliderAngleP.setValue(int(RadToDeg(self.objRB.EVars[4])))
			self.sliderAngleY.setValue(int(RadToDeg(self.objRB.EVars[5])))
		elif tabsel == 2:
			self.valueQ1.setText(str(int(RadToDeg(self.objRB.JVars[0]))))
			self.valueQ2.setText(str(int(RadToDeg(self.objRB.JVars[1]))))
			self.valueQ3.setText(str(int(RadToDeg(self.objRB.JVars[2]))))
			self.valueQ4.setText(str(int(RadToDeg(self.objRB.JVars[3]))))
			self.sliderQ1.setValue(int(RadToDeg(self.objRB.JVars[0])))
			self.sliderQ2.setValue(int(RadToDeg(self.objRB.JVars[1])))
			self.sliderQ3.setValue(int(RadToDeg(self.objRB.JVars[2])))
			self.sliderQ4.setValue(int(RadToDeg(self.objRB.JVars[3])))

		self.valueQ1.setText(str(int(RadToDeg(self.objRB.JVars[0]))))
		self.valueQ2.setText(str(int(RadToDeg(self.objRB.JVars[1]))))
		self.valueQ3.setText(str(int(RadToDeg(self.objRB.JVars[2]))))
		self.valueQ4.setText(str(int(RadToDeg(self.objRB.JVars[3]))))

		self.valueX.setText(str(format(self.objRB.EVars[0], '.2f')))
		self.valueY.setText(str(format(self.objRB.EVars[1], '.2f')))
		self.valueZ.setText(str(format(self.objRB.EVars[2], '.2f')))
		self.valueAngleR.setText(str(int(RadToDeg(self.objRB.EVars[3]))))
		self.valueAngleP.setText(str(int(RadToDeg(self.objRB.EVars[4]))))
		self.valueAngleY.setText(str(int(RadToDeg(self.objRB.EVars[5]))))

app = QApplication(sys.argv)
window = RobotSimulator()
window.setupUI()
window.show()
sys.exit(app.exec_())