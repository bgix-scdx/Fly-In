from .cells import Cell, ZoneType, Connection
from typing import List
from ..motor.Instances import Instance, EasingDirection, EasingStyle
from time import sleep
from pygame import Vector2
from math import sqrt, floor


class Drone():
    Current: Cell
    Previous: Cell
    Next: Cell
    CellList: List[Cell]
    Target: Cell
    Moving: float = 1
    Settings = {}
    Image: Instance
    InConnection: Connection = None
    Path: List[Cell] = []

    def __init__(self, starting: Cell, celllst: List[Cell], target: Cell, Settings):
        self.Current = starting
        self.CellList = celllst
        self.Settings = Settings
        self.Target = target
        self.Previous = None
        self.Next = None
        self.Path = None
        self.Current.Drones.insert(len(self.Current.Drones), self)

    def Move(self):
        if (self.Moving >= 1 or self.Moving <= 0) and (not self.Path or (self.Path and not CheckValidity(self.Current, self.Current.Connections.get(self.Path[len(self.Path) - 1].Name)))):
            last = [] if not self.Previous else [self.Previous]
            moves, path, mmove, found = BackTrackCheck(self.Current, 2147483647, last, 0, False, self.Target)
            if found:
                nextcell = path[len(path) - 1]
                self.Path = path
                connect = self.Current.Connections.get(self.Path[len(self.Path) - 1].Name)
                if self.InConnection:
                    self.InConnection.Drones.remove(self)
                    print(len(self.InConnection.Drones))
                    self.InConnection = None
                self.InConnection = connect
                connect.Drones.append(self)
                self.Path.remove(nextcell)
                if not nextcell:
                    print("Not Found")
                    return
                else:
                    self.Next = nextcell
                    self.Moving = 0
        elif (self.Moving >= 1 or self.Moving <= 0) and self.Path:
            nextcell = self.Path[len(self.Path) - 1]
            connect = self.Current.Connections.get(self.Path[len(self.Path) - 1].Name)
            if self.InConnection:
                self.InConnection.Drones.remove(self)
                print(len(self.InConnection.Drones))
                self.InConnection = None
            self.InConnection = connect
            connect.Drones.append(self)
            self.Path.remove(nextcell)
            if not nextcell:
                print("Not Found")
                return
            else:
                self.Next = nextcell
                self.Moving = 0


    def moveimg(self) -> None:
        size = self.Settings.get("size")
        border = (size - self.Settings.get("inner")) / 2
        if not self.Next:
            return
        if self.Moving == 0:
            # goes to the center animation
            self.Current.Drones.remove(self)
            self.Next.Drones.insert(len(self.Next.Drones), self)
            calculated = ((self.Current.Position * 150) +
                          (Vector2(size, size) - self.Image.size) / 2)
            self.Image.tween({"position": calculated}, 0.1,
                             EasingStyle.Sine, EasingDirection.In)
        self.Moving += 1 / self.Current.Zone.value
        calculated = ((self.Current.Position
                       + ((self.Next.Position - self.Current.Position)
                          * self.Moving)) * 150
                          + (Vector2(size, size) - self.Image.size) / 2)

        self.Image.tween({"position": calculated}, 0.1, EasingStyle.Sine,
                         EasingDirection.InOut)
        if self.Moving == 1:
            pos = self.getslotpos()
            if pos.x != self.Image.position.x or pos.y != self.Image.position.y:
                self.Image.tween({"position": pos}, 0.1, EasingStyle.Sine,
                                 EasingDirection.Out)
            self.Previous = self.Current
            self.Current = self.Next
            self.Next = None

    def getslotpos(self) -> Vector2:
        size = self.Settings.get("size")
        border = (size - self.Settings.get("inner")) / 2
        img = self.Image
        center = ((self.Current.Position +
                   ((self.Next.Position - self.Current.Position) *
                    self.Moving)) * 150 + Vector2(border, border))
        maxslot = int(self.Next.MaxDrone)
        usedslots = len(self.Next.Drones)
        maxroot = sqrt(maxslot)

        side = usedslots % maxroot if usedslots % maxroot > 1 else 0.5 
        upper = floor((usedslots) / maxroot) % maxroot if maxslot > 2 else 0.5
        # side = side * 1.1 if side > 0.5 else side * 0.9 if side < 0.5 else side
        # upper = upper * 1.1 if upper > 0.5 else upper * 0.9 if upper < 0.5 else upper
        return center + Vector2(img.size.x * side, img.size.y * upper)

def CheckValidity(cell: Cell, connection: Connection) -> bool:
    validcell = False
    validconnection = False

    if len(cell.Slot) < int(cell.MaxDrone):
        validcell = True
    if connection and len(connection.Drones) < int(cell.MaxDrone):
        validconnection = True

    return(validcell is True and validconnection is True)

def BackTrackCheck(cell: Cell, moves, path: List[Cell], maxmoves, found, target) -> any:
    if (path.count(cell) > 0 or (found and moves > maxmoves)
            or cell.Zone == ZoneType.blocked):
        return moves, path, maxmoves, found
    else:
        fmoves, freached, fpath, fmax = moves, found, path, maxmoves
        for tmpcell in cell.Connections:
            tmpcell = cell.Connections.get(tmpcell).Target
            reached = found
            lmoves = moves
            lmax = maxmoves
            lpath = []
            tmppath = path + [cell]
            if path.count(tmpcell) > 0:
                continue
            if tmpcell != target:
                lmoves, lpath, lmax, reached = BackTrackCheck(tmpcell, moves,
                                                              tmppath, maxmoves,
                                                              found, target)
                if not reached:
                    continue
            else:
                lmoves = tmpcell.Zone.value - (1 if tmpcell.Zone == ZoneType.priority else 0)
                reached = True
            if fmoves > lmoves:
                freached = reached
                fpath = lpath + [tmpcell]
                fmoves = lmoves + tmpcell.Zone.value - (1 if tmpcell.Zone == ZoneType.priority else 0)
                fmax = lmax + tmpcell.Zone.value - (1 if tmpcell.Zone == ZoneType.priority else 0)
        return fmoves, fpath, fmax, freached
