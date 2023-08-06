from PySide6.QtWidgets import QMenuBar

from ..types import Parent, QSS
from ..context.context_obj import ContextObj


class Panel(ContextObj, QMenuBar):
    def __init__(self, parent: Parent, name: str, visible: bool = True, qss: QSS = None):
        QMenuBar.__init__(self, parent)
        ContextObj.__init__(self, parent, name, visible)
        self.qss = qss
