import pygame
import json
from pydantic import BaseModel, model_validator
from .Instances import InstanceType
from math import floor
from os import path
from typing import Any, Callable, Dict, List, Tuple

class Motor(BaseModel):
    settings: Any = {}
    tps: int = 60
    window: Any = pygame.display.set_mode((1280, 720))
    running: bool = True
    clock: Any = pygame.time.Clock()
    events: Dict[int, Tuple[Callable, Any]] = {}

    @model_validator(mode="after")
    def start(self):
        with open("src/motor/Settings/keybinds.json") as f:
            self.settings = json.load(f)
        self.events[pygame.QUIT] = [self.Stop, []]
        return self

    def VisualLoop(self):
        pygame.init()
        while self.running:
            pygame.display.flip()
            self.clock.tick(self.tps)
            for event in pygame.event.get():
                self.HandleEvent(event)
        self.Stop()

    def HandleEvent(self, event) -> None:
        if dict.get(self.events, event.type):
            self.events[event.type][0](*self.events[event.type][1])

    def Stop(self) -> None:
        self.running = False
        pygame.quit()
