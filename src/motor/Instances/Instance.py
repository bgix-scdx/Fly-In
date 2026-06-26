from pygame import Vector2
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any
from threading import Thread
from time import time, sleep
from math import cos, pi
from ..Color import Color
from ..screen_manager import screen
from typing import Callable


class InstanceType:
    pass


class EasingStyle(Enum):
    @staticmethod
    def Linear(t: float) -> float:
        return t

    @staticmethod
    def Quad(t: float) -> float:
        return t*t

    def Busted(t: float) -> float:
        return t**2

    @staticmethod
    def Sine(t: float) -> float:
        return 1 - cos(t * pi / 2)


class EasingDirection(Enum):
    @staticmethod
    def In(t: float, shape: Callable[[float], float]) -> float:
        return shape(t)

    @staticmethod
    def Out(t: float, shape: Callable[[float], float]) -> float:
        return 1 - (shape(t - 1))

    @staticmethod
    def InOut(t: float, shape: Callable[[float], float]) -> float:
        v: int = 0
        if t < 0.5:
            v = shape(2*t) / 2
        else:
            v = 1 - shape(2 - 2*t) / 2
        return v


class Instance(ABC):
    name: str = "Instance"
    position: Vector2 = Vector2(0, 0)
    color: Color = Color()
    __tween: Any = None
    Parent: Any

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, visual: screen) -> Any:
        pass

    def tween(self, targets: Dict[str, Any],
              duration: str, Type: EasingDirection = EasingStyle.Linear,
              Direction: EasingDirection = EasingDirection.In) -> None:
        while self.__tween:
            sleep(0.001)
        self.__tween = Thread(target=self.tweenThread)
        self.__tween.targets = targets.copy()
        self.__tween.duration = duration
        self.__tween.type = [Type, Direction]
        self.__tween.start()

    def tweenThread(self):
        started = time()
        base = {}
        targets = self.__tween.targets
        duration = self.__tween.duration
        type = self.__tween.type
        for i in targets.keys():
            base[i] = getattr(self, i)
        while time() - started < duration:
            t = (time() - started) / duration
            for i in targets.keys():
                goal = targets.get(i)
                start = base[i]
                final_v = start + (goal - start) * type[1](t, type[0])
                setattr(self, i, final_v)
                sleep(0)
        for i in targets.keys():
            v = targets.get(i)
            setattr(self, i, v)
        self.__tween = None
