import pygame
pygame.init()
class Text:
    def __init__(self,Screen,Font='freesansbold',Hint='Type Here...',Width=100,Height=40,Pos=(5,5),Disarmed_FG=(0,0,0),Active_FG=(255,255,255),Outline_Color=(0,0,0)):
        self.font=pygame.font.SysFont(Font,Height)
        self.active=False
        self.val=Hint
        self.screen=Screen
        self.width=Width
        self.pos=Pos
        self.a=Active_FG
        self.d=Disarmed_FG
        self.bg=Outline_Color
    def Update(self):
        if self.active:
            text=self.font.render(str(self.val),(255,0,0),self.a)
        else:
            text=self.font.render(str(self.val),(255,255,255),self.d)
        self.screen.fill((0,150,150))
        self.screen.blit(text,(self.pos[0]+5,self.pos[1]+5))
        self.rect=text.get_rect(topleft=self.pos)
        rect1=self.rect.copy()
        if self.rect.width<self.width:
            rect1.width=self.width
            rect1.height+=10
            rect1.topleft=self.pos
            self.rect.width+=self.width
        else:
            rect1.width+=10
            rect1.height+=10
            rect1.topleft=self.pos
        pygame.draw.rect(self.screen,self.bg,rect1,2)
    def Check(self,e,Mouse_Pos_X=0,Mouse_Pos_Y=0):
        if e.type==pygame.KEYDOWN:
            if self.active:
                if e.key==pygame.K_BACKSPACE:
                    self.val = self.val[:-1]
                else:
                    if e.key!=pygame.K_RETURN:
                        if e.key!=pygame.K_TAB:
                            self.val=self.val+e.unicode
                        else:
                            pass
                    else:
                        pass
        if e.type==pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(Mouse_Pos_X,Mouse_Pos_Y):
                self.active=True
            else:
                self.active=False
    def Return_Value(self):
        return self.val