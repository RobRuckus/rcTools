'''
Spiral Along Curve version 1.0
This script can draw multiple spiral curves along the curve you selected
Copyright (C) 2014  James.N

written by James.N
title:     spiral along curve
file:      JR_Spiral_Along_Curve
version:   1.0
create:	   2014-10-13
update:    2014-10-13
mailbox:   averst.nj@gmail.com
'''

import pymel.core as pm
import math as math

class spiralAlongCurve(object):
	def __init__(self):
		self.curveCount = 1
		self.ratioStep = 1.0
		self.radius = 1.0
		self.step = 0.05
		self.newCurveName = "spiral"
		self.grpName = "spiral_grp"
		self.__reference = None
		self.__targetGrp = None

	@property
	def spine(self):
		return self.__reference
	@spine.setter
	def spine(self, value):
		try:
			curNode = pm.PyNode(value)
			if pm.nodeType(value) == 'transform':
				shape = curNode.getShape()
				if str(pm.nodeType(shape)) == 'nurbsCurve':
					self.__reference = shape
				else:
					print "this object is not a curve"
			elif str(pm.nodeType(value)) == 'nurbsCurve':
				self.__reference = curNode
			else:
				print "invalid node type"
		except pm.MayaObjectError:
			print "object doesn't exists"

	def curveGroup(self):
		if not pm.objExists(self.grpName):
			if len(self.grpName):
				self.__targetGrp = pm.group(name = self.grpName, empty = True, world = True)
			else:
				self.__targetGrp = None
		else:
			self.__targetGrp = pm.PyNode(self.grpName)

	def drawSpiral(self, count = 0.0):
		minU = self.__reference.attr('min').get()
		maxU = self.__reference.attr('max').get()
		angle = count
		parm = minU+0.00001
		#initial curve
		myCurve = pm.curve(name = self.newCurveName, ws=True, p = [(0.0,0.0,0.0)], degree = 3)
		if self.__targetGrp != None and self.__targetGrp != "":
			pm.parent(myCurve, self.__targetGrp)
		#append curve
		while parm <= maxU:
			pos = pm.pointOnCurve(self.__reference, pr = parm, position = True)
			tan = pm.pointOnCurve(self.__reference, pr = parm, normalizedTangent = True)

			tangent = pm.datatypes.Vector(tan)
			normal = tangent.cross(pm.datatypes.Vector([0.0,-1.0,0.0]))
			direction = normal.rotateBy(tangent,angle)
			direction.normalize()
			newPos = pm.datatypes.Vector(pos) + self.radius * direction
			pm.curve(myCurve, append = True, p = [(newPos.x, newPos.y, newPos.z)])

			parm += self.step
			angle += self.ratioStep
		pm.delete(myCurve.cv[0])

	def drawSpiralSet(self):
		#caculate angle
		incre = (2*math.pi)/float(self.curveCount)
		self.curveGroup()
		for i in range(self.curveCount):
			iniAngle = incre * i
			self.drawSpiral(count = iniAngle)

class spiralAlongCurveUI():
	def __init__(self):
		#ui list
		self.uiList = {}
		#window
		if pm.window('spiralMainWindow', ex=True): pm.deleteUI('spiralMainWindow')

		self.mainWindow = pm.window('spiralMainWindow', title = "Spiral Along Curve", width = 420, height = 270)
		self.mainWindow.setWidthHeight([420,270])
		#layout
		self.mainForm = pm.formLayout(numberOfDivisions=100)
		#widgits
		self.curveNameField = pm.textFieldGrp(label = "Spiral Name", text = "spiral", cw = [1, 80], adj = 2)
		self.uiList["nameField"] = str(self.curveNameField)
		self.curveCountSli = pm.intSliderGrp(label = "Spiral Count", field = True, min = 1, fmn = 1, max = 10, fmx = 10000, step = 1, value = 1, cw = [1, 80])
		self.uiList["countSli"] = str(self.curveCountSli)
		self.spiralRadiusSli = pm.floatSliderGrp(label = "Radius", field = True, min = 0.001, max = 4.0, fmx = 10000, step = 0.1, precision = 3, value = 1.0, cw = [1, 80])
		self.uiList["radiusSli"] = str(self.spiralRadiusSli)
		self.spiralStepSli = pm.floatSliderGrp(label = "Step", field = True, min = 0.001, max = 0.5, fmx = 10000, step = 0.01, precision = 3, value = 0.1, cw = [1, 80])
		self.uiList["stepSli"] = str(self.spiralStepSli)
		self.spiralRatioSli = pm.floatSliderGrp(label = "Ratio Step", field = True, min = 0.001, max = 7.0, fmx = 10000, step = 0.01, precision = 3, value = 1.0, cw = [1, 80])
		self.uiList["ratioSli"] = str(self.spiralRatioSli)
		self.grpNameField = pm.textFieldGrp(label = "Group Name", text = "spiral_grp", cw = [1, 80], adj = 2)
		self.uiList["groupField"] = str(self.grpNameField)
		self.mainButton = pm.button(label = "Create Spiral!", height = 40, command = pm.Callback(self.createSpiralCommand))
		self.uiList["mainButton"] = str(self.mainButton)
		#configure widgets
		self.mainForm.attachForm(self.uiList["nameField"],'top',20)
		self.mainForm.attachForm(self.uiList["nameField"],'left',10)
		self.mainForm.attachForm(self.uiList["nameField"],'right',10)
		self.mainForm.attachForm(self.uiList["countSli"],'left',10)
		self.mainForm.attachForm(self.uiList["countSli"],'right',10)
		self.mainForm.attachControl(self.uiList["countSli"],'top',8,self.uiList["nameField"])
		self.mainForm.attachForm(self.uiList["radiusSli"],'left',10)
		self.mainForm.attachForm(self.uiList["radiusSli"],'right',10)
		self.mainForm.attachControl(self.uiList["radiusSli"],'top',8,self.uiList["countSli"])
		self.mainForm.attachForm(self.uiList["stepSli"],'left',10)
		self.mainForm.attachForm(self.uiList["stepSli"],'right',10)
		self.mainForm.attachControl(self.uiList["stepSli"],'top',8,self.uiList["radiusSli"])
		self.mainForm.attachForm(self.uiList["ratioSli"],'left',10)
		self.mainForm.attachForm(self.uiList["ratioSli"],'right',10)
		self.mainForm.attachControl(self.uiList["ratioSli"],'top',8,self.uiList["stepSli"])
		self.mainForm.attachForm(self.uiList["groupField"],'left',10)
		self.mainForm.attachForm(self.uiList["groupField"],'right',10)
		self.mainForm.attachControl(self.uiList["groupField"],'top',8,self.uiList["ratioSli"])
		self.mainForm.attachForm(self.uiList["mainButton"],'left',10)
		self.mainForm.attachForm(self.uiList["mainButton"],'right',10)
		self.mainForm.attachControl(self.uiList["mainButton"],'top',30,self.uiList["groupField"])
		#show UI
		self.mainWindow.show()

	def createSpiralCommand(self):
		newSpiralCurves = spiralAlongCurve()
		try:
			newSpiralCurves.spine = pm.ls(sl = True)[0]
			newSpiralCurves.newCurveName = self.curveNameField.getText()
			newSpiralCurves.curveCount = self.curveCountSli.getValue()
			newSpiralCurves.radius = self.spiralRadiusSli.getValue()
			newSpiralCurves.step = self.spiralStepSli.getValue()
			newSpiralCurves.ratioStep = self.spiralRatioSli.getValue()
			newSpiralCurves.grpName = self.grpNameField.getText()
			newSpiralCurves.drawSpiralSet()
		except IndexError:
			print "No curve Selected!"


spiralAlongCurveUI()