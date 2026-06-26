from .Instance import Instance
from pygame import Vector2, draw, Rect, transform, surface, display, SRCALPHA
from ..screen_manager import screen
from typing import Any


class Square(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: int = 0
    border_size: int = 0
    edge_size: int = 0

    def execute(self, visual: screen) -> Any:
        sur = surface.Surface(self.size, SRCALPHA)
        sur.fill(self.color.rgb())
        rec = sur.get_rect(center=Vector2(self.size.x / 2, self.size.y / 2))
        # Rect(self.position.x
        #                 + visual.current.CameraPosition.x,
        #                 self.position.y
        #                 + visual.current.CameraPosition.y,
        #                 self.size.x, self.size.y)
        shape = transform.rotate(sur, self.orientation)
        visual.screen.blit(shape,
                           self.position + visual.current.CameraPosition)
        # draw.rect(visual.screen, int(self.color),
        #           sur,
        #           0, self.border_size, self.edge_size, self.edge_size,
        #           self.edge_size, self.edge_size)


class Line(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: int = 0
    border_size: int = 0
    width: int = 1

    def execute(self, visual: screen) -> None:
        draw.line(visual.screen, int(self.color),
                  self.position + visual.current.CameraPosition,
                  self.size + visual.current.CameraPosition,
                  self.width)


class Image(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: int = 0
    texture = None
    border_size: int = 0
    edge_size: int = 0

    def execute(self, visual: screen) -> None:
        if self.texture:
            visual.screen.blit(self.texture, self.position + visual.current.CameraPosition)