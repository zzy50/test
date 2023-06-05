import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel()
        self.btn1 = QPushButton('Open Image', self)
        self.btn1.clicked.connect(self.openImage)
        self.btn2 = QPushButton('Save', self)
        self.btn2.clicked.connect(self.save)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)

        self.setLayout(vbox)

        self.setWindowTitle('PyQt5 Image Viewer')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def openImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './')
        if fname[0]:
            pixmap = QPixmap(fname[0])
            self.resize(pixmap.width(), pixmap.height())

    def save(self):
        if hasattr(self, 'rect'):
            with open('output/coord.txt', 'w') as f:
                f.write(f'{self.rect.topLeft().x()}, {self.rect.topLeft().y()}\n')
                f.write(f'{self.rect.topRight().x()}, {self.rect.topRight().y()}\n')
                f.write(f'{self.rect.bottomRight().x()}, {self.rect.bottomRight().y()}\n')
                f.write(f'{self.rect.bottomLeft().x()}, {self.rect.bottomLeft().y()}\n')

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.start = e.pos()
            self.pressing = True

    def mouseMoveEvent(self, e):
        if hasattr(self, 'start') and hasattr(self, 'pressing') and self.pressing:
            self.end = e.pos()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            try:
                self.end = e.pos()
                self.pressing = False
                left = min(self.start.x(), self.end.x())
                right = max(self.start.x(), self.end.x())
                top = min(self.start.y(), self.end.y())
                bottom = max(self.start.y(), self.end.y())
                from PyQt5.QtCore import QRect
                self.rect = QRect(left, top, right-left, bottom-top)
            except AttributeError:
                pass

    def paintEvent(self, e):
        from PyQt5.QtGui import QPainter
        qp = QPainter()
        qp.begin(self)
        if hasattr(self.label, 'pixmap') and self.label.pixmap():
            qp.drawPixmap(0, 0, self.label.pixmap())
        if hasattr(self, 'start') and hasattr(self, 'end'):
            qp.drawRect(self.start.x(), self.start.y(), abs(self.end.x()-self.start.x()), abs(self.end.y()-self.start.y()))
        qp.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
