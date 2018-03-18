
import sys
from PyQt4 import QtGui, QtCore


class GUI(QtGui.QWidget):
	def __init__(self):
		super(GUI, self).__init__()
		self.initUI()
	
	def initUI(self):
		
		b_start = QtGui.QPushButton("Start")
		b_pause = QtGui.QPushButton("Pause")
		b_analyse = QtGui.QPushButton("Analyse")
	
		
		grid = QtGui.QGridLayout()
		grid.setSpacing(10)
		
		grid.addWidget(b_start,0,0)
		grid.addWidget(b_pause,1,0)
		grid.addWidget(b_analyse,2,0)
		
		pixmap = QtGui.QPixmap("img_def_1.jpg")
		lbl = QtGui.QLabel(self)
		lbl.setPixmap(pixmap)
		grid.addWidget(lbl,0,2,10,40)
		
		titleImg = QtGui.QLabel('Live feed from camera')
		grid.addWidget(titleImg,0,1)
		self.setLayout(grid)
		self.setGeometry(50, 50, 900, 600)
		self.setWindowTitle('GUI-project1')    
		self.show()
		
		
		
app = QtGui.QApplication(sys.argv)
gui = GUI()
sys.exit(app.exec_())