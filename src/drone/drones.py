from .cells import Cell, ZoneType, Connection
from ..motor.Instances import Instance, EasingDirection  # type: ignore[misc]
from ..motor.Instances import EasingStyle  # type: ignore[misc]
from pygame import Vector2
from math import sqrt, floor
from typing import Dict, List, Any

import math


class Drone():
    Current: Cell
    Previous: Cell
    Next: Cell
    CellList: List[Cell]
    Target: Cell
    Moving: float = 1
    Settings: Dict[str, Any] = {}
    Connect: Connection | None = None
    Image: Instance
    Path: List[Cell] | None = []
    DesinationReached: bool = False
    PrecalculatedPaths: Dict[int, List[Cell]] | None = None
    FlyTime: float = 0.1
    InConnection: bool = False
    Steps: int
    Active = False
    ID: int = 0

    def __init__(self, starting: Cell, celllst: List[Cell],
                 target: Cell, Settings: Dict[str, Any],
                 paths: Dict[int, List[Cell]], id: int):
        '''Start the drone'''
        self.Current = starting
        self.CellList = celllst
        self.Settings = Settings
        self.Target = target
        self.Previous = None
        self.Next = None
        self.Moving: float = 0
        self.Path = None
        self.ID = id
        self.PrecalculatedPaths = paths
        self.Current.Drones.insert(len(self.Current.Drones), self)

    def Move(self) -> None:
        '''Precalculate the drone movement before they visibly move'''
        self.Active = False
        if self.DesinationReached:
            return
        try:
            if 1 > self.Moving > 0 and (self.Next.isOk() or
                                        self.Next.Drones.index(self) >= 0):
                self.Active = True
                self.InConnection = True
                self.Next.Insert(self)
                if self.Connect:
                    self.Connect.Remove(self)
                    self.Connect = None
                return
            elif 1 > self.Moving > 0:
                return
        except ValueError:
            print(f"Bakus Mogus {self.ID}")
            return
        if not self.Path:
            self.get_valid_path()
        elif self.Path:
            if self.Connect:
                self.Connect.Remove(self)
                self.Connect = None
            self.MoveAlong()

    def MoveAlong(self) -> None:
        ''''''
        if not self.Path:
            return
        nextcell = None
        nextco = None

        self.Previous = self.Current
        self.Current = self.Next

        try:
            nextcell = self.Path[self.Path.index(self.Next) + 1]
            nextco = nextcell.Connections.get(self.Next.Name)
            if not nextco:
                return
        except IndexError:
            self.Active = True
            self.Next.Remove(self)
            if self.Connect:
                self.Connect.Remove(self)
                self.Connect = None
            self.DesinationReached = True
            return

        oknext = nextcell.isOk() or nextcell is self.Target

        if (oknext and nextcell.Zone and nextco.isOk()):
            if self.Next:
                self.Next.Remove(self)
            if self.Connect:
                self.Connect.Remove(self)
            self.Connect = nextco
            self.Connect.Insert(self)
            self.Next = nextcell
            self.Next.Insert(self)
        elif (not oknext and nextcell.Zone
                is ZoneType.restricted and nextco.isOk()):
            if self.Next:
                self.Next.Remove(self)
            if self.Connect:
                self.Connect.Remove(self)
            self.Connect = nextco
            self.Connect.Insert(self)
            self.Next = nextcell
        else:
            self.Switch_Road()

        self.Active = True

    def Switch_Road(self) -> None:
        '''Switch the road of the drone if the cell ahead is invalid'''
        taken = None
        steps = math.inf
        if not self.PrecalculatedPaths:
            return
        for i in self.PrecalculatedPaths:
            paths = self.PrecalculatedPaths.get(i)
            if not paths:
                continue
            for path in paths:
                try:
                    next_cell = path[path.index(self.Current) + 1]
                    current = self.Current.Connections
                    target_connection = current.get(next_cell.Name)
                    if not target_connection or (next_cell is self.Next):
                        continue
                    if not target_connection.isOk() or not next_cell.isOk():
                        continue
                    if next_cell.Zone is ZoneType.priority:
                        i -= 1
                    if (i < steps):
                        taken = path
                        steps = i
                except IndexError:
                    continue
                except ValueError:
                    continue
        if taken:
            self.Path = taken
            if self.Next:
                self.Next.Remove(self)
            self.Next = taken[self.Path.index(self.Current) + 1]
            target_connection = self.Current.Connections.get(self.Next.Name)
            self.Connect = target_connection if target_connection else None
            self.Next.Insert(self)

    def get_valid_path(self) -> None:
        if not self.PrecalculatedPaths:
            return
        chosen = math.inf
        for i in self.PrecalculatedPaths:
            if int(i) < chosen:
                path = self.PrecalculatedPaths.get(i)
                if not path:
                    continue
                for p in path:
                    try:
                        nextcell: Cell = p[p.index(self.Current) + 1]
                        connect = nextcell.Connections.get(self.Current.Name)
                        if not connect:
                            continue
                        if ((nextcell.isOk() or nextcell is self.Next)
                                and (connect.isOk()
                                     or connect is self.Connect)):
                            if self.Next:
                                self.Next.Remove(self)
                                self.Next = None
                            if self.Connect:
                                self.Connect.Remove(self)
                                self.Connect = None
                            self.Path = p
                            self.Next = self.Path[1]
                            self.Connect = connect
                            self.Connect.Insert(self)
                            self.Next.Insert(self)
                            chosen = int(i)
                            self.Active = True
                    except ValueError:
                        continue

    def moveimg(self) -> str:
        '''Vissibly move the drone on the visual'''
        if not self.Next or not self.Active or self.DesinationReached:
            return ""
        size = self.Settings.get("size")
        border = self.Settings.get("inner")
        if not size or not isinstance(size, int):
            size = 150 * 2
        else:
            size *= 2
        if not border or not isinstance(border, int):
            border = 120
        bordersize = (size - border) / 32
        self.Moving += 1 if self.Next.Zone is not ZoneType.restricted else 0.5
        difference = (self.Current.Position + (self.Next.Position -
                                               self.Current.Position)
                      * self.Moving)
        calculated = ((size *
                       Vector2(difference, difference))
                      + Vector2(size/8, size/8))
        logger_text = f"D{self.ID}-"
        print(f"\033[38;2;0;255;255mD\033[38;2;0;0;255m{self.ID}", end="")
        if self.Moving >= 1:
            print(f"\033[38;2;100;255;100m Inside Cell:"
                  f" \033[38;2;0;255;0m{self.Next.Name}")
            logger_text += f"{self.Next.Name} "
            self.Moving = 0
            animatedpos = self.getslotpos(calculated)
            self.Image.tween({"position": (animatedpos
                                           - Vector2(size/8, size/8))},
                             self.FlyTime)
        else:
            self.Image.tween({"position": calculated + Vector2(bordersize,
                                                               bordersize)},
                             self.FlyTime,
                             EasingStyle.Sine, EasingDirection.InOut)
            print(f"\033[38;2;100;100;255m In Connection: "
                  f"\033[38;2;0;255;255m{self.Current.Name} ->"
                  f"{self.Next.Name}")
            logger_text += (f"{self.Current.Name}-"
                            f"{self.Next.Name} ")
        print("\033[0m", end="")
        if self.Next is self.Target:
            self.DesinationReached = True
            if self.Connect:
                self.Connect.Remove(self)
            self.Next.Remove(self)
        return logger_text

    def getslotpos(self, position: Vector2) -> Vector2:
        '''Get the position within the cell for nice placement.'''
        size = self.Settings.get("size")
        inner = self.Settings.get("inner")
        if not size or not isinstance(size, int):
            size = 150
        if not inner or not isinstance(inner, int):
            inner = 120
        img = self.Image
        border = (size - inner) / 8
        maxslot = (int(self.Next.MaxDrone) if self.Next is not self.Target
                   else 1)
        usedslots = self.Next.Drones.index(self)
        maxroot = sqrt(maxslot)

        side = usedslots % maxroot if maxslot > 1 else 0.5
        upper = floor((usedslots) / maxroot) % maxroot if maxslot > 2 else 0.5
        return (position + (Vector2(img.size.x * side, img.size.y * upper))
                + Vector2(border, border))


def check_validity(cell: Cell | Connection) -> bool:
    '''Check if a cell is valid'''
    if len(cell.Drones) >= cell.MaxDrone:
        return False
    return True
