from pygame import Vector2
from typing import Any, Dict


class Scene():
    '''Scenes is the format that save specific setting and objects
    for the window to handle.'''
    Freecam = False
    CameraPosition = Vector2(0, 0)
    Objects: Dict[str, Any] = {}
    Name: str = "NewScene"
    Zoom: float = 1

    def __init__(self, name: str) -> None:
        '''Start the screen.'''
        self.Name = name
        self.Objects = {}
        self.CameraPosition = Vector2(0, 0)
        self.Zoom = 1
        self.Freecam = False

    def Add(self, object: Any) -> None:
        '''Add a new scene to the window's storage.'''
        object.Parent = self
        self.Objects[object.name] = object
