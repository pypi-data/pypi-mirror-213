from PySide6.QtWidgets import QWidget, QLayoutItem, QSpacerItem
from PySide6.QtCore import Qt, QObject
from typing import Sequence, Iterable

from ...types import Alignment


class LayoutExt(Alignment):
    async def init(
            self, *,
            items: Sequence[QObject] = (),
            **kwargs
    ) -> 'LayoutExt':
        # add items according to the rule item=`widget` or items=`widget, alignment` (not a tuple, but sequentially)
        i = 0
        while i < len(items):
            if i + 1 < len(items) and isinstance(items[i + 1], (Qt.AlignmentFlag, Qt.Alignment)):
                self.add(items[i], items[i + 1])
                i += 1
            else:
                self.add(items[i])
            i += 1
        # set defaults through kwargs if values are not specified
        if not kwargs.get('margins'):
            kwargs['margins'] = (0, 0, 0, 0)
        if not kwargs.get('spacing'):
            kwargs['spacing'] = 0
        return await self._render(**kwargs)  # from ContextObj

    def add(self, obj: QObject, alignment: Alignment.Alignment = None) -> QObject:
        if isinstance(obj, QWidget):
            if alignment:
                self.addWidget(obj, alignment=alignment)
            else:
                self.addWidget(obj)
        elif isinstance(obj, QSpacerItem):
            self.addSpacerItem(obj)
        elif isinstance(obj, QLayoutItem):
            self.addLayout(obj)
        else:
            raise TypeError(f'{obj} has unsupported type {type(obj)} to `add` to {self}')
        return obj

    def reorder(self, at: int, to: int):
        self.removeItem(item := self.itemAt(at))
        self.insertItem(to, item)

    def clear(self, exceptions: Iterable[QObject] = ()):
        for i in reversed(range(self.count())):
            item = self.itemAt(i).widget()
            if not item:
                item = self.itemAt(i).layout()
            if not item:
                item = self.itemAt(i).spacerItem()
            if item not in exceptions:
                item.setParent(None)
