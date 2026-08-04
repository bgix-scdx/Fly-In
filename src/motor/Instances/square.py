from .Instance import Instance
from pygame import Vector2, draw, transform, surface, SRCALPHA, font
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

    def __init__(self, name: str):
        super().__init__(name)
        self.size: Vector2 = Vector2(10, 10)
        self.orientation = 0
        self.texture = None
        self.order_size = 0
        self.edge_size = 0

    def execute(self, visual: screen) -> None:
        if self.texture:
            visual.screen.blit(self.texture, self.position +
                               visual.current.CameraPosition)


class Text(Instance):
    text = "Text"
    size = 20

    def execute(self, visual: screen) -> None:
        tfont = font.SysFont("impact", int(self.size * visual.current.Zoom))
        text = tfont.render(self.text, True, int(self.color))
        visual.screen.blit(text, (self.position * visual.current.Zoom +
                                  visual.current.CameraPosition))
