from pygame import Vector2
from typing import Any


class Scene():
    Freecam = False
    CameraPosition = Vector2(0, 0)
    Objects = {}
    Name = "NewScene"
    Zoom = 1

    def __init__(self, name: str) -> None:
        self.Name = name

    def Add(self, object: Any) -> None:
        object.Parent = self
        self.Objects[object.name] = object
