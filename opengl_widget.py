import numpy as np
from OpenGL.GL import *
from PySide6.QtGui import QMatrix4x4, QSurfaceFormat, QVector3D
from PySide6.QtOpenGL import QOpenGLBuffer, QOpenGLShader, QOpenGLShaderProgram
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from renderable import Renderable


class OpenGLWidget(QOpenGLWidget):

    def __init__(self):
        super().__init__()
        self.housePosX = 0
        self.housePosY = 0
        # Set format
        format = QSurfaceFormat()
        format.setSamples(8)
        self.setFormat(format)

    def initializeGL(self):
        glClearColor(0.77, 0.93, 0.95, 1)
 
        self.program = QOpenGLShaderProgram()
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Vertex,
            "assets/shaders/default.vert")
        self.program.addShaderFromSourceFile(QOpenGLShader.ShaderTypeBit.Fragment,
            "assets/shaders/default.frag")
        self.program.bindAttributeLocation("aPosition", 0)
        self.program.link()
        self.program.bind()

        vertPositions = np.array([
            0, 0, # Quad
            1, 0,
            0, 1,
            1, 1,
            0, 0, # Triangle
            1.2, -1,
            2.4, 0], dtype=np.float32)
        self.vertPosBuffer = QOpenGLBuffer()
        self.vertPosBuffer.create()
        self.vertPosBuffer.bind()
        self.vertPosBuffer.allocate(vertPositions, len(vertPositions) * 4)
        self.program.setAttributeBuffer(0, GL_FLOAT, 0, 2)
        self.program.enableAttributeArray(0)

        self.modelMatrix = QMatrix4x4()
        self.mvpMatrix = QMatrix4x4()

        projMatrix = QMatrix4x4()
        projMatrix.ortho(0, 200, 200, 0, 1, -1)

        viewMatrix = QMatrix4x4()
        viewMatrix.lookAt(
            QVector3D(0, 0, 1),
            QVector3D(0, 0, 0),
            QVector3D(0, 1, 0))

        self.projViewMatrix = QMatrix4x4()
        self.projViewMatrix = projMatrix * viewMatrix

        self.uMvpMatrixLocation = self.program.uniformLocation("uMvpMatrix")
        self.uColorLocation = self.program.uniformLocation("uColor")

        houseBody = Renderable(0, 0, 100, 100, QVector3D(0, 0.7, 0), 0, 4)
        roof = Renderable(-10, 0, 50, 50, QVector3D(0.35, 0.25, 0.2), 4, 4)
        window = Renderable(20, 20, 30, 50, QVector3D(0, 0, 0), 0, 4)
        windowLine0 = Renderable(20, 38, 30, 4, QVector3D(1, 1, 1), 0, 4)
        windowLine1 = Renderable(33, 40, 4, 30, QVector3D(1, 1, 1), 0, 4)

        self.objects = []
        self.objects.append(houseBody)
        self.objects.append(roof)
        self.objects.append(window)
        self.objects.append(windowLine0)
        self.objects.append(windowLine1)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)

        for obj in self.objects:
            self.modelMatrix.setToIdentity()
            self.modelMatrix.translate(self.housePosX + obj.x,
                self.housePosY + obj.y)
            self.modelMatrix.rotate(obj.angle, QVector3D(0, 0, 1))
            self.mvpMatrix = self.projViewMatrix * self.modelMatrix
            self.mvpMatrix.scale(obj.w, obj.h)
            self.program.bind()
            self.program.setUniformValue(self.uMvpMatrixLocation, self.mvpMatrix)
            self.program.setUniformValue(self.uColorLocation, obj.color)
            glDrawArrays(GL_TRIANGLE_STRIP, obj.startIndex, obj.amountOfVertices)

    def setParamsSlot(self, params):
        self.housePosX = params.x
        self.housePosY = params.y
        self.update()
