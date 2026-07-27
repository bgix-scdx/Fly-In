from typing import Dict, List, Any
from pygame import Vector2
from ..motor.Color import Color
from ..motor.Instances import Instance
from enum import Enum


class ZoneType(Enum):
    normal = 1
    blocked = 0
    priority = 0
    restricted = 2


class Connection():
    Maxdrones: int = -1
    Parent: "Cell"
    Target: "Cell"
    Drones: List[Any]

    def __str__(self) -> str:
        return ("\033[38;02;0;255;255mConnection:\033[0m "
                f"{self.Parent.Name} -> {self.Target.Name}")


class Cell():
    Name: str
    Position: Vector2
    MaxDrone: int = 1
    Drones: List[Any] = []
    Color3: Color
    Slot: Any = []
    Zone: ZoneType = ZoneType.normal
    Display: List[Instance] = []
    Connections: Dict[str, Connection] = {}

    def __init__(self):
        self.Display = []
        self.Connections = {}
        self.Position = Vector2(0, 0)
        self.Drones = []
        self.Slot = []

    def __str__(self):
        val = "\nConnections ->\n"
        for i in self.Connections:
            val += f"\t{i},\n"
        return f"{self.Name}: {self.Position}, {self.MaxDrone}, {self.Zone} {val}"
