#создай тут фоторедактор Easy Editor!
from PIL import Image
from PyQt5.QtCore import Qt
from PIL.ImageFilter import SHARPEN
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget,QLabel,QVBoxLayout,QHBoxLayout,QPushButton,QListWidget,QFileDialog)
app = QApplication([])
main_win = QWidget()
main_win.resize(700,500)
main_win.setWindowTitle('Easy Editor')
#elshad
btn_dir = QPushButton('Папка')
list_images = QListWidget()
label_image = QLabel('Картинка')

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч\Б')
 
col_1 = QVBoxLayout()
col_1.addWidget(btn_dir)
col_1.addWidget(list_images)

row_1 = QHBoxLayout()
row_1.addWidget(btn_left)
row_1.addWidget(btn_right)
row_1.addWidget(btn_mirror)
row_1.addWidget(btn_sharp)
row_1.addWidget(btn_bw)

col_2 = QVBoxLayout()
col_2.addWidget(label_image)
col_2.addLayout(row_1)

main_row = QHBoxLayout()
main_row.addLayout(col_1)
main_row.addLayout(col_2)

main_win.setLayout(main_row)

workdir = ''


def choseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    results = []
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results
    
def showFilenameList():
    choseWorkdir()
    extensions = ['.png','.jpg','jpeg','.svg','.bmp','gif']
    files = os.listdir(workdir)
    results = filter(files, extensions)
    list_images.clear()
    for result in results:
        list_images.addItem(result)

btn_dir.clicked.connect(showFilenameList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.dir = None
        self.folder = 'Modified/'

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.folder, self.filename)
        self.showImage(image_path)
    
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.folder, self.filename
        )
        
        self.showImage(image_path)
     
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.folder, self.filename
        )
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.folder, self.filename
        )
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.folder, self.filename
        )
        self.showImage(image_path)

    def saveImage(self):
        #C:\Users\bilol\Downloads\level (78) + Modified
        path = os.path.join(self.dir, self.folder)
        if not(os.path.exists(path)):
            os.mkdir(path)
        #C:\Users\bilol\Downloads\level (78) + Modified + image.png
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def showImage(self, path):
        label_image.hide()
        pixmapimage = QPixmap(path)
        w, h = label_image.width(), label_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        label_image.setPixmap(pixmapimage)
        label_image.show()

t1 = ImageProcessor()

def showChosenImage():
    if list_images.currentRow() >= 0:
        filename = list_images.currentItem().text()
        t1.loadImage(workdir, filename)
        image_path = os.path.join(t1.dir, t1.filename)
        t1.showImage(image_path)
list_images.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(t1.do_bw)
btn_mirror.clicked.connect(t1.do_flip)
btn_left.clicked.connect(t1.do_left)
btn_right.clicked.connect(t1.do_right)
btn_sharp.clicked.connect(t1.do_sharpen)


main_win.show()
app.exec_()
