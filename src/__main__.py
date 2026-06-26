from .map_parser import Loop_Through
from .motor import screen, Square, EasingStyle, EasingDirection, Color
from time import sleep
from pygame import Vector2

val = Loop_Through()
for i, v in enumerate(val):
    print(v)
duration = 1
object = Square("test")
object2 = Square("test2")

visual = screen(150)
visual.current.Add(object)
# visual.current.Add(object2)
visual.current.Freecam = True
object.position = Vector2(1000, 500)
object2.position = Vector2(1100, 500)
object.color = Color(255, 0, 0)
object.size = Vector2(50, 50)
object2.color = Color(255, 0, 255)
object2.size = Vector2(50, 50)
Goal = Color(0, 0, 255)


while visual.running:
    object.tween({"color": Color(255, 0, 0)},
                 duration, EasingStyle.Linear, EasingDirection.InOut)
    sleep(duration)
    object.tween({"color": Color(0, 255, 0)},
                 duration, EasingStyle.Linear, EasingDirection.InOut)
    sleep(duration)
    object.tween({"color": Color(0, 0, 255)},
                 duration, EasingStyle.Linear, EasingDirection.InOut)
    sleep(duration)
