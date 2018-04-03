import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import OpenGLControl
class RobotSimulator(QMainWindow, QTabWidget):
   	def __init__(self, parent = None):
	  	super(RobotSimulator, self).__init__(parent)
		
		# create menu
		bar = self.menuBar()
		file = bar.addMenu("File")
		file.addAction("New")
		file.addAction("Save")
		file.addAction("Quit")

		# embeded OpenGL into Widget
		glWidget = OpenGLControl.GLWidget(self)
		self.setCentralWidget(glWidget)

		# Setup Dock Control
		self.items = QDockWidget("Control", self)
		win = QWidget()
		l1 = QLabel("Name")
		nm = QLineEdit()
		l2 = QLabel("Address")
   		add1 = QLineEdit()
		add2 = QLineEdit()
		fbox = QFormLayout()	
		fbox.addRow(l1,nm)
		vbox = QVBoxLayout()
		vbox.addWidget(add1)
		vbox.addWidget(add2)
		fbox.addRow(l2,vbox)
		hbox = QHBoxLayout()
		r1 = QRadioButton("Male")
		r2 = QRadioButton("Female")
		hbox.addWidget(r1)
		hbox.addWidget(r2)
		hbox.addStretch()
		fbox.addRow(QLabel("sex"),hbox)
		fbox.addRow(QPushButton("Submit"),QPushButton("Cancel"))
		win.setLayout(fbox)
		self.items.setWidget(win)
		self.items.setFloating(False)
		self.addDockWidget(Qt.RightDockWidgetArea, self.items)

		# Setup properties of program
		self.setWindowTitle("Robot Design")
		
def main():
	app = QApplication(sys.argv)
	ex = RobotSimulator()
	ex.setGeometry(100,100,1000,800)
	ex.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
	main()
