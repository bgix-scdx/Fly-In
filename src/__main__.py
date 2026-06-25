from .map_parser import Loop_Through
from sys import argv
from .motor import screen, Scene, Square
from time import sleep
from pygame import Vector2

val = Loop_Through()
for i, v in enumerate(val):
    print(v)

object = Square()


visual = screen(150)
visual.current.Objects["Baka"] = object
visual.current.Freecam = True
object.position = Vector2(1000, 500)
object.tween({"position": Vector2(1000, 1000), "size": Vector2(2500, 2500)}, 10)
