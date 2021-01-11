import json
from random import randint, uniform

# opening and loading the config.json file.
with open("config.json") as fobj:
	config = json.load(fobj)

GRAPHICS = config["graphics"]

if GRAPHICS:
	from graphics import *


def loadFile(path):
	with open(path, 'r') as file:
		list = file.read().splitlines()
	file.close()
	mapList = list
	return list

# Class for holding map specs.
class MapHandle:
	width = 0
	height = 0
	grid = []
	nextID = 0
	removedID = []

	nodeWidth = 0
	nodeHeight = 0

	def createMap(lineString):
		MapHandle.width = len(list(lineString[0]))
		MapHandle.height = len(list(lineString))
		
		MapHandle.nodeWidth = config["windowParams"]["height"]/MapHandle.width
		MapHandle.nodeHeight = config["windowParams"]["width"]/MapHandle.height

		parameters = config["nodeTypes"]
		FOW = config["fogOfWar"]

		for y, line in enumerate(lineString):
			lineList = list(line)
			for x, character in enumerate(lineList):
				#Each nodes parameters are from the config file.
				if character == "B":
					border = parameters["border"]
					MapHandle.grid.append(Node([x,y], [MapHandle.nodeWidth, MapHandle.nodeHeight], "border", border["trees"], bool(border["walkable"]), border["color"], MapHandle.nextID, border["mSpeed"], FOW))
				elif character == "M":#Mountain
					mountain = parameters["mountain"]
					MapHandle.grid.append(Node([x,y], [MapHandle.nodeWidth, MapHandle.nodeHeight], "mountain", mountain["trees"], bool(mountain["walkable"]), mountain["color"], MapHandle.nextID, mountain["mSpeed"], FOW))
				elif(character == "G"):#Ground
					ground = parameters["ground"]
					MapHandle.grid.append(Node([x,y], [MapHandle.nodeWidth, MapHandle.nodeHeight], "ground", ground["trees"], bool(ground["walkable"]), ground["color"], MapHandle.nextID, ground["mSpeed"], FOW))
				elif(character == "T"):#Tree
					tree = parameters["tree"]
					MapHandle.grid.append(Node([x,y], [MapHandle.nodeWidth, MapHandle.nodeHeight], "tree", tree["trees"], bool(tree["walkable"]), tree["color"], MapHandle.nextID, tree["mSpeed"], FOW))
				elif(character == "S"):#Swamp
					swamp = parameters["swamp"]
					MapHandle.grid.append(Node([x,y], [MapHandle.nodeWidth, MapHandle.nodeHeight], "swamp", swamp["trees"], bool(swamp["walkable"]), swamp["color"], MapHandle.nextID, swamp["mSpeed"], FOW))
				elif(character == "W"):#Water
					water = parameters["water"]
					MapHandle.grid.append(Node([x,y], [MapHandle.nodeWidth, MapHandle.nodeHeight], "water", water["trees"], bool(water["walkable"]), water["color"], MapHandle.nextID, water["mSpeed"], FOW))
				MapHandle.nextID += 1

		MapHandle.placeStaticBuildings()

	def placeStaticBuildings():
		townhallPos = config["buildings"]["townHall"]["position"]
		for node in MapHandle.grid:
			if node.id == townhallPos:
				node.building = TownHall(townhallPos)

	def getRandomNode(id):
		break_counter = 0
		while True:
			ychange = randint(-5, 5)
			xchange = randint(-5, 5)
			newID = id + xchange + (ychange*MapHandle.width)
			size = len(MapHandle.grid)

			if newID in MapHandle.removedID or newID < 0 or newID > size or not MapHandle.grid[newID].isWalkable:
				MapHandle.removedID.append(newID)
				break_counter += 1
			else:
				return MapHandle.grid[newID]

			if break_counter >= 10:
				return False

	def getNeighbours(id):
		map = MapHandle.grid
		width = MapHandle.width
		neighbours = []
		if(map[id - 1].isWalkable): #Left of
			neighbours.append(id-1)
		if(map[id - width].isWalkable): #Above
			neighbours.append(id - width)
		if(map[id + 1].isWalkable): #Right of
			neighbours.append(id+1)
		if(map[id + width].isWalkable): #Below
			neighbours.append(id + width)
		return neighbours

	def searchForPath(start, end):
		return BreadthFirst(start, end)

# Class for holding data of individual squares.
class Node:
	isTree = False
	isWalkable = False
	moveSpeed = 0
	color = ""
	id = 0
	g_cost = 0
	h_cost = 0
	x = None
	y = None
	trees = []
	building = None
	reseredTrees = 0
		
	width = 0
	heigth = 0
	position = []
	shape = None

	def __init__(self, pos, size, type, tree, walkable, color, id, speed, FOW):
		self.setPos(pos, size) # HAS TO BE CENTER OF NODE
		self.type = type
		self.isTree = tree
		self.isWalkable = walkable
		self.color = color
		self.id = id
		self.moveSpeed = speed
		self.fogOfWar = FOW

		if GRAPHICS:
			self.shape = Rectangle(Point(self.x - self.size[0]/2, self.y - self.size[1]/2), Point(self.x + self.size[0]/2, self.y + self.size[1]/2))
			if (FOW and not self.type == "border"):
				self.shape.setFill('gray50')
			else:
				self.shape.setFill(self.color)

			self.shape.draw(WindowHandle.window)

	def addTrees(self):
		for x in range(0, 5):
			pos = [uniform(self.x*self.width, (self.x+1)*self.width), uniform(self.y*self.heigth, (self.y+1)*self.heigth)]
			self.trees.append(Tree(self, pos))

	def setPos(self, pos, size):
		self.x			= pos[0] * size[0] + size[0]/2
		self.y			= pos[1] * size[1] + size[1]/2
		self.position	= [self.x, self.y] 
		self.size   = size
		self.width  = size[0]
		self.heigth = size[1]

# Class for holding info off a tree
class Tree:
	size = 4
	shape = None

	def __init__(self, node, pos):
		self.parent = node
		self.pos = pos

# Class for holding the window information and functions of the window/graphics.
class WindowHandle:

	window = None
	heightP = None
	widthP = None

	def createWindow():
		WindowHandle.heightP = config["windowParams"]["height"]
		WindowHandle.widthP = config["windowParams"]["width"]
		if GRAPHICS:
			WindowHandle.window = GraphWin('Ai test', WindowHandle.widthP, WindowHandle.heightP, False)

	def update():
		if GRAPHICS:
			WindowHandle.window.update()

from basegameentity import *