#create the Easy Editor photo editor here
from PyQt5.QtWidgets import (QApplication, QListWidget, QLabel,
                            QPushButton, QVBoxLayout, QHBoxLayout,
                            QWidget, QFileDialog)

import os

from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QPixmap
from PIL import Image
app = QApplication([])
win = QWidget()
win.resize(700, 400)
win.setWindowTitle('Easy Editor')

#button
btn_left = QPushButton('Left')
btn_right = QPushButton('Right')
btn_flip = QPushButton('Mirror')
btn_sharp = QPushButton('Sharpness')
btn_bw = QPushButton('B&W')
btn_dir = QPushButton('Folder')

lb_image = QLabel('Image')
lw_files = QListWidget()

col1 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)

col2 = QVBoxLayout()
col2.addWidget(lb_image)
row1 = QHBoxLayout()
row1.addWidget(btn_left)
row1.addWidget(btn_right)
row1.addWidget(btn_flip)
row1.addWidget(btn_sharp)
row1.addWidget(btn_bw)
col2.addLayout(row1)

row2 = QHBoxLayout()
row2.addLayout(col1, 20)
row2.addLayout(col2, 80)
win.setLayout(row2)

workdir = ' '
def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def Chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.png', '.jpeg', '.gif', '.bmp']
    Chooseworkdir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)
btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
  
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
  
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

workimage = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text() # variable filename: str
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_flip.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)

win.show()
app.exec_()