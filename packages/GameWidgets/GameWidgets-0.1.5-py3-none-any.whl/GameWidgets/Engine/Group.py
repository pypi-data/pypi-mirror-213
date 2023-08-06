import pygame

pygame.init()


class Group:
    def __init__(self, screen, items=[]):
        self.screen = screen
        self.items = items

    def addObj(self, identifier="", visibility=True, image=None, pos=(0, 0)):
        self.items.append([identifier, visibility, image, pos])

    def update(self, identifier="", visibility=True, image=None, pos=(0, 0)):
        self.spot = 0
        for item in self.items:
            for i in item:
                if i == identifier:
                    self.spot = self.items.index(item)

        self.items.pop(self.spot)
        self.items.insert(self.spot, [identifier, visibility, image, pos])

    def destroy(self, identifier=""):
        self.spot = 0
        for item in self.items:
            for i in item:
                if i == identifier:
                    self.spot = self.items.index(item)
        self.items.pop(self.spot)

    def draw(self):
        for i in self.items:
            if i[1]:
                self.screen.blit(i[2],i[3])
