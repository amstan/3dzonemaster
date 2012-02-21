#!/usr/bin/env python2
import serial
import collections

class Point(collections.namedtuple('Point', ['x', 'y', 'z'])):
	def __str__(self):
		return "x=%s\ty=%s\tz=%s\t" % self
	
	def __add__(self,other):
		return Point(*map(lambda x,y: x+y, self, other))
	
	def __sub__(self,other):
		return Point(*map(lambda x,y: x-y, self, other))
	
	def __mul__(self,k):
		return Point(*map(lambda x: x*k, self))

BUTTONMASK={
	"trigger": 0x0000000002,
	"center":  0x0000000040,
	"up":      0x0000000010,
	"down":    0x0000000020,
	"left":    0x0000000004,
	"right":   0x0000000008,
	"1":       0x1000000000,
	"2":       0x0000000001,
	"3":       0x2000000000
}
STARTBYTE  =   0x80
DIRMASK = Point(
           x = 0x0100000000,
           y = 0X0200000000,
           z = 0x0400000000
)
POSMASK = Point(
           x = 0x00FF000000,
           y = 0X0000FF0000,
           z = 0x000000FF00
)

def outputcallback(pos,buttons):
	print pos,
	for button,active in buttons.items():
		if active:
			print button,
	print

class ZoneMaster(object):
	def __init__(self,port="/dev/ttyS0",callback=outputcallback,supressExceptions=False):
		self._s=serial.Serial(port,9600)
		self.callback=callback
		self.supressExceptions=supressExceptions
		
		self.buttons={}
		for buttonname in BUTTONMASK:
			self.buttons[buttonname]=False
		self.pos=Point(0,0,0)
	
	def newmessage(self,buf):
		for button,mask in BUTTONMASK.items():
			self.buttons[button]=(buf&mask)!=0
		
		def normalizepos(coord,d):
			if d:
				coord-=128
			return coord
		rawpos=Point(*((buf&coord)/(coord/0xFF) for coord in POSMASK))
		dir=Point(*((buf&coord)/coord for coord in DIRMASK))
		self.pos=Point(*map(normalizepos,rawpos,dir))
		
		try:
			self.callback(self.pos,self.buttons)
		except Exception as e:
			if not self.supressExceptions:
				raise
			else:
				print "Exception in callback: %r" % e
	
	def run(self):
		buf=[]
		while 1:
			byte=ord(self._s.read(1))
			if byte&STARTBYTE:
				buf=reduce(lambda x,y: x*256+y,buf)
				self.newmessage(buf)
				buf=[]
			buf.append(byte)

if __name__=="__main__":
	driver=ZoneMaster()
	driver.run()