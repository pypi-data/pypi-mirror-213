from PySide6.QtWidgets import QMenuBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent

from ..types import Parent, QSS
from ..context.context_obj import ContextObj


class Panel(ContextObj, QMenuBar):
    def __init__(self, parent: Parent, name: str, visible: bool = True, qss: QSS = None):
        QMenuBar.__init__(self, parent)
        ContextObj.__init__(self, parent, name, visible)
        self.qss = qss

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.core.setProperty('position', event.globalPos())

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() is Qt.LeftButton:
            delta = event.globalPos() - self.core.property('position')
            self.core.move(self.core.x() + delta.x(), self.core.y() + delta.y())
            self.core.setProperty('position', event.globalPos())

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.core.showToggle()
