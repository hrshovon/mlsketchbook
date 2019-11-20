from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QFileDialog, QListWidgetItem, QGraphicsScene
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread,QTimer
from PyQt5.QtGui import QPixmap
from mlsketchbookui import Ui_frmmain
import os 
import sys
class mainui(QDialog):
	def __init__(self):
		super().__init__()
		self.src_fldr=None
		self.ui=Ui_frmmain()
		self.ui.setupUi(self)
		self.ui.bttnsetsrc_fldr.clicked.connect(self.open_src_fldr)
		self.ui.lstfilename.itemClicked.connect(self.src_item_clk)
	def src_item_clk(self,item):
		filename=QListWidgetItem(item)
		self.load_img(filename.text())
	def load_img(self,image_filename):
		path=os.path.join(self.src_fldr,image_filename)
		qimg=QPixmap(path)
		qgs=QGraphicsScene()
		
		img_set_h=self.ui.image_disp.height()
		print(img_set_h)
		img_h=qimg.height()
		img_w=qimg.width()
		aspect_ratio=img_w/img_h
		qimg=qimg.scaledToHeight(img_set_h)
		qimg=qimg.scaledToWidth(int(aspect_ratio*img_set_h))
		qgs.addPixmap(qimg)

		self.ui.image_disp.setScene(qgs)
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
