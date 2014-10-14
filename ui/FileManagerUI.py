import os
from pymel.core import *
from pymel.all import *
from PySide import QtGui
from rcTools2.ui.loadUI import get_maya_window, load_ui_type

ui_file= os.path.join(os.path.dirname(os.path.realpath(__file__)),'FileManager.ui')#path to ui file 

list_form, list_base = load_ui_type(ui_file)
		
class TreeView(QtGui.QTreeView):
	def edit(self,index, trigger, event):
		if trigger == QtGui.QAbstractItemView.DoubleClicked:
			print 'Killed'
			return false
		return QtGui.QTreeView.edit(self, index, trigger,event)
			

class bdFMUI(list_form, list_base):
	def __init__(self,parent= get_maya_window()):
		self.window_name= 'FileManager'
		#self.setDockingNestingEnabled(True)
		if window(self.window_name,exists=True): deleteUI(self.window_name)
		super(bdFMUI,self).__init__(parent)
		self.setupUi(self)
		#setup interaction of GUI HERE
		#FileSystemModel
		#bld File system Model
		model=QtGui.QFileSystemModel()
		model.setRootPath('')
		#setSystemModel to Widget
		self.list_Browse.setModel(model)
		self.list_Browse.setRootIndex(model.index(workspace.getPath()))
		self.list_Browse.hideColumn(2)
		#self.list_Browse.setColumnHidden(column=1,hide=1)
		"""
		print 'Current Units:',str(mc.currentUnit(query=True))
		print 'Frame Rate:',str(getSceneData()['fps'])
		print 'Resolution:',str(mc.getAttr('defaultResolution.width'))+'x'+str(mc.getAttr('defaultResolution.height'))
		print 'Project:',mc.workspace(q=1,active=1)
		"""
		#self.btn
		#for each in rc.getSceneData()['cameras']:
			#self.list_Browse.addItem(each)#addItems to ListWidget 
		
def runplugin():
	ex=bdFMUI()
	ex.show()
	
	
