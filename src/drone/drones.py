from .cells import Cell, ZoneType
from typing import List
from ..motor.Instances import Instance

class Drone():
    Current: Cell
    Previous: Cell
    CellList: List[Cell]
    Target: Cell
    Moving: float = 1
    Image: Instance

    def __init__(self, starting: Cell, celllst: List[Cell], target: Cell):
        self.Current = starting
        self.CellList = celllst
        self.Target = self.Target

    def Move(self):
        bestmove, nextcell = 0, None
        connectionCount = len(self.Current.Connections)
        if self.Moving >= 1 or self.Moving <= 0:
            for cell in self.Current.Connections:
                if (cell.Slot is not None or cell.Zone == ZoneType.blocked and
                   (connectionCount > 1 and cell == self.Previous)):
                    continue
                moves, priorities, found = recursiveCheck()

                if bestmove < moves - priorities and found:
                    bestmove, nextcell = moves - priorities, cell
        else:
            self.Moving += 1 / self.Current.Zone
        if not nextcell:
            return
        self.Previous = self.Current
        self.Current = nextcell

def recursiveCheck(cell: Cell, Previous: Cell,
                   moves: int = 0, priorities: int = 0, Reached: bool = False):
    if cell.Zone == ZoneType.blocked or cell.Slot is not None:
        return moves, priorities, False
    elif (len(cell.Connections) > 2 
          or (len(cell.Connections) > 1
          and cell.Connections[0] is not Previous)):
        for tmpcell in cell.Current.Connections:
            if (tmpcell == Previous):
                continue
            moves, priorities, Reached = recursiveCheck(tmpcell, cell, moves,
                                                        priorities, Reached)
            if Reached:
                break
        if Reached:
            moves += cell.Zone
            if cell.Zone == ZoneType.priority:
                priorities += 1
            return moves, priorities, Reached
        if not Reached:
           return moves, priorities, False 
        if cell.Zone == ZoneType.priority:
            priorities += 1
    return moves, priorities, Reached
