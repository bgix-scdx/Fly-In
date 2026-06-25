from pygame import Vector2


class Scene():
    Freecam = False
    CameraPosition = Vector2(0, 0)
    Objects = {}
    Name = "NewScene"

    def __init__(self, name: str) -> None:
        self.Name = name
