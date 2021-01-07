class Kiln():
	numberOfKilns = 0
	kilns = []

	def __init__(self, nodeId):
		self.nodeId = nodeId
		self.position = MapHandle.grid[nodeId].pos
		self.trees = 0
		self.charcoal = 0
		self.populated = False
		self.complete = False
		self.type = "kiln"
		Kiln.kilns.append(self)
		Kiln.numberOfKilns += 1

class Smith():
	numberOfSmiths = 0
	smiths = []

	def __init__(self, nodeId):
		self.nodeId = nodeId
		self.position = MapHandle.grid[nodeId].pos
		self.trees = 0
		self.treeCoal = 0
		self.populated = False
		self.complete = False
		self.type = "smith"
		Smith.smiths.append(self)
		Smith.numberOfSmiths += 1
	pass

class Smelter():
	numberOfSmelters = 0
	smelters = []

	def __init__(self, nodeId):
		self.nodeId = nodeId
		self.position = MapHandle.grid[nodeId].pos
		self.ironBar = 0
		self.ironOre = 0
		self.populated = False
		self.complete = False
		self.type = "smelter"
		Smelter.smelters.append(self)
		Smelter.numberOfSmelters += 1

class TrainingCamp():
	pass

class TownHall():
	nodeId = 0
	position = []
	center = []
	centerPoint = None
	charcoal = 0
	trees = 0
	ironOre = 0
	ironBars = 0
	shape = None

	def __init__(self, nodeId):
		TownHall.nodeId = nodeId
		TownHall.position = MapHandle.grid[nodeId].pos.copy()
		TownHall.center = TownHall.position.copy()
		TownHall.center[0] = (TownHall.center[0] * MapHandle.nodeWidth) + (MapHandle.nodeWidth / 2)
		TownHall.center[1] = (TownHall.center[1] * MapHandle.nodeHeight) + (MapHandle.nodeHeight / 2)
		TownHall.position[0] = TownHall.position[0] * MapHandle.nodeWidth
		TownHall.position[1] = TownHall.position[1] * MapHandle.nodeHeight
		pos = TownHall.position
		size = [MapHandle.nodeWidth/10*9, MapHandle.nodeHeight/10*9]

		TownHall.shape = Rectangle(Point(pos[0]+MapHandle.nodeWidth/10, pos[1]+MapHandle.nodeWidth/10), Point(pos[0]+MapHandle.nodeWidth/10+size[0], pos[1]+MapHandle.nodeWidth/10+size[1]))
		TownHall.shape.setFill("orange")
		TownHall.shape.draw(WindowHandle.window)
		TownHall.centerPoint = Point(TownHall.center[0], TownHall.center[1])
		TownHall.centerPoint.setFill("black")
		TownHall.centerPoint.draw(WindowHandle.window)

from config import *
from basegameentity import *