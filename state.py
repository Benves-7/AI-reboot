class State:
	def messageRecvd(message):#Check what the message contains and act accordingly
		#Type 1: request, Type 2: ack, Type 3: go now, Type 4: leave

		if(message['type'] == 1):
			pass
		elif(message['type'] == 2): 
			pass
		elif(message['type'] == 3):
			pass
		elif(message['type'] == 4):
			pass
	def Enter(self):
		assert 0, "Something went very wrong"
	def Execute(self):
		assert 0, "Something went very wrong"
	def Exit(self):
		assert 0, "Something went very wrong"

	#Used for checking if a worker is in a certain state, equality check
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.__dict__ == other.__dict__
	def __ne__(self, other):
		return not self.__eq__(other)

class Idle(State):
	def Enter(self, unit):
		print(str(unit.ID) + " is idle.")
		pass
	def Execute(self, unit):
		pass
	def Exit(self, unit):
		pass
##======================================================
#Craftsman states
class CStart(State):
	def Enter(self, craftsman):
		print(str(unit.ID) + " now a craftsman")
	def Execute(self, craftsman):
		pass
	def Exit(self, craftsman):
		pass
class CMoveToKiln(State):
	def Enter(self, craftsman):
		pass
	def Execute(self, craftsman):
		pass
	def Exit(self, craftsman):
		pass
class CMoveToSmith(State):
	def Enter(self, builder):
		pass
	def Execute(self, builder):
		pass
	def Exit(self, builder):
		pass
class CWorking(State):
	def Enter(self, worker):
		pass
	def Execute(self, worker):
		pass
	def Exit(self, worker):
		pass

##======================================================
#Worker states
class WStart(State):
	def Enter(self, worker):
		pass
	def Execute(self, worker):
		worker.changeState(Idle())
	def Exit(self, worker):
		pass

class WUpgradeToExplorer(State):

	def Enter(unit):
		print(str(unit.ID) + ": upgrading to explorer.")
		unit.startTime = perf_counter()
		unit.doneWhen = config["upgradeTimes"]["explorer"]
	
	def Execute(unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			unit.upgrade("e")
			return

	def Exit(unit):
		pass

class WUpgradeToCraftsman(State):
	def Enter(self, unit):
		print(str(unit.ID) + " upgrading to craftsman.")
		unit.startTime = perf_counter()
		unit.doneWhen = config["upgradeTimes"]["explorer"]
	def Execute(self, unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			unit.changeState(CStart())
	def Exit(self, unit):
		 pass

class WCuttingTree(State):
	def Enter(self, unit):
		unit.startTime = perf_counter()
		unit.doneWhen = config["workTime"]["woodChop"]

	def Execute(self, unit):
		if perf_counter() - unit.startTime > unit.doneWhen:
			unit.destroyTrees.append(unit.endNode.trees.pop())
			unit.changeState(WMoveBackToTownHall())
			
	def Exit(self, unit):
		pass

class WMoveBackToTownHall(State):
	def Enter(self, unit):
		unit.path = unit.mapHandle.findHome(unit)
		if unit.path:
			unit.path.pop(0)
			unit.tryagain = False
		else:
			unit.tryagain = True

	def Execute(self, unit):
		if not unit.tryagain:
			if len(unit.path) < 1:	# never enters..
				TownHall.trees += 1
				print(TownHall.trees)
				unit.changeState(Idle())
			elif unit.MoveTo():
				unit.nodeId = unit.path[0]
				unit.path.pop(0)
				unit.exploreCloseNodes()
		else:
			unit.changeState(WMoveBackToTownHall())

	def Exit(self, unit):
		pass

class WGoToTree(State):
	def Enter(self, unit):
		unit.path = unit.mapHandle.findTree(unit)
		if unit.path:
			unit.path.pop(0)
		else:
			unit.changeState(Idle())

	def Execute(self, unit):
		if len(unit.path) < 1:
			unit.changeState(WCuttingTree())
		elif unit.MoveTo():
			unit.nodeId = unit.path[0]
			unit.path.pop(0)
			unit.exploreCloseNodes()

	def Exit(self, unit):
		pass

##======================================================
#Builder states
class BStart(State):
	def Enter(self, builder):
		pass

	def Execute(self, builder):
		pass

	def Exit(self, builder):
		pass

class BBuildBuilding(State):
	def Enter(self, builder):
		pass

	def Execute(self, builder):
		pass

	def Exit(self, builder):
		pass

class BMoveBackToTownHall(State):
	def Enter(self, builder):
		pass

	def Execute(self, builder):
		pass

	def Exit(self, Entity):
		return

##======================================================
#Explorer states
class EStart(State):
	def Enter(self, unit):
		pass

	def Execute(self, unit):
		unit.changeState(EExploring())

	def Exit(self, unit):
		pass

class EExploring(State):
	def Enter(self, unit):
		unit.path = unit.findExploration()
		if unit.path:
			unit.path.pop(0)
		else:
			unit.changeState(EWaiting())

	def Execute(self, unit):
		if len(unit.path) < 1:
			unit.changeState(EWaiting())
		elif unit.move():
			unit.nodeId = unit.path[0]
			unit.path.pop(0)
			unit.exploreCloseNodes()
			
	def Exit(self, unit):
		pass

class EWaiting(State):
	def Enter(self, unit):
		pass

	def Execute(self, unit):
		unit.changeState(EExploring())

	def Exit(self, unit):
		pass



from basegameentity import *
from messaging import *
from pathfinding import *
from managers import *
from config import *
from graphics import *
from time import perf_counter