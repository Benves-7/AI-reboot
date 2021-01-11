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
	centerPoint = None
	charcoal = 0
	trees = 0
	ironOre = 0
	ironBars = 0
	shape = None

	def __init__(self, nodeId):
		TownHall.nodeId = nodeId
		node = MapHandle.grid[nodeId]
		TownHall.position = node.position.copy() # Center
		pos = TownHall.position
		size = [node.size[0]/10*8/2, node.size[1]/10*8/2]

		TownHall.shape = Rectangle(Point(pos[0]-size[0], pos[1]-size[1]), Point(pos[0]+size[0], pos[1]+size[1]))
		TownHall.shape.setFill("orange")
		TownHall.shape.draw(WindowHandle.window)

from config import *
from basegameentity import *