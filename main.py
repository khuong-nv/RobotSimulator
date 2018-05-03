import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import OpenGLControl as DrawRB
from PyQt5.QtWidgets import QApplication
class RobotSimulator(QMainWindow, QTabWidget):
	def tick():
		self.glWidget.q1 = self.glWidget.q1 + 1
		self.glWidget.updateJoint()

	def __init__(self, parent = None):
		super(RobotSimulator, self).__init__(parent)
		self.timer = QTimer()
		# create menu
		bar = self.menuBar()
		file = bar.addMenu("File")
		file.addAction("New")
		file.addAction("Save")
		file.addAction("Quit")
		file.addAction("Open")

		# embeded OpenGL into Widget
		# glWidget = OpenGLControl.GLWidget(self)
		self.glWidget = DrawRB.GLWidget(self)
		self.setCentralWidget(self.glWidget)

		# Setup Dock Control
		self.items = QDockWidget("Control", self)
		win = QWidget()
		fbox = QFormLayout()	
		hbox1 = QHBoxLayout()
		hbox2 = QHBoxLayout()
		hbox3 = QHBoxLayout()
		hbox4 = QHBoxLayout()


		self.slider_1 = QSlider(Qt.Horizontal)
		self.slider_2 = QSlider(Qt.Horizontal)
		self.slider_3 = QSlider(Qt.Horizontal)
		self.slider_4 = QSlider(Qt.Horizontal)
		self.value1 = QLineEdit()
		self.value1.setFont(QFont("Arial",8))
		self.value2 = QLineEdit()
		self.value2.setFont(QFont("Arial",8))
		self.value3 = QLineEdit()
		self.value3.setFont(QFont("Arial",8))
		self.value4 = QLineEdit()
		self.value4.setFont(QFont("Arial",8))

		self.slider_1.setMinimum(0)
		self.slider_1.setMaximum(360)
		self.slider_1.setValue(180)
		self.slider_1.setTickPosition(QSlider.TicksBelow)
		self.slider_1.setTickInterval(5)
		self.slider_1.valueChanged.connect(self.valuechangeslider1)

		self.slider_2.setMinimum(0)
		self.slider_2.setMaximum(360)
		self.slider_2.setValue(180)
		self.slider_2.setTickPosition(QSlider.TicksBelow)
		self.slider_2.setTickInterval(5)
		self.slider_2.valueChanged.connect(self.valuechangeslider2)

		self.slider_3.setMinimum(0)
		self.slider_3.setMaximum(360)
		self.slider_3.setValue(180)
		self.slider_3.setTickPosition(QSlider.TicksBelow)
		self.slider_3.setTickInterval(5)
		self.slider_3.valueChanged.connect(self.valuechangeslider3)

		self.slider_4.setMinimum(0)
		self.slider_4.setMaximum(360)
		self.slider_4.setValue(180)
		self.slider_4.setTickPosition(QSlider.TicksBelow)
		self.slider_4.setTickInterval(5)
		self.slider_4.valueChanged.connect(self.valuechangeslider4)




		hbox1.addWidget(self.slider_1)
		hbox1.addWidget(self.value1)
		hbox1.addStretch()
		hbox2.addWidget(self.slider_2)
		hbox2.addWidget(self.value2)
		hbox2.addStretch()
		hbox3.addWidget(self.slider_3)
		hbox3.addWidget(self.value3)
		hbox3.addStretch()
		hbox4.addWidget(self.slider_4)
		hbox4.addWidget(self.value4)
		hbox4.addStretch()



		textslder_1 = QLabel("q1")
		textslder_2 = QLabel("q2")
		textslder_3 = QLabel("q3")
		textslder_4 = QLabel("q4")
		fbox.addRow(textslder_1,hbox1)
		fbox.addRow(textslder_2,hbox2)
		fbox.addRow(textslder_3,hbox3)
		fbox.addRow(textslder_4,hbox4)
		fbox.addRow(QPushButton("KHUONG"))
		fbox.addRow(QPushButton("DONG"))
		fbox.addRow(QPushButton("VU"))



		win.setLayout(fbox)
		self.items.setWidget(win)
		self.items.setFloating(False)
		self.addDockWidget(Qt.RightDockWidgetArea, self.items)

		# Setup properties of program
		self.setWindowTitle("Robot Design")



	def valuechangeslider1(self):
		valueslider1 = self.slider_1.value()
		self.value1.setText(str(valueslider1))
		self.glWidget.q1 = valueslider1
		self.glWidget.updateJoint()

	def valuechangeslider2(self):
		valueslider2 = self.slider_2.value()
		self.value2.setText(str(valueslider2))
		self.glWidget.q2 = valueslider2
		self.glWidget.updateJoint()
		pass
	def valuechangeslider3(self):
		valueslider3 = self.slider_3.value()
		self.value3.setText(str(valueslider3))
		self.glWidget.q3 = valueslider3
		self.glWidget.updateJoint()
		pass
	def valuechangeslider4(self):
		valueslider4 = self.slider_4.value()
		self.value4.setText(str(valueslider4))
		self.glWidget.q4 = valueslider4
		self.glWidget.updateJoint()
		pass
def main():
	app = QApplication(sys.argv)
	ex = RobotSimulator()
	ex.setGeometry(100,100,1000,800)
	ex.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
