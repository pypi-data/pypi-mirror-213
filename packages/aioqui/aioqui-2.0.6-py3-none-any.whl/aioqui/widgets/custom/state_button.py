from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon
from typing import Callable, Awaitable

from ..button import Button
from ...types import Icon
from ...asynq import asyncSlot


class StateButton(Button):
    def __init__(self, parent: QWidget, name: str = None, visible: bool = True, state: bool = False):
        super().__init__(parent, name if name else self.__class__.__name__, visible)
        self.__state: bool = state
        self.icon_true: Icon = Icon('star-fill.svg', (30, 30))
        self.icon_false: Icon = Icon('star.svg', (30, 30))

    async def init(
            self, *,
            icon_true: Icon = None, icon_false: Icon = None, pre_slot: Callable[..., bool],
            **kwargs
    ) -> 'StateButton':
        if icon_false:
            self.setIcon(QIcon(icon_false.icon))
            self.setIconSize(icon_false.size)
        if icon_true:
            self.icon_true = icon_true
            self.setIconSize(icon_true.size)
        if icon_false:
            self.icon_false = icon_false
        return await Button.init(self, on_click=lambda: self.__mainevent(pre_slot), **kwargs)

    @asyncSlot()
    async def __mainevent(self, pre_slot: Callable[..., Awaitable[bool]]) -> None:
        if await pre_slot():
            self.state = not self.state

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, state: bool) -> None:
        if state:
            self.setIcon(self.icon_true.icon)
            self.setIconSize(self.icon_true.size)
        else:
            self.setIcon(self.icon_false.icon)
            self.setIconSize(self.icon_false.size)
        self.__state = state
