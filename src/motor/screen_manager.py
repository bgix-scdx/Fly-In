import pygame
from math import floor
from .Scene import Scene
from typing import Callable, List, Any
from threading import Thread


class screen():
    '''Handle the visual sceen of Pygames'''
    def __init__(self, resolution: int, exec: Callable[[Any], Any]):
        '''Set up all default settings'''
        print("Starting Screen...")
        self.res = resolution
        self.running = True
        self.TPS = 60
        self.fullscreen = False
        self.speed = pygame.Vector2(0, 0)
        self.maxspeed = 10
        self.scenes: List[Scene] = []
        self.current: Scene = self.GetScene("Default")
        self.thread = Thread(target=exec)
        self.thread.visual = self  # type: ignore[attr-defined]
        self.thread.start()
        try:
            self.ScreenLoop()
        except KeyboardInterrupt:
            self.running = False
            raise KeyboardInterrupt

    def ScreenLoop(self) -> None:
        '''Initiate the screen loop and handle the execution'''
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0))
# pygame.FULLSCREEN)
        self.camera = pygame.Vector2(0, 0)
        self.clock = pygame.time.Clock()
        self.center = pygame.Vector2(0, 0)
        self.size = [self.screen.get_width() / 2, self.screen.get_height() / 2]
        while self.running is True:
            self.screen.fill((0, 0, 0))
            self.KeyHeld()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.fullscreen:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 4:
                        self.current.Zoom += 0.1
                    elif event.button == 5 and self.current.Zoom >= 0.1:
                        self.current.Zoom -= 0.1
            try:
                for obj in self.current.Objects.values():
                    obj.execute(self)
            except RuntimeError:
                pass
            pygame.display.flip()
            self.clock.tick(self.TPS)
        pygame.quit()

    def GetScene(self, name: str) -> Scene:
        """Look for a scene, if not found it will create one."""
        for i in self.scenes:
            if i.Name == name:
                return i
        print("Creating New Scene")
        newscene = Scene(name)
        self.scenes.append(newscene)
        return newscene

    def ChangeScene(self, scene: Scene) -> None:
        '''Change the current scene to the one sent'''
        self.current = scene

    def KeyHeld(self) -> None:
        '''Handle Keyboard Movements to move on the screen.'''
        if not self.current.Freecam:
            self.speed = pygame.Vector2(0, 0)
            return
        keys = pygame.key.get_pressed()
        steps = 10
        changed = [0, 0]
        if keys[pygame.K_s]:
            changed[1] = 1
            if self.speed.y > -self.maxspeed:
                self.speed.y -= self.maxspeed / steps
        elif keys[pygame.K_z]:
            changed[1] = 1
            if self.speed.y < self.maxspeed:
                self.speed.y += self.maxspeed / steps
        if keys[pygame.K_d]:
            changed[0] = 1
            if self.speed.x > -self.maxspeed:
                self.speed.x -= self.maxspeed / steps
        elif keys[pygame.K_q]:
            changed[0] = 1
            if self.speed.x < self.maxspeed:
                self.speed.x += self.maxspeed / steps
        self.current.CameraPosition += pygame.Vector2(floor(
                                                            self.speed.x
                                                            * self.current.Zoom
                                                            ),
                                                      floor(self.speed.y
                                                            *
                                                            self.current.Zoom))
        for i, v in enumerate(self.speed):
            if changed[i] == 0:
                if self.speed[i] > -1 and self.speed[i] < 1:
                    self.speed[i] = 0
                elif self.speed[i] > 0:
                    self.speed[i] -= self.maxspeed / steps
                elif self.speed[i] < 0:
                    self.speed[i] += self.maxspeed / steps
