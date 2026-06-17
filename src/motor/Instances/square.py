from .Instance import Instance
from pygame import Vector2, display, draw, Rect


class square(Instance):
    size: Vector2 = Vector2(10, 10)
    orientation: Vector2 = Vector2(0, 0)
    border_size: int = 0
    egde_size: int = 0

    def execute(self, screen: display) -> None:
        draw.rect(screen, self.color, Rect(self.position.x, self.position.y,
                                           self.size.x, self.size.y),
                  0, self.border_size, self.edge_size, self.edge_size,
                  self.edge_size, self.edge_size)
