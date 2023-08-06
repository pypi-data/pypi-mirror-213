from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Callable, Literal

import time, ctypes, inspect, threading
from aclib.winlib import winapi

EXCTYPE = SystemExit if inspect.isclass(SystemExit) else type(SystemExit)

def async_raise(ident, exctype=EXCTYPE) -> int:
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(ident), ctypes.py_object(exctype))
    if res > 1: ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(ident), None)
    return res		# 0: invalied ident; 1: raise single sent; above 1: error

class Thread(object):

    @classmethod
    def main_thread(cls) -> Self:
        return cls.__new(threading.main_thread())

    @classmethod
    def current_thread(cls) -> Self:
        return cls.__new(threading.current_thread())

    @classmethod
    def active_threads(cls) -> list[Self]:
        return [cls.__new(tobj) for tobj in threading.enumerate()]

    @classmethod
    def __new(cls, tobj: threading.Thread) -> Self:
        self = super().__new__(cls)
        self.__init(tobj)
        return self

    def __init(self, tobj: threading.Thread):
        self.__tobj = tobj
        self.__updatetime()

    def __new__(cls, target: Callable, args: tuple=None, kwargs: dict=None) -> Self:
        return cls.__new(threading.Thread(target=target, args=args or (), kwargs=kwargs or {}, daemon=True))

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}-{self.ident} {self.state}>'

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.__tobj == other.__tobj

    def __updatetime(self):
        hthread = winapi.OpenThreadHandle(self.ident)
        self.__time = winapi.GetThreadTimes(hthread)[0]
        winapi.CloseHandle(hthread)

    @property
    def ident(self) -> int:
        return self.__tobj.ident or 0

    @property
    def time(self) -> float:
        return self.__time

    @property
    def isrunning(self) -> bool:
        if self.ident:
            hthread = winapi.OpenThreadHandle(self.ident)
            if hthread:
                thtime, exittime = winapi.GetThreadTimes(hthread)[:2]
                running = thtime == self.__time and not exittime
            else: running = False
            winapi.CloseHandle(hthread)
        else: running = False
        return running

    @property
    def state(self) -> Literal['UNSTARTED', 'RUNNING', 'EXITED']:
        if self.ident == 0:
            return 'UNSTARTED'
        if self.isrunning:
            return 'RUNNING'
        return 'EXITED'

    def start(self) -> Self:
        self.__tobj.start()
        self.__updatetime()
        return self

    def pause(self):
        if self.isrunning:
            hthread = winapi.OpenThreadHandle(self.ident)
            winapi.SuspendThread(hthread)
            winapi.CloseHandle(hthread)

    def resume(self):
        if self.isrunning:
            hthread = winapi.OpenThreadHandle(self.ident)
            winapi.RusumeThread(hthread)
            winapi.CloseHandle(hthread)

    def kill(self):
        # 强制杀死线程，线程资源无法释放，可能会造成内存泄漏，谨慎使用
        if self.isrunning:
            hthread = winapi.OpenThreadHandle(self.ident)
            winapi.TerminateThread(hthread)
            winapi.CloseHandle(hthread)

    def stop(self) -> int:
        """0: not running; 1: raise single sent; above 1: error"""
        # 向目标线程发送退出信号
        # 目标线程会在一些阻塞的任务（例如time.sleep）完成时抛出 SystemExit 以结束线程
        return int(self.isrunning) and async_raise(self.ident)

    def join(self):
        if not self.ident:
            raise RuntimeError("cannot join thread before it is started")
        while self.isrunning: time.sleep(.001)
