from config import *
from basegameentity import *

from time import perf_counter, sleep
import threading


if __name__ == '__main__':
	WindowHandle.createWindow()						# Create the window in configured size
	MapHandle.createMap(loadFile("map.txt"))		# Create the map and place townhall

	BaseGameEntity.create(25, "w");

	while WindowHandle.window.isOpen():
		ResourceManager.Update()
		BuildingManager.Update()
		EntityManager.Update()

		UnitManager.Update()

		WindowHandle.update()