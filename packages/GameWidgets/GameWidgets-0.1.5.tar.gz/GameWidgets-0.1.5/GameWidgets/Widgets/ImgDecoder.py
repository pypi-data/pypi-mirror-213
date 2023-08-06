import pygame
pygame.init()

class PPM:
    def __init__(self,display,PPMFile=''):
        self.ppm=PPMFile
        self.display=display
    def Decode(self):
        file=open('All_Textures.ppm','r').readlines()
        LPC=[]
        CPC=[]
        counter=0
        for item in file:
            counter+=1
            if counter!=4:
                h=item.split(',')
                CPC.append(h[0])
            if counter==4:
                LPC.append(CPC)
                counter=0
                CPC=[]
        R=0
        G=0
        B=0
        counter=0
        pixilX=0
        pixilY=0
        maxX=self.display.get_width()
        maxY=self.display.get_height()
        fullset=()
        for pixilCombo in LPC:
            for PixilColor in pixilCombo:
                if counter==2:
                    R=int(PixilColor)
                if counter==3:
                    G=int(PixilColor)
                if counter==4:
                    B=int(PixilColor)
                if counter==5:
                    fullset=(R,G,B)
                    pygame.draw.rect(self.display,fullset,pygame.Rect(pixilX,pixilY,1,1))
                    if pixilX==maxX:
                        if pixilY==maxY:
                            break
                        pixilY+=1
                        pixilX=0
                        
                    pixilX+=1
                    fullset=()
                    counter=0
                    R=0
                    G=0
                    B=0
                    
                counter+=1
            break
        