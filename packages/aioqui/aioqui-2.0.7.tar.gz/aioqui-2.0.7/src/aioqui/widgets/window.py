from PySide6.QtWidgets import QMainWindow

from ..context import ContextObj
from ..types import WindowHint, QSS


class Window(ContextObj, WindowHint, QMainWindow):
    def __init__(self, name: str, qss: QSS = None):
        QMainWindow.__init__(self)
        self.setObjectName(name)
        self.qss = qss

    async def init(
            self, *,
            _=...,
            **kwargs
    ) -> 'Window':
        return await self._apply(**kwargs)

    def setPanel(self, panel: 'QObject'):
        self.setWindowFlag(Window.Frameless)
        self.setMenuBar(panel)
