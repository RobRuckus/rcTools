import os 
import sys
import maya.cmds as mc
import maya.mel as mel 
import ctypes
from rcTools import rcMaya as rc
from main import *
from functools import partial
def delay(method,string,*args): exec(method+string) #Button Delay Function

###
ui=rc.ui('Dup')
def UI():
	ui.win()
	ui.toolBox()
	ui.tab('DUP')
	mc.rowColumnLayout('FURIROW',numberOfColumns=2,columnWidth=[(1,ui.rowWidth/2),(2,ui.rowWidth/2)])
	mc.frameLayout('CREATE',cll=0,bgc=[.0,.0,.0]);
	mc.gridLayout(numberOfColumns=5,cellWidthHeight=[28,28])
	
	mc.button(l='',c=partial(delay,'mel.eval','(toMiddle(\"max\" ,\"max\", \"max\")'))
	mc.button(l='')
	mc.button(l='Y+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'copyAmt ','("0","10","0")'))
	mc.button(l='')
	mc.button(l='')
	mc.button(l='Z+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'copyAmt ','("0","0","10")'))
	mc.button(l='X+',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'copyAmt ','("10","0","0")'))
	mc.intField('AmtField',v=5)#
	mc.button(l='X-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'copyAmt ','("-10","0","0")'))
	mc.button(l='Z-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'copyAmt ','("0","0","-10")'))
	mc.button(l='')
	mc.button(l='')
	mc.button(l='Y-',ann='Set Selected Pivot to',bgc=[.6,.6,.6],c=partial(delay,'copyAmt ','("0","-10","0")'))
	mc.button(l='')
	mc.button(l='')
	mc.setParent('..')
	mc.setParent('..')
	
def copyAmt(x,y,z):
	print x
	print y
	print z
	obj=mc.duplicate(rr=1)
	mc.move(x,y,z,obj,r=1)
	for each in range(0,mc.intField('AmtField',q=1,v=1)-1):
		mc.duplicate(rr=1,st=1)
	#print direction
	
if __name__== 'rcDup' :
	ui.win()
	ui.toolBox()
	ui.tab('DUP')
	UI()