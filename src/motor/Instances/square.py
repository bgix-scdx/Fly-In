from .Instance import Instance
from pygame import Vector2, draw, transform, surface, SRCALPHA
from ..screen_manager import screen
from typing import Any


class Square(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: int = 0
    border_size: int = 0
    edge_size: int = 0

    def execute(self, visual: screen) -> Any:
        sur = surface.Surface(self.size * visual.current.Zoom, SRCALPHA)
        sur.fill(self.color.rgb())
        shape = transform.rotate(sur, self.orientation)
        visual.screen.blit(shape,
                           (self.position * visual.current.Zoom
                            + visual.current.CameraPosition))


class Line(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: int = 0
    border_size: int = 0
    width: int = 1

    def execute(self, visual: screen) -> None:
        draw.line(visual.screen, int(self.color),
                  (self.position * visual.current.Zoom +
                   visual.current.CameraPosition),
                  (self.size * visual.current.Zoom +
                   visual.current.CameraPosition),
                  int(self.width * visual.current.Zoom))


class Image(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: int = 0
    texture = None
    border_size: int = 0
    edge_size: int = 0

    def execute(self, visual: screen) -> None:
        if self.texture:
            visual.screen.blit(self.texture, self.position +
                               visual.current.CameraPosition)
