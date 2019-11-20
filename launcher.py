from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QFileDialog, QListWidgetItem, QGraphicsScene
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTimer, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QPainterPath
import PyQt5.QtCore as QtCore
from mlsketchbookui import Ui_frmmain
import os 
import sys

class Drawer(QWidget):
	newPoint = pyqtSignal(QPoint)
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.path = QPainterPath()    
		self.h=parent.height()
		self.w=parent.width()
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.drawPath(self.path)

	def mousePressEvent(self, event):
		self.path.moveTo(event.pos())
		self.update()

	def mouseMoveEvent(self, event):
		self.path.lineTo(event.pos())
		self.newPoint.emit(event.pos())
		self.update()

	def sizeHint(self):
		return QtCore.QSize(self.w, self.h)


class mainui(QDialog):
	def __init__(self):
		super().__init__()
		self.drawing = False
		self.lastPoint = QPoint()
		self.src_fldr=None
		self.ui=Ui_frmmain()
		self.ui.setupUi(self)
		self.ui.bttnsetsrc_fldr.clicked.connect(self.open_src_fldr)
		self.ui.bttnnext.clicked.connect(self.save_img)
		self.ui.lstfilename.itemClicked.connect(self.src_item_clk)
		self.qgs=QGraphicsScene()
		self.drawer=Drawer(self.ui.image_disp)
		self.qimg=QPixmap(self.ui.image_disp.width(),self.ui.image_disp.height())

		#self.painter = QPainter(self.ui.image_disp)
	
	def save_img(self):
		pixmap=self.ui.image_disp.grab()
		pixmap.save("test.jpg")

	def src_item_clk(self,item):
		filename=QListWidgetItem(item)
		self.load_img(filename.text())

	def load_img(self,image_filename):
		path=os.path.join(self.src_fldr,image_filename)
		self.qimg=QPixmap(path)
		img_set_w=self.ui.image_disp.width()
		#print(img_set_h)
		img_h=self.qimg.height()
		img_w=self.qimg.width()
		print(img_h)
		print(img_w)
		aspect_ratio=img_w/img_h
		img_set_h=int(1/aspect_ratio)*img_set_w
		self.qimg=self.qimg.scaledToWidth(img_set_w)
		#self.qimg=self.qimg.scaledToHeight(img_set_h)
		self.qgs=QGraphicsScene()
		#qimg=qimg.scaledToWidth()
		self.qgs.addPixmap(self.qimg)
				
		self.ui.image_disp.setScene(self.qgs)
		#self.draw_something()
	def open_src_fldr(self):
		fldr = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		list_files=os.listdir(fldr)
		self.ui.lstfilename.clear()
		self.src_fldr=fldr
		self.ui.lstfilename.addItems(list_files)
		
if __name__=="__main__":
    app = QApplication(sys.argv)
    ui_out = mainui()
    ui_out.show()
    sys.exit(app.exec_())
