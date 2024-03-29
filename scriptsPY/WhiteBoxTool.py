#########################
##White Box Tool
##By James DeMonaco
#########################
import maya.cmds as mc
sourceObject= 0
numberOfTargets = 0
targetObjects = 0
mScale = 1
mRot = 1
mTrans = 1
def cancel(): mc.deleteUI('findAndReplace', window=True)
def cancelHelp(): mc.deleteUI('helpWin', window=True)
def UI():
    #Check if window is already open
    if mc.window('findAndReplace', exists=True, w=150):
    #delete if it is already open
       mc.deleteUI('findAndReplace', window=True)
    #create window
    findAndReplace = mc.window('findAndReplace',t="White Box Tool", rtf=True)
    #layout
    mc.columnLayout(columnAttach=('both', 5), rowSpacing=10, columnWidth=200, h=300)
    mc.windowPref('findAndReplace', w=50, exists=True)
    #Text and buttons
    mc.text(label= 'This Script will replace all targets with the source model', ww=True, rs=True, al="center", fn="boldLabelFont")
    mc.text(label = 'Please select the initial model to be duplicated and click the"store source model" button', ww=True, al='center')
    mc.button(label= 'Store Source Model', align='right', command='storeTarget()')
    mc.checkBox(label='Match Targets Translation?', onc='matchTranslate()', ofc='dontMatchTranslate()', v=True)
    mc.checkBox(label='Match Targets Scale?', onc='matchScale()', ofc='dontMatchScale()', v=True)
    mc.checkBox(label='Match Targets Rotation?', onc='matchRotation()', ofc='dontMatchRotation()', v=True)
    mc.text(label = 'Please select the target meshes where you would like to have the stored model duplicated to and click the "Replace Targets" button', ww=True, al='center')
    mc.button(label= 'Replace Targets', align='right', command='replaceTargets()')
    mc.button(label= 'Help', command='helpWin()')
    mc.button(label= 'Cancel', command='cancel()')
    #Call window
    mc.showWindow(findAndReplace)
#Function to control state of "Match Translateion" option (on)
def matchTranslate():
    global mTrans
    mTrans = 1
#Function to control state of "Match Translateion" option (on)
def dontMatchTranslate():
    global mTrans
    mTrans = 0
#Function to control state of "Match Scale" option (on)
def matchScale():
    global mScale
    mScale = 1
#Function to control state of "Match Scale" option (off)
def dontMatchScale():
    global mScale
    mScale = 0
    
#Function to control state of "Match Rotation" option (on)
def matchRotation():
    global mRot
    mRot = 1

#Function to control state of "Match Rotation" option (off)
def dontMatchRotation():
    global mRot
    mRot = 0

#function to store target as a list
def storeTarget():
    global sourceObject
    sourceObject = mc.ls(sl = True)
    #error check variable, checks to make sure only one object is being sourced
    sourceCheck = len(sourceObject)
    if (sourceCheck != 1):
       mc.warning ('1 source object should be stored at a time.  Please select one object.')
       sourceObject = 'empty[]'
    elif (sourceCheck == 1):
       mc.headsUpMessage('Source Object Stored!') 
#replace function
def replaceTargets():
   
    global sourceObject
    global mScale
    global mRot
    global mTrans
   
    #store number of user selected targets as an int
    targetObjects = mc.ls(sl = True)
    numberOfTargets = len(targetObjects)
    print targetObjects
    
    #loop to replace Objects
    for x in range (numberOfTargets):
       mc.select(targetObjects[x])
       mc.xform(cp= True) 
       #Duplicate the source object
       sO=mc.duplicate(sourceObject)
       mc.select(sO)
       mc.xform(cp= True)
       #get rotation info for target
       tRotX = mc.getAttr(targetObjects[x] + ".rotateX")
       tRotY = mc.getAttr(targetObjects[x] + ".rotateY")
       tRotZ = mc.getAttr(targetObjects[x] + ".rotateZ")
       #Orient Constrain target to source temporarily for BB info
       mc.orientConstraint (sO[0], targetObjects[x])
       #Get BB Info for target
       StoredBB = mc.polyEvaluate(targetObjects[x], b=True)
       tLength = StoredBB[0][1] - StoredBB[0][0]
       tHeight = StoredBB[1][1] - StoredBB[1][0]
       tDepth = StoredBB[2][1] - StoredBB[2][0]
       #If statement to translate or not
       if mTrans == 1:
           #Translate the source object to target location
           mc.pointConstraint(targetObjects[x], sO[0])
       elif mTrans == 0:
           print "No need to translate"
       #If statement for scaling
       if mScale == 1:
           #Get new BB Info from translated and rotated source object
           aStoredBB = mc.polyEvaluate(sO[0], b=True)
           sbLength = aStoredBB[0][1] - aStoredBB[0][0]
           sbHeight = aStoredBB[1][1] - aStoredBB[1][0]
           sbDepth = aStoredBB[2][1] - aStoredBB[2][0]
           #Get scale info from duplicated source object
           stLength = mc.getAttr(sO[0] + ".scaleX")
           stHeight = mc.getAttr(sO[0] + ".scaleY")
           stDepth = mc.getAttr(sO[0] + ".scaleZ")
           #Find the difference between BB info and Scale info
           sLengthD = stLength/sbLength
           sHeightD = stHeight/sbHeight
           sDepthD = stDepth/sbDepth
           #Get final number for scaling
           fLength = tLength*sLengthD
           fHeight = tHeight*sHeightD
           fDepth = tDepth*sDepthD
           #Scale object to final number
           mc.setAttr(sO[0] + ".scaleX", fLength)
           mc.setAttr(sO[0] + ".scaleY", fHeight)
           mc.setAttr(sO[0] + ".scaleZ", fDepth)
       elif mScale == 0:
           print "No need to scale"
       #If statement for rotation
       if mRot == 1:
           mc.setAttr(sO[0] + ".rotateX", tRotX)
           mc.setAttr(sO[0] + ".rotateY", tRotY)
           mc.setAttr(sO[0] + ".rotateZ", tRotZ)
       elif mRot == 0:
           print "No need to rotate"
       mc.delete(targetObjects[x])      
def helpWin():
    #Check if window is already open
    if mc.window('helpWin', exists=True):
    #delete if it is already open
       mc.deleteUI('helpWin', window=True)
    #create window
    helpWin = mc.window('helpWin', t="Help with the White Box Tool", rtf=True)
    #layout
    mc.columnLayout(columnAttach=('both', 5), rowSpacing=10, columnWidth=200, h=300)
    mc.windowPref('helpWin', w=50, exists=True)
    
    #Type in the Help Info here
    mc.text(label = 'How to use the White Box Tool', fn="boldLabelFont", ww=True)
    mc.text(label = 'First, select a singular mesh object in your scene that you want to use as the source object', ww=True, align='left')
    mc.text(label = 'Use the "Store Source Model" button to store the information of that model', ww=True, align='left')
    mc.text(label = 'Then select the target meshes that you would like to replace in your scene', ww=True, align='left')
    mc.text(label = 'You can then choose the options you would like to use while replacing the objects via the check boxes', ww=True, align='left')
    mc.text(label = '   Match Targets Translation?', fn="boldLabelFont", ww=True, align='left')
    mc.text(label = '       -This will allow you to match the targets location when duplicating the source object', ww=True, align='left')
    mc.text(label = '   Match Targets Scale?', fn="boldLabelFont", ww=True, align='left')
    mc.text(label = '       -This will allow you to match the targets scale when duplicating the source object', ww=True, align='left')
    mc.text(label = '   Match Targets Rotation?', fn="boldLabelFont", ww=True, align='left')
    mc.text(label = '       -This will allow you to match the targets rotation when duplicating the source object', ww=True, align='left')
    mc.text(label = 'Now that you have chosen the options for the duplication process, you can now click the "Replace Targets" button', ww=True, align='left')
    mc.text(label = '\n\n Tips for making white boxing go more smoothly', fn="boldLabelFont", ww=True, align='left')
    mc.text(label = '   -If you want to use multiple meshes as the source object, it is necessary to combine the objects into one mesh first', ww=True, align='left')
    mc.text(label = '   -The script will automaticall center the pivots of all objects in order to make sure the translation and scale work correctly', ww=True, align='left')
    #Close Help button
    mc.button(label= 'Close Help', command='cancelHelp()')
    #Call window
    mc.showWindow(helpWin)

UI()