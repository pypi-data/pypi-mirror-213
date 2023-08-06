print("Complete Folder damage check?\n******Warning******\nThis test may result in low preformance and in some cases may slow down this device. This test imports all files in this package.")
try:
	from GameWidgets.GameWidgets import *
	print("GameWidgets.GameWidgets Test Succsess")
except:
	print("GameWidgets.GameWidgets has an error inside it.")
try:
	from GameWidgets.SetUp import *
	print("GameWidgets.SetUp Test Succsess")
except:
	print("GameWidgets.SetUp has an error inside it.")
try:
	from GameWidgets.Widgets import *
	print("GameWidgets.Widgets Test Succsess")
except:
	print("GameWidgets.Widgets has an error inside it.")