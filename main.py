import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import OpenGLControl as DrawRB
from PyQt5.QtWidgets import QApplication
from ConfigRobot import *
class RobotSimulator(QMainWindow, QTabWidget):
	def tick():
		self.RB.q1 = self.RB.q1 + 1
		self.RB.updateJoint()

	def __init__(self, parent = None):
		super(RobotSimulator, self).__init__(parent)
		self.timer = QTimer()
		self.cf = ConfigRobot()
		# create menu
		bar = self.menuBar()
		file = bar.addMenu("File")
		file.addAction("New")
		file.addAction("Save")
		file.addAction("Quit")
		file.addAction("Open")

		self.RB = DrawRB.GLWidget(self)
		self.setCentralWidget(self.RB)

		# Setup Dock Control
		self.items = QDockWidget("Control", self)


		win = QWidget()
		fbox = QFormLayout()	
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox3 = QHBoxLayout()
		hbox4 = QHBoxLayout()

		self.tabs = QTabWidget()
		self.tab1 = QWidget()
		self.tab2 = QWidget()

		# add tab
		self.tabs.addTab(self.tab1, "Joint")
		self.tabs.addTab(self.tab2, "End Effector")
		# components of tab1
		self.tab1.layout = QFormLayout(self)
		self.sliderQ1 = QSlider(Qt.Horizontal)
		self.sliderQ2 = QSlider(Qt.Horizontal)
		self.sliderQ3 = QSlider(Qt.Horizontal)
		self.sliderQ4 = QSlider(Qt.Horizontal)
		self.valueQ1 = QLineEdit()
		self.valueQ2 = QLineEdit()
		self.valueQ3 = QLineEdit()
		self.valueQ4 = QLineEdit()

		self.sliderQ1.setMinimum(-360)
		self.sliderQ1.setMaximum(360)
		self.sliderQ1.setValue(RadToDeg(self.cf.q_init[0]))
		self.sliderQ1.setTickPosition(QSlider.TicksBelow)
		self.sliderQ1.setTickInterval(1)
		self.sliderQ1.valueChanged.connect(lambda: self.valueChangeQVars(0, self.sliderQ1.value()))

		self.sliderQ2.setMinimum(-360)
		self.sliderQ2.setMaximum(360)
		self.sliderQ2.setValue(RadToDeg(self.cf.q_init[1]))
		self.sliderQ2.setTickPosition(QSlider.TicksBelow)
		self.sliderQ2.setTickInterval(1)
		self.sliderQ2.valueChanged.connect(lambda: self.valueChangeQVars(1, self.sliderQ2.value()))

		self.sliderQ3.setMinimum(-360)
		self.sliderQ3.setMaximum(360)
		self.sliderQ3.setValue(RadToDeg(self.cf.q_init[2]))
		self.sliderQ3.setTickPosition(QSlider.TicksBelow)
		self.sliderQ3.setTickInterval(1)
		self.sliderQ3.valueChanged.connect(lambda: self.valueChangeQVars(2, self.sliderQ3.value()))

		self.sliderQ4.setMinimum(-360)
		self.sliderQ4.setMaximum(360)
		self.sliderQ4.setValue(RadToDeg(self.cf.q_init[3]))
		self.sliderQ4.setTickPosition(QSlider.TicksBelow)
		self.sliderQ4.setTickInterval(1)
		self.sliderQ4.valueChanged.connect(lambda: self.valueChangeQVars(3, self.sliderQ4.value()))

		hbox1.addWidget(self.sliderQ1)
		hbox1.addWidget(self.valueQ1)
		hbox1.addStretch()
		hbox2.addWidget(self.sliderQ2)
		hbox2.addWidget(self.valueQ2)
		hbox2.addStretch()
		hbox3.addWidget(self.sliderQ3)
		hbox3.addWidget(self.valueQ3)
		hbox3.addStretch()
		hbox4.addWidget(self.sliderQ4)
		hbox4.addWidget(self.valueQ4)
		hbox4.addStretch()

		textslderQ1 = QLabel("q1")
		textslderQ2 = QLabel("q2")
		textslderQ3 = QLabel("q3")
		textslderQ4 = QLabel("q4")
		self.tab1.layout.addRow(textslderQ1,hbox1)
		self.tab1.layout.addRow(textslderQ2,hbox2)
		self.tab1.layout.addRow(textslderQ3,hbox3)
		self.tab1.layout.addRow(textslderQ4,hbox4)
		self.tab1.layout.addRow(QPushButton("KHUONG"))
		self.tab1.setLayout(self.tab1.layout)

		# components of tab2
		self.tab2.layout = QFormLayout(self)
		# self.sliderX = QSlider(Qt.Horizontal)
		# self.sliderY = QSlider(Qt.Horizontal)
		# self.sliderZ = QSlider(Qt.Horizontal)
		# self.sliderR = QSlider(Qt.Horizontal)
		# self.sliderP = QSlider(Qt.Horizontal)
		# self.sliderY = QSlider(Qt.Horizontal)
		# self.valueX = QLineEdit()
		# self.valueY = QLineEdit()
		# self.valueZ = QLineEdit()
		# self.valueR = QLineEdit()
		# self.valueP = QLineEdit()
		# self.valueY = QLineEdit()
		# self.sliderX.setMinimum(-1000)
		# self.sliderX.setMaximum(1000)
		# self.sliderQ1.setValue(RadToDeg(self.cf.q_init[0]))
		# self.sliderQ1.setTickPosition(QSlider.TicksBelow)
		# self.sliderQ1.setTickInterval(1)
		# self.sliderQ1.valueChanged.connect(lambda :valueChangeQVars(0, self.sliderQ1.value()))

		# self.sliderQ2.setMinimum(-360)
		# self.sliderQ2.setMaximum(360)
		# self.sliderQ2.setValue(RadToDeg(self.cf.q_init[1]))
		# self.sliderQ2.setTickPosition(QSlider.TicksBelow)
		# self.sliderQ2.setTickInterval(1)
		# self.sliderQ2.valueChanged.connect(self.valuechangeslider2)

		# self.sliderQ3.setMinimum(-360)
		# self.sliderQ3.setMaximum(360)
		# self.sliderQ3.setValue(RadToDeg(self.cf.q_init[2]))
		# self.sliderQ3.setTickPosition(QSlider.TicksBelow)
		# self.sliderQ3.setTickInterval(1)
		# self.sliderQ3.valueChanged.connect(self.valuechangeslider3)

		# self.sliderQ4.setMinimum(-360)
		# self.sliderQ4.setMaximum(360)
		# self.sliderQ4.setValue(RadToDeg(self.cf.q_init[3]))
		# self.sliderQ4.setTickPosition(QSlider.TicksBelow)
		# self.sliderQ4.setTickInterval(1)
		# self.sliderQ4.valueChanged.connect(self.valuechangeslider4)

		# hbox1.addWidget(self.sliderQ1)
		# hbox1.addWidget(self.value1)
		# hbox1.addStretch()
		# hbox2.addWidget(self.sliderQ2)
		# hbox2.addWidget(self.value2)
		# hbox2.addStretch()
		# hbox3.addWidget(self.sliderQ3)
		# hbox3.addWidget(self.value3)
		# hbox3.addStretch()
		# hbox4.addWidget(self.sliderQ4)
		# hbox4.addWidget(self.value4)
		# hbox4.addStretch()

		# textslder_1 = QLabel("q1")
		# textslder_2 = QLabel("q2")
		# textslder_3 = QLabel("q3")
		# textslder_4 = QLabel("q4")
		# self.tab2.layout.addRow(textslder_1,hbox1)
		# self.tab2.layout.addRow(textslder_2,hbox2)
		# self.tab2.layout.addRow(textslder_3,hbox3)
		# self.tab2.layout.addRow(textslder_4,hbox4)
		# self.tab2.layout.addRow(QPushButton("KHUONG"))
		self.tab2.setLayout(self.tab2.layout)
		# add tabs to widget
		fbox.addWidget(self.tabs)
		win.setLayout(fbox)
		self.items.setWidget(win)
		self.items.setFloating(False)
		self.addDockWidget(Qt.RightDockWidgetArea, self.items)

		# Setup properties of program
		self.setWindowTitle("Robot Design")

	def valueChangeQVars(self, index, value):
		self.RB.q[index] = DegToRad(value)
		self.RB.updateGL()

def main():
	app = QApplication(sys.argv)
	ex = RobotSimulator()
	ex.setGeometry(100,100,1000,800)
	ex.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
