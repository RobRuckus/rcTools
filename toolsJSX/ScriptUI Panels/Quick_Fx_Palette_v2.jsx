﻿////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  Quick_Fx_Palette 1.2     by Fred CRETET
//  This script apply effects ( my "favorite" ) with button bar like Fusion or Nuke
// fcretet aaat gmail dooot com
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// edit the arrays "But_01",... for customize the script


var But_01=["Fst Blr",			// text on button, max is 7 char
					"fx",				// fx or preset
					"Fast Blur",		//exact effect name or preset path (copy the name in effects pallette in AE)
					"Blurriness",		// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurriness is "0" , to modify more one property you could create a  preset)
					9];					//custom property value for fx
					
var But_02=["Gs Blr",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Gaussian Blur",		//exact effect name or preset path (copy the name in effects pallette in AE)
					"Blurriness",		// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
					6];					//custom property value for fx

var But_03=["R F Blr",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"CC Radial Fast Blur",		//exact effect name or preset path (copy the name in effects pallette in AE)
					"Zoom",		// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
					2];					//custom property value for fx

var But_04=["Rd Flik",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Reduce Interlace Flicker",		//exact effect name or preset path (copy the name in effects pallette in AE)
					"Softness",		// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
					0.7];				//custom property value for fx

var But_05=["Level",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Levels (Individual Controls)"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx

var But_06=["Hue.Sat",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Hue/Saturation"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx

var But_07=["Curves",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Curves"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx

var But_08=["Tint",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Tint"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx
															
var But_09=["Keylight",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Keylight (1.2)"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx	

var But_10=["Extract",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Extract"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx															

var But_11=["Invert",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Invert"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx
var But_12=["Mchoke",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Matte Choker"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx
var But_13=["Schoke",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Simple Choker"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx	

var But_14=["Glow",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Glow"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx
															
var But_15=["Fill",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Fill",		//exact effect name or preset path (copy the name in effects pallette in AE)
					"Color",		// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
					[255,255,255]];				//custom property value for fx

var But_16=["Ramp",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Ramp"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx

var But_17=["FNoise",			// text on button,  max is 7 char
					"fx",				// fx or preset
					"Fractal Noise"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx
///// Preset exemple !
var But_18=["601 to RGB",			// text on button,  max is 7 char
					"preset",				// fx or preset
					"C:/Program Files (x86)/Adobe/Adobe After Effects CS4/Support Files/Presets/Image - Utilities/Levels - video to computer.ffx"];	//exact effect name or preset path (copy the name in effects pallette in AE)
															// custom property name only for fx (if you want to modify one default property for exemple the fast blur blurruness is "0" , to modify more one property you could create a  preset)
															//custom property value for fx
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

{
   var myPanel;
   function Quick_fx_palette(thisObj) {
      myPanel = (thisObj instanceof Panel) ? thisObj : new Window("palette", "Fx_palette", [100, 100, 300, 300]);
      //Jeff Almasol's solution to fix text color
      var winGfx = myPanel.graphics;
      var darkColorBrush = winGfx.newPen(winGfx.BrushType.SOLID_COLOR, [0,0,0], 1);

     myPanel.but_01 = myPanel.add("button", [10, 5, 50, 25], But_01[0]);
	 myPanel.but_02 = myPanel.add("button", [60, 5, 100, 25], But_02[0]);
	 myPanel.but_03 = myPanel.add("button", [110, 5, 150, 25], But_03[0]);
	 myPanel.but_04 = myPanel.add("button", [160, 5, 200, 25], But_04[0]);
	 
	// myPanel.sep = myPanel.add("staticText", [210, 10, 220, 25], "|");	 
	 
	 myPanel.but_05 = myPanel.add("button", [225, 5, 265, 25], But_05[0]);
	 myPanel.but_06 = myPanel.add("button", [273, 5, 317, 25], But_06[0]);
	 myPanel.but_07 = myPanel.add("button", [325, 5, 365, 25], But_07[0]);
	 myPanel.but_08 = myPanel.add("button", [375, 5, 415, 25], But_08[0]);
	 
	// myPanel.sep2 = myPanel.add("staticText", [425, 10, 435, 25], "|");	 
	 
	 myPanel.but_09 = myPanel.add("button", [438, 5, 482, 25], But_09[0]);
	 myPanel.but_10 = myPanel.add("button", [490, 5, 530, 25], But_10[0]);
	 myPanel.but_11 = myPanel.add("button", [540, 5, 580, 25], But_11[0]);
	 myPanel.but_12 = myPanel.add("button", [590, 5, 630, 25], But_12[0]);
	 myPanel.but_13 = myPanel.add("button", [640, 5, 680, 25], But_13[0]);
	 
	// myPanel.sep3 = myPanel.add("staticText", [690, 10, 695, 25], "|");	 
	 
	 myPanel.but_14 = myPanel.add("button", [705, 5, 745, 25], But_14[0]);
	 myPanel.but_15 = myPanel.add("button", [755, 5, 795, 25], But_15[0]);	 
	 myPanel.but_16 = myPanel.add("button", [805, 5, 845, 25], But_16[0]);	 
	 myPanel.but_17 = myPanel.add("button", [855, 5, 895, 25], But_17[0]);	 
	 myPanel.but_18 = myPanel.add("button", [905, 5, 965, 25], But_18[0]);
	 
     myPanel.but_01.onClick =ApplyFx01;
	 myPanel.but_02.onClick =ApplyFx02;
	 myPanel.but_03.onClick =ApplyFx03;
	 myPanel.but_04.onClick =ApplyFx04;
	 
	 myPanel.but_05.onClick =ApplyFx05;
	 myPanel.but_06.onClick =ApplyFx06;
	 myPanel.but_07.onClick =ApplyFx07; 
	 myPanel.but_08.onClick =ApplyFx08;
	 
	 myPanel.but_09.onClick =ApplyFx09;
	 myPanel.but_10.onClick =ApplyFx10;
	 myPanel.but_11.onClick =ApplyFx11; 
	 myPanel.but_12.onClick =ApplyFx12;
	 myPanel.but_13.onClick =ApplyFx13;
	 
	 myPanel.but_14.onClick =ApplyFx14;
	 myPanel.but_15.onClick =ApplyFx15;
	 myPanel.but_16.onClick =ApplyFx16;
	 myPanel.but_17.onClick =ApplyFx17;
	 myPanel.but_18.onClick =ApplyFx18;
	 
      return myPanel;

}

function ApplyFx01(){
	if(But_01[01]=="fx")
		{
			ApplyFx(But_01[2],But_01[3],But_01[4]);
		}
	if(But_01[01]=="preset")
		{
			ApplyPresetbutton(But_01[2]);
		}

}

function ApplyFx02(){
	if(But_02[01]=="fx")
		{
			ApplyFx(But_02[2],But_02[3],But_02[4]);
		}
	if(But_02[01]=="preset")
		{
			ApplyPresetbutton(But_02[2]);
		}

}

function ApplyFx03(){
	if(But_03[01]=="fx")
		{
			ApplyFx(But_03[2],But_03[3],But_03[4]);
		}
	if(But_03[01]=="preset")
		{
			ApplyPresetbutton(But_02[2]);
		}

}

function ApplyFx04(){
	if(But_04[01]=="fx")
		{
			ApplyFx(But_04[2],But_04[3],But_04[4]);
		}
	if(But_04[01]=="preset")
		{
			ApplyPresetbutton(But_04[2]);
		}

}

function ApplyFx05(){
	if(But_05[01]=="fx")
		{
			ApplyFx(But_05[2],But_05[3],But_05[4]);
		}
	if(But_05[01]=="preset")
		{
			ApplyPresetbutton(But_05[2]);
		}

}

function ApplyFx06(){
	if(But_06[01]=="fx")
		{
			ApplyFx(But_06[2],But_06[3],But_06[4]);
		}
	if(But_06[01]=="preset")
		{
			ApplyPresetbutton(But_06[2]);
		}

}

function ApplyFx07(){
	if(But_07[01]=="fx")
		{
			ApplyFx(But_07[2],But_07[3],But_07[4]);
		}
	if(But_07[01]=="preset")
		{
			ApplyPresetbutton(But_07[2]);
		}

}

function ApplyFx08(){
	if(But_08[01]=="fx")
		{
			ApplyFx(But_08[2],But_08[3],But_08[4]);
		}
	if(But_08[01]=="preset")
		{
			ApplyPresetbutton(But_08[2]);
		}

}

function ApplyFx09(){
	if(But_09[01]=="fx")
		{
			ApplyFx(But_09[2],But_09[3],But_09[4]);
		}
	if(But_09[01]=="preset")
		{
			ApplyPresetbutton(But_09[2]);
		}

}

function ApplyFx10(){
	if(But_10[01]=="fx")
		{
			ApplyFx(But_10[2],But_10[3],But_10[4]);
		}
	if(But_10[01]=="preset")
		{
			ApplyPresetbutton(But_10[2]);
		}

}

function ApplyFx11(){
	if(But_11[01]=="fx")
		{
			ApplyFx(But_11[2],But_11[3],But_11[4]);
		}
	if(But_11[01]=="preset")
		{
			ApplyPresetbutton(But_11[2]);
		}

}

function ApplyFx12(){
	if(But_12[01]=="fx")
		{
			ApplyFx(But_12[2],But_12[3],But_12[4]);
		}
	if(But_12[01]=="preset")
		{
			ApplyPresetbutton(But_12[2]);
		}

}

function ApplyFx13(){
	if(But_13[01]=="fx")
		{
			ApplyFx(But_13[2],But_13[3],But_13[4]);
		}
	if(But_13[01]=="preset")
		{
			ApplyPresetbutton(But_13[2]);
		}

}

function ApplyFx14(){
	if(But_14[01]=="fx")
		{
			ApplyFx(But_14[2],But_14[3],But_14[4]);
		}
	if(But_14[01]=="preset")
		{
			ApplyPresetbutton(But_14[2]);
		}

}

function ApplyFx15(){
	if(But_15[01]=="fx")
		{
			ApplyFx(But_15[2],But_15[3],But_15[4]);
		}
	if(But_15[01]=="preset")
		{
			ApplyPresetbutton(But_15[2]);
		}

}

function ApplyFx16(){
	if(But_16[01]=="fx")
		{
			ApplyFx(But_16[2],But_16[3],But_16[4]);
		}
	if(But_16[01]=="preset")
		{
			ApplyPresetbutton(But_16[2]);
		}

}

function ApplyFx17(){
	if(But_17[01]=="fx")
		{
			ApplyFx(But_17[2],But_17[3],But_17[4]);
		}
	if(But_17[01]=="preset")
		{
			ApplyPresetbutton(But_17[2]);
		}

}

function ApplyFx18(){
	if(But_18[01]=="fx")
		{
			ApplyFx(But_18[2],But_18[3],But_18[4]);
		}
	if(But_18[01]=="preset")
		{
			ApplyPresetbutton(But_18[2]);
		}

}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function ApplyFx(Effect_Name,CustomProperty,CustomValue){
	app.beginUndoGroup("Apply Fx");
	if ((app.project.activeItem == null) || ((app.project.activeItem != null) && !(app.project.activeItem instanceof CompItem)))
		{
		}
	else
		{
				var comp = app.project.activeItem;
				var layerCollection = comp.selectedLayers;
				for (idx=0;idx<layerCollection.length;idx++)
					{
						if(CustomProperty==null){
							layerCollection[idx].Effects.addProperty(Effect_Name);
						}
						else{
							layerCollection[idx].Effects.addProperty(Effect_Name).property(CustomProperty).setValue(CustomValue);
						}
					}
		}
	app.endUndoGroup();
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function ApplyPresetbutton(PresetPath){
	app.beginUndoGroup("Apply Preset");
	 var myPreset = File(PresetPath);
	if ((app.project.activeItem == null) || ((app.project.activeItem != null) && !(app.project.activeItem instanceof CompItem)))
		{
		}
	else
		{
				var comp = app.project.activeItem;
				var layerCollection = comp.selectedLayers;
				for (idx=0;idx<layerCollection.length;idx++)
					{						
							layerCollection[idx].applyPreset(myPreset);
						
					}
		}
	app.endUndoGroup();
}


 Quick_fx_palette(this); 
 }
