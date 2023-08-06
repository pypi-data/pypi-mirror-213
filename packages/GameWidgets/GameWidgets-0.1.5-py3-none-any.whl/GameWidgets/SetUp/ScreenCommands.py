import pygame
pygame.init()
class Screen:
    def __init__(self,**kwarg):
        self.Color=(0,0,0)
        self.Xsize=500
        self.Ysize=500
        self.Icon=''
        self.Title='    Pygame Window'
        self.resizable = False
        for key,val in kwarg.items():
            if key=='Color':
                self.Color=val
            elif key=='Xsize':
                self.Xsize=val
            elif key=='Ysize':
                self.Ysize=val
            elif key=='Icon':
                self.Icon=val
            elif key=='Title':
                self.Title=val
            elif key=='Resizable':
                self.resizable = True
            else:
                print(f'Value Error! No Attribute to {key}')
                quit()
        self.Master=None
        if self.Icon=='':
            self.img=pygame.Surface((100,100))
            self.img.fill((0,0,0))
        else:
            self.img=pygame.image.load(self.Icon)
        
    def Return(self):
        if self.resizable!=True:
            return pygame.display.set_mode((self.Xsize,self.Ysize))
        else:
            return pygame.display.set_mode((self.Xsize,self.Ysize),pygame.RESIZABLE)
    def Register_Master(self,master):
        self.Master=master
    def Return_HW(self,Type='List'):
        if Type=='List':
            return [self.Xsize,self.Ysize]
        if Type=='Dictionary':
            return {'Height':self.Xsize,'Width':self.Ysize}
        if Type=='Tuple':
            return (self.Xsize,self.Ysize)
    def Fill(self):
        self.Master.fill(self.Color)
    def Set_Icon(self):
        pygame.display.set_icon(self.img)
        pygame.display.set_caption(self.Title)
    