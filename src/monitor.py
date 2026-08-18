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
from threading import Thread


def getmapdata(raw_map: Dict[str, Any]) -> Any:
    '''Turn the raw map data into a well organised dict'''
    map: Dict[str, Dict[str, Cell]] = {}
    for name in raw_map:
        parsedmap = raw_map.get(name)
        if not parsedmap:
            continue
        map[name] = {}

        map[name]["Cells"] = {}
        map[name]["StartingCell"] = raw_map[name].get("StartingCell")
        map[name]["EndingCell"] = raw_map[name].get("EndingCell")
        for cell in parsedmap["cells"]:
            celldata = cell
            cell = Cell()
            cell.MaxDrone = 1
            cell.Zone = ZoneType.normal

            zone = celldata["settings"].get("zone")
            color = celldata["settings"].get("color")
            if color and hasattr(ColorPallet, color):
                cell.Color3 = getattr(ColorPallet,
                                      color).value
            else:
                print(f"\033[38;2;255m - Color '{color}' not found.\033[0m")
                return None, None
            if (zone and hasattr(ZoneType, celldata["settings"].get("zone"))):
                cell.Zone = getattr(ZoneType, zone)
            if (celldata["settings"].get("max_drones")):
                temp = int(celldata["settings"].get("max_drones"))
                if temp < 0:
                    print("\033[38;2;255m - Cell's max drones "
                          "can't be inferior to 1\033[0m")
                    return None, None
                cell.MaxDrone = temp
            cell.Position = Vector2(celldata["position"][0],
                                    celldata["position"][1])
            cell.Name = celldata["name"]
            map[name]["Cells"][cell.Name] = cell

        for connection in parsedmap["connections"]:
            for connectname in connection.get("connection"):
                cell1: Cell = map[name]["Cells"][connectname]
                for name2 in connection.get("connection"):
                    if connectname == name2:
                        continue
                    connect_count = (1 if not connection.get("max_drone")
                                     else connection.get("max_drone"))
                    cell2: Cell = map[name]["Cells"][name2]
                    if connect_count <= 0:
                        print("\033[38;2;255m - Connection can't be "
                              "inferior to 1\033[0m")
                        return None, None
                    connect = Connection()
                    connect.Parent = cell1
                    connect.Target = cell2
                    connect.Drones = []
                    connect.Maxdrones = connect_count
                    cell1.Connections[cell2.Name] = connect

                    connect2 = Connection()
                    connect2.Parent = cell2
                    connect2.Target = cell1
                    connect2.Drones = []
                    connect2.Maxdrones = connect_count
                    cell2.Connections[cell1.Name] = connect2
    return map, raw_map


def rainbow() -> None:
    from .motor import EasingStyle, EasingDirection
    current: Thread = current_thread()
    obj = current.obj  # type: ignore[attr-defined]
    duration = 1
    while current.visual.running:  # type: ignore[attr-defined]
        sleep(duration)
        obj.tween({"color": Color(255, 0, 0)},
                  duration, EasingStyle.Linear, EasingDirection.In)
        if not current.visual.running:  # type: ignore[attr-defined]
            break
        sleep(duration)
        obj.tween({"color": Color(255, 255, 0)},
                  duration, EasingStyle.Linear, EasingDirection.In)
        if not current.visual.running:  # type: ignore[attr-defined]
            break
        sleep(duration)
        obj.tween({"color": Color(0, 255, 0)},
                  duration, EasingStyle.Linear, EasingDirection.In)
        if not current.visual.running:  # type: ignore[attr-defined]
            break
        sleep(duration)
        obj.tween({"color": Color(0, 255, 255)},
                  duration, EasingStyle.Linear, EasingDirection.In)
        if not current.visual.running:  # type: ignore[attr-defined]
            break
        sleep(duration)
        obj.tween({"color": Color(0, 0, 255)},
                  duration, EasingStyle.Linear, EasingDirection.In)
        if not current.visual.running:  # type: ignore[attr-defined]
            break
        sleep(duration)
        obj.tween({"color": Color(255, 0, 255)},
                  duration, EasingStyle.Linear, EasingDirection.In)


def make_cells_scenes(visual: screen,
                      maps: Dict[str, Any]) -> Dict[str, Scene]:
    '''Assemble the scene for the maps'''
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
        connections: Dict[str, bool] = {}
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
                if ncell2.Zone is not ZoneType.restricted:
                    continue
                for index in range(ncell2.Zone.value - 1):
                    P1 = Vector2(ncell1.Position[0], ncell1.Position[1])
                    P2 = Vector2(ncell2.Position[0], ncell2.Position[1])
                    i = (index + 1) / (ncell2.Zone.value)
                    pos = (P1 + ((P2 - P1) * i)) * cell_size * 2
                    minibackground = Square("mini"+ncell2.Name
                                            + ncell1.Name+str(index))
                    minibackground.size = Vector2(cell_size / 2, cell_size / 2)
                    minibackground.position = (pos + Vector2(cell_size / 2,
                                                             cell_size / 2)
                                               - minibackground.size / 2)
                    if ncell2.Color3:
                        minibackground.color = (ncell1.Color3 +
                                                ncell2.Color3) * 0.5
                    local_scene.Add(minibackground)

                    minibackinner = Square("miniiner"+ncell2.Name+ncell1.Name
                                           + str(index))
                    minibackinner.size = (Vector2(cell_size / 2, cell_size / 2)
                                          - Vector2(cell_border, cell_border))
                    minibackinner.position = (pos + Vector2(cell_size / 2,
                                                            cell_size / 2)
                                              - minibackinner.size / 2)
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
                if str(bgcell.Color3) == str(Color(255, 255, 255)):
                    newthread = Thread(target=rainbow)
                    newthread.visual = visual  # type: ignore[attr-defined]
                    newthread.obj = background  # type: ignore[attr-defined]
                    newthread.start()
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
            namebg.text = f"{namecell.Name}  ({namecell.Zone.name})"
            namebg.position = Vector2(namecell.Position[0] * cell_size * 2,
                                      namecell.Position[1] * cell_size * 2 -
                                      cell_border * 4)
            local_scene.Add(namebg)

        local_scene.Zoom = 0.25
        map_scenes[map_name] = local_scene
        visual.scenes.append(local_scene)
    return map_scenes


def create_drones(raw_map: Dict[str, Any], map: Dict[str, Cell],
                  scene: Scene, path: Any) -> List[Drone] | None:
    '''Create and setup all drone for usage'''
    cell_settings = load_settings("settings/cells.json")
    drone_settings = load_settings("settings/drone.json")

    if not cell_settings or not drone_settings:
        return None

    cell_size = cell_settings.get("cell_size")
    cell_border = cell_settings.get("cell_border")

    drone_count = raw_map.get("nb_drones")
    if not drone_count or not cell_size or not cell_border:
        return None
    try:
        starting_cells = map["Cells"].get(map.get("StartingCell"))
        ending_cells = map["Cells"].get(map.get("EndingCell"))
    except KeyError:
        return None
    if not starting_cells or not ending_cells:
        print("\033[38;2;255mNo starting pos or ending pos.\033[0m")
        return None

    drone_size = (cell_size - cell_border) / 2
    drone_list = []
    for i in range(drone_count):
        drone = Drone(starting_cells, ending_cells, ending_cells,
                      {"size": cell_size, "inner": cell_size - drone_size},
                      path, i)
        drone.Name = f"Drone {i+1}"
        drone.Position = Vector2(0, 0)
        drone.PrecalculatedPaths = path
        drone.Current = starting_cells
        drone.FlyTime = drone_settings.get("drone_tween_time")
        drone.AllowConnection = drone_settings.get("allow_connection_wait")
        drone_img = Square(f"drone{i}")
        drone_img.size = Vector2(drone_size, drone_size)
        drone_img.color = Color(255, 255, 255)
        scene.Add(drone_img)
        drone.Image = drone_img
        drone_img.position = (Vector2(starting_cells.Position[0],
                                      starting_cells.Position[1])
                              * cell_size
                              + Vector2(cell_size/4, cell_size/4))
        drone_list.append(drone)
        starting_cells.Drones.append(drone)

    return drone_list


def start() -> None:
    '''Start the program andd checks errors'''
    thread = current_thread()
    visual: screen = thread.visual  # type: ignore[attr-defined]
    mapdata, raw_map = None, None
    try:
        mapdata, raw_map = getmapdata(Loop_Through())
    except KeyError:
        print("\033[38;2;255mFile Parsing Error.\033[0m")
        visual.running = False
        return
    if not mapdata or not raw_map:
        print("\033[38;2;255mAn error occured while loading maps.\033[0m")
        visual.running = False
        return
    mapscenes = make_cells_scenes(visual, mapdata)
    selected = argv[1]

    if selected not in mapdata:
        print(f"Map {selected} not found.")
        visual.running = False
        return
    else:
        print(f"Loading map {selected}...")

    visual.ChangeScene(mapscenes[selected])

    map = mapdata[selected]
    goal = map["Cells"][map.get("EndingCell")]
    paths = CheckPossiblePath(map["Cells"][map.get("StartingCell")],
                              None, goal, [], 0, [])
    sorted_paths: Dict[int, List[Cell]] = {}
    for chain in paths:
        steps = int(chain[len(chain)-1])
        if not sorted_paths.get(steps):
            sorted_paths[steps] = []
        sorted_paths[steps].append(chain[0:-1])  # Remove the steps
    target = 0
    i = None
    for i in sorted_paths:
        if i <= target:
            target = i
    if not i:
        print("No valid paths found.")
        visual.running = False
        return
    if sorted_paths.get(i):
        p = sorted_paths.get(i)
        if isinstance(p, list):
            target = p[0]
    else:
        print("Invalid Path, no end reachable")
        visual.running = False

    drone_list = create_drones(raw_map[selected],
                               mapdata[selected], visual.current,
                               sorted_paths)

    if not drone_list:
        visual.running = False
        return
    turn = 0
    reached = 0
    final_text = ""
    log = ""
    sleep(1)
    while visual.running and reached < len(drone_list):
        turn += 1
        text = f"--[ Turn {turn} ]--"
        spaces = " " * (int(len(drone_list) / 2) - int((len(text)) / 2) + 2)
        log = ""
        print("\033[2J")
        print(f"\n\033[38;2;255m{spaces}{text}\033[0m\n")
        reached = 0
        for i in drone_list:
            i.Move()
        for i in drone_list:
            log += i.moveimg()
            if i.DesinationReached:
                reached += 1
        if reached >= len(drone_list):
            break
        final_text += f" == Turn {turn} ==\n{log}\n\n"
        ProgessBar(reached, len(drone_list))
        sleep(1)
    final_text += f" == Turn {turn} ==\n{log}\n\n"
    if not visual.running:
        return
    spaces = " " * (int(len(drone_list) / 2) - int((len(text)) / 2) + 2)
    print("\033[2J")
    print(f"\n\033[38;2;255m{spaces}{text}\033[0m\n")
    print(f"\033[38;2;255;255mCompleted in \033[2;4;38;2;255;255m{turn}\033[0m"
          f" \033[38;2;255;255mturns\033[0m")
    with open("logs.txt", "a") as f:
        f.write(final_text)
        print("\033[38;2;255;0;255mLogs saved as \033[4;2mlogs.txt\033[0m")
    ProgessBar(reached, len(drone_list))
    return


def ProgessBar(a: int, b: int) -> None:
    '''Display a progress bar'''
    full, empty = "▣", "□"
    text = f"\033[38;2;0;255m {full*(a)}\033[38;2;255m{empty*(b-a)} "
    print()
    print(f"\033[38;2;255;0;255m┏{"━"*(b+2)}┓")
    print(f"\033[38;2;255;0;255m┃{text}\033[38;2;255;0;255m┃")
    print(f"\033[38;2;255;0;255m┗{"━"*(b+2)}┛\033[0m")
    print()


def CheckValidity(Cell: Cell, Connection: Connection,
                  last: Cell | None, path: List[Cell]) -> bool:
    '''Check if the cells and connection are valid'''
    if Cell is last or Cell in path:  # cell comp
        return False
    elif Cell.Zone is ZoneType.blocked:  # cell types
        return False
    return True


def CheckPossiblePath(Current: Cell, Last: Cell | None,
                      Target: Cell, Path: List[Cell],
                      Steps: int, GoalPaths: Any) -> Any:
    '''Calculate all possible paths from a map'''
    connection = Current.Connections
    if Current is Target:
        return [Path + [Current, Steps]]
    for i in connection:
        addedsteps = 0
        current = connection.get(i)
        current_zone = current.Target.Zone
        if not CheckValidity(current.Target, current, Last, Path):
            continue
        continuedpath = Path + [current.Parent]
        if (current_zone is ZoneType.blocked or current.Target.MaxDrone <= 0):
            continue
        elif current_zone is ZoneType.restricted:
            addedsteps += 2
        elif (current_zone is ZoneType.normal):
            addedsteps += 1
        addedsteps += Steps
        GoalPaths += CheckPossiblePath(current.Target, Current, Target,
                                       continuedpath, addedsteps, GoalPaths)
    return GoalPaths if not Last else []


@cache
def load_settings(path: str) -> Any | None:
    '''load settings from a json settings'''
    try:
        with open(path, "r") as f:
            return (load(f))
    except FileNotFoundError:
        print("File not found.")
        pass
    return None
