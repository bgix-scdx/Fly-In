from .map_parser import Loop_Through
from .motor import screen, Square, EasingStyle, EasingDirection, Color, Line, ColorPallet, Image
from time import sleep
from sys import argv
from pygame import Vector2, image, transform
from threading import Thread, current_thread
from enum import Enum
val = Loop_Through()
from random import randint
maps = {}

duration = 1
object = Square("test")
visual = screen(150)
visual.current.Freecam = True

target = val.get(argv[1])
scale = 1.5
size = 50
dif = 10

for i in target["connections"]:
    cells = target["cells"]
    pos = Vector2(0, 0)
    fpos = Vector2(0, 0)

    for t in target["cells"]:
        if t["name"] == i[1]:
            pos = Vector2(t["position"][0] * 100 + size / 2, t["position"][1] * 100 + size / 2) * scale
        elif t["name"] == i[0]:
            fpos = Vector2(t["position"][0] * 100 + size / 2, t["position"][1] * 100 + size / 2) * scale
    fpos = fpos
    object = Line(f"{i[0]}-{i[1]}")
    object.position = pos
    object.size = fpos
    object.width = round(5 * scale)
    visual.current.Add(object)


def rainbow() -> None:
    current = current_thread()
    duration = 1
    while current.visual.running:
        sleep(duration)
        current.obj.tween({"color": Color(255, 0, 0)},
                          duration, EasingStyle.Linear, EasingDirection.In)
        sleep(duration)
        current.obj.tween({"color": Color(255, 255, 0)},
                          duration, EasingStyle.Linear, EasingDirection.In)
        sleep(duration)
        current.obj.tween({"color": Color(0, 255, 0)},
                          duration, EasingStyle.Linear, EasingDirection.In)
        sleep(duration)
        current.obj.tween({"color": Color(0, 255, 255)},
                          duration, EasingStyle.Linear, EasingDirection.In)
        sleep(duration)
        current.obj.tween({"color": Color(0, 0, 255)},
                          duration, EasingStyle.Linear, EasingDirection.In)
        sleep(duration)
        current.obj.tween({"color": Color(255, 0, 255)},
                          duration, EasingStyle.Linear, EasingDirection.In)


for i in target["cells"]:
    border = (size - (size - dif)) / 2

    object = Square(i["name"])
    object.size = Vector2(size, size) * scale
    if (hasattr(ColorPallet, i["settings"]["color"])
            or i["settings"]["color"] == "rainbow"):
        if i["settings"]["color"] == "rainbow":
            t = Thread(target=rainbow)
            t.visual = visual
            t.obj = object
            t.start()
        else:
            colpal = ColorPallet[i["settings"]["color"]].value
            object.color = colpal
    else:
        print(i["settings"]["color"])
    object.position = Vector2(i["position"][0] * 100, i["position"][1] * 100) * scale
    visual.current.Add(object)
    cache = object = Square(f"{i["name"]}cache")
    cache.position = Vector2(i["position"][0] * 100 + border, i["position"][1] * 100 + border) * scale
    object.size = Vector2(size - dif, size - dif) * scale
    cache.color = Color(0, 0, 0)
    visual.current.Add(cache)

test = Square("Baka")
test.size = Vector2(50, 50)
visual.current.Add(test)

while visual.running:
    sleep(1)
    test.tween({"position": Vector2(randint(0, 1000), randint(0, 1000)),
                "orientation": test.orientation + 360 * 2,
                "color": Color(randint(0, 255), randint(0, 255),randint(0, 255))},
               1, EasingStyle.Busted, EasingDirection.In)
    pass
