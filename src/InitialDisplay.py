from .map_parser import Loop_Through
from .motor import Square, EasingStyle, EasingDirection, Text
from .motor import Color, Line, ColorPallet
from .drone.cells import Cell, ZoneType, Connection
from .motor import Scene
from time import sleep
from sys import argv
from pygame import Vector2
from threading import Thread, current_thread
from .drone.drones import Drone

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


def DisplayCells(visual, maps, cell_size, cell_inner) -> None:
    sceneList = {}

    cell_size = 100
    cell_inner = 80
    cell_difference = cell_size - cell_inner
    inner_size = cell_inner/cell_size

    settings = {
        "size": cell_size,
        "inner": cell_inner,
        "border": inner_size
    }

    for i in maps:
        scene = Scene(i)
        scene.Freecam = True
        data = maps.get(i)

        for cell_name in data["Cells"]:
            cell: Cell = data["Cells"].get(cell_name)
            for conection in cell.Connections:
                cell2: Connection = cell.Connections.get(conection).Target
                line = Line(cell_name+"->"+cell2.Name)
                line.size = (cell.Position * cell_size * 1.5) + Vector2(1, 1) * (cell_size / 2)
                line.position = (cell2.Position * cell_size * 1.5) + Vector2(1, 1) * (cell_size / 2)
                line.color = (cell.Color3 + cell2.Color3) * 0.5
                line.width = cell_size / 10
                scene.Add(line)

        for cell_name in data["Cells"]:
            cell: Cell = data["Cells"].get(cell_name)
            col = Square(cell_name)
            if col is not ColorPallet.rainbow:
                col.color = cell.Color3
            col.position = cell.Position * cell_size * 1.5
            col.size = Vector2(1, 1) * cell_size
            scene.Add(col)

        for cell_name in data["Cells"]:
            cell: Cell = data["Cells"].get(cell_name)
            back = Square(cell_name+"inside")
            back.size = (Vector2(1, 1) * cell_size) * inner_size
            back.position = ((cell.Position * cell_size * 1.5)
                             + Vector2(cell_difference / 2,
                                       cell_difference / 2))
            back.color = Color(0, 0, 0)
            scene.Add(back)
        # for cell_name in data["Cells"]:
        #     cell: Cell = data["Cells"].get(cell_name)
        #     txt = Text(cell_name+"inside")
        #     txt.text = cell_name
        #     txt.size = 15
        #     txt.position = ((cell.Position * cell_size * 1.5)
        #                     - Vector2(0,
        #                               cell_difference / 2))
        #     if txt is not ColorPallet.rainbow:
        #         txt.color = cell.Color3
        #     scene.Add(txt)
        sceneList[i] = scene
        visual.scenes.append(scene)

    Target = "01_the_impossible_dream"
    visual.ChangeScene(visual.GetScene(Target))
    Cells = maps.get(Target).get("Cells")

    drones = []
    for i in range(10):
        dr = Drone(Cells.get("start"), Cells, Cells.get("impossible_goal"),
                   settings)
        dr.Image = Square(f"Drone{i}")
        dr.Image.Color = Color(255, 255, 255)
        dr.Image.size = Vector2(1, 1) * (cell_inner / 2)
        dr.Image.position = Vector2(cell_difference / 2, cell_difference / 2)
        drones.append(dr)
        visual.current.Add(dr.Image)

    while not sleep(0.01) and visual.running:
        print("New Cycle")
        for i in drones:
            i.Move()
        for i in drones:
            i.moveimg()
