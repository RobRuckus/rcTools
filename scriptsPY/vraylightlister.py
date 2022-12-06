##########################################
# VRAY LIGHT LISTER  0.2                 #
#                                        #
# by Ricardo Viana                       #
# Feb 2014                               #
#                                        #
##########################################


import pymel.core as pm
from PySide import QtGui, QtCore
import maya.OpenMayaUI as omui
from shiboken import wrapInstance




def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance (long(main_window_ptr), QtGui.QWidget)
    
    

class Lister(object):
    
    def __init__(self):
        self.showUI()

    def showUI(self):
        #main window
        self.window = QtGui.QWidget(parent = maya_main_window())
        self.window.setWindowFlags (QtCore.Qt.Window)
        self.window.setGeometry(400,400,275,550)
        self.window.setWindowTitle("VRAY LIGHT LISTER")
        
        

       
        # Main Layout
        self.mainLayout = QtGui.QVBoxLayout()
        self.window.setLayout(self.mainLayout)
        
        self.refresh= QtGui.QPushButton("Refresh")
        
        # List widget
        self.listWidget = QtGui.QListWidget()
        self.listWidget.setStyleSheet("line-height:20px;")
        
        #rename Window
        
        self.newName = QtGui.QLineEdit(parent = self.listWidget)
        
        
        self.newName.hide()
        
        
        # properties widgets
        
        #intensity and subdivision Widgets
        self.intSubdivWidget = QtGui.QWidget()
        self.hlayout1=QtGui.QHBoxLayout()
        self.intSubdivWidget.setLayout(self.hlayout1)
        
        
       
        #light intensity
        
        self.intensityLabel = QtGui.QLabel("Intensity Multiplier:")
        self.intensityValue = QtGui.QDoubleSpinBox(parent = self.intSubdivWidget)
        self.intensityValue.setRange(0, 100000)
        
        
        #light subdivisions
        self.subdivisionLabel = QtGui.QLabel("Subdivisions:")
        self.subdivisionValue = QtGui.QSpinBox()
        self.subdivisionValue.setRange(1, 1000)
        
        
        #diffuse specular reflection and visibility widget
        
        self.contributeWidget = QtGui.QWidget()
        self.hlayout2=QtGui.QHBoxLayout()
        self.contributeWidget.setLayout(self.hlayout2)
        
        self.diffuseLabel = QtGui.QLabel("diff")
        self.specLabel = QtGui.QLabel("spec")
        self.refLabel = QtGui.QLabel("reflect")
        self.invisiblityLabel = QtGui.QLabel("invisible")
        
        self.diffuseSwitch = QtGui.QCheckBox()
        self.specSwitch = QtGui.QCheckBox()
        self.refSwitch = QtGui.QCheckBox()
        self.invisibilitySwitch = QtGui.QCheckBox()
        
     
        #add to layout
        self.mainLayout.addWidget(self.refresh)
        self.mainLayout.addWidget(self.listWidget)
        
        
        
        self.hlayout1.addWidget(self.intensityLabel)
        self.hlayout1.addWidget(self.intensityValue)
        self.hlayout1.addWidget(self.subdivisionLabel)
        self.hlayout1.addWidget(self.subdivisionValue)
        
        self.hlayout2.addWidget(self.invisiblityLabel)
        self.hlayout2.addWidget(self.invisibilitySwitch)
        self.hlayout2.addWidget(self.diffuseLabel)
        self.hlayout2.addWidget(self.diffuseSwitch)
        self.hlayout2.addWidget(self.specLabel)
        self.hlayout2.addWidget(self.specSwitch)
        self.hlayout2.addWidget(self.refLabel)
        self.hlayout2.addWidget(self.refSwitch)
        
        self.mainLayout.addWidget(self.intSubdivWidget)
        self.mainLayout.addWidget(self.contributeWidget)

    
        
        #signals
        self.listWidget.itemClicked.connect(self.on_item_changed)
        self.listWidget.itemDoubleClicked.connect(self.renameUI)
        self.subdivisionValue.valueChanged[int].connect(self.updateSubdivValue)
        self.intensityValue.valueChanged[float].connect(self.updateIntensityValue)
        
        self.invisibilitySwitch.stateChanged.connect(self.toggleVisibility)
        self.diffuseSwitch.stateChanged.connect(self.toggleDiffuse)
        self.refSwitch.stateChanged.connect(self.toggleRef)
        self.specSwitch.stateChanged.connect(self.toggleSpec)
        self.refresh.clicked.connect(self.loadLights)

        self.newName.returnPressed.connect(self.rename)
        
        
        
        
        
             
        self.loadLights()      
         
        self.window.show()
        
        
        
        
        
    def loadLights(self):
        
        
        """
        load all VRAY lights in the scene into the QListWidget
        
        """
        self.listWidget.clear()
        lights = pm.ls(shapes=1)


        for light in lights: 
            if light.nodeType() == "VRayLightRectShape" or light.nodeType() == "VRayLightDomeShape":
                item = QtGui.QListWidgetItem("%s"%light)
                self.listWidget.addItem(item)
                size = QtCore.QSize()
                size.setHeight(20)
                item.setSizeHint(size)

    
    
    
    
    
    def on_item_changed(self,curr):
        
        """
        function to update the widgets everytime a new selection is made in the List.
        
        """     
        
        pm.select(curr.text())
        self.selectedLight=curr.text()
        currentValue = pm.getAttr(self.selectedLight + ".intensityMult")
        self.intensityValue.setValue(currentValue)
        
        currentSubdivision = pm.getAttr(self.selectedLight + ".subdivs")
        self.subdivisionValue.setValue(currentSubdivision)

        currentInvisibility = pm.getAttr(self.selectedLight + ".invisible")
        
        if currentInvisibility == 1:
            self.invisibilitySwitch.setCheckState(QtCore.Qt.Checked)
        else:
            self.invisibilitySwitch.setCheckState(QtCore.Qt.Unchecked)
            
            
            
        currentDiffuse = pm.getAttr(self.selectedLight + ".affectDiffuse")
        
        if currentDiffuse == 1:
            self.diffuseSwitch.setCheckState(QtCore.Qt.Checked)
        else:
            self.diffuseSwitch.setCheckState(QtCore.Qt.Unchecked)
            
            
            
            
        currentSpec = pm.getAttr(self.selectedLight + ".affectSpecular")
        
        if currentSpec == 1:
            self.specSwitch.setCheckState(QtCore.Qt.Checked)
        else:
            self.specSwitch.setCheckState(QtCore.Qt.Unchecked)
            
            
            
            
            
        currentRef = pm.getAttr(self.selectedLight + ".affectReflections")
        
        if currentRef == 1:
            self.refSwitch.setCheckState(QtCore.Qt.Checked)
        else:
            self.refSwitch.setCheckState(QtCore.Qt.Unchecked)





    def updateIntensityValue(self):
        
        """
        updates the intensity values for the given light
        
        """
        
        pm.setAttr(self.selectedLight+".intensityMult",self.intensityValue.value() )
        
        
        
        

    def updateSubdivValue(self):
        
        """
        updates the subdivision values for the given light
        
        """
        pm.setAttr(self.selectedLight+".subdivs",self.subdivisionValue.value() )
        
        
        
    
    def toggleVisibility(self):
        
        """
        toggles the visibility of the selected light
        """
        
        
        state=self.invisibilitySwitch.checkState()
        if state == 0:
            pm.setAttr(self.selectedLight+".invisible",0 )
        else:
            pm.setAttr(self.selectedLight+".invisible",1 )
            
          
    def toggleDiffuse(self):
        
        """
        toggles the diffuse contribution of the selected light
        """
        
        
        state=self.diffuseSwitch.checkState()
        if state == 0:
            pm.setAttr(self.selectedLight+".affectDiffuse",0 )
        else:
            pm.setAttr(self.selectedLight+".affectDiffuse",1 )
            
            
            
    def toggleSpec(self):
        
        """
        toggles the specular contribution of the selected light
        """
        
        
        state=self.specSwitch.checkState()
        if state == 0:
            pm.setAttr(self.selectedLight+".affectSpecular",0 )
        else:
            pm.setAttr(self.selectedLight+".affectSpecular",1 )
            
            
    
    def toggleRef(self):
        
        """
        toggles the reflection contribution of the selected light
        """
        
        
        state=self.refSwitch.checkState()
        if state == 0:
            pm.setAttr(self.selectedLight+".affectReflections",0 )
        else:
            pm.setAttr(self.selectedLight+".affectReflections",1 )
            
     
    def renameUI(self):
        item = self.listWidget.currentItem()
        self.nameRect=self.listWidget.visualItemRect(item)
        self.newName.setGeometry(self.nameRect)
        self.newName.setText(self.selectedLight)
        self.newName.show()
        self.newName.raise_()
        self.newName.setFocus()
        self.newName.selectAll()
        
        
        
    def rename(self):
        
        newName = self.newName.text()
        
        sel=pm.PyNode(self.selectedLight)
        parent = sel.getParent(1)

        pm.rename(self.selectedLight,"%s" %newName)
        pm.rename(parent,"%s_light" %newName)
        
        

        self.loadLights()
        
        self.newName.hide()
        
        self.newName.clear()
        
        
        
            
            

if __name__ == "__main__":
    new = Lister()
    
    
    
