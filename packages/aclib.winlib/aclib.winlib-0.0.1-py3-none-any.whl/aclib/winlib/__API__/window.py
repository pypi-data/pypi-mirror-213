from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self
    _Pos = _Size = tuple[int, int]
    _Area = tuple[int, int, int, int]

from typing import overload

from ._winapi import *
from .basewindow import BaseWindow

class Window(BaseWindow):


    @overload
    def __new__(cls, hwnd: int) -> Self: ...

    @overload
    def __new__(cls, title='', classname='', visible: bool=None) -> Self | None: ...

    def __new__(cls, target: int | str ='', classname='', visivle: bool=None) -> Self | None:
        if isinstance(target, int):
            return super()._new_(target)
        return super()._newwnd_(FilterWindow(IterDescendantWindows(0), target, classname, visivle))


    @classmethod
    def findwindows(cls, title='', classname='', visible: bool=None) -> list[Self]:
        return [cls._new_(h) for h in FilterWindows(IterDescendantWindows(0), title, classname, visible)]


    @classmethod
    def desktopwindow(cls) -> Self:
        """winapi中定义的DesktopWindow"""
        return cls._new_(GetDesktopWindow())

    @classmethod
    def desktop(cls) -> Self:
        """显示桌面图标的窗口"""
        return cls._new_(GetDesktopView())

    @classmethod
    def taskbar(cls) -> Self:
        return cls._new_(GetTaskbarWindow())


    @classmethod
    def pointwindow(cls, pos: tuple[int, int] = None) -> Self:
        return cls._new_(GetPointWindow(pos or GetCursorPos()))

    @classmethod
    def foregroundwindow(cls) -> Self:
        return cls._new_(GetForegroundWindow())


    def parent(self) -> Self:
        return self._new_(GetParentWindow(self.handle))

    def root(self) -> Self:
        return self._new_(GetRootWindow(self.handle))

    def rootowner(self) -> Self:
        return self._new_(GetRootOwnerWindow(self.handle))


    def prevbrother(self) -> Self | None:
        return self._newwnd_(GetPrevWindow(self.handle))

    def nextbrother(self) -> Self | None:
        return self._newwnd_(GetNextWindow(self.handle))

    def brother(self, title='', classname='', visible: bool=None) -> Self | None:
        return self._newwnd_(FilterWindow(IterBrotherWindows(self.handle), title, classname, visible))

    def brothers(self, title='', classname='', visible: bool=None) -> list[Self]:
        return [self._new_(h) for h in FilterWindows(IterBrotherWindows(self.handle), title, classname, visible)]


    def child(self, title='', classname='', visible: bool=None) -> Self | None:
        return self._newwnd_(FilterWindow(IterChildWindows(self.handle), title, classname, visible))

    def children(self, title='', classname='', visible: bool=None) -> list[Self]:
        return [self._new_(h) for h in FilterWindows(IterChildWindows(self.handle), title, classname, visible)]


    def descendant(self, title='', classname='', visible: bool=None) -> Self | None:
        return self._newwnd_(FilterWindow(IterDescendantWindows(self.handle), title, classname, visible))

    def descendants(self, title='', classname='', visible: bool=None) -> Self | None:
        return [self._new_(h) for h in FilterWindows(IterDescendantWindows(self.handle), title, classname, visible)]
