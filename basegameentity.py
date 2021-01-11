from config import *

class BaseGameUnit:
	entities = []

	def __init__(self, ID):
		self.ID = ID

		BaseGameUnit.entities.append(self)

		self.size = [MapHandle.nodeWidth/3, MapHandle.nodeHeight/3]
		self.position = TownHall.position.copy()
		self.lastPosition = TownHall.position.copy()

		self.shape = Oval(Point(self.position[0]-self.size[0], self.position[1]-self.size[1]), Point(self.position[0]+self.size[0], self.position[1]+self.size[1]))

		self.nodeId = TownHall.nodeId
		self.path = []

	def move(self):
		try:
			node = MapHandle.grid[self.path[0]]
			distX = (self.position[0] - node.position[0])
			distY = (self.position[1] - node.position[1])
		except:
			return False

		angle = atan2(distY, distX)

		dxangle = -cos(angle)
		dyangle = -sin(angle)

		dx = dxangle * node.moveSpeed
		dy = dyangle * node.moveSpeed

		if abs(dx) > abs(distX):
			dx = -distX
		if abs(dy) > abs(distY):
			dy = -distY

		self.position[0] += dx
		self.position[1] += dy

		self.shape.move(dx,dy)

		return self.position[0] == node.position[0] and self.position[1] == node.position[1]

	def getMove(self):
		dx = -(self.lastPosition[0] - self.position[0])
		dy = -(self.lastPosition[1] - self.position[1])

		self.lastPosition[0] = self.position[0]
		self.lastPosition[0] = self.position[1]

		return [dx,dy]

	def Update(self):
		self.currentState.Execute(self)

	def changeState(self, state):
		self.currentState.Exit(self)
		self.currentState = state
		self.currentState.Enter(self)


class Entity(BaseGameUnit):

	def __init__(self, id, type, profession = ""):
		BaseGameUnit.__init__(self, id)
		self.type = type
		self.profession = profession

		self.startTime = None
		self.size = [MapHandle.nodeWidth/3, MapHandle.nodeHeight/3]

		self.carrying = [] # tree, iron ingot, sword etc.

		self.destroyTrees = []  # NEEDED? (TODO)

		self.position = TownHall.center.copy()
		self.lastPosition = TownHall.center.copy()

		self.shape = Oval(Point(self.position[0]-self.size[0], self.position[1]-self.size[1]), Point(self.position[0]+self.size[0]+1, self.position[1]+self.size[1]+1))
		self.shape.setFill("yellow")
		self.shape.draw(WindowHandle.window)

		self.nodeId = TownHall.nodeId
		self.path = []

		if(type == "explorer"):
			self.m_currentState = state.EStart()
		elif(type == "worker"):
			self.m_currentState = state.WStart()
			self.trees = 0
		elif(type == "craftsman"):
			self.m_currentState = state.CStart()


	#Used for upgrading an entity
	def changeType(self, type, profession = ""):
		if(type == "explorer"):
			self.type = "explorer"
			self.changeState(state.WUpgradeToExplorer())
		elif(type == "craftsman"):
			self.type = "craftsman"
			self.profession = profession
			self.working = False
			self.changeState(state.WUpgradeToCraftsman())

	def Update(self):
		self.m_currentState.Execute(self) #execute current state execute method

	def changeLocation(self, location):
		self.m_currentLocation = location

	def changeState(self, state):
		self.m_currentState.Exit(self)
		self.m_currentState = state
		self.m_currentState.Enter(self)

	def recvMessage(self, message):
		self.m_currentState.messageRecvd(message)

	def getMove(self):
		
		dx = -(self.lastPosition[0] - self.position[0])
		dy = -(self.lastPosition[1] - self.position[1])

		self.lastPosition[0] = self.position[0]
		self.lastPosition[1] = self.position[1]

		return [dx,dy]

		#Follows a path and returns true when it has reached the next point
	def MoveTo(self):
		try:
			node = self.map[self.path[0]]
			distX = (self.position[0] - node.pos[0])
			distY = (self.position[1] - node.pos[1])
		except:
			return False

		angle = atan2(distY, distX)

		dxangle = -cos(angle)
		dyangle = -sin(angle)

		dx = -cos(angle) * node.moveSpeed
		dy = -sin(angle) * node.moveSpeed

		if abs(dx) > abs(distX):
			dx = -distX
		if abs(dy) > abs(distY):
			dy = -distY

		self.position[0] += dx
		self.position[1] += dy

		return self.position[0] == node.pos[0] and self.position[1] == node.pos[1]

	#This is called when an explorer goes to a new now and it removes the fog of war
	def exploreCloseNodes(self):
		neighbours = []
		
		width = self.mapHandle.width
		localMap = self.mapHandle.grid
		id = self.nodeId
		checklist = [id - 1 - width, id - width, id + 1 - width, id - 1, id, id + 1, id - 1 + width, id + width, id + 1 + width]

		#Checks if the node is aleady explored to avoid redrawing trees
		for nodeID in checklist:
			tile = localMap[nodeID]
			if(tile.fogOfWar):
				tile.fogOfWar = False
				Window.exploredID.append(nodeID)

class Worker(BaseGameUnit):

	def __init__(self, id):
		BaseGameUnit.__init__(self, id)
		self.type = "worker"
		self.startTime = 0

		self.carrying = []

		self.shape.setFill("yellow")
		self.shape.draw(WindowHandle.window)

		self.currentState = state.WStart()
		self.trees = 0 # TODO (NEEDED?)

	def upgrade(self, type):
		i = self.ID
		if type == "e":
			BaseGameUnit.entities[i] = Explorer(i)
		elif type == "c":
			BaseGameUnit.entities[i] = Craftsman(i)


class Craftsman(BaseGameUnit):
	def __init__(self, id):
		BaseGameUnit.__init__(self, id)
		self.type = "craftsman"
		self.startTime = 0

		self.carrying = []

		self.shape.setFill("blue")
		self.shape.draw(WindowHandle.window)

		self.currentState = state.CStart()

class Explorer(BaseGameUnit):
	def __init__(self, id):
		BaseGameUnit.__init__(self, id)
		self.type = "explorer"
		self.startTime = 0
		
		self.shape.setFill("red")
		self.shape.draw(WindowHandle.window)

		self.currentState = state.EStart()

	def exploreCloseNodes(self):
		neighbours = []

		width = MapHandle.width
		localMap = MapHandle.grid
		id = self.nodeId
		checklist = [
			id - 1 - width, id - width, id + 1 - width,
			id - 1,			id,			id + 1,
			id - 1 + width, id + width, id + 1 + width ]

		for nodeId in checklist:
			node = localMap[nodeId]
			if node.fogOfWar:
				node.shape.setBorder("")
				node.fogOfWar = False

	def findExploration(self):
		endNode = MapHandle.getRandomNode(self.nodeId)
		if endNode:
			return MapHandle.searchForPath(self.nodeId, endNode.id)
		else:
			return False
				



import state
from math import *
from graphics import *
from managers import *
from config import *
from buildings import *