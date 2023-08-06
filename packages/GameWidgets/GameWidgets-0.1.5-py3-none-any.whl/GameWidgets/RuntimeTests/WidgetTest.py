print("Initializing WidgetTest...")
print("Test for GameWidgets.Widgets from GameWidgets.RuntimeTests.WidgetTest.py")
print("Current process:\n out: 0")
try:
	from GameWidgets.Widgets import *
	print("Succesfull")
except:
	print("GameWidgets.Widgets Folder has been corrupted or removed.\nExit 1 WidgetTest.py Result")
print("GameWidget.Widget Test completed.")