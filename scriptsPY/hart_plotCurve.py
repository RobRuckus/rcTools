''' 
	PlotCurves v1.26

	Christian Hart. 
	Hartwork Studio
	www.hartwork.com.au

	Draws a curve from the position of any group, object or vertex selected as it travels along it's animation.
	Allows multiple selection.
	Good for modeling unique things like springs or wires by using animation to design the shape. 
	Or good when needing a motion trail that can have things attached to the path.

	Installation:	Put the script in your scripts directory and create a python shelf button with the following two lines.

					from hart_plotCurve import *
					plotCurve()
'''
import maya.cmds as mc
import random
from functools import partial
#
def plotWithCurve(startFrame, endFrame, step, *args):
	#
	startFrame = mc.floatField(startFrame, query=True, value=True)
	endFrame = mc.floatField(endFrame, query=True, value=True)
	step = mc.floatField(step, query=True, value=True)
	#
	selected = mc.ls(sl=True, flatten=True) 
	if not selected:
		mc.error(" Nothing Selected ")
	# empty dictionary for object name plus curve name
	curveDetails = []
	# remember current frame
	userTime = currentFrame = mc.currentTime(query=True)
	# set current frame to the startFrame.
	currentFrame = mc.currentTime(startFrame, update=True)
	# create a group to store the curves in.
	group = mc.group(name="plotCurves", empty=True)
	# create the initial curves
	for item in selected:
		try:
			POS = mc.xform(item, query=True, worldSpace=True, translation=True)
			# Vertex or object
			curve = mc.curve(name=item+"_plotCurve", point=POS)
			# set the curve yellow
			mc.setAttr(curve+".ove", 1)
			color = random.randint(0, 31)
			mc.setAttr(curve+".ovc", color)
			# append to dictionary
			curveDetails.append({item:curve})
			mc.parent(curve, group)
		except:
			mc.error("This selection is currently unsupported.")
	#
	# Report number of curves to be made.
	numOfCurves = len(curveDetails)
	print "Creating {n} curve/s".format(n=numOfCurves)
	#
	# update the curves with a cv for each frame till the end frame is reached.
	while currentFrame < endFrame:
		# step frame
		frm = currentFrame+step
		currentFrame = mc.currentTime(frm, update=True)
		# Create a cv for each curve for the current frame.
		for curveDict in curveDetails:
			item = curveDict.keys()[0]
			curve = curveDict.values()[0]
			POS = mc.xform(item, query=True, worldSpace=True, translation=True)
			mc.curve("{group}|{curve}".format(group=group, curve=curve), append=True, point=POS)
		# deselect so that nothing is selected while curves are made.
		mc.select(deselect=True)
	# reset frame back to what it was before creating curves.
	mc.currentTime(userTime, update=True)
	print "Done"

def showInfo():
	print "info"
	WIN_info = "About_PlotCurve"
	if mc.window(WIN_info, exists=True):
		mc.deleteUI(WIN_info, window=True)
	win = mc.window(WIN_info, sizeable=False, width=300, height=100, minimizeButton=False, maximizeButton=False)
	mc.rowColumnLayout(numberOfColumns=3)
	mc.separator(width=20, style='none')
	mc.rowColumnLayout(numberOfColumns=1)
	mc.separator(height=20, style='none')
	mc.text("About")
	mc.separator(height=20, style="in")
	mc.text("Plot Curve 1.26 - Created by Christian Hart 2014\n") 
	mc.text("For more information and to get more functionality with PlotCurves Pro\nhead to the hartwork website.\n", align="left", font="boldLabelFont")
	mc.button(label=" Go to Website ", command="mc.showHelp('http://www.hartwork.com.au/studio/tools', absolute=True)")
	mc.separator(height=20, style='none')
	mc.setParent("..")
	mc.separator(width=20, style='none')
	mc.setParent("..")
	mc.showWindow(WIN_info)

def setFrame(op, startFrame, endFrame, *args):
	if op == "reset":
		findStart = mc.playbackOptions(query=True, minTime=True)
		findEnd = mc.playbackOptions(query=True, maxTime=True)
		mc.floatField(startFrame, value=findStart, edit=True, precision=2)
		mc.floatField(endFrame, value=findEnd, edit=True, precision=2)
	elif op == "getStart":
		current = mc.currentTime(query=True)
		mc.floatField(startFrame, value=current, edit=True, precision=2)
	elif op == "getEnd":
		current = mc.currentTime(query=True)
		mc.floatField(endFrame, value=current, edit=True, precision=2)
	elif op == "gotoStart":
		start = mc.floatField(startFrame, query=True, value=True)
		mc.currentTime(start, edit=True)
	elif op == "gotoEnd":
		end = mc.floatField(endFrame, query=True, value=True)
		mc.currentTime(end, edit=True)
#
# UI
#
def plotCurve():
	WIN_plot = "Plot_Curves"
	#
	if mc.window(WIN_plot, exists=True):
		mc.deleteUI(WIN_plot, window=True)
	#
	titleBG = (0.2,0.2,0.2)
	mc.window(WIN_plot, sizeable=False)
	#
	mc.scrollLayout(childResizable=True)
	mc.rowColumnLayout( numberOfRows=1, bgc=titleBG)
	mc.separator(width=20, height= 40, style="none")
	mc.text(" Plot Curves on animated objects or its Vertices     ")
	mc.iconTextButton(width=40, image="SP_MessageBoxInformation.png", command="showInfo()", annotation="Information, Help and Examples")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1)
	mc.separator(height=10, style="none")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1)
	mc.separator(width=20, style="none")
	mc.text("Start Frame ")
	findStart = mc.playbackOptions(query=True, minTime=True)
	startFrame = mc.floatField(value=findStart, precision=2)
	mc.separator(width=10, style="none")
	mc.text("End Frame ")
	findEnd = mc.playbackOptions(query=True, maxTime=True)
	endFrame = mc.floatField(value=findEnd, precision=2)
	resetBut = mc.button(label="Reset", command=partial(setFrame, 'reset', startFrame, endFrame), annotation="Reset start and end frame to timeslider min, max.")
	mc.separator(width=20, style="none")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1)
	mc.separator(width=80, style="none")
	setStartBut = mc.button(label="Set", command=partial(setFrame, 'getStart', startFrame, endFrame), annotation="Use current frame as start")
	gotoStartBut = mc.button(label="Goto", command=partial(setFrame, 'gotoStart', startFrame, endFrame), annotation="Go to the above frame")
	mc.separator(width=66, style="none")
	setEndBut = mc.button(label="Set", command=partial(setFrame, 'getEnd', startFrame, endFrame), annotation="Use current frame as end")
	gotoEndBut = mc.button(label="Goto", command=partial(setFrame, 'gotoEnd', startFrame, endFrame), annotation="Go to the above frame")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1)
	mc.separator(height=5, style="none")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1)
	mc.separator(width=20, style="none")
	mc.text("Create CV at every  ")
	step = mc.floatField(value=1.0, precision=2, annotation=" Lower number creates more detailed curve - Higher number creates less detailed curve")
	mc.text("  frame/s")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1)
	mc.separator(height=5, style="none")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1, bgc=titleBG)
	mc.separator(height=5, style="none")
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1, bgc=titleBG)
	mc.separator(width=120, style="none")
	mc.button(label="Plot!", width=100, height=40, command=partial(plotWithCurve, startFrame, endFrame, step), bgc=(0.4,0.4,0.4))
	mc.setParent("..")
	#
	mc.rowColumnLayout( numberOfRows=1, bgc=titleBG)
	mc.separator(height=5, style="none")
	mc.setParent("..")
	#
	mc.setParent("..")
	#
	#
	mc.showWindow(WIN_plot)


