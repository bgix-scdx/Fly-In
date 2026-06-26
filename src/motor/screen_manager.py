import pygame
from math import floor
from .Scene import Scene
from threading import Thread


class screen():
    def __init__(self, resolution: int):
        print("Starting Screen...")
        self.res = resolution
        self.running = True
        self.TPS = 120
        self.fullscreen = False
        self.speed = pygame.Vector2(0, 0)
        self.maxspeed = 10
        self.scenes = []
        self.current = self.GetScene("Default")
        self.thread = Thread(target=self.ScreenLoop)
        self.thread.start()

    def ScreenLoop(self) -> None:
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
            if self.current.Freecam:
                font = pygame.font.SysFont("impact", 25)
                text = font.render(f"x: {self.current.CameraPosition.x},"
                                   f"y: {self.current.CameraPosition.y}",
                                   True, (255, 255, 255))
                self.screen.blit(text, [0, 0])
            for obj in self.current.Objects.values():
                obj.execute(self)
            pygame.display.flip()
            self.clock.tick(self.TPS)
        pygame.quit()

    def GetScene(self, name: str) -> Scene:
        """Look for a scene, if not found it will create one."""
        for i in self.scenes:
            if i.Name is name:
                return i
        newscene = Scene(name)
        self.scenes.append(newscene)
        return newscene

    def KeyHeld(self) -> None:
        if not self.current.Freecam:
            self.speed = pygame.Vector2(0, 0)
            return
        keys = pygame.key.get_pressed()
        steps = 10
        changed = [0, 0]
        if keys[pygame.K_w]:
            changed[1] = 1
            if self.speed.y > -self.maxspeed:
                self.speed.y -= self.maxspeed / steps
        elif keys[pygame.K_s]:
            changed[1] = 1
            if self.speed.y < self.maxspeed:
                self.speed.y += self.maxspeed / steps
        if keys[pygame.K_a]:
            changed[0] = 1
            if self.speed.x > -self.maxspeed:
                self.speed.x -= self.maxspeed / steps
        elif keys[pygame.K_d]:
            changed[0] = 1
            if self.speed.x < self.maxspeed:
                self.speed.x += self.maxspeed / steps
        self.current.CameraPosition += pygame.Vector2(floor(self.speed.x),
                                                      floor(self.speed.y))
        for i, v in enumerate(self.speed):
            if changed[i] == 0:
                if self.speed[i] > -1 and self.speed[i] < 1:
                    self.speed[i] = 0
                elif self.speed[i] > 0:
                    self.speed[i] -= self.maxspeed / steps
                elif self.speed[i] < 0:
                    self.speed[i] += self.maxspeed / steps

# for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                 if event.type == pygame.MOUSEBUTTONUP:
#                     if event.button == 4:
#                         self.maxspeed += 1
#                     elif event.button == 5:
#                         if self.maxspeed > 1:
#                             self.maxspeed -= 1
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_ESCAPE and self.fullscreen:
#                         self.running = False
#                     if event.key == pygame.K_n and self.fullscreen:
#                         if self.current == self.scenes["baka"]:
#                             self.scenes["baka"]["position"] = self.center
#                             self.current = self.scenes["main"]
#                             self.center = self.current["position"]
#                         else:
#                             self.scenes["main"]["position"] = self.center
#                             self.current = self.scenes["baka"]
#                             self.center = self.current["position"]
#                     if event.key == pygame.K_TAB and not self.fullscreen:
#                         self.screen = pygame.display.set_mode((0, 0),
#                                                           pygame.FULLSCREEN)
#                         self.fullscreen = True
#                     elif event.key == pygame.K_TAB and self.fullscreen:
#                         self.screen = pygame.display.set_mode((self.res * 16,
#                                                              self.res * 10),
#                                                                pygame.SCALED)
#                         self.fullscreen = False
