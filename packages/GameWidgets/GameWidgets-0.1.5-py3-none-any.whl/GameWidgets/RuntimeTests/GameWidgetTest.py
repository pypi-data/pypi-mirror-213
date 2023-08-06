print("Initializing GameWidgetTest...")
print("Test for GameWidgets.GameWidgets from GameWidgets.RuntimeTests.GameWidgetTest.py")
print("Current process:\n out: 0")
try:
	from GameWidgets.GameWidgets import *
	print("Succesfull")
except:
	print("GameWidgets.GameWidgets Folder has been corrupted or removed.\nExit 1 GameWidgetTest.py Result")
print("GameWidget.GameWidget Test completed.")