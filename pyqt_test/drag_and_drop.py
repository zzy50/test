import sys
from PyQt5 import QtWidgets, QtCore

class DraggableLabel(QtWidgets.QLabel):
    def __init__(self, text, target_layout, source_layout):
        super().__init__(text)
        self.target_layout = target_layout
        self.source_layout = source_layout

    def mousePressEvent(self, event):
        self.offset = event.pos()
        self.original_position = self.pos()
        self.setCursor(QtCore.Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def mouseReleaseEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        target_geometry = self.target_layout.parent().geometry()
        source_geometry = self.source_layout.parent().geometry()

        if self.geometry().intersects(target_geometry):
            new_label = DraggableLabel(self.text(), self.source_layout, self.target_layout)
            new_label.setFrameStyle(QtWidgets.QLabel.Panel | QtWidgets.QLabel.Raised)
            self.target_layout.addWidget(new_label)
            self.deleteLater()
        elif self.geometry().intersects(source_geometry):
            new_label = DraggableLabel(self.text(), self.target_layout, self.source_layout)
            new_label.setFrameStyle(QtWidgets.QLabel.Panel | QtWidgets.QLabel.Raised)
            self.source_layout.addWidget(new_label)
            self.deleteLater()
        else:
            self.move(self.original_position)

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QHBoxLayout()

        self.source_container = QtWidgets.QWidget()
        source_layout = QtWidgets.QVBoxLayout()
        self.source_container.setLayout(source_layout)

        self.target_container = DropContainer()
        target_layout = self.target_container.layout

        label = DraggableLabel("Drag me!", target_layout, source_layout)
        label.setFrameStyle(QtWidgets.QLabel.Panel | QtWidgets.QLabel.Raised)
        source_layout.addWidget(label)

        layout.addWidget(self.source_container)
        layout.addWidget(self.target_container)

        self.setLayout(layout)
        self.setWindowTitle('Drag and Drop Example')
        self.show()

class DropContainer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
