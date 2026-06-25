from pygame import Vector2
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, Dict, Any, List
from threading import Thread
from time import time


class InstanceType(Enum):
    pass


class Instance(ABC):
    name: str = "Instance"
    position: Vector2 = Vector2(0, 0)
    color: Tuple[int, int, int]
    __tween: Any
    @abstractmethod
    def execute(self) -> None:
        pass

    def tween(self, targets: Dict[str, Any], duration: str) -> None:
        self.__tween = Thread(target=self.tweenThread)
        self.__tween.targets = targets
        self.__tween.duration = duration
        self.__tween.start()

    
    def tweenThread(self):
        started = time()
        base = {}
        targets = self.__tween.targets
        duration = self.__tween.duration
        for i in targets.keys():
            base[i] = getattr(self, i)
        while time() - started < duration:
            t = (time() - started) / duration
            for i in targets.keys():
                setattr(self, i, (base[i] * (1-t)) + (targets.get(i) * t))
                print(getattr(self, i))
        for i in targets.keys():
            setattr(self, i, targets.get(i))
        self.__tween = None