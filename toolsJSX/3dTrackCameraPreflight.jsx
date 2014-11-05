
// 3D_TrackedCamera_Preflight (formerly "PF Preflight"), version 3.5, by CR Green
// This script is a pre-flight type o' thing for working with .ma files
//  exported from the pixel farm's PFHoe (and other programs). It is meant to be used right after importing
//  one of those .ma files.
// This version includes a user interface for turning various options on or off
// v3 corrects a big bad boolean (faulty logic operation) which kept my progress window from showing up (via ugly brute force workaround)
// v3.2 fixes auto-close (and changed undo string)
//      and fixes cosmetic checkbox title problem
// v3.3 makes simple changes to outdated text strings
// v3.5 uses source for null finding, because it is better, and because syntheyes now exports differently. This
//   is better over-all, recognizing original null to be used as solid source by its nullLayer property,
//   AND we now keep original name of layer for each layer, which is  nice.
//   Also added progress bar, and made options dialog close earlier.

//globals:
var activeItem = app.project.activeItem;
var progStr = 'Starting ... ';
var undoStr = "3D Camera-track Preflight";
var shutAng = 180;
var shutPha = -90;
var trackerOpac = 60;
var colorArray = new Array([1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 0]);
var modeArray = new Array(BlendingMode.ADD, BlendingMode.SCREEN, BlendingMode.MULTIPLY, BlendingMode.OVERLAY, BlendingMode.DIFFERENCE);
var pal = new Window('palette', '',[300,50,590,132]);

//////// for timing tests /////////
var oldTime = "";
var newTime = "";
/////////////////////////////////

var uiWin = new Window('dialog', '3D Track Preflight Options',[300,200,740,539]);
var builtWin = buildTheUI();
if (builtWin != null) {
    builtWin.show();
}

function getRadioGroupSelected(groupArray, dialogRef, objRefBase) {
    v = groupArray[0];
    for (idx = 0; idx <= (groupArray.length-1); idx++) {
        currentValue = eval("dialogRef." + objRefBase + idx + ".value");
        if (currentValue) {
            v = groupArray[idx];
            break
        }
    }
    return v;
}

function bigHelp() {
    var bigHelpTxt = "PF Preflight Help\rIf all options are selected this script does the following:\r\r(1) Sorts all layers in the comp by their Z positions. " + 
    "Though optimized as much as possible, this usually takes a while. " +
    "This is very helpful for locating specific tracker layers. Also, bad trackers usually are in the extreme Z positions, so deleting those first is usually a good idea." +
    "\r\r(2) Replaces each tracker layer with a visible solid (at 60% opacity).\r\r(3) Changes the Shutter Angle and Shutter Phase to more agreeable values :-)." +
    "\r\r(3) Sets the \"Preserve framerate when nested\" switch on.\r\r(4) Corrects for change in framerate (30 back to 29.97 or 24 back to 23.976)." +
    "\r\r(5) Removes all unused footage. If the nulls were replaced with one solid source, the remaining unnecessary solid sources are deleted."+
    "\r----------------------------------------------\rSelect Red, Green, Blue, Cyan, Magenta or Yellow for the tracker color." +
    "\rFor tracker layer Transfer Mode, choose between Add, Screen, Multiply, Overlay and Difference." +
    "\rThese last two settings depend on the footage you are compositing the trackers against; choose settings that make the trackers nice and visible against " +
    "the footage.";
    alert(bigHelpTxt);
}

function doAbout() {
    var aboutTxt = "3D Track Preflight (v3.5)\rThis script is neat.";
    alert(aboutTxt);
}

function buildTheUI() {
    if (uiWin != null) {
        uiWin.solidCPnl = uiWin.add('panel', [17,165.5,423,220.5], 'Tracker Color:');
        uiWin.modePnl = uiWin.add('panel', [17,227.5,423,282.5], 'Tracker Transfer Mode:');
        uiWin.modeRad0 = uiWin.modePnl.add('radiobutton', [12.5,19,67.5,41], 'Add');
        uiWin.modeRad1 = uiWin.modePnl.add('radiobutton', [72.5,19,142.5,41], 'Screen');
        uiWin.modeRad1.value = true;
        
        uiWin.modeRad2 = uiWin.modePnl.add('radiobutton', [147.5,19,222.5,41], 'Multiply');
        uiWin.modeRad3 = uiWin.modePnl.add('radiobutton', [227.5,19,302.5,41], 'Overlay');
        uiWin.modeRad4 = uiWin.modePnl.add('radiobutton', [307.5,19,392.5,41], 'Difference');
        
        uiWin.colorRad0 = uiWin.solidCPnl.add('radiobutton', [26.5,20,81.5,42], 'R');
        uiWin.colorRad0.value = true;
        
        uiWin.colorRad1 = uiWin.solidCPnl.add('radiobutton', [86.5,20,141.5,42], 'G');
        uiWin.colorRad2 = uiWin.solidCPnl.add('radiobutton', [146.5,20,201.5,42], 'B');
        uiWin.colorRad3 = uiWin.solidCPnl.add('radiobutton', [206.5,20,261.5,42], 'C');
        uiWin.colorRad4 = uiWin.solidCPnl.add('radiobutton', [266.5,20,321.5,42], 'M');
        uiWin.colorRad5 = uiWin.solidCPnl.add('radiobutton', [326.5,20,381.5,42], 'Y');
        
        uiWin.nullRHuhBtn = uiWin.add('button', [17,10,47,32], '?', {name:'nullRHuhBtn'});
        uiWin.nullRHuhBtn.onClick = function () {displayHuh(0)};
        uiWin.nonSqHuhBtn = uiWin.add('button', [17,40,47,62], '?', {name:'nonSqHuhBtn'});
        uiWin.nonSqHuhBtn.onClick = function () {displayHuh(1)};
        uiWin.fpsHuhBtn = uiWin.add('button', [17,70,47,92], '?', {name:'fpsHuhBtn'});
        uiWin.fpsHuhBtn.onClick = function () {displayHuh(2)};
        uiWin.unusedHuhBtn = uiWin.add('button', [17,100,47,122], '?', {name:'unusedHuhBtn'});
        uiWin.unusedHuhBtn.onClick = function () {displayHuh(3)};
        uiWin.pftbugHuhBtn = uiWin.add('button', [17,130,47,152], '?', {name:'pftbugHuhBtn'});
        uiWin.pftbugHuhBtn.onClick = function () {displayHuh(4)};
        uiWin.pftbugHuhBtn.visible = false;
        uiWin.nullReplacCheck = uiWin.add('checkbox', [62,12,382,32], 'Replace Tracker Nulls with Single Solid source');
        uiWin.nonSqCheck = uiWin.add('checkbox', [62,42,382,62], 'Use \'Square/Non-Square Pixel\' comps model');
        uiWin.fpsCheck = uiWin.add('checkbox', [62,72,382,92], 'Change 30/24 fps back to 29.97/23.976 fps');
        uiWin.removeUnusedCheck = uiWin.add('checkbox', [62,102,382,122], 'Lastly, remove all unused footage');
        
        uiWin.nullReplacCheck.value = true; 
        uiWin.nonSqCheck.value = true; 
        uiWin.fpsCheck.value = true; 
        uiWin.removeUnusedCheck.value = true; 
        
        uiWin.pftrackBugCheck = uiWin.add('checkbox', [62,132,382,152], '--------------------------------');
        uiWin.pftrackBugCheck.visible = false;
        
        uiWin.helpBtn = uiWin.add('button', [16,301,96,323], 'Help', {name:'help'});
        uiWin.helpBtn.onClick = bigHelp;
        
        uiWin.cancBtn = uiWin.add('button', [250,301,330,323], 'Cancel', {name:'cancel'});
        uiWin.cancBtn.onClick = function () {this.parent.close(0)};
        
        uiWin.okBtn = uiWin.add('button', [344,301,424,323], 'OK', {name:'ok'});
        uiWin.okBtn.onClick = function () { main(this.parent); }; 
        
    }
    return uiWin
}

function displayHuh(thisOne) {
    var manyAlerts = new Array("When checked, each Null layer will be replaced with a script-designated Solid source and made visible. " + 
        "Layers are sorted by their Z positions regardless of this setting.", 
        "If importing the .ma project resulted in two comps, one square-pixels (the name of which starts with \"Square \") and one non-square pixels, you should check this. " +
        "Otherwise, only the selected comp will be affected.", "Tracked footage that is 29.97 frames per second results in exported .ma files that have fps at 30. " +
        "Similarly, 23.976 fps footage results in .ma projects at 24 fps. Checking this box will cause 30 fps and 24 fps comps to be changed back to their original and correct framerates " +
        "(which is actually important).", 
        "When checked, all unused footage will be removed from the project as the last stage " +
        "(choosing null-to-solid replacement -- the first checkbox -- results in a bunch of unused solid sources).", 
        "I ... um ... what?");
    alert(manyAlerts[thisOne]);
}

function buildProgBarWin()
//just a simple window that replaced my original Info window stuff.
//this way it always gives feedback
{   
    if (pal != null)
    {
        pal.mainPnl = pal.add('statictext', [10,6,268,30], 'Progress (Sort and Replace):');
        pal.progArea = pal.add("statictext", [21,27,268,43], progStr);
        pal.progBar = pal.add("progressbar", [21,52,268,68], 0, 100);
    }
    
    return pal;
}

//this is for the javascript sort method; it's for sorting numerically
function compareNums(a, b) {return a - b;}

//remove oneSolid here...
function sortAndReplace(comp_layers, p, doTheReplace, blendMode, trackerColor) {
    // alert('s and r');
    
    //do tracker make here now:
    for (o = 1; o <= comp_layers.length; o++) {
        var curLayer = comp_layers[o];
        if (curLayer.nullLayer) {
            var firstTrackername = curLayer.name;
            curLayer.source.name = " tracker";
            curLayer.name = firstTrackername;
            curLayer.source.mainSource.color = trackerColor;
            // alert('2');
            oneSolid = curLayer.source;
            // alert('3');
            break;
        }
		//**value at time zero
		//***false means ignore expression
	}
	
	zz = new Array;
	
	//collect all the z positions into an array:
	for (o = 1; o <= comp_layers.length; o++) {
	    var curLayer = comp_layers[o];
		//**value at time zero
		//***false means ignore expression
		zz[zz.length] = curLayer.property("Position").valueAtTime(0, false)[2];
	}
	
	//sort those z positions using built-in javascript 1.1 sort method
	//(compareNums function makes sorting numerical)
	zz = zz.sort(compareNums);
	allZs = zz.length;
	
	for (n = 0;n < allZs;n++) {
	    
	    if (p != null) {
	        p.progArea.text = ("Finding & moving layer " + n + " of " + allZs);
	        p.progBar.value = ( n * ( 100/(allZs) ) );
	    }
	    // I think usually, in v6.5 and 7, Windows does not update the progress window.
	    // Mac has this problem only in 7 (as far as I know)
	    // therefore, we want to pop the window on and off unless we are on Mac using ae6.5
	    // it is really an ugly workaround
	    ////   so ugly, in fact, that i'm commenting this crap out for v3.5+
	    //  if (  (system.osName != "MacOS") || (app.version.slice(0, 1) != "6") ) {
	    //     pal.hide();
	    //    pal.show();
	    //unfortunately this slows things down a bit (10-20%?)
	    // }
	    
	    foundOne = false;
	    thisZ = zz[n];
	    //	r is always one ahead of n because the array's first element is zero,
	    //	but the layers object's first element is one;
	    r=(n+1);
	    //	we increment r below because we need to ignore previous layers,
	    //	shorten the list on every pass
	    //now move layers with matching Z positions to top, in order of sorted array,
	    
	    while( !foundOne ) {
	        
	        if (thisZ == comp_layers[r].property("Position").valueAtTime(0, false)[2]) {
	            foundOne = true;
	            foundLayer = comp_layers[r];
	            
	            if (n == 0) {
	                foundLayer.moveToBeginning();
	            }else{
	                foundLayer.moveAfter(comp_layers[n]);
	            }
	            // make sure we've got the null-to-solid preferences set, and make sure we're not working on a layer that cannot be
	            // an adjustment layer (a camera, for example), and make sure the layer is 3D (perhaps the footage was brought in to the comp)
	            if ( doTheReplace && ( (foundLayer.adjustmentLayer != undefined) && (foundLayer.threeDLayer) ) ) {
	                layerForBlendChange = replaceWithOneSolid(foundLayer, oneSolid);
	                //put blendmode here
	            } else {
	                layerForBlendChange = foundLayer;
	            }
	            layerForBlendChange.blendingMode = blendMode;
	        }else{
	            
	            r=(r+1);
	            
	            //just a safeguard in case, for some bizarre reason, no match is found between thisZ and all layers' z positions:
	            if (r > allZs) { foundOne=true; }
	        }
	    }
	}
	
}//function sortAndReplace

function replaceWithOneSolid(doomedLayer, s) {
	//quite a bit of overhead here, but what the heck
	//add solid to comp (put it in the right place - right after doomedLayer
    var origLaName = doomedLayer.name;
	layerCollObj = activeItem.layers;
	replLayer = layerCollObj.add(s);
	replLayer.moveAfter(doomedLayer);
	//make it 3D
	replLayer.threeDLayer = true;
	//take doomedLayer's important properties
	po=doomedLayer.property("Position").value;
	sc=doomedLayer.property("Scale").value;
	
	replLayer.property("Position").setValue(po);
	replLayer.property("Scale").setValue(sc);
	replLayer.property("Anchor Point").setValue([0, 0, 0]);
	replLayer.property("Opacity").setValue(trackerOpac);
	replLayer.name = origLaName;
	//kill doomed layer
	doomedLayer.remove();
	return replLayer;
}

function startTime(){
    d = new Date();
    oldTime = d.getTime();
}

function endTime(){
    d = new Date();
    newTime = d.getTime();
    return ((newTime - oldTime)/1000);
}
////////////////////////////////////////////////////////
////////////////////////////////////////////////////////
function main(optionsDialog)
{
    var trackerColor = getRadioGroupSelected(colorArray, optionsDialog, "colorRad");
    var trackerMode = getRadioGroupSelected(modeArray, optionsDialog, "modeRad");
    var sp = "";
    if (optionsDialog.nonSqCheck.value) {
        sp = "(square-pixel) ";
    }
    
	// make sure a comp is selected
	if (activeItem == null || !(activeItem instanceof CompItem)){
		alert("You need to select one " + sp + "comp first.");
	} else {
		compSelName = activeItem.name;
		if ( (optionsDialog.nonSqCheck.value) && (compSelName.length < 8) ) {
			alert("Cannot continue: comp name too short!");
		} else {
			compNameHead = compSelName.slice(0, 7);
            if ( optionsDialog.nonSqCheck.value && (compNameHead != "Square ") ) {
                alert("Cannot continue; selected comp name should start with \"Square \".");
            }else{
                compPxAsp = activeItem.pixelAspect;
                
                if (compPxAsp == 1) {
                    app.beginUndoGroup(undoStr);
                    nonSqCompName = compSelName.slice(7, compSelName.length);
                    //// we must loop through comps and find one that matches
                    var nonSqComp = null;
                    for (i = 1; i <= app.project.numItems; ++i) { //for/next loop goes through all Items
                        
                        var curItem = app.project.item(i);
                        if (curItem instanceof CompItem) { //test if current item is a composition
                            thisName = curItem.name;
                            if ((thisName == nonSqCompName) && (curItem.pixelAspect != 1)) {
                                nonSqComp = curItem;
                                break;
                            }
                        }
                    }
                    
                    if ( (nonSqComp == null) && (optionsDialog.nonSqCheck.value) ) {
                        alert("Could not find non-square pixel comp called \"" + nonSqCompName + "\". Cannot continue.");
                    } else {
                        
                        ///change shutter angle and phase
                        activeItem.shutterAngle = shutAng;
                        activeItem.shutterPhase = shutPha;
                        
                        cfr = activeItem.frameRate;
                        
                        if ( optionsDialog.fpsCheck.value ) {
                            if (cfr == 30) {
                                activeItem.frameRate = 29.97;
                                if (optionsDialog.nonSqCheck.value) {nonSqComp.frameRate = 29.97;}
                                activeItem.preserveNestedFrameRate = true;
                            } else if (cfr == 24) {
                                activeItem.frameRate = 23.976;
                                if (optionsDialog.nonSqCheck.value) {nonSqComp.frameRate = 23.976;}
                            } else {
                                alert("Unrecognized Frame Rate. Will continue ... ");
                            }
                        }
                        var nullReplBool = optionsDialog.nullReplacCheck.value;
                        optionsDialog.close();
                        
                        var palette = buildProgBarWin();
                        if (palette != null) {
                        palette.show(); }
                        
                        activeCompLayers = activeItem.layers;
                        startTime();
                        sortAndReplace(activeCompLayers, palette, nullReplBool, trackerMode, trackerColor);
                        if (palette != null) {palette.close();}
                        alert( (endTime()) + " seconds." )
                        if (optionsDialog.removeUnusedCheck.value) {
                            app.project.removeUnusedFootage();
                        }
                        
                    }
                    app.endUndoGroup();
                    //////////////////////////////
                } else {
                    alert("That comp is not the right Pixel Aspect Ratio! Cannot continue.");
                }
            }
		}
	}
}
