
from types import SimpleNamespace

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QSizePolicy, QVBoxLayout, QWidget)

from opengl_widget import OpenGLWidget


class MainWindow(QWidget):

    setParams = Signal(object)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenGL21 PySide6 Python")
        self.setFixedSize(QSize(312, 400))

        coordLabel = QLabel("Введите координаты домика:")
        coordLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.xLineEdit = QLineEdit("75")
        self.yLineEdit = QLineEdit("100")

        xLabel = QLabel("x:")
        yLabel = QLabel("y:")
        hbox = QHBoxLayout()
        hbox.addWidget(xLabel)
        hbox.addWidget(self.xLineEdit)
        hbox.addWidget(yLabel)
        hbox.addWidget(self.yLineEdit)
        # hbox.addStretch(1)

        applyButton = QPushButton("Применить")
        applyButton.setFixedSize(QSize(100, 30))
        applyButton.clicked.connect(self.onApplyButtonClick)
        applyButtonLayout = QHBoxLayout()
        applyButtonLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        applyButtonLayout.addWidget(applyButton)

        openGLWidget = OpenGLWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(coordLabel)
        vbox.addLayout(hbox)
        vbox.addLayout(applyButtonLayout)
        vbox.addWidget(openGLWidget)
        self.setLayout(vbox)

        font = QFont("serif", 11)
        coordLabel.setFont(font)
        self.xLineEdit.setFont(font)
        self.yLineEdit.setFont(font)
        xLabel.setFont(font)
        yLabel.setFont(font)
        applyButton.setFont(font)

        self.setParams.connect(openGLWidget.setParamsSlot)
        obj = SimpleNamespace()
        obj.x = int(self.xLineEdit.text())
        obj.y = int(self.yLineEdit.text())
        self.setParams.emit(obj)

    def onApplyButtonClick(self):
        obj = SimpleNamespace()
        obj.x = int(self.xLineEdit.text())
        obj.y = int(self.yLineEdit.text())
        self.setParams.emit(obj)
