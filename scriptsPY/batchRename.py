'''
BATCH RENAME

Batch renamer for Maya

Author: Peppe Russo
All rights reserved (c) 2017

pepperusso.uk
contact.pepperusso@gmail.com

---------------------------------------------------------------------------------------------

INSTALLATION:

Place the batchRename.py in your maya scripts folder and run this code (in python):

import batchRename
batchRename.install()

This will create an icon in the current shelf

To run it simply click the shelf button or run this code (python):

import batchRename
batchRename.start()


---------------------------------------------------------------------------------------------

You are using this script on you own risk.
Things can always go wrong, and under no circumstances the author
would be responsible for any damages caused from the use of this software.

---------------------------------------------------------------------------------------------

The coded instructions, statements, computer programs, and/or related
material (collectively the "Data") in these files are subject to the terms
and conditions defined by
Creative Commons Attribution-NonCommercial-NoDerivs 4.0 Unported License:
   http://creativecommons.org/licenses/by-nc-nd/4.0/
   http://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
   http://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.txt

---------------------------------------------------------------------------------------------
'''

__version__ = '2.1.1'
__author__ = 'Peppe Russo'


from maya import cmds
import urllib
import os
import maya.mel as mel


# Qt
try:
    from PySide2 import QtWidgets, QtCore, QtGui
except ImportError:
    from PySide import QtCore, QtGui
    QtWidgets = QtGui

# Logger
import logging

logging.basicConfig()
logger = logging.getLogger('BatchRename')
logger.setLevel(logging.INFO)



def start():
    w = MainWindow()
    w.show()

    try:
        checkUpdates()
    except:
        logger.debug("Can't check updates")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        windowName = 'BatchRename'
        # Delete if exists
        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName)
            logger.debug('Deleted previous UI')
        else:
            logger.debug('No previous UI exists')

        # Delete Manual Mode window
        if cmds.window('BRManualWindow', exists=True):
            cmds.deleteUI('BRManualWindow')
            logger.debug('Deleted previous UI')

        # Get Maya window and parent the controller to it
        mayaMainWindow = {o.objectName(): o for o in QtWidgets.qApp.topLevelWidgets()}["MayaWindow"]
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setWindowTitle('Batch Rename')
        self.setObjectName(windowName)

        self.list = {}

        self.buildUI()
        self.addItems()

    def buildUI(self):
        # Main widget
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)

        # Layout
        layout = QtWidgets.QGridLayout()
        widget.setLayout(layout)

        # List Widget
        self.listwidget = QtWidgets.QListWidget()
        #self.listwidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.listwidget,0,0,15,2)

        self.listwidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)




        #################
        # PREFIX/SUFFIX #
        #################
        psLabel = QtWidgets.QLabel()
        psLabel.setText('Prefix/Suffix')
        layout.addWidget(psLabel,0,2)

        self.prefixField = QtWidgets.QLineEdit()
        self.prefixField.setPlaceholderText('Prefix')
        layout.addWidget(self.prefixField,1,2)

        self.suffixField = QtWidgets.QLineEdit()
        self.suffixField.setPlaceholderText('Suffix')
        layout.addWidget(self.suffixField,1,3)

        psBtn = QtWidgets.QPushButton()
        psBtn.setText('OK')
        layout.addWidget(psBtn,1,4)
        psBtn.clicked.connect(self.okPS)


        #################
        separator1 = QtWidgets.QFrame()
        separator1.setFrameShape(separator1.HLine)
        separator1.setFrameShadow(separator1.Sunken)
        layout.addWidget(separator1,2,2,1,3)

        #################
        #    INSERT     #
        #################
        insertLabel = QtWidgets.QLabel()
        insertLabel.setText('Insert')
        layout.addWidget(insertLabel,3,2)

        self.insertField = QtWidgets.QLineEdit()
        self.insertField.setPlaceholderText('Insert at')
        layout.addWidget(self.insertField,4,2)

        self.atField = QtWidgets.QSpinBox()
        layout.addWidget(self.atField,4,3)

        insertBtn = QtWidgets.QPushButton()
        insertBtn.setText('OK')
        layout.addWidget(insertBtn,4,4)
        insertBtn.clicked.connect(self.okInsert)


        #################
        separator2 = QtWidgets.QFrame()
        separator2.setFrameShape(separator2.HLine)
        separator2.setFrameShadow(separator2.Sunken)
        layout.addWidget(separator2,5,2,1,3)

        #################
        #    REPLACE    #
        #################
        replaceLabel = QtWidgets.QLabel()
        replaceLabel.setText('Replace')
        layout.addWidget(replaceLabel,6,2)

        self.replaceField = QtWidgets.QLineEdit()
        self.replaceField.setPlaceholderText('Replace')
        layout.addWidget(self.replaceField,7,2)

        self.replaceWithField = QtWidgets.QLineEdit()
        self.replaceWithField.setPlaceholderText('With')
        layout.addWidget(self.replaceWithField,7,3)

        replaceBtn = QtWidgets.QPushButton()
        replaceBtn.setText('OK')
        layout.addWidget(replaceBtn,7,4)
        replaceBtn.clicked.connect(self.okReplace)


        #################
        separator3 = QtWidgets.QFrame()
        separator3.setFrameShape(separator3.HLine)
        separator3.setFrameShadow(separator3.Sunken)
        layout.addWidget(separator3,8,2,1,3)

        #################
        #     REMOVE    #
        #################
        removeLabel = QtWidgets.QLabel()
        removeLabel.setText('Remove String')
        layout.addWidget(removeLabel,9,2)

        self.removeField = QtWidgets.QLineEdit()
        self.removeField.setPlaceholderText('Remove')
        layout.addWidget(self.removeField,10,2,1,2)

        removeBtn = QtWidgets.QPushButton()
        removeBtn.setText('OK')
        layout.addWidget(removeBtn,10,4)
        removeBtn.clicked.connect(self.okRemove)


        #################
        separator3 = QtWidgets.QFrame()
        separator3.setFrameShape(separator3.HLine)
        separator3.setFrameShadow(separator3.Sunken)
        layout.addWidget(separator3,11,2,1,3)

        #################
        # REMOVE FROM/TO#
        #################
        removeFTLabel = QtWidgets.QLabel()
        removeFTLabel.setText('Remove From/To')
        layout.addWidget(removeFTLabel,12,2)

        self.removeFromSBox = QtWidgets.QSpinBox()
        self.removeFromSBox.setStatusTip("Remove From")
        self.removeFromSBox.valueChanged.connect(self.removeFTvalues)
        layout.addWidget(self.removeFromSBox,13,2)

        self.removeToSBox = QtWidgets.QSpinBox()
        self.removeToSBox.setStatusTip("Remove To")
        self.removeToSBox.setMinimum(1)
        self.removeFromSBox.valueChanged.connect(self.removeFTvalues)
        layout.addWidget(self.removeToSBox,13,3)

        removeFTBtn = QtWidgets.QPushButton()
        removeFTBtn.setText('OK')
        layout.addWidget(removeFTBtn,13,4)
        removeFTBtn.clicked.connect(self.okRemoveFT)


        ###################
        # FIX SIZE POLICY #
        ###################

        #QtWidgets.QLineEdit.setMinimumWidth()
        for lineedit in layout.parentWidget().findChildren(QtWidgets.QLineEdit):
            lineedit.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

        for spinbox in layout.parentWidget().findChildren(QtWidgets.QSpinBox):
            spinbox.setSizePolicy(QtWidgets.QSizePolicy.Ignored,QtWidgets.QSizePolicy.Fixed)

        for label in layout.parentWidget().findChildren(QtWidgets.QLabel):
            label.setSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)

        for pushbtn in layout.parentWidget().findChildren(QtWidgets.QPushButton):
            pushbtn.setSizePolicy(QtWidgets.QSizePolicy.Maximum,QtWidgets.QSizePolicy.Maximum)


        ## Spacer
        emptyLabel = QtWidgets.QLabel()
        emptyLabel.setText("")
        emptyLabel.setFixedHeight(0)
        emptyLabel.setHidden(True)
        layout.addWidget(emptyLabel,14,2,1,3, QtCore.Qt.AlignVCenter)



        #################
        # Confirm Btns  #
        #################

        resetBtn = QtWidgets.QPushButton()
        resetBtn.setText('Reset')
        layout.addWidget(resetBtn,15,2)
        resetBtn.clicked.connect(self.reset)

        applyBtn = QtWidgets.QPushButton()
        applyBtn.setText('Apply')
        layout.addWidget(applyBtn,15,3)
        applyBtn.clicked.connect(self.apply)

        manualBtn = QtWidgets.QPushButton()
        manualBtn.setIcon(QtGui.QIcon(":/channelBox.png"))
        layout.addWidget(manualBtn,15,4)
        manualBtn.clicked.connect(self.startManualMode)



        #################
        #  Add/Remove   #
        #################

        addBtn = QtWidgets.QPushButton()
        addBtn.setIcon(QtGui.QIcon(":/QR_add.png"))
        layout.addWidget(addBtn,15,0)
        addBtn.clicked.connect(self.addItems)

        removeBtn = QtWidgets.QPushButton()
        removeBtn.setIcon(QtGui.QIcon(":/QR_delete.png"))
        layout.addWidget(removeBtn,15,1)
        removeBtn.clicked.connect(self.removeItems)





    def addItems(self):
        logger.debug("Add Items")

        selected = cmds.ls(sl=True) or []
        for eachSel in selected:
            self.list[eachSel.split("|")[-1]] = eachSel.split("|")[-1]


        self.populate()

    def removeItems(self):
        logger.debug("Remove")
        for item in self.listwidget.selectedItems():
            self.listwidget.takeItem(self.listwidget.row(item))
            self.list.pop(item.text(), None) # Delete key from dict


    def okPS(self):
        logger.debug('OK PS')

        # Name can't begin with a number. Maya is stupid


        if self.prefixField.text() and self.suffixField.text():
            for oldName in self.list:
                self.list[oldName] = self.prefixField.text() + self.list[oldName] + self.suffixField.text()
        elif self.prefixField.text():
            for oldName in self.list:
                self.list[oldName] = self.prefixField.text() + self.list[oldName]
        elif self.suffixField.text():
            for oldName in self.list:
                self.list[oldName] = self.list[oldName] + self.suffixField.text()

        self.populate()

    def okInsert(self):
        logger.debug('OK Insert')

        index = self.atField.value()

        for oldName in self.list:
            self.list[oldName] = self.list[oldName][:index] + self.insertField.text() + self.list[oldName][index:]

        self.populate()

    def okReplace(self):
        logger.debug('OK Replace')
        for oldName in self.list:
            newName = self.list[oldName].replace(self.replaceField.text(), self.replaceWithField.text())
            self.list[oldName] = newName

        self.populate()

    def okRemove(self):
        logger.debug('OK Remove')

        for oldName in self.list:
            newName = self.list[oldName].replace(self.removeField.text(), '') # Cheating. Replace with nothing
            self.list[oldName] = newName

        self.populate()

    def okRemoveFT(self):
        logger.debug('OK Remove FT')

        fromIndex = self.removeFromSBox.value()
        toIndex = self.removeToSBox.value()

        for oldName in self.list:
            newName = oldName[:fromIndex] + oldName[toIndex:]
            self.list[oldName] = newName

        self.populate()

    def removeFTvalues(self):

        self.removeToSBox.setMinimum(self.removeFromSBox.value()+1)


    def populate(self):
        self.listwidget.clear()

        for name in self.list:
            newName = self.list.get(name)
            item = QtWidgets.QListWidgetItem()
            item.setToolTip(name)
            item.setText(newName)

            self.listwidget.addItem(item)


    def isNameOk(self,newName,oldName):
        if oldName == newName:
            logger.info("The object name not changed for: " + oldName + ". Renaming Skipped")
            return True
        elif newName == '':
            logger.error("Please insert a name for " + newName)
            return False
        elif newName[0].isdigit():
            logger.error("Object name can't start with a number, choose a different name for  " + newName)
            return False
        elif cmds.ls(newName, long=True):
            logger.error("An object named " + newName + " already exists")
            return False

        else:
            return True


    def reset(self, resetList=True):
        logger.debug('Reset')
        self.prefixField.clear()
        self.suffixField.clear()
        self.insertField.clear()
        self.atField.setValue(0)
        self.replaceField.clear()
        self.replaceWithField.clear()
        self.removeField.clear()

        # Reset List dict
        if resetList==True:
            for item in self.list:
                self.list[item] = item

        self.populate()


    def apply(self):
        logger.debug('Apply')
        for oldName in self.list.keys():
            newName = str(self.list[oldName])

            logger.debug(oldName + " -> " + newName)

            # Check new name
            if not self.isNameOk(newName, oldName):
                return

            try:
                cmds.rename(oldName,newName)
                self.list[newName] = self.list.pop(oldName)
            except:
                logger.error("New name not correct, " + oldName + " not renamed.")

        self.reset(resetList=False)
        self.populate()

        logger.debug(self.list)

    def startManualMode(self):
        # clear the active list
        cmds.select( clear=True )


        for item in self.list:
            print item
            cmds.select(item, add=True )

        self.close()

        mw = ManualModeWindow()
        mw.show()

class ManualModeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ManualModeWindow, self).__init__()
        # Delete if exists
        if cmds.window('BRManualWindow', exists=True):
            cmds.deleteUI('BRManualWindow')
            logger.debug('Deleted previous UI')



        # Get Maya window and parent the controller to it
        mayaMainWindow = {o.objectName(): o for o in QtWidgets.qApp.topLevelWidgets()}["MayaWindow"]
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setWindowTitle('Batch Rename: Manual Mode')
        self.setObjectName('BRManualWindow')

        #self.setMinimumWidth(400)
        print
        self.resize(400, self.heightForWidth(True))


        self.buildUI()
        self.populate()


    def buildUI(self):
        # Main widget
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        # Layout
        self.layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.layout)


    def populate(self):
        logger.debug("Populating...")
        # HERE SHOULD CLEAR THE WIDGET
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.signalMapper = QtCore.QSignalMapper(self)# set mapper

        selection = cmds.ls(selection=True) # Get selected objs
        selectionCount = len(selection)

        # Add Widgets
        if selection:
            for i in range(selectionCount):
                nameFld = QtWidgets.QLineEdit()
                nameFld.setText(selection[i])
                nameFld.setPlaceholderText(selection[i])

                nameFld.returnPressed.connect(self.signalMapper.map)
                self.signalMapper.setMapping(nameFld, str(nameFld.text()))


                self.layout.addWidget(nameFld)

            self.signalMapper.mapped[str].connect(self.updateName)

            # BUTTONS
            subLayout = QtWidgets.QGridLayout()

            goBackBtn = QtWidgets.QPushButton()
            goBackBtn.setIcon(QtGui.QIcon(":/undo_s.png"))
            goBackBtn.clicked.connect(self.autoMode)
            subLayout.addWidget(goBackBtn,0,0)

            applyBtn = QtWidgets.QPushButton()
            applyBtn.setText('Apply')
            applyBtn.clicked.connect(self.updateAll)
            subLayout.addWidget(applyBtn,0,1)

            renameBtn = QtWidgets.QPushButton()
            renameBtn.setText('Rename')
            renameBtn.clicked.connect(lambda: self.updateAll(True))
            subLayout.addWidget(renameBtn,0,2)

            self.layout.addLayout(subLayout)


        elif not selection:
            # NO OBJECTS SELECTED
            logger.info("No objects selected")
            infoText = QtWidgets.QLabel()
            infoText.setText("Please select an object")
            infoText.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

            self.layout.addWidget(infoText)

            refreshBtn = QtWidgets.QPushButton()
            refreshBtn.setText("Refresh")
            refreshBtn.clicked.connect(self.populate)

            self.layout.addWidget(refreshBtn)



    def updateName(self, currentName):
        sender = self.signalMapper.mapping(currentName)
        newName = str(sender.text())


        if not newName:
            logger.info('Please insert a valid name for the object: '+currentName)
            pass
        else:
            logger.debug("Current: " + currentName + " New: " + newName)
            self.rename(currentName, newName)

        # Update sender placeholder txt
        sender.setPlaceholderText(newName)
        # Focus on next
        sender.focusNextChild()

        # Recreate widget
        sender.deleteLater()

        newFld = QtWidgets.QLineEdit()
        newFld.setText(newName)
        newFld.setPlaceholderText(newName)
        newFld.returnPressed.connect(self.signalMapper.map)
        self.signalMapper.setMapping(newFld, str(newFld.text()))

        index = self.layout.indexOf(sender)
        self.layout.insertWidget(index,newFld)


    def updateAll(self, closeWindow=False):
        logger.debug("Updating all..")
        for currentWidget in self.widget.children():
            if isinstance(currentWidget, QtWidgets.QLineEdit):
                currentName = str(currentWidget.placeholderText())
                newName = str(currentWidget.text())
                logger.debug("Current: " + currentName + " New: " + newName)
                self.rename(currentName, newName)

        self.populate()


        if closeWindow == True:
            self.close()
            self.deleteLater()

    def rename(self, currentName, newName):
        if currentName and newName:
            try:
                if currentName != newName:
                    cmds.rename(currentName, newName)
                    logger.debug("Renamed: " + currentName + " to: " + newName)
                else:
                    logger.debug(currentName + " not renamed.")
            except:
                logger.error(currentName + " not renamed.")
        else:
            pass

    def autoMode(self):
        self.close()
        start()



def install():
    ############
    url = 'http://pepperusso.uk/scripts/batchRename/icon.png' # Url of your icon
    imageName = 'batchrename.png' # The icon will be saved using this name (include ext) in the icons folder of the current maya version (usually : documents/version/prefs/icons)

    name = 'Batch Rename' # Name to use for the shelf button
    tooltip = 'Rename multiple objects' # Tooltip to use for the shelf button

    # Command of the shelf button.
    command = """import batchRename
batchRename.start()"""

    ############


    ## Get current maya version
    version = cmds.about(version=True)

    ## Download Icon
    appPath = os.environ['MAYA_APP_DIR']
    path = os.path.join(appPath, version, "prefs/icons", imageName)
    urllib.urlretrieve(url, path)

    ## Add to current shelf
    topShelf = mel.eval('$nul = $gShelfTopLevel')
    currentShelf = cmds.tabLayout(topShelf, q=1, st=1)
    cmds.shelfButton(parent=currentShelf, i=path, c=command, label=name, annotation=tooltip)


def checkUpdates():

    url = "http://pepperusso.uk/scripts/batchRename/update.txt" # Current version of the script. In the file: "1.0.0"
    update = urllib.urlopen(url).read()

    if update.split("\n")[0] > __version__:
        logger.info("\n".join(update.split("\n")[1:]))
