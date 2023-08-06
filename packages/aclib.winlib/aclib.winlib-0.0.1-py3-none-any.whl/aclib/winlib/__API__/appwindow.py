from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Callable, Any
    Pos, Size = tuple[int, int]

import ctypes
from time import sleep
from functools import wraps

from .basewindow import BaseWindow
from ._winapi import *
from . import _wincon, _wintype


class AppWindow(BaseWindow):

    class Creator(dict):
        def __init__(self,
            clsname='aclib.winapp', title='', relpos: Pos=0, size: Size=0, visible=True, transparency=1.0
        ): super().__init__(locals())

    class Render(dict):
        def __init__(self,
            cursor: int | str = _wincon.IDC_ARROW,
            text='', textcplor=0x0, textalign=(3,3), font='', fontsize=18, fillcolor=0xffffff
        ): super().__init__(locals())

    __wndcount = 0
    __wndthread = 0
    __wndevents: dict[int, dict[int, list[Callable]]] = {}  # {hwnd: {msg: callback}}

    @classmethod
    def __wndproc(cls, hwnd, message, wparam, lparam):
        if message == _wincon.WM_CREATE:
            lplistener = ctypes.cast(lparam, ctypes.POINTER(_wintype.CREATESTRUCTW)).contents.lpCreateParams
            cls.__wndevents[hwnd] = ctypes.cast(lplistener, ctypes.py_object).value
        if hwnd in cls.__wndevents and message in cls.__wndevents[hwnd]:
            for callback in cls.__wndevents[hwnd][message]:
                callback(hwnd, message, wparam, lparam)
        if message == _wincon.WM_NCDESTROY:
            cls.__wndevents.pop(hwnd, None)

    @classmethod
    def __checkthread(cls):
        if not cls.__wndthread:
            cls.__wndthread = CreateMsgloopThread()

    @classmethod
    def __checkwindow(cls):
        if not cls.__wndcount and cls.__wndthread:
            cls.__wndthread = DestroyMsgloopThread(cls.__wndthread)

    @classmethod
    def loop(cls):
        while True: sleep(1)

    @classmethod
    def __new(cls, *args, **kwargs):
        window = cls._new_(0)
        window.__init(*args, **kwargs)
        return window

    def newoverlapped(parent: Self | int = 0, creator: Creator = None, render: Render = None):
        return AppWindow.__new(_wincon.WS_OVERLAPPEDWINDOW, parent, creator, render)

    def newpopup(parent: Self | int, creator: Creator = None, render: Render = None):
        return AppWindow.__new(_wincon.WS_POPUPWINDOW, parent, creator, render)

    def newchild(parent: Self | int, creator: Creator = None, render: Render = None):
        return AppWindow.__new(_wincon.WS_CHILDWINDOW, parent, creator, render)

    def __init(self, wndtype: int, parent: Self | int, creator: Creator, render: Render):
        render = render or self.Render()
        creator = creator or self.Creator()
        creator.update({'wndtype': wndtype, 'parent': parent})
        self.__creator = creator
        self.__listener = {}
        self.__trackingmouse = False
        self.cursor = render['cursor']
        self.text = render['text']
        self.textcolor = render['textcplor']
        self.textalign = render['textalign']
        self.font = render['font']
        self.fontsize = render['fontsize']
        self.fillcolor = render['fillcolor']
        for method in filter(lambda k: k.startswith('_AppWindow__on_'), AppWindow.__dict__.keys()):
            self.addmsglistener(getattr(_wincon, f'WM_{method[15:].upper()}'), getattr(self, method))

    def __repr__(self):
        wndid = self.handle or hex(id(self))
        wndsummary = self.title or self.classname if self.handle else 'UNCREATED'
        return f'AppWindow-{wndid} {wndsummary}'

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if self.handle == 0:
            return
        if key in ['fillcolor','text','textcolor','textalign','font','fontsize']:
            RedrawWindow(self.handle)
        if key == 'cursor':
            PostMessage(self.handle, _wincon.WM_SETCURSOR, self.handle, MakeLong(_wincon.HTCLIENT, _wincon.WM_MOUSEMOVE))

    def addmsglistener(self, msg: int | str, callback: Callable[[int, int], Any]):
        if isinstance(msg, str):
            msg = getattr(_wincon, f'WM_{msg.upper()}')
        if msg not in self.__listener:
            self.__listener[msg] = []
        self.__listener[msg].append(callback)

    def create(self) -> Self:
        assert self.handle == 0
        args = self.__creator
        parent = args['parent']
        hparent = parent if isinstance(parent, int) else parent.handle
        dwstyle = args['wndtype'] | _wincon.WS_VISIBLE * args['visible']
        dwexstyle = _wincon.WS_EX_LAYERED
        if not GetWindowClassInfo(args['clsname']).lpszClassName:
            RegisterWindowClass(args['clsname'], self.__wndproc)
        self.__checkthread()
        CreateWindowAsync(
            self.__wndthread, hparent, args['clsname'], args['title'],
            args['relpos'], args['size'], dwstyle, dwexstyle, id(self.__listener)
        )   # 如果成功创建窗口，那么在函数返回前，会先执行 __on_create 中的任务
        self.__checkwindow()
        return self

    def __on_create(self, h, m, w, l):
        self._sethandle_(h)
        self.__class__.__wndcount += 1
        self.settransparency(self.__creator['transparency'])
        del self.__creator

    def __on_ncdestroy(self, h, m, w, l):
        self.__class__.__wndcount -= 1
        self.__checkwindow()

    def __on_setcursor(self, h, m, w, l):
        if w == h and ParseLong(l)[0] == _wincon.HTCLIENT:
            SetCursor(self.cursor)

    def __on_paint(self, *args):
        Paint(self.handle, self.text, self.textcolor, self.textalign, self.font, self.fontsize, self.fillcolor)

    def __on_mousemove(self, *args):
        if not self.__trackingmouse:
            TrackMouseEvent(self.handle)
            self.__trackingmouse = True

    def __on_mouseleave(self, *args):
        self.__trackingmouse = False

    @staticmethod
    def __apptask(task):
        @wraps(task)
        def wrappedtask(self, *args, **kwargs):
            if self.handle == 0:
                return None
            if GetCurrentThreadId() == self.__wndthread:
                return task(self, *args, **kwargs)
            return RequestMsgloopTask(task, self.__wndthread, self, *args, **kwargs)
        return wrappedtask

    @__apptask
    def capturemouse(self):
        SetCapture(self.handle)

    @__apptask
    def releasecapture(self):
        ReleaseCapture()
