import shiboken 
from PySide import QtGui
import maya.OpenMayaUI as apiUI
from cStringIO import StringIO
import pysideuic
import xml.etree.ElementTree as xml 

def get_maya_window():
	ptr= apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr),QtGui.QMainWindow)


def load_ui_type(ui_file):
	parsed= xml.parse(ui_file)
	widget_class =parsed.find('widget').get('class')
	form_class =parsed.find('class').text
	with open(ui_file,'r') as f:
		o= StringIO()
		frame={}
		
		pysideuic.compileUi(f,o,indent=0)
		pyc= compile(o.getvalue(), '<string>',  'exec')
		exec pyc in frame
		
		form_class = frame ['Ui_{0}'.format (form_class)]
		base_class = eval( 'QtGui.{0}'.format(widget_class))
	return form_class, base_class
	
