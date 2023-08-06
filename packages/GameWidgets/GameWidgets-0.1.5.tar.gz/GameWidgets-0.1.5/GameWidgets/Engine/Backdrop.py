import pygame
pygame.init()


class Backdrop:
    def __init__(self, screen, img, draw_group, screen_HW=(500, 500), state=True, identifier="Backdrop"):
        self.img = img
        self.screen = screen
        self.screen_HW = screen_HW
        self.img = pygame.transform.scale(self.img, self.screen_HW)
        self.vis_state = state
        self.draw_group = draw_group
        self.iden = identifier

    def Load(self):
        self.draw_group.addObj(self.iden, self.vis_state, self.img, (0, 0))

    def State(self, state):
        self.vis_state = state
        self.draw_group.update(self.iden, self.vis_state, self.img, (0,0))

    def Destroy(self):
        self.draw_group.delete(self. iden)

    def Change(self, img, screen_HW=(500, 500)):
        self.img = img
        self.screen_HW = screen_HW
        self.img = pygame.transform.scale(self.img, self.screen_HW)

    def Update(self):
        self.draw_group.update(self.iden, self.vis_state, self.img, (0, 0))
