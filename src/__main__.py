from .map_parser import Loop_Through
from .motor import screen, Square, EasingStyle, EasingDirection
from .motor import Color, Square, ColorPallet
from .drone.cells import Cell, ZoneType
from .drone.drones import Drone
from time import sleep
from sys import argv
from pygame import Vector2
from .InitialDisplay import DisplayCells


unsetmaps = Loop_Through()
maps = {}

for i in unsetmaps:
    data = unsetmaps.get(i)
    i = i.split("/")[len(i.split("/")) - 1].split(".")[0]

    mapdata = {}
    mapdata["Cells"] = {}
    for cell in data["cells"]:
        newcell = Cell()
        newcell.Position = Vector2(cell["position"][0], cell["position"][1])
        newcell.Name = cell["name"]
        newcell.Color3 = getattr(ColorPallet, cell["settings"]["color"]) if hasattr(ColorPallet, cell["settings"]["color"]) else Color(0, 0, 0)
        if cell["settings"].get("max_drones"):
            newcell.MaxDrone = cell["settings"]["max_drones"]
        if cell["settings"].get("zone"):
            newcell.Zone = getattr(ZoneType, cell["settings"].get("zone"))
        mapdata["Cells"][newcell.Name] = newcell

    for connection in data["connections"]:
        for name in connection:
            cell: Cell = mapdata["Cells"][name]
            for name2 in connection:
                if name == name2:
                    continue
                cell2: Cell = mapdata["Cells"][name2]

                cell.Connections[cell2.Name] = cell2
    maps[i] = mapdata


visual = screen(150)
visual.current.Freecam = True

target = maps.get(argv[1])
scale = 1.5
size = 50
dif = 10


DisplayCells(visual, maps)

# cube = Square("BAkus")
# visual.current.Add(cube)
# cube.tween({"position": Vector2(1000, 1000), "size": Vector2(100, 100),
#             "orientation": 360, "color": Color(255, 0, 0)}, 4, EasingStyle.Sine, EasingDirection.InOut)
