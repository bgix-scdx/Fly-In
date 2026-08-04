from .cells import Cell, ZoneType, Connection
from ..motor.Instances import Instance, EasingDirection  # type: ignore[misc]
from ..motor.Instances import EasingStyle  # type: ignore[misc]
from ..motor.Color import Color  # type: ignore[misc]
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
    Image: Instance
    InConnection: Connection = None
    Path: List[Cell] | None = []
    DesinationReached: bool = False
    PrecalculatedPaths: Dict[int, List[Cell]] | None = None
    FlyTime: float = 0.5
    Steps: int
    ID: int

    def __init__(self, starting: Cell, celllst: List[Cell],
                 target: Cell, Settings: Dict[str, Any]):
        self.Current = starting
        self.CellList = celllst
        self.Settings = Settings
        self.Target = target
        self.Previous = None
        self.Next = None
        self.Moving: float = 0
        self.Path = None
        self.Current.Drones.insert(len(self.Current.Drones), self)

    def Move(self) -> None:
        if (self.PrecalculatedPaths and self.Moving == 0 and
                self.Current is not self.Target):
            if self.Next:
                self.Next.Drones.remove(self)
            if not self.Path:
                chosen = math.inf
                for i in self.PrecalculatedPaths:
                    if int(i) < chosen:
                        path = self.PrecalculatedPaths.get(i)
                        if not path:
                            continue
                        for p in path:
                            try:
                                if check_validity(p[p.index(self.Current)
                                                    + 1]):
                                    self.Path = p
                                    chosen = int(i)
                            except ValueError:
                                continue
            if not self.Path:
                return
            index = self.Path.index(self.Current)
            if index < len(self.Path) - 1:
                if True:
                    if self.Next:
                        self.Next.Drones.remove(self)
                    self.Next = self.Path[index + 1]
            target_connection = self.Current.Connections.get(self.Next.Name)
            if ((len(target_connection.Drones) >= target_connection.Maxdrones
                    and target_connection.Maxdrones > 0)
                    or not check_validity(self.Next)):
                self.Switch_Road()
            elif self.Next is not None and check_validity(self.Next):
                target_connection.Drones.append(self)
                self.InConnection = target_connection
                self.Next.Drones.append(self)
            self.DesinationReached = False
        if self.Path is None:
            self.Image.color = Color(255, 0, 0)
        else:
            self.Image.color = Color(255, 255, 255)

    def Switch_Road(self) -> None:
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
                    if (len(target_connection.Drones) >=
                            target_connection.Maxdrones):
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
        if not taken:
            self.Next = None
        else:
            self.Path = taken
            self.Next = taken[self.Path.index(self.Current) + 1]
            target_connection = self.Current.Connections.get(self.Next.Name)
            if self.InConnection:
                self.InConnection.Drones.remove(self)
            target_connection.Drones.append(self)
            self.Next.Drones.append(self)
            self.InConnection = target_connection

    def moveimg(self) -> str:
        if not self.Next:
            return ""

        size = self.Settings.get("size")
        border = self.Settings.get("inner")
        if not size or not isinstance(size, int):
            size = 150 * 2
        else:
            size *= 2
        if not border or not isinstance(border, int):
            border = 120

        self.Moving += 1 if self.Next.Zone is not ZoneType.restricted else 0.5
        difference = (self.Current.Position + (self.Next.Position -
                                               self.Current.Position)
                      * self.Moving)
        calculated = (difference * size +
                      (Vector2(border, border) / 2))
        self.Image.tween({"position": calculated}, self.FlyTime,
                         EasingStyle.Sine, EasingDirection.InOut)
        logger_text = f"D{self.ID}-"
        print(f"\033[38;2;0;255;255mD\033[38;2;0;0;255m{self.ID}", end="")
        if self.Moving >= 1:
            print(f"\033[38;2;100;255;100m Inside Cell:"
                  f" \033[38;2;0;255;0m{self.Next.Name}")
            logger_text += f"{self.Next.Name} "
            self.Previous = self.Current
            self.Current = self.Next
            self.Moving = 0
            self.Next.Drones.remove(self)
            self.Next = None
            if self.Current is self.Target:
                self.DesinationReached = True
        else:
            print(f"\033[38;2;100;100;255m In Connection: "
                  f"\033[38;2;0;255;255m{self.InConnection.Parent.Name} ->"
                  f"{self.InConnection.Target.Name}")
            logger_text += (f"{self.InConnection.Parent.Name}-"
                            f"{self.InConnection.Target.Name} ")
        if self.InConnection:
            self.InConnection.Drones.remove(self)
            self.InConnection = None
        print("\033[0m", end="")
        return logger_text

    def getslotpos(self) -> Vector2:
        size = self.Settings.get("size")
        inner = self.Settings.get("inner")
        if not size or not isinstance(size, int):
            size = 150
        if not inner or not isinstance(inner, int):
            inner = 120
        border = (size - inner)
        img = self.Image
        center: Vector2 = ((self.Current.Position +
                           ((self.Next.Position - self.Current.Position) *
                            self.Moving)) * size + Vector2(border, border))
        maxslot = int(self.Next.MaxDrone)
        usedslots = len(self.Next.Drones)
        maxroot = sqrt(maxslot)

        side = usedslots % maxroot if usedslots % maxroot > 1 else 0.5
        upper = floor((usedslots) / maxroot) % maxroot if maxslot > 2 else 0.5
        return center + Vector2(img.size.x * side, img.size.y * upper)


def check_validity(cell: Cell | Connection) -> bool:
    if len(cell.Drones) > cell.MaxDrone:
        return False
    return True
