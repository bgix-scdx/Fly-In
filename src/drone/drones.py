from .cells import Cell, ZoneType
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

    def __init__(self, starting: Cell, celllst: List[Cell], target: Cell, Settings):
        self.Current = starting
        self.CellList = celllst
        self.Settings = Settings
        self.Target = target
        self.Next = None
        self.Current.Drones.insert(len(self.Current.Drones), self)

    def Move(self):
        bestmove, nextcell = 0, None
        connectionCount = len(self.Current.Connections)
        if self.Moving >= 1 or self.Moving <= 0:
            if self.Next:
                self.Current = self.Next
            for cell in self.Current.Connections:
                cell = self.Current.Connections.get(cell)
                print("=======> Moving from "+cell.Name)
                moves, priorities, found = recursiveCheck(cell, self.Current, self, path={})
                print(moves, priorities, found)
                if bestmove < moves - priorities and found:
                    bestmove, nextcell = moves - priorities, cell
                    self.Moving = 0
            if nextcell:
                self.Next = nextcell
        if not self.Next:
            print("Not Found")
            return
        else:
            self.Next = nextcell
        self.moveimg()

    def moveimg(self) -> None:
        size = self.Settings.get("size")
        border = (size - self.Settings.get("inner")) / 2
        if self.Moving == 0:
            # goes to the center animation
            self.Current.Drones.remove(self)
            self.Next.Drones.insert(len(self.Next.Drones), self)
            calculated = ((self.Current.Position * 150) +
                          (Vector2(size, size) - self.Image.size) / 2)
            self.Image.tween({"position": calculated}, 0.5,
                             EasingStyle.Sine, EasingDirection.In)
        self.Moving += 1 / self.Current.Zone.value
        calculated = ((self.Current.Position
                       + ((self.Next.Position - self.Current.Position)
                          * self.Moving)) * 150
                          + (Vector2(size, size) - self.Image.size) / 2)

        self.Image.tween({"position": calculated}, 1, EasingStyle.Sine,
                         EasingDirection.InOut)

        if self.Moving == 1:
            pos = self.getslotpos()
            calculated = ((self.Current.Position
                           + ((self.Next.Position - self.Current.Position)
                              * self.Moving)) * 150 + Vector2(border, border))
            self.Image.tween({"position": pos}, 0.5, EasingStyle.Sine,
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
        return center + Vector2(img.size.x * side, img.size.y * upper)


def recursiveCheck(cell: Cell, Previous: Cell, drone,
                   moves: int = 0, priorities: int = 0, Reached: bool = False, path = {}):
    if cell.Zone == ZoneType.blocked or len(cell.Slot) + 1 > int(cell.MaxDrone):
        return moves, priorities, False
    elif Reached and (moves + cell.Zone.value) - priorities # WAS HEREE
    elif (len(cell.Connections) >= 2
          or (len(cell.Connections) == 1
          and Previous and not cell.Connections.get(Previous.Name))):
        for tmpcell in cell.Connections:
            if (tmpcell == Previous.Name or path.get(tmpcell)):
                continue
            tmpcell = cell.Connections.get(tmpcell)
            path[cell.Name] = cell
            moves, priorities, Reached = recursiveCheck(tmpcell, cell, drone, moves,
                                                        priorities, Reached, path)
            if Reached:
                break
        if Reached:
            moves += cell.Zone.value
            if cell.Zone == ZoneType.priority:
                priorities += 1
            return moves, priorities, Reached
        if not Reached:
            return moves, priorities, False
        if cell.Zone == ZoneType.priority:
            priorities += 1
    elif cell.Name == drone.Target.Name:
        print("Ending Reached")
        return moves, priorities, True
    return moves, priorities, Reached
