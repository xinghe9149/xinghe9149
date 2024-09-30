from abc import ABC, abstractmethod

from PySide6.QtCore import QTimerEvent, Qt
from PySide6.QtGui import QCursor
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from app import live2d
from config import Configuration


class Scene(QOpenGLWidget):
    class CallBackSet(ABC):

        @abstractmethod
        def onUpdate(self, ww: int, wh: int):
            pass

        @abstractmethod
        def onResize(self, ww: int, wh: int):
            pass

        @abstractmethod
        def onLeftClick(self, rx: int, ry: int):
            pass

        @abstractmethod
        def onRightClick(self, rx: int, ry: int):
            pass

        @abstractmethod
        def onMouseMoved(self, mx: int, my: int):
            pass

        @abstractmethod
        def onInitialize(self):
            pass

        @abstractmethod
        def onIntervalReached(self):
            pass

        @abstractmethod
        def IsFinished(self):
            pass

    config: Configuration
    callBackSet: CallBackSet
    timer: int
    jiffies: int

    def __init__(self) -> None:
        super().__init__()
        self.lastX = -1
        self.lastY = -1
        self.timer = -1
        self.isMoving = False
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint
        )
        self.setWindowTitle("com.arkueid.host")

    def setup(self, config: Configuration, callbackSet: CallBackSet):
        self.config = config
        self.resize(config.width.value, config.height.value)
        self.callBackSet = callbackSet
        self.move(self.config.lastX.value, self.config.lastY.value)

        self.config.width.valueChanged.connect(self.setWidth)
        self.config.height.valueChanged.connect(self.setHeight)
        self.config.fps.valueChanged.connect(self.setFPS)

    def start(self):
        self.show()

        self.setFPS(self.config.fps.value)

    def show(self):
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self.config.stay_on_top.value)
        self.setVisible(self.config.visible.value)

    def initializeGL(self) -> None:
        self.makeCurrent()
        if live2d.LIVE2D_VERSION == 3:
            live2d.glewInit()
            live2d.setGLProperties()

        self.callBackSet.onInitialize()

    def resizeGL(self, w: int, h: int) -> None:
        self.callBackSet.onResize(w, h)

    def paintGL(self) -> None:
        self.callBackSet.onUpdate(self.width(), self.height())

    def timerEvent(self, event: QTimerEvent) -> None:

        if not self.isVisible():
            return

        if self.config.track_enable:
            pos = QCursor.pos()

            self.callBackSet.onMouseMoved(pos.x() - self.x(), pos.y() - self.y())

        if self.callBackSet.IsFinished():  # 当前动作已结束，等待 motion_interval 秒
            self.jiffies -= 1  # 递减等待时间

            if self.jiffies <= 0:  # 等待时间耗尽，启动新动作
                self.jiffies = self.config.fps.value * self.config.motion_interval.value
                self.callBackSet.onIntervalReached()

        self.update()

    def mousePressEvent(self, event):
        self.lastX = event.x()
        self.lastY = event.y()
        self.isMoving = False

    def mouseReleaseEvent(self, event):
        if self.isMoving:
            pass
        elif self.config.enable and event.button() == Qt.MouseButton.LeftButton:
            self.callBackSet.onLeftClick(event.x(), event.y())
        elif self.config.enable and event.button() == Qt.MouseButton.RightButton:
            self.callBackSet.onRightClick(event.x(), event.y())
        self.isMoving = False

    def mouseMoveEvent(self, event):
        if self.config.enable and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalX() - self.lastX, event.globalY() - self.lastY)
            self.config.lastX.value = self.x()
            self.config.lastY.value = self.y()
            self.isMoving = True

    def setWidth(self, width: int):
        self.resize(width, self.height())

    def setHeight(self, height: int):
        self.resize(self.width(), height)

    def setFPS(self, fps: int):
        self.jiffies = self.config.motion_interval.value * fps
        if self.timer != -1:
            self.killTimer(self.timer)
        self.timer = self.startTimer(1000 // fps)
