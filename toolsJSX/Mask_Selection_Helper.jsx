
// Mask Selection Helper
// by CR Green
// a palette that helps in selecting masks

var win = new Window('palette', 'Mask Selection Helper',[300,100,543,260]);
var w = buildUI();
if (w != null) {
   w.show();
}

function prelimCheck() {
   var ok = false;
   if (app.project != null) {
      if (app.project.activeItem != null) {
         if (app.project.activeItem instanceof CompItem) {
            aComp = app.project.activeItem;
            layerCol = aComp.layers;
            numOfLayers = layerCol.length;
            if (numOfLayers != 0) {
               maskSum = 0;
               for (row = 1; row <= numOfLayers; row++) {
                  thisL = layerCol[row];
                  var itsMasks = thisL.property("Masks");
                  // nonmaskable layer returns null
                  if (itsMasks != null) {
                     var mskNum = itsMasks.numProperties;
                     var maskSum = (maskSum + mskNum);
                  }
               }
               if (maskSum != 0) {
                  ok = true;
               }
            }
         }
      }
   }
   return ok;
}

function doSelectByName(searchStr) {
   if (prelimCheck()) {
      var allLayers = app.project.activeItem.layers;
      var layerLim = allLayers.length;
      for (n = 1; n <= layerLim; n++) {
         var thisRo = allLayers[n];
         // if it's locked, ignore it
         if (!thisRo.locked && (thisRo.property("Masks") != null) ) {
            var itsMasks = thisRo.property("Masks");
            var mskNum = itsMasks.numProperties;
            for (mIdx = 1; mIdx <= mskNum; mIdx++) {
               m = itsMasks(mIdx);
               mNa = m.name;
               if ( mNa.indexOf(searchStr) != -1) {
                  m.selected = true;
               }
            }
         }
      }
   } else {
      // nothin!
   }
}

function doSelectByIndex(theIndex) {
   if (prelimCheck()) {
      theIndex = parseFloat(theIndex);
      var allLayers = app.project.activeItem.layers;
      var layerLim = allLayers.length;
      for (n = 1; n <= layerLim; n++) {
         var thisRo = allLayers[n];
         // if it's locked, ignore it
         if (!thisRo.locked && (thisRo.property("Masks") != null) ) {
            var itsMasks = thisRo.property("Masks");
            var mskNum = itsMasks.numProperties;
            for (mIdx = 1; mIdx <= mskNum; mIdx++) {
               if (mIdx == (theIndex) ) {
                  itsMasks(mIdx).selected = true;
               }
            }
         }
      }
   } else {
      // nothin!
   }
   
}

function buildUI() {
   if (win != null) {
      win.upperPnl = win.add('panel', [7.5,29,235.5,88], '');
      win.lowerPnl = win.add('panel', [7.5,93,235.5,152], '');
      win.winNameLbl = win.add('statictext', [8,7,236,25], 'Select from all masks in comp ... ');
      win.winNameLbl.justify = "center";
      win.byNameLbl = win.add('statictext', [18,36,128,58], 'by name (empty = all):');
      win.byNameLbl.justify = "center";
      win.byNameT = win.add('edittext', [18,59,128,81], '');
      win.byIndexLbl = win.add('statictext', [18,99,128,121], 'by index:');
      win.byIndexLbl.justify = "center";
      win.dnBtn = win.add('button', [19,122,49,142], '<', {name:'<'});
      win.dnBtn.name = "<";
      win.dnBtn.onClick = function () { changeIndex(this, this.parent); };
      win.indexLbl = win.add('statictext', [53,125,93,147], '1');
      win.indexLbl.justify = "center";
      win.upBtn = win.add('button', [96,122,126,142], '>', {name:'>'});
      win.upBtn.name = ">";
      win.upBtn.onClick = function () { changeIndex(this, this.parent); };
      win.byNameBtn = win.add('button', [143,47,223,69], ' Select', {name:'selectN'});
      win.byNameBtn.onClick = function () { doSelectByName(this.parent.byNameT.text); };
      win.byIndexBtn = win.add('button', [143,110,223,132], 'Select', {name:'selectI'});
      win.byIndexBtn.onClick = function () { doSelectByIndex(this.parent.indexLbl.text); };
   }
   return win
}

function changeIndex(theButton, pal) {
   if (theButton.name == "<") {
      i = parseFloat(pal.indexLbl.text);
      if (i != 1) {
         i = (i - 1);
         pal.indexLbl.text = i;
      }
   }else{
      i = parseFloat(pal.indexLbl.text);
      i = (i + 1);
      pal.indexLbl.text = i;
   }
}
