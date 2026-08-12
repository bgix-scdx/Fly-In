from typing import Dict, List, Any
from pygame import Vector2
from ..motor.Color import Color  # type: ignore[misc]
from ..motor.Instances import Instance  # type: ignore[misc]
from enum import Enum


class ZoneType(Enum):
    normal = 1
    blocked = 0
    priority = 3
    restricted = 2


class Connection():
    Maxdrones: int = -1
    Parent: "Cell"
    Target: "Cell"
    Drones: List[Any]

    def __str__(self) -> str:
        return ("\033[38;02;0;255;255mConnection:\033[0m "
                f"{self.Parent.Name} -> {self.Target.Name}")

    def isOk(self) -> bool:
        if self.Maxdrones <= len(self.Drones):
            return False
        return True

    def Insert(self, cell: "Cell") -> None:
        self.Drones.append(cell)

    def Remove(self, cell: "Cell") -> None:
        if cell not in self.Drones:
            print("\033[38;2;125;255m -> Tryed to remove a cell.\033[0m")
            return
        self.Drones.remove(cell)


class Cell():
    Name: str
    Position: Vector2
    MaxDrone: int = 1
    Drones: List[Any] = []
    Color3: Color
    Slot: Any = []
    Zone: ZoneType = ZoneType.normal
    Display: List[Instance] = []
    Queue: List[Any] = []
    Connections: Dict[str, Connection] = {}

    def __init__(self) -> None:
        self.Display = []
        self.Connections = {}
        self.Position = Vector2(0, 0)
        self.Drones = []
        self.Slot = []
        self.Queue

    def __str__(self) -> str:
        val = "\nConnections ->\n"
        for i in self.Connections:
            val += f"\t{i},\n"
        return (f"{self.Name}: {self.Position},"
                f"{self.MaxDrone}, {self.Zone} {val}")

    def Insert(self, drone: Any) -> None:
        try:
            self.Queue.remove(self)
        except ValueError:
            pass
        try:
            self.Drones.index(drone)
        except ValueError:
            self.Drones.append(drone)

    def Remove(self, drone: Any) -> None:
        if drone not in self.Drones:
            print("Tryed to remove cell that is not stored.")
            return
        self.Drones.remove(drone)

    def isOk(self) -> bool:
        if len(self.Drones) >= self.MaxDrone:
            return False
        return True
