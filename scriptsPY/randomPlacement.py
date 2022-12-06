###################################################################################
#
#         Copyright (C) 2013, Michael Yates. All rights reserved.
#
###################################################################################
#
#                                Random Placement
#
###################################################################################
#
# Name	    : randomPlacement()
#                                                  
# Version   : 1.0.2                                               
#				                                                   
# Author    : Michael Yates 	                               
#				                                                   
# Email     : michaelyates@creativegears.com.au  	                           
#
#
##########################   DESCRIPTION   ########################################
#
# Randomly translate, rotate and scale a number of objects in a user specified area.
#
###########################   VERSIONS   ##########################################
#				                                                   
# Version  1.0.0  : 10/Dec/2013
#
# Version  1.0.1  : 12/Dec/2013
#
#           Notes : - Removed viewport refresh after every move to calculate faster 
#                     on slower machines and heavy scenes.
#                   - Added warning to notify users if objects are intersecting
#
# Version  1.0.2  : 6/Jan/2014
#
#           Notes : - Fixed various bugs
#                   - Added relative scale function so that objects maintain their 
#                     base scale when defined.
#
#########################   INSTRUCTIONS   ########################################
#
# Type Python script "randomPlacement()" in commandLine to Run	
#                           
# Select objects to move and hit "Define". Selected objects are automatically 
# defined when the "Move Objects!" button is pressed and no objects are pre-defined.
#
# Change translate, rotate and scale min and max values below. "Uniform Scale" 
# checkbox will randomize scale values uniformly along each axis. "Relative Scale" 
# will use the scale of each object when it is defined as the base point for the 
# random scale.
# 
# ----------------
# Placement Type
#
# Scene Origin: Use the world coordinate 0,0,0 at the center of the grid as the 
# center point from where all objects are randomly moved from.
#
# Parent Origin: Use the immediate parents position as the center point for all 
# movements. If objects are grouped under different parents, positions may alter much 
# more drastically.
#
# Center of Objects: Uses the combined center point of the defined objects. This is 
# recalculated each time objects are moved and may result in the group shifting around.
#
# Use Locators: 3 locators and a bounding box will appear that the user can move and 
# resize to create the area in which the objects will be randomly moved within.
# ----------------
#
# Keep Positions: A seed value is used to keep the calculations the same each time 
# "Move Objects!" is pressed.
#
# Stop Intersections: Tests the bounding box of each object to check if it's colliding 
# with another object. If it is, then it will find a new position until it reaches the 
# max samples. Too many objects being moved in a space too small to fit all of them will 
# result in the maximum number of samples being used with a colliding result in the end.
# If this happens and the samples are too high, hit escape at any point to cancel the 
# calculation.
#
###################################################################################

import maya.cmds as cmds
import random
import pymel.core as pm

# ----------------------------------------------------
#                  MOVE OBJECTS
# ----------------------------------------------------
definedObjects = cmds.ls(sl=True)
relativeScaleX = []
relativeScaleY = []
relativeScaleZ = []

def moveObjectsTest(*args):
    global definedObjects
    # Test if objects in list have been deleted since defining
    objectExists = True
    for object in definedObjects :
        if(cmds.objExists(object)==False):
            objectExists = False
    # If all objects exist, run the script
    if(objectExists==True):
        moveObjects()
    else:
        # Object in defined list is missing, so reset everything
        cmds.warning("Object in defined list is missing, resetting list")
        cmds.text("defineText", e=True, l="No objects defined", bgc=(.404,.188,.188), en=True)
        del definedObjects[:]

def moveObjects():

    # Define selected objects to move
    global definedObjects
    if(len(definedObjects)==0):
        defineObjects()
    selList = definedObjects
    # Variable for if objects are intersecting
    positionFailed = False
    
    # Test if objects are defined
    if(len(definedObjects)>0):
        
        # Define Progress Bar
        cmds.progressWindow(min=0, max=(len(selList)), isInterruptable=True, title="Moving Objects" )
        progress = 0
        
        # If Keep positions, create seed
        if cmds.checkBox( "seedCheckbox", q=True, v=True) :
            random.seed(cmds.intField( "seedField", q=True, v=True))
        
        # Test for intersections
        if cmds.checkBox( "intersectionsCheckbox", q=True, v=True) :
            # Variable saying if intersecting or not
            intersectTest = True
            # Number of times the test can fail before it gives up
            samples = cmds.intField( "samplesField", q=True, v=True)
            # List of objects moved so far so only objects moved are sampled
            objMovedList = []
            del objMovedList[:]
            # Number of objects moved 
            objectsMoved = 0
            # Go through each object, move it and test it against previous objects
            for sel in selList :
                
                # Variables for testing each object in sampling
                testResults = []
                del testResults[:]
                # Test for each sample until broken or at end
                trySamples = True
                samp = -1
                # Update Progress Bar
                progress += 1
                progressQ = progress
                cmds.progressWindow(e=True, pr=progressQ)
                while trySamples == True :
                    samp+=1
                    # Move new object to new sample position
                    moveObj(sel,(progress-1))
                    
                    # Break if it''s the first object (after adding object to list)
                    if(len(objMovedList) == 0) :
                        trySamples = False
                        objMovedList[objectsMoved:]=[sel]
                        break
                    # Reset test results
                    del testResults[:]
                    objectsTested = -1
                    # Test if inside X, Y and Z values for each object  
                    for objMoved in objMovedList :
                        objectsTested += 1
                        # If not testing this axis, make sure it's always a negative result
                        trySamples = True
                        testResults[objectsTested:]=["Failure"]
                        # Test if any axis completely misses the position of the object
                        bb1= cmds.exactWorldBoundingBox(sel)
                        bb2= cmds.exactWorldBoundingBox(objMoved)
                        if (( (bb1[0]>bb2[3]) or (bb2[0]>bb1[3]) or \
                               (bb1[1]>bb2[4]) or (bb2[1]>bb1[4]) or \
                               (bb1[2]>bb2[5]) or (bb2[2]>bb1[5]) )):
                            testResults.pop(objectsTested)
                            testResults[objectsTested:]=["Success"]
                        # Cancel progress bar
                        if cmds.progressWindow(query=True, isCancelled=True) :
                            break
                    # Test if new position is a success for not intersecting with any object
                    testQ = "Success"
                    for test in testResults:
                        # If a single failure is returned, the result is no good
                        if(test=="Failure"):
                            testQ = "Failure"
                    # If the result is a success, keep the position by ending the loop
                    if testQ=="Success" :
                        #print(sel +" is all good after "+str(samp)+" samples")
                        trySamples = False
                    # Test if max number of samples has been reached
                    if(samp == samples) :
                            trySamples = False
                            print(sel +" FAILED to find a position")
                            positionFailed = True
                # Add current object to the moved list
                objMovedList[objectsMoved:]=[sel]         
                objectsMoved += 1
        else :    
            # Just move objects  
            for sel in selList :
                # Update or cancel Progress Bar
                progress += 1
                progressQ = progress
                cmds.progressWindow(e=True, pr=progressQ)
                if cmds.progressWindow(query=True, isCancelled=True) :
                    break
                # Move objects
                moveObj(sel,(progress-1))
        # If cancelled, notify user
        if cmds.progressWindow(query=True, isCancelled=True) :
            print("Move Objects Cancelled")
        # Destroy progress bar
        cmds.progressWindow(endProgress=True)
        # Refresh viewport (there is a refresh issue when moving defined objects)
        pm.refresh(force=True)
        # If objects didn't find a unique position, notify the user
        if(positionFailed):
            cmds.warning("Some objects are intersecting, see Script Editor for details")
        

# ----------------------------------------------------
#               Move objects procedure
# ----------------------------------------------------
    
def moveObj(object,number):
    # Get all of the window values and give them to variables
    minPosX = cmds.floatField("minPosXSlider", q=True, v=True)
    maxPosX = cmds.floatField("maxPosXSlider", q=True, v=True)
    minPosY = cmds.floatField("minPosYSlider", q=True, v=True)
    maxPosY = cmds.floatField("maxPosYSlider", q=True, v=True)
    minPosZ = cmds.floatField("minPosZSlider", q=True, v=True)
    maxPosZ = cmds.floatField("maxPosZSlider", q=True, v=True)
    minRotX = cmds.floatField("minRotXSlider", q=True, v=True)
    maxRotX = cmds.floatField("maxRotXSlider", q=True, v=True)
    minRotY = cmds.floatField("minRotYSlider", q=True, v=True)
    maxRotY = cmds.floatField("maxRotYSlider", q=True, v=True)
    minRotZ = cmds.floatField("minRotZSlider", q=True, v=True)
    maxRotZ = cmds.floatField("maxRotZSlider", q=True, v=True)
    minScaleX = cmds.floatField("minScaleXSlider", q=True, v=True)
    maxScaleX = cmds.floatField("maxScaleXSlider", q=True, v=True)
    minScaleY = cmds.floatField("minScaleYSlider", q=True, v=True)
    maxScaleY = cmds.floatField("maxScaleYSlider", q=True, v=True)
    minScaleZ = cmds.floatField("minScaleZSlider", q=True, v=True)
    maxScaleZ = cmds.floatField("maxScaleZSlider", q=True, v=True)
    moveXq = cmds.checkBox("PositionXCheckbox", q=True, v=True)
    moveYq = cmds.checkBox("PositionYCheckbox", q=True, v=True)
    moveZq = cmds.checkBox("PositionZCheckbox", q=True, v=True)
    rotXq = cmds.checkBox("rotationXCheckbox", q=True, v=True)
    rotYq = cmds.checkBox("rotationYCheckbox", q=True, v=True)
    rotZq = cmds.checkBox("rotationZCheckbox", q=True, v=True)
    scaleXq = cmds.checkBox("scaleXCheckbox", q=True, v=True)
    scaleYq = cmds.checkBox("scaleYCheckbox", q=True, v=True)
    scaleZq = cmds.checkBox("scaleZCheckbox", q=True, v=True)
    unformScale = cmds.checkBox("uniformScaleCheckbox", q=True, v=True)
    relativeScale = cmds.checkBox("relativeScaleCheckbox", q=True, v=True)
    localSpace = False
    global relativeScaleX
    global relativeScaleY
    global relativeScaleZ
    
    # Identify objects parent
    parentQ = cmds.listRelatives(object, parent=True)

    # Calculate the Center of all the objects
    if(cmds.optionMenu("placementType", q=True, v=True) == 'Center of Objects'):     
        # Calculate the Center of all the objects
        centerX = 0
        centerY = 0
        centerZ = 0
        position = cmds.xform( definedObjects[0], query=True, translation=True)
        for sel in definedObjects:
            # Get the world space position of each object and add them all together
            position = cmds.xform( sel, query=True, translation=True, ws=True)
            centerX += position[0]
            centerY += position[1]
            centerZ += position[2]
        # Divide the total value of the transformations by the number of objects to get the average
        finalCenterX = centerX / len(definedObjects)
        finalCenterY = centerY / len(definedObjects)
        finalCenterZ = centerZ / len(definedObjects)
    elif(cmds.optionMenu("placementType", q=True, v=True) == 'Parent Origin'):     
        if(parentQ == None):
            # The object's parent is the scene
            finalCenterX = 0
            finalCenterY = 0
            finalCenterZ = 0
        else :
            # Get the world position of each objects immediate parent
            position = cmds.xform( parentQ[0], query=True, translation=True, ws=True)
            finalCenterX = position[0]
            finalCenterY = position[1]
            finalCenterZ = position[2]
    elif(cmds.optionMenu("placementType", q=True, v=True) == 'Use locators'):     
        # Get position of origin Locator
        position = cmds.xform( "LOC_origin", query=True, translation=True, ws=True)
        finalCenterX = 0
        finalCenterY = 0
        finalCenterZ = 0
        # Replace slider values with that of locators
        minPosX = 0
        maxPosX = cmds.getAttr("LOC_area.tx")
        minPosY = 0
        maxPosY = cmds.getAttr("LOC_height.ty")
        minPosZ = 0
        maxPosZ = cmds.getAttr("LOC_area.tz")
        # Parent to locator to move locally
        cmds.parent(object,"LOC_origin")
        localSpace  = True
    else :
        finalCenterX = 0
        finalCenterY = 0
        finalCenterZ = 0
    
    # Position Objects
    if(moveXq):
        cmds.move( (random.uniform(minPosX,maxPosX)+finalCenterX), object, x=True, a=True, ls=localSpace )
    if(moveYq):
        cmds.move( (random.uniform(minPosY,maxPosY)+finalCenterY), object, y=True, a=True, ls=localSpace )
    if(moveZq):
        cmds.move( (random.uniform(minPosZ,maxPosZ)+finalCenterZ), object, z=True, a=True, ls=localSpace )
    # Rotate objects
    if(rotXq):
        cmds.rotate( (random.uniform(minRotX,maxRotX)), object, x=True, a=True)
    if(rotYq):
        cmds.rotate( (random.uniform(minRotY,maxRotY)), object, y=True, a=True)
    if(rotZq):
        cmds.rotate( (random.uniform(minRotZ,maxRotZ)), object, z=True, a=True)
    # Is the scale relative?       
    if relativeScale:
        scaleXOrigin = relativeScaleX[number]
        scaleYOrigin = relativeScaleY[number]
        scaleZOrigin = relativeScaleZ[number]
        cmds.scale( scaleXOrigin, scaleYOrigin, scaleZOrigin, object, a=True)
        if(scaleXq):
            cmds.scale( scaleXOrigin, object, x=True, a=True)
        if(scaleYq):
            cmds.scale( scaleYOrigin, object, y=True, a=True)
        if(scaleZq):
            cmds.scale( scaleZOrigin, object, z=True, a=True)
    # Scale objects     
    if unformScale:
        scaleX = random.uniform(minScaleX,maxScaleX)
        if(scaleXq):
            cmds.scale( scaleX, object, x=True, a=(1-relativeScale), r=relativeScale)
            scaleX = float(`cmds.getAttr(object+".sx")`)
            cmds.scale( scaleX, object, y=True, a=True)
            cmds.scale( scaleX, object, z=True, a=True)
    else:
        scaleX = random.uniform(minScaleX,maxScaleX)
        scaleY = random.uniform(minScaleY,maxScaleX)
        scaleZ = random.uniform(minScaleZ,maxScaleX)
        if(scaleXq):
            cmds.scale( scaleX, object, x=True, a=(1-relativeScale), r=relativeScale)
        if(scaleYq):
            cmds.scale( scaleY, object, y=True, a=(1-relativeScale), r=relativeScale)
        if(scaleZq):
            cmds.scale( scaleZ, object, z=True, a=(1-relativeScale), r=relativeScale)
    # Parent object under original parent
    if(cmds.optionMenu("placementType", q=True, v=True) == 'Use locators'): 
        # Check if previously had a prent or was parented to world
        if(parentQ==None):
            cmds.parent(object,w=True)
        else:
            cmds.parent(object,parentQ[0])
    
    
# ----------------------------------------------------
#                  PLACEMENT TYPE
# ----------------------------------------------------

def closeWindow(*args):
    # Close window
    cmds.deleteUI("randomPlacementUI")
    # If locators exist, delete them
    if(cmds.objExists("LOC_origin")==True):
        cmds.delete("LOC_origin")
   
# ----------------------------------------------------
#                  PLACEMENT TYPE
# ----------------------------------------------------

def togPlacementType(*args):
    if(cmds.optionMenu("placementType", q=True, v=True) == 'Use locators'):  
        # Disable menu options
        cmds.checkBox( "PositionXCheckbox", e=True, v=True, en=False)
        cmds.checkBox( "PositionYCheckbox", e=True, v=True, en=False)
        cmds.checkBox( "PositionZCheckbox", e=True, v=True, en=False)
        cmds.floatField( "minPosXSlider", e=True, en=False)
        cmds.floatField( "maxPosXSlider", e=True, en=False)
        cmds.floatField( "minPosYSlider", e=True, en=False)
        cmds.floatField( "maxPosYSlider", e=True, en=False)
        cmds.floatField( "minPosZSlider", e=True, en=False)
        cmds.floatField( "maxPosZSlider", e=True, en=False)
        # Create locators
        cmds.spaceLocator(n="LOC_origin")
        cmds.spaceLocator(n="LOC_height")
        cmds.spaceLocator(n="LOC_area")
        cmds.move( 10, "LOC_height", y=True)
        cmds.move( 10, 10, "LOC_area", x=True, z=True)
        # Create cube to represent area
        polycube = cmds.polyCube(n="LOC_cubeArea")
        cmds.rename(polycube[1], "LOC_cubeAreaPoly")
        # Lock and hide unused attributes
        cmds.setAttr("LOC_area.ty", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_area.rx", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_area.ry", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_area.rz", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_area.sx", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_area.sy", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_area.sz", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_area.v", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.tx", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.tz", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.rx", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.ry", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.rz", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.sx", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.sy", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.sz", lock=True, keyable=False, channelBox=False)
        cmds.setAttr("LOC_height.v", lock=True, keyable=False, channelBox=False)
        # Set transform limits
        cmds.transformLimits("LOC_area", tx=(0,10), etx=(1,0), tz=(0,1), etz=(1,0))
        cmds.transformLimits("LOC_height", ty=(0,10), ety=(1,0))
        # Make origin locator the parent
        cmds.parent("LOC_cubeArea","LOC_height","LOC_area","LOC_origin")
        # Make cube a template
        cmds.toggle("LOC_cubeArea",template=True, state=True) 
        # Create expression for size of cube
        cmds.expression(n="EXP_randPlacement", s="LOC_cubeArea.translateX = (LOC_area.translateX)/2;\nLOC_cubeArea.translateZ = (LOC_area.translateZ)/2;\nLOC_cubeArea.translateY = (LOC_height.translateY)/2;\n\nLOC_cubeAreaPoly.width = max(.001,LOC_area.translateX);\nLOC_cubeAreaPoly.depth = max(.001,LOC_area.translateZ);\nLOC_cubeAreaPoly.height = max(.001,LOC_height.translateY);")
        cmds.select(cl=True)
    else:  
        # No longer on "Use Locators", so delete locators
        if(cmds.objExists("LOC_origin")==True):
            cmds.delete("LOC_origin")
        # Enable menu options
        cmds.checkBox( "PositionXCheckbox", e=True, en=True)
        cmds.checkBox( "PositionYCheckbox", e=True, en=True)
        cmds.checkBox( "PositionZCheckbox", e=True, en=True)
        cmds.floatField( "minPosXSlider", e=True, en=True)
        cmds.floatField( "maxPosXSlider", e=True, en=True)
        cmds.floatField( "minPosYSlider", e=True, en=True)
        cmds.floatField( "maxPosYSlider", e=True, en=True)
        cmds.floatField( "minPosZSlider", e=True, en=True)
        cmds.floatField( "maxPosZSlider", e=True, en=True)


# ----------------------------------------------------
#                  DEFINE OBJECTS
# ----------------------------------------------------
    
def defineObjects(*args):
    # Set Variables
    global definedObjects
    del definedObjects[:]
    global relativeScaleX
    global relativeScaleY
    global relativeScaleZ
    del relativeScaleX[:]
    del relativeScaleY[:]
    del relativeScaleZ[:]
    
    # Test whether selected objects are transformable objects
    testObjects = cmds.ls(sl=True)
    for test in testObjects:
        # If current object is transformable, then add to defined list
        testObjectType = cmds.objectType(test)
        if(testObjectType=="transform" or \
           testObjectType=="joint" or \
           testObjectType=="cluster"):
                definedObjects[len(definedObjects):] = [test]
                # Record current scale values for relative scale
                relativeScaleX[(len(definedObjects)-1):] = [float(`cmds.getAttr(test+".sx")`)]
                relativeScaleY[(len(definedObjects)-1):] = [float(`cmds.getAttr(test+".sy")`)]
                relativeScaleZ[(len(definedObjects)-1):] = [float(`cmds.getAttr(test+".sz")`)]
    
    # Test if any moveable objects are in the final list
    if(len(definedObjects)==0):
        cmds.warning("No moveable objects selected")
        cmds.text("defineText", e=True, l="No objects defined", bgc=(.404,.188,.188), en=True)
    else:
        # Change textfield in window
        cmds.text("defineText", e=True, l="Objects Defined", bgc=(.188,.404,.188), en=True)
        cmds.select(cl=True) 

# ----------------------------------------------------
#                  TOGGLE CHECKBOXES
# ----------------------------------------------------

def togPosX(*args):
    if cmds.checkBox( "PositionXCheckbox", q=True, v=True) :
        cmds.floatField( "minPosXSlider", e=True, en=True)
        cmds.floatField( "maxPosXSlider", e=True, en=True)
    else :
        cmds.floatField( "minPosXSlider", e=True, en=False)
        cmds.floatField( "maxPosXSlider", e=True, en=False)

def togPosY(*args):
    if cmds.checkBox( "PositionYCheckbox", q=True, v=True) :
        cmds.floatField( "minPosYSlider", e=True, en=True)
        cmds.floatField( "maxPosYSlider", e=True, en=True)
    else :
        cmds.floatField( "minPosYSlider", e=True, en=False)
        cmds.floatField( "maxPosYSlider", e=True, en=False)
        
def togPosZ(*args):
    if cmds.checkBox( "PositionZCheckbox", q=True, v=True) :
        cmds.floatField( "minPosZSlider", e=True, en=True)
        cmds.floatField( "maxPosZSlider", e=True, en=True)
    else :
        cmds.floatField( "minPosZSlider", e=True, en=False)
        cmds.floatField( "maxPosZSlider", e=True, en=False)
#-----------------
def togRotX(*args):
    if cmds.checkBox( "rotationXCheckbox", q=True, v=True) :
        cmds.floatField( "minRotXSlider", e=True, en=True)
        cmds.floatField( "maxRotXSlider", e=True, en=True)
    else :
        cmds.floatField( "minRotXSlider", e=True, en=False)
        cmds.floatField( "maxRotXSlider", e=True, en=False)
        
def togRotY(*args):
    if cmds.checkBox( "rotationYCheckbox", q=True, v=True) :
        cmds.floatField( "minRotYSlider", e=True, en=True)
        cmds.floatField( "maxRotYSlider", e=True, en=True)
    else :
        cmds.floatField( "minRotYSlider", e=True, en=False)
        cmds.floatField( "maxRotYSlider", e=True, en=False)
        
def togRotZ(*args):
    if cmds.checkBox( "rotationZCheckbox", q=True, v=True) :
        cmds.floatField( "minRotZSlider", e=True, en=True)
        cmds.floatField( "maxRotZSlider", e=True, en=True)
    else :
        cmds.floatField( "minRotZSlider", e=True, en=False)
        cmds.floatField( "maxRotZSlider", e=True, en=False)    
#-----------------
def togScaleX(*args):
    if cmds.checkBox( "scaleXCheckbox", q=True, v=True) :
        cmds.floatField( "minScaleXSlider", e=True, en=True)
        cmds.floatField( "maxScaleXSlider", e=True, en=True)
    else :
        cmds.floatField( "minScaleXSlider", e=True, en=False)
        cmds.floatField( "maxScaleXSlider", e=True, en=False)
        
def togScaleY(*args):
    if cmds.checkBox( "scaleYCheckbox", q=True, v=True) :
        cmds.floatField( "minScaleYSlider", e=True, en=True)
        cmds.floatField( "maxScaleYSlider", e=True, en=True)
    else :
        cmds.floatField( "minScaleYSlider", e=True, en=False)
        cmds.floatField( "maxScaleYSlider", e=True, en=False)
        
def togScaleZ(*args):
    if cmds.checkBox( "scaleZCheckbox", q=True, v=True) :
        cmds.floatField( "minScaleZSlider", e=True, en=True)
        cmds.floatField( "maxScaleZSlider", e=True, en=True)
    else :
        cmds.floatField( "minScaleZSlider", e=True, en=False)
        cmds.floatField( "maxScaleZSlider", e=True, en=False)    
#-----------------
def togUniform(*args):
    if cmds.checkBox( "uniformScaleCheckbox", q=True, v=True) :
        cmds.floatField( "minScaleYSlider", e=True, en=False)
        cmds.floatField( "maxScaleYSlider", e=True, en=False)
        cmds.floatField( "minScaleZSlider", e=True, en=False)
        cmds.floatField( "maxScaleZSlider", e=True, en=False)
        cmds.checkBox( "scaleYCheckbox", e=True, en=False, v=False)
        cmds.checkBox( "scaleZCheckbox", e=True, en=False, v=False)
    else :
        cmds.floatField( "minScaleYSlider", e=True, en=True)
        cmds.floatField( "maxScaleYSlider", e=True, en=True)
        cmds.floatField( "minScaleZSlider", e=True, en=True)
        cmds.floatField( "maxScaleZSlider", e=True, en=True)
        cmds.checkBox( "scaleYCheckbox", e=True, en=True, v=True)
        cmds.checkBox( "scaleZCheckbox", e=True, en=True, v=True)           
#-----------------
def togKeepPos(*args):
    if cmds.checkBox( "seedCheckbox", q=True, v=True) :
        cmds.intField( "seedField", e=True, en=True)
        cmds.text("seedFieldTxt", e=True, en=True)
    else :
        cmds.intField( "seedField", e=True, en=False)
        cmds.text("seedFieldTxt", e=True, en=False)
#-----------------
def togIntersectSamples(*args):
    if cmds.checkBox( "intersectionsCheckbox", q=True, v=True) :
        cmds.intField( "samplesField", e=True, en=True)
        cmds.text("samplesFieldTxt", e=True, en=True)
    else :
        cmds.intField( "samplesField", e=True, en=False)
        cmds.text("samplesFieldTxt", e=True, en=False)
        

# ----------------------------------------------------
#                  CREATE WINDOW
# ----------------------------------------------------

def randomPlacement():
    
    if cmds.window("randomPlacementUI", ex=1):
        cmds.deleteUI("randomPlacementUI")
    # If placement locators exist, delete them
    if(cmds.objExists("LOC_origin")==True):
        cmds.delete("LOC_origin")
    # Clean defined objects
    global definedObjects
    del definedObjects[:]
    
    width=260
    height=200
    randomPlacementUI = cmds.window("randomPlacementUI", title = "Random Placement", s=False, wh = (width,height), 
                        titleBarMenu=False, rtf=True)
    
    # Define Variable inputs
    width1 = 87
    width2 = 50
    width3 = width-width1-width2-5
    cmds.columnLayout(rowSpacing=0)
    #----------------
    cmds.rowLayout( numberOfColumns=3, columnWidth3=[width1, width2, width3])
    cmds.text( label='  Select objects' )
    cmds.button("defineBut", l="Define", w=width2, c=defineObjects)
    cmds.text("defineText", width=width3, h=20, l="No objects defined", bgc=(.404,.188,.188) )
    cmds.setParent('..')
    #----------------
    width1 = 87
    width2 = 115
    cmds.rowLayout( numberOfColumns=2, columnWidth2=[width1, width2])
    cmds.text( label='  Placement Type' )
    cmds.optionMenu("placementType", width=width2, cc=togPlacementType)
    cmds.menuItem( label='Scene Origin')
    cmds.menuItem( label='Parent Origin')
    cmds.menuItem( label='Center of Objects' )
    cmds.menuItem( label='Use locators' )
    cmds.setParent('..')
    #----------------
    width1 = 102
    width2 = 20
    width3 = 90
    width4 = width-width1-width2-width3-7
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Keep Positions")
    cmds.checkBox("seedCheckbox", l="", v=False, cc=togKeepPos)
    cmds.text( "seedFieldTxt", l="Seed Value", al="right", en=False)
    cmds.intField( "seedField", minValue=0, maxValue=100, value=1, width=width4, en=False)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Stop Intersections")
    cmds.checkBox("intersectionsCheckbox", l="", v=False, cc=togIntersectSamples)
    cmds.text( "samplesFieldTxt", l="Intersect Samples", en=False)
    cmds.intField( "samplesField", minValue=1, maxValue=1024, value=1024, width=width4, en=False)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=1, w=width)
    cmds.separator( height=10, style='in', width=width)
    cmds.setParent('..')
    #----------------
    width1 = 70
    width2 = 75
    width3 = width2+11
    width4 = 10
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="", vis=False)
    cmds.text(l="     Min Value")
    cmds.text(l="     Max Value")
    cmds.text(l="", vis=False)
    cmds.setParent('..')
    #----------------
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Position X")
    cmds.floatField( "minPosXSlider", precision=2, value=-10, width=width2)
    cmds.floatField( "maxPosXSlider", precision=2, value=10, width=width2)
    cmds.checkBox("PositionXCheckbox", l="", v=True, cc=togPosX)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Position Y")
    cmds.floatField( "minPosYSlider", precision=2, value=-10, width=width2)
    cmds.floatField( "maxPosYSlider", precision=2, value=10, width=width2)
    cmds.checkBox("PositionYCheckbox", l="", v=True, cc=togPosY)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Position Z")
    cmds.floatField( "minPosZSlider", precision=2, value=-10, width=width2)
    cmds.floatField( "maxPosZSlider", precision=2, value=10, width=width2)
    cmds.checkBox("PositionZCheckbox", l="", v=True, cc=togPosZ)
    cmds.setParent('..')
    #----------------
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Rotation X")
    cmds.floatField( "minRotXSlider", precision=2, value=0, width=width2)
    cmds.floatField( "maxRotXSlider", precision=2, value=360, width=width2)
    cmds.checkBox("rotationXCheckbox", l="", v=True, cc=togRotX)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Rotation Y")
    cmds.floatField( "minRotYSlider", precision=2, value=0, width=width2)
    cmds.floatField( "maxRotYSlider", precision=2, value=360, width=width2)
    cmds.checkBox("rotationYCheckbox", l="", v=True, cc=togRotY)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Rotation Z")
    cmds.floatField( "minRotZSlider", precision=2, value=0, width=width2)
    cmds.floatField( "maxRotZSlider", precision=2, value=360, width=width2)
    cmds.checkBox("rotationZCheckbox", l="", v=True, cc=togRotZ)
    cmds.setParent('..')
    #----------------
    #----------------
    width1 = 72
    width2 = 70
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3+3, width4])
    cmds.text(l="  Uniform Scale", h=20)
    cmds.checkBox("uniformScaleCheckbox", l="", v=True, cc=togUniform)
    cmds.text(l="  Relative Scale", h=20)
    cmds.checkBox("relativeScaleCheckbox", l="", v=False)
    cmds.setParent('..')
    #----------------
    width1 = 70
    width2 = 75
    width3 = width2+11
    width4 = 10
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Scale X")
    cmds.floatField( "minScaleXSlider", minValue=0, maxValue=10, precision=2, value=.5, width=width2, en=True)
    cmds.floatField( "maxScaleXSlider", minValue=0, maxValue=10, precision=2, value=1, width=width2, en=True)
    cmds.checkBox("scaleXCheckbox", l="", v=True, cc=togScaleX)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Scale Y")
    cmds.floatField( "minScaleYSlider", minValue=0, maxValue=10, precision=2, value=.5, width=width2, en=False)
    cmds.floatField( "maxScaleYSlider", minValue=0, maxValue=10, precision=2, value=1, width=width2, en=False)
    cmds.checkBox("scaleYCheckbox", l="", v=False, en=False, cc=togScaleY)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=4, columnWidth4=[width1, width2, width3, width4])
    cmds.text(l="  Scale Z")
    cmds.floatField( "minScaleZSlider", minValue=0, maxValue=10, precision=2, value=.5, width=width2, en=False)
    cmds.floatField( "maxScaleZSlider", minValue=0, maxValue=10, precision=2, value=1, width=width2, en=False)
    cmds.checkBox("scaleZCheckbox", l="", v=False, en=False, cc=togScaleZ)
    cmds.setParent('..')
    #----------------
    #----------------
    cmds.rowLayout( numberOfColumns=1, w=width)
    cmds.separator( height=10, style='in', width=width)
    cmds.setParent('..')
    #----------------
    cmds.columnLayout(rowSpacing=4)
    cmds.rowLayout( numberOfColumns=1)
    cmds.button("moveBut", l="Move Objects!", c="moveObjectsTest()", width=width, height=50)
    cmds.setParent('..')
    #----------------
    cmds.rowLayout( numberOfColumns=1)
    cmds.button("closeBut", l="Close", c="closeWindow()", width=width)
    cmds.setParent('..')
    
    cmds.showWindow(randomPlacementUI)

