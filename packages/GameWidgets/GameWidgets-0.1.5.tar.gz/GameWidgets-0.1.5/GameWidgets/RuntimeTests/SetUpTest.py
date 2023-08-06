print("Initializing SetUpTest...")
print("Test for GameWidgets.SetUp from GameWidgets.RuntimeTests.SetUpTest.py")
print("Current process:\n out: 0")
try:
	from GameWidgets.SetUp import *
	print("Succesfull")
except:
	print("GameWidgets.SetUp Folder has been corrupted or removed.\nExit 1 SetUpTest.py Result")
print("GameWidget.SetUp Test completed.")