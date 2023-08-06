import pygame
pygame.init()
class Button:
    def __init__(self):
        self.X = 0
        self.CIRCLE = 1
        self.SQUARE = 2
        self.TRIANGLE = 3
        self.OPTIONS = 6
        self.SHARE = 4
        self.PS = 5
        self.UP = 11
        self.DOWN = 12
        self.LEFT = 13
        self.RIGHT = 13
        self.PAD = 15
        self.L1 = 9
        self.R1 = 10
        self.joysticks = {}
        self.AllBtn = {"X":0,"CIRCLE":1,"SQUARE":2,"TRIANGLE":3,
        "OPTIONS":6,"SHARE":6,"PS":5,"UP":11,"DOWN":12,"LEFT":13,"RIGHT":13,
        "PAD":15,"L1":9,"R1":10}
        self.ButtonPressed = None
    def SearchController(self):
        for e in pygame.event.get():
            if e.type == pygame.JOYDEVICEADDED:
                joy = pygame.joystick.Joystick(e.device_index)
                self.joysticks[joy.get_instance_id()] = joy
                self.joy = joy
                return ("Connected", joy.get_instance_id())
    def CheckButton(self):
        for joystick in self.joysticks.values():
            buttons = joystick.get_numbuttons()

            for i in range(buttons):
                button = joystick.get_button(i)
                if i==0:
                	if button == 1:
                		return "yay"
                		break
        
                    

            
button = Button()
iden = button.SearchController()
print(iden)
while True:
    clicked = button.CheckButton()

    print(clicked)
