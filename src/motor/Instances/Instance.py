from pygame import Vector2
from pydantic import BaseModel
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

class InstanceType(Enum):
    pass


class Instance(ABC):
    name: str = "Instance"
    position: Vector2 = Vector2(0, 0)
    color: Tuple[int, int, int]

    @abstractmethod
    def execute(self) -> None:
        pass
