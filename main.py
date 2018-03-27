import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import OpenGLControl
class dockdemo(QMainWindow):
	def __init__(self, parent = None):
		super(dockdemo, self).__init__(parent)
		w = QWidget()
		layout = QHBoxLayout()
		bar = self.menuBar()
		file = bar.addMenu("File")
		file.addAction("New")
		file.addAction("save")
		file.addAction("quit")
		glWidget = OpenGLControl.GLWidget(self)
		self.setCentralWidget(glWidget)		
		self.items = QDockWidget("Dockable", self)
		self.listWidget = QListWidget()
		self.listWidget.addItem("item1")
		self.listWidget.addItem("item2")
		self.listWidget.addItem("item3")
		
		self.items.setWidget(self.listWidget)
		self.items.setFloating(False)
		self.setCentralWidget(glWidget)
		self.addDockWidget(Qt.RightDockWidgetArea, self.items)
		self.setLayout(layout)
		self.setWindowTitle("Robot Design")
		
def main():
	app = QApplication(sys.argv)
	ex = dockdemo()
	ex.setGeometry(100,100,1000,800)
	ex.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()