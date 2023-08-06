# Get all essential Files
from GameWidgets.Widgets import Colors, Clock, Btn,Cursor
from GameWidgets.SetUp import ScreenCommands
from GameWidgets.GameWidgets.ScreenSlide import Slide
# Pygame is required
import pygame

# You always have to run the init of pygame
pygame.init()
# Here is a Demo of the Color Widget, it contains RGB codes of 155 colors
White = Colors.white
# Demo of Clock widget
clock = Clock.Clock()
# Demo of the ScreenCommand SetUp to make a window
manager = ScreenCommands.Screen(Resizable=True)
# Assigning screen
screen = manager.Return()
# Registering The screen to the class
manager.Register_Master(screen)
# ScreenSlide Demo which can be used in games for cut scenes.
slide = Slide(screen, (150, 150, 150), x=-500, y=0)
run = True
# Different types of buttons
Button = Btn.Active_Btn(screen, (White, (0, 0, 255), (255, 0, 0), (0, 255, 0)))
Button2 = Btn.Normal_Btn(screen, fgcolor=(0, 255, 255), xy=(0, 50), size=50, Thickness=0, Outline=(0, 0, 255))
# Demo of cursor
cursor = Cursor.Rect_Cursor(screen, (0, 0, 255), Width=10, Height=10)
while run:
    # Uses the Tick to run the clock and the Fill to fill the screen
    clock.Tick()
    manager.Fill()
    # Drawing the two different types of buttons
    Button.Draw()
    Button2.Draw()
    cursor.Draw()
    # Draw the Screen slide
    slide.Draw()
    # Update display
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        # Detect for buttons, returns True if clicked
        a = Button.Detect(pygame.mouse.get_pos(), e)
        b = Button2.Detect(pygame.mouse.get_pos(), e)
    # Update pos of screen slide
    slide.Update()
# Quit pygame if exited
pygame.quit()
