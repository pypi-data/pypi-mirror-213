from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self, Callable, Literal

from time import sleep
from datetime import datetime
from aclib.winlib import winapi, wincon
from aclib.threads import Thread


def makevkcode(key: int | str) -> int:
    vkcode = winapi.MakeKeyCode(key)
    if not vkcode: raise ValueError(
        f'Invalid key: "{key}"')
    return vkcode


class Event(object):

    KEYDOWN, KEYUP = 'down', 'up'

    def __init__(self, key: int | str, action: Literal['down', 'up'], time: datetime, kstates: dict[int, bool]):
        self.key = key
        self.kcode = makevkcode(key)
        self.kname = wincon.VK_MAP.get(self.kcode)
        self.action = action
        self.time = time
        self.__kstates = kstates

    def __repr__(self) -> str:
        info = ', '.join(f'{k}={v}' for k, v in self.__dict__.items() if k[0] != '_')
        return f'<{self.__class__.__name__} {info}>'

    def stateof(self, key: int | str) -> Literal['down', 'up'] | None:
        kcode = makevkcode(key)
        if kcode in self.__kstates:
            return ('up', 'down')[self.__kstates[kcode]]

    def iskeydown(self, key: int | str) -> bool:
        return bool(self.__kstates.get(makevkcode(key)))


class Listener(object):

    def __init__(self, *keys: int | str, callback: Callable, args: tuple=None, kwargs: dict=None):
        self.__listening = False
        self.__stopsignal = True
        self.__keymap = {makevkcode(k): k for k in keys or wincon.VK_MAP}
        self.__calllbackdata = (callback, args or (), kwargs or {})
        self.__runningcallback: list[Thread] = []

    def __callback(self, event: Event):
        try:
            self.__runningcallback.append(Thread.current_thread())
            callback, args, kwargs = self.__calllbackdata
            callback(event, *args, **kwargs)
        except SystemExit:
            pass
        if Thread.current_thread() in self.__runningcallback:
            self.__runningcallback.remove(Thread.current_thread())

    def __get_kstates(self) -> dict[int, bool]:
        return {vkcode: winapi.GetAsyncKeyState(vkcode) for vkcode in self.__keymap}

    def __listener_thread(self):
        last_kstates = self.__get_kstates()
        while not self.__stopsignal:
            current_kstates = self.__get_kstates()
            for vkcode in filter(lambda code: current_kstates[code] != last_kstates[code], current_kstates):
                action = ('up', 'down')[current_kstates[vkcode]]
                event = Event(self.__keymap[vkcode], action, datetime.now(), current_kstates.copy())
                Thread(self.__callback, (event,)).start()
            last_kstates = current_kstates
            sleep(.001)
        self.__listening = False

    @property
    def listening(self) -> bool:
        return self.__listening

    def listen(self) -> Self:
        if self.__listening: raise TypeError(
            'listener is running, cannot listen again before stop.')
        self.__listening = True
        self.__stopsignal = False
        Thread(self.__listener_thread).start()
        return self

    def stop(self, stopcallback=True):
        self.__stopsignal = True
        for thread in stopcallback * self.__runningcallback:
            thread.stop()

    @staticmethod
    def loop():
        while True: sleep(1)
