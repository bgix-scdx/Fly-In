from threading import current_thread
from json import load
from .drone.drones import Drone
from .map_parser import Loop_Through
from .motor import screen, Scene, Square, Color, Line, ColorPallet, Text
from typing import Dict, Any, List
from sys import argv
from .drone.cells import Cell, ZoneType, Connection
from pygame import Vector2
from time import sleep
from functools import cache

def getmapdata(raw_map: Dict[str, Any]) -> Dict[str, Any]:
    map = {}
    for name in raw_map:
        parsedmap = raw_map.get(name)
        map[name] = {}

        map[name]["Cells"] = {}
        for cell in parsedmap["cells"]:
            celldata = cell
            cell = Cell()
            cell.MaxDrone = celldata.get("MaxDrone")
            cell.Zone = ZoneType.normal
            if hasattr(ColorPallet, celldata["settings"].get("color")):
                cell.Color3 = getattr(ColorPallet,
                                      celldata["settings"].get("color")).value
            else:
                print(f"Color {celldata["settings"].get("color")} not found")
                cell.Color3 = Color(255, 255, 255)

            if celldata["settings"].get("zone") and hasattr(ZoneType, celldata["settings"].get("zone")):
                cell.Zone = getattr(ZoneType,
                                    celldata["settings"].get("zone"))
            if celldata["settings"].get("maxdrone") and hasattr(ZoneType, celldata["settings"].get("maxdrone")):
                cell.Zone = getattr(ZoneType,
                                    celldata["settings"].get("maxdrone"))
            cell.Position = Vector2(celldata["position"][0], celldata["position"][1])
            cell.Name = celldata["name"]
            map[name]["Cells"][cell.Name] = cell

        for connection in parsedmap["connections"]:
            for connectname in connection.get("connection"):
                cell: Cell = map[name]["Cells"][connectname]
                for name2 in connection.get("connection"):
                    if connectname == name2:
                        continue
                    cell2: Cell = map[name]["Cells"][name2]
                    connect = Connection()
                    connect.Parent = cell
                    connect.Target = cell2
                    connect.Drones = []
                    connect.Maxdrones = connection.get("max_drone")
                    cell.Connections[cell2.Name] = connect

                    connect2 = Connection()
                    connect2.Parent = cell2
                    connect2.Target = cell
                    connect2.Drones = []
                    connect2.Maxdrones = 1
                    cell2.Connections[cell.Name] = connect2
    print(raw_map)
    return map, raw_map

def make_cells_scenes(visual: screen, maps: Dict[str, Any]) -> Dict[str, Scene]:
    map_scenes = {}
    cell_settings = {}
    with open("settings/cells.json", "r") as f:
        cell_settings = load(f)

    cell_size = cell_settings.get("cell_size")
    cell_border = cell_settings.get("cell_border")

    for map_name in maps:
        local_scene = Scene(map_name)
        local_scene.Freecam = True
        local_scene.Zoom = 1
        connections = {}
        for connection_name in maps[map_name]["Cells"]:
            cell1 = maps[map_name]["Cells"][connection_name]
            connect: Connection = cell1.Connections
            for name in connect:
                cell2: Cell = connect.get(name).Target
                if (connections.get(f"{cell1.Name}-{cell2.Name}")
                        or connections.get(f"{cell2.Name}-{cell1.Name}")):
                    continue
                line = Line(f"{cell1.Name}-{cell2.Name}")
                connections[f"{cell1.Name}-{cell2.Name}"] = True
                if cell1.Color3 and cell2.Color3:
                    line.color = (cell1.Color3 + cell2.Color3) * 0.5
                else:
                    line.color = Color(255, 255, 255)
                line.position = Vector2(cell1.Position[0] * cell_size * 2
                                        + cell_size / 2,
                                        cell1.Position[1] * cell_size * 2
                                        + cell_size / 2)
                line.size = Vector2(cell2.Position[0] * cell_size * 2
                                    + cell_size / 2,
                                    cell2.Position[1] * cell_size * 2
                                    + cell_size / 2)
                line.width = cell_border
                local_scene.Add(line)

        for connection_name in maps[map_name]["Cells"]:
            ncell1 = maps[map_name]["Cells"][connection_name]
            nconnect: Connection = ncell1.Connections
            for name in nconnect:
                ncell2: Cell = nconnect.get(name).Target
                if ncell2.Zone.value <= 1:
                    continue
                for index in range(ncell2.Zone.value - 1):
                    P1 = Vector2(ncell1.Position[0], ncell1.Position[1])
                    P2 = Vector2(ncell2.Position[0], ncell2.Position[1])
                    i = (index + 1) / (ncell2.Zone.value)
                    pos = (P1 + ((P2 - P1) * i)) * cell_size * 2
                    minibackground = Square("mini"+ncell2.Name+str(index))
                    minibackground.size = Vector2(cell_size / 2, cell_size / 2)
                    minibackground.position = pos + Vector2(cell_size / 2, cell_size / 2) - minibackground.size / 2
                    if ncell2.Color3:
                        minibackground.color = (ncell1.Color3 + ncell2.Color3) * 0.5
                    local_scene.Add(minibackground)

                    minibackinner = Square("miniiner"+ncell2.Name+str(index))
                    minibackinner.size = Vector2(cell_size / 2, cell_size / 2) - Vector2(cell_border, cell_border)
                    minibackinner.position = pos + Vector2(cell_size / 2, cell_size / 2) - minibackinner.size / 2
                    if ncell2.Color3:
                        minibackinner.color = Color(0, 0, 0)
                    local_scene.Add(minibackinner)

        for cell_name in maps[map_name]["Cells"]:
            bgcell: Cell = maps[map_name]["Cells"][cell_name]
            background = Square("bg"+cell_name)
            background.size = Vector2(cell_size, cell_size)
            background.color = Color(255, 255, 255)
            background.position = Vector2(bgcell.Position[0] * cell_size * 2,
                                          bgcell.Position[1] * cell_size * 2)
            if bgcell.Color3:
                background.color = bgcell.Color3
            local_scene.Add(background)

        for cell_name in maps[map_name]["Cells"]:
            cell: Cell = maps[map_name]["Cells"][cell_name]
            innersize = cell_size - cell_border * 2
            inner = Square("inner"+cell_name)
            inner.size = Vector2(innersize, innersize)
            inner.color = Color(0, 0, 0)
            inner.position = Vector2(cell.Position[0] * cell_size * 2
                                     + cell_border,
                                     cell.Position[1] * cell_size * 2
                                     + cell_border)
            local_scene.Add(inner)

        for cell_name in maps[map_name]["Cells"]:
            namecell: Cell = maps[map_name]["Cells"][cell_name]
            namebg = Text("name"+cell_name)
            namebg.size = cell_size / 8
            namebg.color = Color(255, 255, 255)
            namebg.text = namecell.Name
            namebg.position = Vector2(namecell.Position[0] * cell_size * 2,
                                      namecell.Position[1] * cell_size * 2 - cell_border * 4)
            if namecell.Color3:
                namebg.color = namecell.Color3
            local_scene.Add(namebg)

        local_scene.Zoom = 0.25
        map_scenes[map_name] = local_scene
        visual.scenes.append(local_scene)
    return map_scenes


def create_drones(raw_map: Dict[str, Any], map: Dict[str, Cell],
                  scene: Scene, path) -> List[Drone] | None:

    cell_settings = load_settings("settings/cells.json")
    drone_settings = load_settings("settings/drone.json")

    if not cell_settings or not drone_settings:
        return None

    cell_size = cell_settings.get("cell_size")
    cell_border = cell_settings.get("cell_border")

    drone_count: int = raw_map.get("nb_drones")
    starting_cells = map["Cells"].get("start")
    ending_cells = map["Cells"].get("impossible_goal")

    drone_size = (cell_size - cell_border) / 2
    drone_list = []
    for i in range(drone_count):
        drone = Drone(starting_cells, ending_cells, ending_cells,
                      {"size": cell_size, "inner": cell_size - drone_size})
        drone.Name = f"Drone {i+1}"
        drone.Position = Vector2(0, 0)
        drone.PrecalculatedPaths = path
        drone.FlyTime = drone_settings.get("drone_tween_time")
        drone_img = Square(f"drone{i}")
        drone_img.size = Vector2(drone_size, drone_size)
        drone_img.color = Color(255, 255, 255)
        scene.Add(drone_img)
        drone.Image = drone_img
        drone_img.position = Vector2(starting_cells.Position[0],
                                     starting_cells.Position[1]) * cell_size + Vector2(cell_size/4, cell_size/4)
        drone_list.append(drone)

    return drone_list


def start() -> None:
    thread = current_thread()
    visual: screen = thread.visual
    mapdata, raw_map = getmapdata(Loop_Through())
    mapscenes = make_cells_scenes(visual, mapdata)
    selected = argv[1]

    if selected not in mapdata:
        print(f"Map {selected} not found.")
        return
    else:
        print(f"Loading map {selected}...")

    visual.ChangeScene(mapscenes[selected])

    map = mapdata[selected]
    paths = CheckPossiblePath(map["Cells"]["start"], None, map["Cells"]["impossible_goal"], [], 0, [])

    sorted_paths: Dict[int, List[Cell]] = {}
    for chain in paths:
        steps = int(chain[len(chain)-1])
        if not sorted_paths.get(steps):
            sorted_paths[steps] = []
        sorted_paths[steps].append(chain[0:-1])  # Remove the steps
    target = 0
    for i in sorted_paths:
        if i <= target:
            target = i
    target = sorted_paths.get(i)[0]
    drone_list = create_drones(raw_map[selected],
                               mapdata[selected], visual.current,
                               sorted_paths)
    while visual.running:
        sleep(1)
        for i in drone_list:
            i.Move()
        for i in drone_list:
            i.moveimg()


def CheckValidity(Cell: Cell, Connection, last, path) -> bool:
    if Cell is last or Cell in path:  # cell comp
        return False
    elif Cell.Zone is ZoneType.blocked:  # cell types
        return False
    return True


def CheckPossiblePath(Current: Cell, Last: Cell | None, Target, Path, Steps, GoalPaths):
    connection = Current.Connections

    if Current is Target:
        return [Path + [Current , Steps]]
    for i in connection:
        current = connection.get(i)
        if not CheckValidity(current.Target, current, Last, Path):
            continue
        continuedpath = Path + [current.Parent]
        addedsteps = Steps + current.Target.Zone.value
        GoalPaths += CheckPossiblePath(current.Target, Current, Target,
                                       continuedpath, addedsteps, GoalPaths)
    return GoalPaths if not Last else []

@cache
def load_settings(path) -> Dict[str, Any] | None:
    try:
        with open(path, "r") as f:
            return (load(f))
    except FileNotFoundError:
        print("File not found.")
        pass
    return None
