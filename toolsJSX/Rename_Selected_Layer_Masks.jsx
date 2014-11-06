
// by CR Green
// Requested by Lukas v. Monkiewitsch
// v1.1 replaces dangerous parseInts with parseFloats (because of radix feature in parseInt)
// v1.2 fixes tail-not-being-removed bug
vers = "1.2";
var win = new Window('palette', 'Mask Rename (v' + vers + ')',[300,100,645,396]);
var w = buildUI();
if (w != null) {
    w.show();
}

function mainMaskOperation(theDialog) {
    var ok = false;
    if (app.project != null) {
        if (app.project.activeItem != null) {
            if (app.project.activeItem instanceof CompItem) {
                aComp = app.project.activeItem;
                var selectedLayers = aComp.selectedLayers;
                var selNum = aComp.selectedLayers.length;
                if (selNum == 1) {
                    maskSum = 0;
                    thisL = selectedLayers[0];
                    var itsMasks = thisL.property("Masks");
                    // nonmaskable layer returns null
                    ok = true;
                    if ((thisL.property("Masks") != null) ) {
                        var itsMasks = thisL.property("Masks");
                        var mskNum = itsMasks.numProperties;
                        inputError = false;
                        app.beginUndoGroup("mask rename");
                        n = 0;
                        for (mIdx = 1; mIdx <= mskNum; mIdx++) {
                            
                            if ( itsMasks(mIdx).selected == true ) {
                                item = itsMasks(mIdx);
                                
                                //if the mask is selected, operate upon't
                                sear = theDialog.nameSearchT.text;
                                repl = theDialog.nameReplaceT.text;
                                oldName = item.name;
                                newName = oldName;
                                if (theDialog.repRad.value) {
                                    newName = splitReplace(newName, sear, repl);
                                    //alert(newName);
                                    //now we check for pre-cs4 app version, for which we truncate:
                                    if ((parseFloat(app.version) < 9.0)) { newName=(newName.substr(0,25));}
                                } else if (theDialog.appRad.value) {
                                    newName=(sear + oldName + repl );
                                } else if (theDialog.remRad.value) {
                                    
                                    
                                    if (sear == "") {sear = 0;}
                                    if (repl == "") {repl = 0;}
                                    sear = ( parseInt(sear) );
                                    repl = ( parseInt(repl) );
                                    if ( (isNaN(sear)) || (isNaN(repl)) ) {
                                        alert('Error: Not a number?');
                                        inputError = true;
                                    } else {
                                        newName=(newName.substr( sear, oldName.length ));
                                        newName=(newName.substr( 0, newName.length-repl ));
                                        sear="";
                                        repl="";
                                    }
                                    
                                } else if (theDialog.numRad.value) {
                                    stNum = theDialog.startNumT.text;
                                    byNum = theDialog.countNumT.text;
                                    
                                    if (stNum == "") {stNum = 0;}
                                    if ( (byNum == "") || (byNum == 0) ) {byNum = "NaN";}
                                    stNum = ( parseInt(stNum) );
                                    byNum = ( parseInt(byNum) );
                                    if ( (isNaN(stNum)) || (isNaN(byNum)) ) {
                                        alert('Error: Not a number, or invalid number to count by.');
                                        inputError = true;
                                    } else {
                                        h = theDialog.nameSearchT.text;
                                        t = theDialog.nameReplaceT.text;
                                        numNum = ((n * byNum) + stNum);
                                        newName = (h + numNum.toString() + t);
                                        //now we check for pre-cs4 app version and we error if name too long:
                                        if ((parseFloat(app.version) < 9.0)) {
                                            if (newName.length > 25) {
                                                inputError = true ;
                                                // this generates 'error', at beginning of loop,
                                                // which is largest number (highest number)
                                                alert('Error: Name too long.');
                                            }
                                        }
                                        sear="";
                                        repl="";
                                        stNum="";
                                        byNum="";
                                    }
                                }
                                
                                if (! inputError) { 
                                    item.name = newName;
                                    item.selected = false;
                                    item.selected = true;
                                }
                                n = (n + 1);
                            }//if mask selected
                        }// mask loop
                        app.endUndoGroup();
                        
                    }
                }
            }
        }
        return ok;
    }
}

///////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////

function buildUI() {
    if (win != null) {
        win.nameSearchLabel = win.add('statictext', [14,15,314,37], 'Search in Names:');
        win.nameSearchT = win.add('edittext', [25,40,325,62], '');
        win.nameReplaceLabel = win.add('statictext', [14,73,314,95], 'Replace with:');
        win.nameReplaceT = win.add('edittext', [25,98,325,120], '');
        win.typePnl = win.add('panel', [16,138,206,268], 'Rename Type:');
        win.progLbl = win.add('statictext', [20,271,206,308], '');
        
        win.repRad = win.typePnl.add('radiobutton', [14,13,174,35], 'Search and Replace');
        win.repRad.value = true;
        win.repRad.onClick = function () {
            doTextChange(win.nameSearchLabel, 'Search in Names:');
            doTextChange(win.nameReplaceLabel, 'Replace with:');
            
            doViz(win.startNumLabel, true);
            doViz(win.startNumT, true);
            doViz(win.countNumLabel, true);
            doViz(win.countNumT, true);
        };
        win.appRad = win.typePnl.add('radiobutton', [14,39,174,61], 'Append');
        win.appRad.onClick = function () {
            doTextChange(win.nameSearchLabel, 'Append Head with:');
            doTextChange(win.nameReplaceLabel, 'Append Tail with:');
            doViz(win.startNumLabel, true);
            doViz(win.startNumT, true);
            doViz(win.countNumLabel, true);
            doViz(win.countNumT, true);
        };
        win.remRad = win.typePnl.add('radiobutton', [14,65,174,87], 'Remove # of Characters');
        win.remRad.onClick = function () {
            doTextChange(win.nameSearchLabel, 'Remove this many chars from head (number):');
            doTextChange(win.nameReplaceLabel, 'Remove this many chars from tail (number):');
            doViz(win.startNumLabel, true);
            doViz(win.startNumT, true);
            doViz(win.countNumLabel, true);
            doViz(win.countNumT, true);
            
        };
        win.numRad = win.typePnl.add('radiobutton', [14,90,174,112], 'Number');
        win.numRad.onClick = function () {
            doTextChange(win.nameSearchLabel, 'String BEFORE number (or blank):');
            doTextChange(win.nameReplaceLabel, 'String AFTER number (or blank):');
            doViz(win.startNumLabel, false);
            doViz(win.startNumT, false);
            doViz(win.countNumLabel, false);
            doViz(win.countNumT, false);
            
        };
        
        win.startNumLabel = win.add('statictext', [225,143,270,165], 'Start #:');
        win.startNumLabel.visible = false;
        win.startNumT = win.add('edittext', [279,140,324,162], '0');
        win.startNumT.visible = false;
        win.countNumLabel = win.add('statictext', [225,176,281,198], 'Count by:');
        win.countNumLabel.visible = false;
        win.countNumT = win.add('edittext', [290,173,324,195], '1');
        win.countNumT.visible = false;
        
        win.okBtn = win.add('button', [240,245,320,267], 'OK', {name:'OK'});
        win.okBtn.onClick = function () { mainMaskOperation(this.parent); };
        
        win.cancBtn = win.add('button', [240,210,320,232], 'Close', {name:'Cancel'});
        win.cancBtn.onClick = function () {this.parent.close(1)};
        
    }
    return win
}

function doTextChange(target, newText) {
    target.text = newText;
}

function doViz(target, bool) {
    target.visible = !bool;
}

function splitReplace(st, ss, rs) {
    var stArray = st.split(ss);
    var patchedString = "";
    var i = 0;
    while (i < (stArray.length)) {
        if (i == (stArray.length-1)) {rs = "";}
        patchedString = (patchedString + (stArray[i] + rs) );
        i = (i + 1);
    }
    //  alert(patchedString);
    return patchedString
}


