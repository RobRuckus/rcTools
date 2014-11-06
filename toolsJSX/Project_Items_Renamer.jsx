
//version 1.9 brings code up-to-date to work as dockable, if desired, and makes window more compact
var vers = '1.9';

function buildUI(this_obj_) {
    var win = (this_obj_ instanceof Panel)
    ? this_obj_
    : new Window('palette', 'Rename Project Items (v' + vers + ')',[300,100,524,362+22]);
    
    win.nameSearchLabel = win.add('statictext', [14,15,314,37], 'Search in Names:');
    win.nameSearchT = win.add('edittext', [25,40,325-125,62], '');
    win.nameReplaceLabel = win.add('statictext', [14,73,314,95], 'Replace with:');
    win.nameReplaceT = win.add('edittext', [25,98,325-125,120], '');
    win.typePnl = win.add('panel', [16,138,206,243], 'Rename Type:');
    
    win.repRad = win.typePnl.add('radiobutton', [14,13,174,35], 'Search and Replace');
    win.repRad.value = true;
    win.repRad.onClick = function () {
        doTextChange(win.nameSearchLabel, 'Search in Names:');
        doTextChange(win.nameReplaceLabel, 'Replace with:');
    };
    win.appRad = win.typePnl.add('radiobutton', [14,39,174,61], 'Append');
    win.appRad.onClick = function () {
        doTextChange(win.nameSearchLabel, 'Append Head with:');
        doTextChange(win.nameReplaceLabel, 'Append Tail with:');
    };
    win.remRad = win.typePnl.add('radiobutton', [14,65,174,87], 'Remove # of Characters');
    win.remRad.onClick = function () {
        doTextChange(win.nameSearchLabel, 'Remove from head (number):');
        doTextChange(win.nameReplaceLabel, 'Remove from tail (number):');
    };
    //[16,138,206,243]
    win.okBtn = win.add('button', [140,253,140+66,253+20], 'OK', {name:'OK'});
    win.okBtn.onClick = function () { doRenaming(this.parent); };
    
    win.cancBtn = win.add('button', [16,253,16+77,253+20], 'Close', {name:'Cancel'});
    win.cancBtn.onClick = function () {this.parent.close(1)};
    win.cancBtn.visible = false;
    
    return win
}
var w = buildUI(this);
if (w.toString() == "[object Panel]") {
    w;
} else {
    w.show();
    w.cancBtn.visible = true;
}

function doTextChange(target, newText) {
    target.text = newText;
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
    return patchedString
}

function doRenaming(theDialog) {
    // make sure comps are selected
    var everyItem = app.project.items;
    selectedObs = new Array();
    for (var i = everyItem.length; i >= 1; i--) {
        eyeTem = everyItem[i];
        if (eyeTem.selected) {
            selectedObs[selectedObs.length] = eyeTem;
        }
    }
    
    if ( selectedObs.length == 0 ) {
        alert("No Project Items selected.");
    } else {
        var s = selectedObs;
        var selNum = s.length;
        
        app.beginUndoGroup("the renaming of project items");
        var inputError = false;
        
        for (var n = (selNum-1); n >= 0; n--) {
            if ( ! inputError ) {
                item = s[n];
                oldName = item.name;
                sear = theDialog.nameSearchT.text;
                repl = theDialog.nameReplaceT.text
                newName = oldName;
                
                if (theDialog.repRad.value) {
                    newName = splitReplace(newName, sear, repl);
                    if ((parseFloat(app.version) < 9.0)) {newName=(newName.substr(0,31));}
                } else if (theDialog.appRad.value) {
                    newName=(sear + oldName + repl );
                } else if (theDialog.remRad.value) {
                    
                    if (sear == "") {sear = 0;}
                    if (repl == "") {repl = 0;}
                    sear = ( parseFloat(sear) );
                    repl = ( parseFloat(repl) );
                    if ( (isNaN(sear)) || (isNaN(repl)) ) {
                        alert('Error: Not a number?');
                        inputError = true;
                    } else {
                        newName=(newName.substr( sear, oldName.length ));
                        newName=(newName.substr( 0, newName.length-repl ));
                        sear="";
                        repl="";
                    }
                    
                }
                //////////////////////
                try {
                    item.name = newName;
                } catch (error ) {
                    // just ignore errors; if it can't be named, what the hay
                }
                sear="";
                repl="";
                //////////////////////
            }
        }
        app.endUndoGroup();
    }
}