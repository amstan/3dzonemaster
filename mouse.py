#!/usr/bin/env python2

from driver import ZoneMaster, Point
from pymouse import PyMouse
m = PyMouse()

mousemapping={
	1: ("trigger","1"),
	2: ("3",),
	3: ("2",)
}

def mouseEmulator(pos,buttons):
	#Check for mouse clicks
	for mouse,mapping in mousemapping.items():
		state=reduce(lambda x,y: x or y,(buttons[button] for button in mapping))
		
		if state:
			m.press(m.position()[0],m.position()[1],mouse)
		else:
			m.release(m.position()[0],m.position()[1],mouse)
	
	#Move mouse when center is held
	if(buttons["center"]):
		print "Moving delta: x=%4d, y=%4d" % pos[:2]
		mx, my = m.position()
		m.move(mx+pos.x,my+pos.y)

driver=ZoneMaster(callback=mouseEmulator)
driver.run()