from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QFileDialog, QListWidgetItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTimer, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QPainterPath, QImage
import PyQt5.QtCore as QtCore
from mlsketchbookui import Ui_frmmain
import os 
import sys
import cv2
import numpy as np

class Drawer(QWidget):
	newPoint = pyqtSignal(QPoint)
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.path = QPainterPath()    
		self.h=parent.height()
		self.w=parent.width()
		self.qImg = QPixmap(self.w, self.h).toImage() #.rgbSwapped()
		self.p=parent
		self.clrev=False
	def paintEvent(self, event):
		painter = QPainter(self)
		painter_rep=QPainter(self.qImg)
		#painter.eraseRect(self.p.sceneRect())	
			
		painter.drawPath(self.path)
		painter_rep.setPen(Qt.white)
		painter_rep.drawPath(self.path)
	def mousePressEvent(self, event):
		self.path.moveTo(event.pos())
		self.update()
	def clear(self):
		self.path = QPainterPath()  
		self.update()
		self.qImg = QPixmap(self.w, self.h).toImage()
		self.qImg.fill(Qt.black)
		#self.qImg = QPixmap(self.w, self.h).toImage()  
			
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
		self.dest_fldr=None
		self.ui=Ui_frmmain()
		self.ui.setupUi(self)
		self.ui.bttnsetsrc_fldr.clicked.connect(self.open_src_fldr)
		self.ui.bttnsetdest_folder.clicked.connect(self.open_dest_fldr)
		self.ui.bttnnext.clicked.connect(self.next)
		self.ui.bttnclr.clicked.connect(self.clearall)
		self.ui.lstfilename.itemClicked.connect(self.src_item_clk)
		self.qgs=QGraphicsScene()
		self.drawer=Drawer(self.ui.image_disp)
		self.qimg=QPixmap(self.ui.image_disp.width(),self.ui.image_disp.height())
		self.aspect_ratio=16/9
		self.qimg.fill(Qt.black)
		self.curitem=None
		self.cur_height=0
		self.cur_width=0
		
		#self.painter = QPainter(self.ui.image_disp)
	def clearall(self):
		self.drawer.clear()
	
	
	def prev(self):
		self.save_img()
		
		sIndex=self.ui.lstfilename.currentRow()
		if self.ui.lstfilename.currentRow()>0:
			self.ui.lstfilename.setCurrentRow(sIndex-1)
			self.src_item_clk(self.ui.lstfilename.currentItem())
	def next(self):
		self.save_img()
		#print(self.ui.image_disp.items())
		#self.qgs.clear()
		#self.ui.image_disp.items().clear()
		#self.ui.image_disp.viewport().update()
		self.drawer.clear()
		#self.drawer=Drawer(self.ui.image_disp)
		#self.drawer.qImg = QPixmap(self.ui.image_disp.width(), self.ui.image_disp.height()).toImage()
		sIndex=self.ui.lstfilename.currentRow()
		if self.ui.lstfilename.currentRow()<self.ui.lstfilename.count()-1:
			self.ui.lstfilename.setCurrentRow(sIndex+1)
			self.src_item_clk(self.ui.lstfilename.currentItem())
	def get_cropped_img(self,image):
		channels_count = 4
		#image = pixmap.toImage()
		b = image.bits()
		# sip.voidptr must know size to support python buffer interface
		b.setsize(image.height() * image.width() * channels_count)
		arr = np.frombuffer(b, np.uint8).reshape((image.height(), image.width(), channels_count))
		height=image.width()//self.aspect_ratio
		y1=int((image.height()//2)-(height//2))
		y2=int((image.height()//2)+(height//2))
		image=arr[y1:y2,:]
		return image

	def draw_cnt(self,img):
		#img_b=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		_,img_b=cv2.threshold(img,250,255,cv2.THRESH_BINARY)
		#cv2.imshow("tehe",img_b)
		#img_b = np.float32(img_b)
		im_floodfill = img_b.copy()
	
		# Mask used to flood filling.
		# Notice the size needs to be 2 pixels than the image.
		h, w = img_b.shape[:2]
		mask = np.zeros((h+2, w+2), np.uint8)
		
		# Floodfill from point (0, 0)
		cv2.floodFill(im_floodfill, mask, (0,0), 255)
		img_b=cv2.bitwise_not(im_floodfill)
		#img_b=cv2.bitwise_and(img,img,mask=img_b)
		return img_b
	
	def save_img(self):
		#filename=self.ui.lstfilename.SelectItems()[0]
		#print(filename)
		file_path=os.path.join(self.dest_fldr,self.curitem)
		#pixmap=self.ui.image_disp.grab()
		pixmap2=self.drawer.qImg
		img=self.get_cropped_img(pixmap2)
		img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
		img=self.draw_cnt(img)
		
		img=cv2.resize(img,(self.cur_width,self.cur_height))
		cv2.imwrite(file_path,img)
	
	def src_item_clk(self,item):
		filename=QListWidgetItem(item)
		self.load_img(filename.text())
		self.curitem=filename.text()
	def load_img(self,image_filename):
		path=os.path.join(self.src_fldr,image_filename)
		self.qimg=QPixmap(path)
		img_set_w=self.ui.image_disp.width()
		#print(img_set_h)
		img_h=self.qimg.height()
		img_w=self.qimg.width()
		self.cur_height=img_h
		self.cur_width=img_w
		
		self.aspect_ratio=img_w/img_h
		#self.qimg=self.qimg.scaled(img_set_h, img_set_h, Qt.KeepAspectRatio)
		self.qimg=self.qimg.scaledToWidth(img_set_w)
		print(self.qimg.height(),self.qimg.width())
		#print(img_w)
		
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

	def open_dest_fldr(self):
		fldr = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
		self.dest_fldr=fldr
		
if __name__=="__main__":
    app = QApplication(sys.argv)
    ui_out = mainui()
    ui_out.show()
    sys.exit(app.exec_())
