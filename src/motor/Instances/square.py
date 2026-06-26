from .Instance import Instance
from pygame import Vector2, draw, Rect
from ..screen_manager import screen
from typing import Any

class Square(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: Vector2 = Vector2(0, 0)
    border_size: int = 0
    edge_size: int = 0

    def execute(self, visual: screen) -> Any:
        draw.rect(visual.screen, int(self.color),
                  Rect(self.position.x
                       + visual.current.CameraPosition.x,
                       self.position.y
                       + visual.current.CameraPosition.y,
                       self.size.x, self.size.y),
                  0, self.border_size, self.edge_size, self.edge_size,
                  self.edge_size, self.edge_size)
