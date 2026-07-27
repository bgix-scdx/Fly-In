from .cells import Cell, ZoneType, Connection
from typing import List
from ..motor.Instances import Instance, EasingDirection, EasingStyle
from time import sleep
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
    Settings: Dict[str, int | str] = {}
    Image: Instance
    InConnection: Connection = None
    Path: List[Cell] = []
    PrecalculatedPaths: Dict[int, List[Cell]] | None = None
    FlyTime: float = 0.5
    Steps: int

    def __init__(self, starting: Cell, celllst: List[Cell], target: Cell, Settings):
        self.Current = starting
        self.CellList = celllst
        self.Settings = Settings
        self.Target = target
        self.Previous = None
        self.Next = None
        self.Moving = 0
        self.Path = None
        self.Current.Drones.insert(len(self.Current.Drones), self)

    def Move(self):
        if self.PrecalculatedPaths and self.Moving == 0 and self.Current is not self.Target:
            if not self.Path:
                chosen = math.inf
                for i in self.PrecalculatedPaths:
                    if int(i) < chosen:
                        self.Path = self.PrecalculatedPaths.get(i)[0]
                        chosen = int(i)
            index = self.Path.index(self.Current)
            if index < len(self.Path) - 1:
                if True:
                    self.Next = self.Path[index + 1]
            target_connection = self.Current.Connections.get(self.Next.Name)
            if (len(target_connection.Drones) >= target_connection.Maxdrones
                    and target_connection.Maxdrones > 0):
                self.Switch_Road()
            elif self.Next is not None:
                if self.InConnection:
                    self.InConnection.Drones.remove(self)
                target_connection.Drones.append(self)
                self.InConnection = target_connection
        else:
            return

    def Switch_Road(self) -> None:
        taken = None
        steps = math.inf
        for i in self.PrecalculatedPaths:
            targ = self.PrecalculatedPaths.get(i)
            for path in targ:
                try:
                    next_cell = path[path.index(self.Current) + 1]
                    target_connection = self.Current.Connections.get(next_cell.Name)
                    if (len(target_connection.Drones) >= target_connection.Maxdrones or
                            not self.Current in path):
                        continue
                    elif (not target_connection or path is self.Path
                            or self.Next is next_cell):
                        continue
                    if (i < steps):
                        taken = path
                        steps = i
                except IndexError:
                    pass
                except ValueError:
                    pass
        self.Path = taken
        if not taken:
            self.Next = None
        else:
            print(f"-> {steps}, {len(taken)}")
            self.Next = taken[self.Path.index(self.Current) + 1]
            target_connection = self.Current.Connections.get(self.Next.Name)
            if self.InConnection:
                self.InConnection.Drones.remove(self)
            target_connection.Drones.append(self)
            self.InConnection = target_connection

    def moveimg(self) -> None:
        if not self.Next:
            return
        size = self.Settings.get("size") * 2
        border = self.Settings.get("inner")

        self.Moving += 1 / self.Current.Zone.value
        difference = self.Current.Position + (self.Next.Position - self.Current.Position) * self.Moving
        calculated = (difference * size + 
                      (Vector2(border, border) / 2 ))
        self.Image.tween({"position": calculated}, self.FlyTime,
                         EasingStyle.Sine, EasingDirection.InOut)
        if self.Moving >= 1:
            self.Previous = self.Current
            self.Current = self.Next
            self.Moving = 0
            self.Next = None

    def getslotpos(self) -> Vector2:
        size = self.Settings.get("size")
        border = (size - self.Settings.get("inner"))
        img = self.Image
        center = ((self.Current.Position +
                   ((self.Next.Position - self.Current.Position) *
                    self.Moving)) * size + Vector2(border, border))
        maxslot = int(self.Next.MaxDrone)
        usedslots = len(self.Next.Drones)
        maxroot = sqrt(maxslot)

        side = usedslots % maxroot if usedslots % maxroot > 1 else 0.5 
        upper = floor((usedslots) / maxroot) % maxroot if maxslot > 2 else 0.5
        # side = side * 1.1 if side > 0.5 else side * 0.9 if side < 0.5 else side
        # upper = upper * 1.1 if upper > 0.5 else upper * 0.9 if upper < 0.5 else upper
        return center + Vector2(img.size.x * side, img.size.y * upper)

def count_steps_from_position(index, path: List[Cell]) -> float:
    total = 0
    for i in path[index::]:
        total += i.Zone.value
    return(total)