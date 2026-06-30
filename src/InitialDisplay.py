from .map_parser import Loop_Through
from .motor import Square, EasingStyle, EasingDirection
from .motor import Color, Line, ColorPallet
from .drone.cells import Cell, ZoneType
from .motor import Scene
from time import sleep
from sys import argv
from pygame import Vector2
from threading import Thread, current_thread

val = Loop_Through()
target = val.get(argv[1])
size = 50
dif = 10


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


def DisplayCells(visual, maps) -> None:
    sceneList = {}

    cell_size = 100
    inner_size = cell_size/cell_size

    for i in maps:
        scene = Scene(i)
        data = maps.get(i)

        for cell_name in data["Cells"]:
            cell: Cell = data["Cells"].get(cell_name)
            col = Square(cell_name)
            if col is not ColorPallet.rainbow:
                col.color = cell.Color3()
            col.position = cell.Position * cell_size * 1.5
            col.size = Vector2(1, 1) * cell_size
            scene.Add(col)

        sceneList[i] = scene
        print(f"{i} Pre-Loaded.")
    visual.Current = sceneList["02_simple_fork"]
