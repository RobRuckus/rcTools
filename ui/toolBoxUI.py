import maya.cmds as mc

class toolbox4():
	def __init(self,name):
		self.rowWidth=300
		self.name=name
		
		self.frame=mc.frameLayout('frame'+self.name,bgc=[.2,.2,.2],fn='smallBoldLabeFont',bs='in',l=name)
		
class ui():#UI VARIABLES
	def __init__(self):
		self.btn_small=20
		self.btn_med=25
		self.btn_large=30
		self.checkBoxHeight=15
		self.textSize=17
		self.textHeight=10
		self.rowWidth=300
		self.iconDim=15
		self.iconSize=13
		self.borders=2
		self.tabWidth=765
		self.titleFont='boldLabelFont'
		self.fieldFont='fixedWidthFont'
	
