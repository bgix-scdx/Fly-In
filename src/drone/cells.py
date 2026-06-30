from typing import Dict, List, Any
from pygame import Vector2
from ..motor.Color import Color
from ..motor.Instances import Instance
from enum import Enum


class ZoneType(Enum):
    normal = 1
    blocked = 0
    priority = 1
    restricted = 2


class Cell():
    Name: str
    Position: Vector2
    MaxDrone: int = 1
    Drones: List[Any] = []
    Color3: Color
    Slot: Any
    Zone: ZoneType = ZoneType.normal
    Display: List[Instance] = []
    Connections: Dict[str, "Cell"] = {}

    def __init__(self):
        self.Display = []
        self.Connections = {}
        self.Drones = []

    def __str__(self):
        val = "\nConnections ->\n"
        for i in self.Connections:
            val += f"\t{i},\n"
        return f"{self.Name}: {self.Position}, {self.MaxDrone}, {self.Zone} {val}"
