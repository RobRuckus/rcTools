{  

// THIS IS MY MODIFIED VERSION for Maya 2015 and above
// Modified at the UI.main.browseButton.onClick function to fix the file save dialog bug
// Modified the ktv attribute writing code to be written so as if there is only 1 value in the array then the setAttr is written with ktv[0] instead of ktv[1:1]

/*------------------------*/    
function initGlobals(G)
/*------------------------*/ 
{
	G.RET = "\r"; 
//-------------------------------------------------------------------------------------------- About info    
	G.ABOUT = "AE3D Export, v1.16 (2008)" 											+ G.RET +
				"exports the selected layers and cameras within"					+ G.RET +
				"the work area to Maya, 3ds Max, or Lightwave."					+ G.RET + G.RET +
				
				"by Ryan Gilmore (www.urbanspaceman.net)"							+ G.RET + G.RET +
				
				"with coding help from Nab (www.nabscripts.com)" 					+ G.RET + 
				"and others on the AE Enhancers forum (www.aenhancers.com)"		;
//---------------------------------------------------------------------------------------- Global Variables    
	G.APP_VERSION 			= parseFloat(app.version);
	G.FILE_FOLDER				= "~/Desktop";
	G.FILE_NAME				= "Untitled.ma";
	G.FILE_PATH				= G.FILE_FOLDER + "/" + G.FILE_NAME;
	G.FILE_PATH_SET			= false;

	G.RADIOBUTTON_ON			= 1;
	
	G.WORLD_CENTER			= [0,0,0];
	G.WORLD_SCALE				= [1, 0.0254, 1];

	G.RATIO					= [0.8592, 0.9, 0.9481481, 1.0, 1.0186, 1.0667, 1.2, 1.333, 1.4222, 1.5, 1.8962962, 2];
	// [0]D2 NTSC, [1]D1 NTSC, [2]D4 Stan, [3]SQUARE, [4]D2 PAL, [5]D1 PAL, [6]D1 NTSC wide, [7]HDV, [8]D1 PAL wide, [9]DVCPROHD, [10]D4 Ana, [11]Ana2:1
	G.ORIGINAL_ASPECT		= 1;
	G.HEIGHT					= ""; // set dynamically
	G.WIDTH					= ""; // set dynamically
	G.MAYA_FB_H				= 1; 
	G.FPS_NAME				= ["ntsc", "pal", "film", "game", "show", "ntscf", "palf"];
	
	G.LAYER_TYPE				= "Layer";
	G.LAYER_WAS_2D			= false;
	G.LAYER_IS_ANIMATED		= [false, false, false, false, false, false, false, false, false, false];
	G.LAYER_ORIG_NAMES		= [];
	G.LAYER_NAMES				= [];
	G.LAYER_NAME_MATCH		= false;
	G.LAYER_NAME_TOO_LONG 	= false;
	G.LAYER_NAME				= ""; // set dynamically
	G.SHORT_LAYER_NAME 	 	= ""; // set dynamically
	G.SCENE_STRING			= ""; // set dynamically
	G.LAYER_KEYS_STRING 	= ""; // set dynamically
//--------------------------------------------------------------------------------------------- Alert messages
	G.SAFE_DUR			= 180; // 3 minutes
	G.SAFE_DUR_WNG 		= "Warning. The composition work area exceeds " + G.SAFE_DUR + " seconds. Do you want to continue ?";      
}

/*------------------------*/    
function initUI(UI)
/*------------------------*/
{
	if (app.project.file != null)
	{
		fullProjectName=File.decode(app.project.file.name);
		projectName=fullProjectName.substring(0,fullProjectName.lastIndexOf("."));
		G.FILE_NAME = projectName + ".ma";
		G.FILE_PATH = G.FILE_FOLDER + "/" + G.FILE_NAME;
	}
	
	UIunit=10;
	UIwidth=275;
	UIheight=UIunit*28;
	
//------------------------------------------------------------------------------------- main interface draw

	UI.main = new Window('palette', '', [0,0,UIwidth,UIheight]);
	
	UI.main.name=UI.main.add('statictext', [UIunit,UIunit*1.5,UIwidth-(UIunit*17),UIunit*3], "AE3D EXPORT");
	UI.main.optionsButton=UI.main.add('button', [UIwidth-(UIunit*16)-5,UIunit-2,UIwidth-(UIunit*9),UIunit*3+2], "Options");
	UI.main.aboutButton=UI.main.add('button', [UIwidth-(UIunit*8),UIunit-2,UIwidth-UIunit,UIunit*3+2], "About");
	UI.main.add('panel' ,[UIunit,UIunit*4,UIwidth-UIunit,UIunit*4+4], "");
	
//Export to
	UI.main.add('statictext' ,[UIunit*2+2,UIunit*5+5,UIwidth-UIunit,UIunit*7], "Export to:");
	UI.main.MAYA=UI.main.add('radiobutton', [UIunit*2,UIunit*7+5,UIwidth/3-UIunit,UIunit*10], "Maya");
	UI.main.MAX=UI.main.add('radiobutton', [UIwidth/3-UIunit,UIunit*7+5,UIwidth*(2/3)-(UIunit*2),UIunit*10], "3ds Max");
	UI.main.LW=UI.main.add('radiobutton', [UIwidth*(2/3)-(UIunit*2),UIunit*7+5,UIwidth-(UIunit*2),UIunit*10], "Lightwave");
	UI.main.MAYA.value=true;
	
//Save as
	UI.main.add('statictext', [UIunit*2+2,UIunit*12,UIwidth-UIunit,UIunit*14-5], "Save as:");
	UI.main.fileName=UI.main.add('edittext', [UIunit*2,UIunit*14+8,UIwidth-(UIunit*10),UIunit*16+8], G.FILE_NAME);
	UI.main.browseButton=UI.main.add('button', [UIwidth-(UIunit*9),UIunit*14+5,UIwidth-(UIunit*2),UIunit*17], "Browse");
	UI.main.add('panel' ,[UIunit,UIunit*11,UIwidth-UIunit,UIunit*11+1], "");
	UI.main.add('panel' ,[UIunit,UIunit*11,UIunit+1,UIunit*18], "");
	UI.main.add('panel' ,[UIunit,UIunit*18,UIwidth-UIunit,UIunit*18+1], "");
	UI.main.add('panel' ,[UIwidth-UIunit,UIunit*11,UIwidth-UIunit+1,UIunit*18], "");

//Export button
	UI.main.exportButton=UI.main.add('button', [UIunit,UIunit*19+5,UIwidth-UIunit,UIunit*22+5], "Export");

//progress
	UI.main.progress=UI.main.add('statictext', [UIunit*2+2,UIunit*25-2,UIwidth-(UIunit*3),UIunit*26+5], "");
	UI.main.progress.text="Ready.";
	UI.main.add('panel' ,[UIunit,UIunit*24,UIwidth-UIunit,UIunit*24+1], "");
	UI.main.add('panel' ,[UIunit,UIunit*24,UIunit+1,UIunit*27], "");
	UI.main.add('panel' ,[UIunit,UIunit*27,UIwidth-UIunit,UIunit*27+1], "");
	UI.main.add('panel' ,[UIwidth-UIunit,UIunit*24,UIwidth-UIunit+1,UIunit*27], "");
	
//------------------------------------------------------------------------------------- options interface draw

	UI.options = new Window('palette', '', [0,0,UIwidth,UIunit*23]); 
	
	UI.options.name=UI.options.add('statictext', [UIunit,UIunit*1.5,UIwidth-(UIunit*8),UIunit*3], "AE3D EXPORT : Options");
	
//Shift Center
	UI.options.add('panel' ,[UIunit,UIunit*4,UIwidth-UIunit,UIunit*4+1], "");
	UI.options.add('panel' ,[UIunit,UIunit*4,UIunit+1,UIunit*7+5], "");
	UI.options.originShift=UI.options.add('checkbox', [UIunit*2,UIunit*5,UIwidth-(UIunit*3),UIunit*6+5], "shift the comp center to 0,0,0");
	UI.options.originShift.value = true;
	UI.options.add('panel' ,[UIwidth-UIunit,UIunit*4,UIwidth-UIunit+1,UIunit*7+7], "");
	UI.options.add('panel' ,[UIunit,UIunit*7+5,UIwidth-UIunit,UIunit*7+6], "");
	
//Scale scene
	UI.options.scaleSlider = UI.options.add('scrollbar', [UIunit,UIunit*12,UIwidth-UIunit,UIunit*13+5], 0, -4, 4);
	UI.options.scaleSlider.value = -2;
	UI.options.sliderValDisplay = UI.options.add('statictext', [UIunit*2+2,UIunit*9,UIwidth-UIunit,UIunit*10+5], "");
	UI.options.sliderValDisplay.text = "world scale set at 1 : " + Math.pow(10, UI.options.scaleSlider.value);

//Extra Maya cameras
	UI.options.add('panel' ,[UIunit,UIunit*15,UIwidth-UIunit,UIunit*15+1], "");
	UI.options.add('panel' ,[UIunit,UIunit*15,UIunit+1,UIunit*18+5], "");
	UI.options.extraMayaCams=UI.options.add('checkbox', [UIunit*2,UIunit*16,UIwidth-(UIunit*3),UIunit*17+5], "add 4 views for new Maya scene");
	UI.options.extraMayaCams.value = true;
	UI.options.add('panel' ,[UIwidth-UIunit,UIunit*15,UIwidth-UIunit+1,UIunit*18+7], "");
	UI.options.add('panel' ,[UIunit,UIunit*18+5,UIwidth-UIunit,UIunit*18+6], "");

//Close button
	UI.options.closeButton=UI.options.add('button', [UIwidth-(UIunit*8),UIunit*19+5,UIwidth-UIunit,UIunit*22], "Close");


//------------------------------------------------------------------------------ user interface functionality
	UI.main.center();
	UI.main.show();

//About button
	UI.main.aboutButton.onClick = function()
	{
		UI.main.progress.text="Ready.";
		alert(G.ABOUT);
	}
	
//Options button
	UI.main.optionsButton.onClick = function()
	{
		UI.main.progress.text="Ready.";
		UI.options.center();
		UI.main.visible = false;
		UI.options.show();
		
	}

//radio buttons
	UI.main.MAYA.onClick = function ()
	{
		UI.main.progress.text="Ready.";
		G.FILE_NAME = G.FILE_NAME.substring(0,G.FILE_NAME.lastIndexOf(".")) + ".ma";
		UI.main.fileName.text = G.FILE_NAME;
		G.RADIOBUTTON_ON = 1;
		G.FILE_PATH = G.FILE_FOLDER + "/" + G.FILE_NAME;
	}
	UI.main.MAX.onClick = function ()
	{
		UI.main.progress.text="Ready.";
		G.FILE_NAME = G.FILE_NAME.substring(0,G.FILE_NAME.lastIndexOf(".")) + ".ms";
		UI.main.fileName.text = G.FILE_NAME;
		G.RADIOBUTTON_ON = 2;
		G.FILE_PATH = G.FILE_FOLDER + "/" + G.FILE_NAME;
	}
	UI.main.LW.onClick = function ()
	{
		UI.main.progress.text="Ready.";
		G.FILE_NAME = G.FILE_NAME.substring(0,G.FILE_NAME.lastIndexOf(".")) + ".lws";
		UI.main.fileName.text = G.FILE_NAME;
		G.RADIOBUTTON_ON = 3;
		G.FILE_PATH = G.FILE_FOLDER + "/" + G.FILE_NAME;
	}
	
//Save As box
	UI.main.fileName.onChange = function ()
	{
		UI.main.progress.text="Ready.";
		G.FILE_NAME = UI.main.fileName.text
		G.FILE_NAME = addSuffixIfMissing(G.FILE_NAME);
		UI.main.fileName.text = G.FILE_NAME;
		G.FILE_PATH = G.FILE_FOLDER + "/" + G.FILE_NAME;
	}	
	
//"Browse" button for saving file
	UI.main.browseButton.onClick = function ()
	{
//        alert("working");
		UI.main.progress.text="Ready.";
//		G.FILE_PATH = filePutDialog ("Save the exported file as...", UI.main.fileName.text, "");
//		G.FILE_PATH = Folder.selectDialog("Save the exported file as...", UI.main.fileName.text, "");
		G.FILE_PATH = File.saveDialog ("Save the exported file as...");
		if (G.FILE_PATH != null) // if user entered new info, update the path
		{
			G.FILE_FOLDER = G.FILE_PATH.path;
			G.FILE_NAME = G.FILE_PATH.name;
			G.FILE_NAME = addSuffixIfMissing(G.FILE_NAME);
			G.FILE_PATH = G.FILE_FOLDER + "/" + G.FILE_NAME;
			UI.main.fileName.text = G.FILE_NAME;
			G.FILE_PATH_SET = true;
		}
		else // if user presses cancel
		{
			G.FILE_PATH = G.FILE_FOLDER + "/" + G.FILE_NAME;
		}
	}
	
//Export button
	
	UI.main.exportButton.onClick = function ()
	{
		UI.main.progress.text="Ready.";
		G.FILE_NAME = UI.main.fileName.text;
		if (File(G.FILE_PATH).exists == true && G.FILE_PATH_SET == false)
		{
			var overwrite = confirm("Overwrite item named \"" + File(G.FILE_PATH).name + "\" ?");
			if (overwrite==true) 
			{	
				UI.main.progress.text="Processing...";
				UI.main.hide();
				UI.main.show();
				main();
			}
			else // user said no, don't overwrite
			{
				return
			}
		}
		else
		{	
			UI.main.progress.text="Processing...";
			G.FILE_PATH_SET = false;
			UI.main.hide();
			UI.main.show();
			main();
		}
	}
	
//Options window
	UI.options.onClose = function()
	{
		UI.main.visible = true;
	}
//Origin shift check box
	UI.options.originShift.onClick = function ()
	{
		UI.main.progress.text="Ready.";
	}	

//Scale Slider
	UI.options.scaleSlider.onChange = function ()
	{
		UI.main.progress.text="Ready.";
		UI.options.scaleSlider.value = Math.round(UI.options.scaleSlider.value);
		UI.options.sliderValDisplay.text = "world scale set at 1 : " + Math.pow(10, UI.options.scaleSlider.value);
		
	}	
//Options Close button
	UI.options.closeButton.onClick = function ()
	{
		UI.main.progress.text="Ready.";
		UI.options.close();
		UI.main.visible = true;
	}
	
}	

/*---------------------------------------------------------------------------------------------------------    
 SUBROUTINES
---------------------------------------------------------------------------------------------------------*/

/*-------------------------------------*/
function radiansToDegrees(r) 
/*-------------------------------------*/
{
	return r * (180 / Math.PI);
}

/*---------------------------------------*/
function degreesToRadians(d) 
/*----------------------------------------*/
{
	return d * ( Math.PI / 180 );
}
    
/*-----------------------------------------------------*/
function removeForbiddenCharacters(str) 
/*-----------------------------------------------------*/
{
	FirstChar=str.charAt(0);
	if (FirstChar>"0" && FirstChar<"9") {str="L" + str};
	return str.replace(/[^a-zA-Z0-9]+/g,""); 
}

/*------------------------------------------*/
function addSuffixIfMissing (Str)
/*-------------------------------------------*/
{
	if (Str.indexOf(".") == -1)
	{
		var suffix = "";
		if (G.RADIOBUTTON_ON == 1)			{suffix=".ma"}
		else if (G.RADIOBUTTON_ON == 2)	{suffix=".ms"}
		else									{suffix=".lws"};
		Str = Str + suffix;
	}
	return (Str);
}

/*-----------------------------------------*/   
function storeOriginalLayerNames (selLayers)
/*-----------------------------------------*/
{
	for (var i=0; i<selLayers.length; i++)
	{
		var layer = selLayers[i];
		G.LAYER_ORIG_NAMES[i] = layer.name;
	}
}
/*----------------------------------------*/   
function checkForBadLayerNames (selLayers)
/*----------------------------------------*/
{
	// shorten long names
	for (var i=0; i<selLayers.length; i++)
	{
		var layer = selLayers[i];
		if (layer.name.length > 15)
		{
			layer.name = layer.name.substring(0,15);
			G.LAYER_NAME_TOO_LONG = true;
		}
	}
	// get rid of duplicate names
	var NumMatches = 0;
	for (var i=0; i<selLayers.length; i++) 
	{
		var layer = selLayers[i];
		G.LAYER_NAMES[i] = layer.name;
	}
	for (var i=0; i<selLayers.length; i++) 
	{
		var heroLayer = G.LAYER_NAMES[i];
		for (j=0;j<selLayers.length;j++)
		{
			if (heroLayer == G.LAYER_NAMES[j]) {NumMatches += 1}
		}
	}
	if (NumMatches > selLayers.length)
	{
		G.LAYER_NAME_MATCH = true;
		for (var i=0; i<selLayers.length; i++) 
		{
			selLayers[i].name = selLayers[i].name + "CC" + (i+1);
		}
	}
}

/*-----------------------------------*/   
function restoreLayerNames (selLayers)
/*-----------------------------------*/
{
	if (G.LAYER_NAME_MATCH == true || G.LAYER_NAME_TOO_LONG == true)
	{
		for (var i=0; i<selLayers.length; i++) 
		{
			selLayers[i].name = G.LAYER_ORIG_NAMES[i] ;
		}
	}
}

/*-----------------------------*/    
function getTotalFrames(comp)
/*-----------------------------*/    
{
	return (comp.workAreaDuration / comp.frameDuration);   
}

/*----------------------------------------*/    
function getFrameAspect()
/*----------------------------------------*/    
{
	return (Math.round(G.WIDTH * G.ORIGINAL_ASPECT)) / G.HEIGHT;
}

/*-------------------------------*/    
function getPreciseCompPAR(comp)
/*-------------------------------*/    
{
	var compPAR;
	switch (comp.pixelAspect) 
	{
		case 0.86:
			compPAR = G.RATIO[0];
			break;
		case 0.9:
			compPAR = G.RATIO[1];
			break;            
		case 0.95:
			compPAR = G.RATIO[2];
			break;
		case 1.0:
			compPAR = G.RATIO[3];
			break;
		case 1.02:
			compPAR = G.RATIO[4];
			break;
		case 1.07:
			compPAR = G.RATIO[5];
			break;
		case 1.2:
			compPAR = G.RATIO[6];
			break;
		case 1.33:
			compPAR = G.RATIO[7];
			break;
		case 1.42:
			compPAR = G.RATIO[8];
			break;
		case 1.5:
			compPAR = G.RATIO[9];
			break;
		case 1.9:
			compPAR = G.RATIO[10];
			break;
		case 2:
			compPAR = G.RATIO[11];
			break;
		default:
			compPAR = comp.pixelAspect;
		break;
	}
	return compPAR
}

/*----------------------------*/    
function getFPSName(comp)
/*----------------------------*/    
{
	var fpsName;
	switch (comp.frameRate)
	{
		case 30:
			fpsName = G.FPS_NAME[0];
			break;
		case 25:
			fpsName = G.FPS_NAME[1];
			break;
		case 24:
			fpsName = G.FPS_NAME[2];
			break;
		case 15:
			fpsName = G.FPS_NAME[3];
			break;
		case 48:
			fpsName = G.FPS_NAME[4];
			break;
		case 60:
			fpsName = G.FPS_NAME[5];
			break;
		case 50:
			fpsName = G.FPS_NAME[6];
			break;
		default:
			fpsName = G.FPS_NAME[0];
			break;
	}
	return fpsName;
}

/*-------------------------------------------------*/
function getFLenOrFOVorZFacFromZoom(comp, zoomVal)
/*-------------------------------------------------*/
{
	var compPAR = getPreciseCompPAR(comp);
	var frameAspect = getFrameAspect(); 
	var hFOV = Math.atan((0.5 * comp.width * compPAR) / zoomVal);
        
	if (G.RADIOBUTTON_ON == 1) // focal length (Maya)
	{
		var mayaFB = frameAspect * G.MAYA_FB_H; 
		return 25.4 * ((0.5 * mayaFB) / Math.tan(hFOV));
	}
	else if (G.RADIOBUTTON_ON == 2)  // fov (MAX)
	{
		return 2 * radiansToDegrees(hFOV);    
	}
	else if (G.RADIOBUTTON_ON == 3) // zoom factor (Lightwave)
	{
		return frameAspect / Math.tan(hFOV);
	}
}

/*-------------------------------------------------*/
function nonSquareToSquare (comp)
/*-------------------------------------------------*/
{
	if (G.ORIGINAL_ASPECT != 1)
	{
		var WorldCenterNull = comp.layers.addNull(comp.duration);
		WorldCenterNull.name = "WorldCenter";
		WorldCenterNull.startTime = 0;
		for (i=2;i<=comp.numLayers;i++)
		{
			if (comp.layer(i).parent == null)
			{
				comp.layer(i).parent = WorldCenterNull;
			}
		}
		var squareWidth = Math.round( G.WIDTH * G.ORIGINAL_ASPECT );
		comp.width = squareWidth;
		comp.pixelAspect = 1;
		WorldCenterNull.position.setValue([squareWidth/2, comp.height/2]);
	}
}

/*-------------------------------------------------*/
function squareToNonSquare (comp)
/*-------------------------------------------------*/
{
	if (G.ORIGINAL_ASPECT != 1)
	{
		comp.layer("WorldCenter").position.setValue([G.WIDTH/2, comp.height/2]);
		comp.pixelAspect = G.ORIGINAL_ASPECT;
		comp.width = G.WIDTH;
		comp.layer("WorldCenter").remove();
	}
}

/*-------------------------------------------------*/
function checkLayerType(layer)
/*-------------------------------------------------*/
{
	if (layer.zoom != null)
	{
		G.LAYER_TYPE="Camera";
	}
	else if (layer.property("Intensity") != null)
	{
		G.LAYER_TYPE="Light";
	}
	else
	{
		G.LAYER_TYPE="Layer";
		if (layer.threeDLayer == false) 
		{
			layer.threeDLayer = true;
			G.LAYER_WAS_2D = true;
		}
	}
}

/*------------------------*/
function DataContainer()
/*------------------------*/
{
	var data = new Object();

	data.xpos   = ""; // Maya and Lightwave, one parameter at a time
	data.ypos   = ""; 
	data.zpos   = ""; 
	data.xscal  = "";
	data.yscal  = ""; 
	data.zscal  = "";
	data.xrot   = ""; 
	data.yrot   = ""; 
	data.zrot   = "";
	
	data.flen   = ""; 
 
	data.keys   = ""; // Max, all paramerters one frame at a time

	return data;
}

/*--------------------------------------------------------------------------------------------*/
function collectValueAtCurrentTime_ZYX_Camera (comp, layerCopy, layerCopyParent, t)
/*--------------------------------------------------------------------------------------------*/
{
	var temp_xpos  = layerCopyParent.position.valueAtTime(t, false)[0];
	var temp_ypos  = layerCopyParent.position.valueAtTime(t, false)[1];
	var temp_zpos  = layerCopyParent.position.valueAtTime(t, false)[2];
	var temp_xscal = 100;
	var temp_yscal = 100;
	var temp_zscal = 100;
	var temp_xrot  = layerCopy.rotationX.valueAtTime(t, false);
	var temp_yrot  = layerCopy.orientation.valueAtTime(t, false)[1];
	var temp_zrot  = layerCopyParent.rotationZ.valueAtTime(t, false);
	var temp_flen  = getFLenOrFOVorZFacFromZoom(comp, layerCopy.zoom.valueAtTime(t, false) / (layerCopyParent.scale.valueAtTime(t, false)[0]/100) );
	return [temp_xpos, temp_ypos, temp_zpos, temp_xscal, temp_yscal, temp_zscal, temp_xrot, temp_yrot, temp_zrot, temp_flen];
}

/*--------------------------------------------------------------------------------------------*/
function collectValueAtCurrentTime_ZYX_Layer (comp, layerCopy, layerCopyParent, t)
/*--------------------------------------------------------------------------------------------*/
{
	var temp_xpos  = layerCopyParent.position.valueAtTime(t, false)[0];
	var temp_ypos  = layerCopyParent.position.valueAtTime(t, false)[1];
	var temp_zpos  = layerCopyParent.position.valueAtTime(t, false)[2];
	var temp_xscal = layerCopy.scale.valueAtTime(t, false)[0];
	var temp_yscal = layerCopy.scale.valueAtTime(t, false)[1];
	var temp_zscal = layerCopy.scale.valueAtTime(t, false)[2];
	var temp_xrot  = layerCopy.rotationX.valueAtTime(t, false);
	var temp_yrot  = layerCopy.orientation.valueAtTime(t, false)[1];
	var temp_zrot  = layerCopyParent.rotationZ.valueAtTime(t, false);
	var temp_flen  = "";
	return [temp_xpos, temp_ypos, temp_zpos, temp_xscal, temp_yscal, temp_zscal, temp_xrot, temp_yrot, temp_zrot, temp_flen];
}

/*--------------------------------------------------------------------------------------------*/
function collectValueAtCurrentTime_YXZ_Camera (comp, layerCopy, layerCopyParent, t)
/*--------------------------------------------------------------------------------------------*/
{
	var temp_xpos  = layerCopyParent.position.valueAtTime(t, false)[0];
	var temp_ypos  = layerCopyParent.position.valueAtTime(t, false)[1];
	var temp_zpos  = layerCopyParent.position.valueAtTime(t, false)[2];
	var temp_xscal = 100;
	var temp_yscal = 100;
	var temp_zscal = 100;
	var temp_xrot  = layerCopy.rotationX.valueAtTime(t, false);
	var temp_yrot  = layerCopy.orientation.valueAtTime(t, false)[1];
	var temp_zrot  = layerCopy.rotationZ.valueAtTime(t, false);
	var temp_flen  = getFLenOrFOVorZFacFromZoom(comp, layerCopy.zoom.valueAtTime(t, false) / (layerCopyParent.scale.valueAtTime(t, false)[0]/100) );
	return [temp_xpos, temp_ypos, temp_zpos, temp_xscal, temp_yscal, temp_zscal, temp_xrot, temp_yrot, temp_zrot, temp_flen];
}

/*--------------------------------------------------------------------------------------------*/
function collectValueAtCurrentTime_YXZ_Layer (comp, layerCopy, layerCopyParent, t)
/*--------------------------------------------------------------------------------------------*/
{
	var temp_xpos  = layerCopyParent.position.valueAtTime(t, false)[0];
	var temp_ypos  = layerCopyParent.position.valueAtTime(t, false)[1];
	var temp_zpos  = layerCopyParent.position.valueAtTime(t, false)[2];
	var temp_xscal = layerCopy.scale.valueAtTime(t, false)[0];
	var temp_yscal = layerCopy.scale.valueAtTime(t, false)[1];
	var temp_zscal = layerCopy.scale.valueAtTime(t, false)[2];
	var temp_xrot  = layerCopy.rotationX.valueAtTime(t, false);
	var temp_yrot  = layerCopy.orientation.valueAtTime(t, false)[1];
	var temp_zrot  = layerCopy.rotationZ.valueAtTime(t, false);
	var temp_flen  = "";
	return [temp_xpos, temp_ypos, temp_zpos, temp_xscal, temp_yscal, temp_zscal, temp_xrot, temp_yrot, temp_zrot, temp_flen];
}

/*--------------------------------------------------------------------------------------------*/
function storeValueAtCurrentTime_Maya (data, frameCounter, layerState, worldScale)
/*--------------------------------------------------------------------------------------------*/
{
	if (G.LAYER_IS_ANIMATED[0] == true || frameCounter == 1) {data.xpos  += frameCounter + " " + (layerState[0] - G.WORLD_CENTER[0]) * worldScale + " ";};
	if (G.LAYER_IS_ANIMATED[1] == true || frameCounter == 1) {data.ypos  += frameCounter + " " + (-(layerState[1] - G.WORLD_CENTER[1])) * worldScale + " ";};
	if (G.LAYER_IS_ANIMATED[2] == true || frameCounter == 1) {data.zpos  += frameCounter + " " + (-layerState[2]) * worldScale + " ";};
	if (G.LAYER_IS_ANIMATED[3] == true || frameCounter == 1) {data.xscal += frameCounter + " " + layerState[3]*0.572957782866373 + " ";};
	if (G.LAYER_IS_ANIMATED[4] == true || frameCounter == 1) {data.yscal += frameCounter + " " + layerState[4]*0.572957782866373 + " ";};
	if (G.LAYER_IS_ANIMATED[5] == true || frameCounter == 1) {data.zscal += frameCounter + " " + layerState[5]*0.572957782866373 + " ";};		
	if (G.LAYER_IS_ANIMATED[6] == true || frameCounter == 1) {data.xrot  += frameCounter + " " + layerState[6] + " ";};
	if (G.LAYER_IS_ANIMATED[7] == true || frameCounter == 1) {data.yrot  += frameCounter + " " + (-layerState[7]) + " ";};
	if (G.LAYER_IS_ANIMATED[8] == true || frameCounter == 1) {data.zrot  += frameCounter + " " + (-layerState[8]) + " "; };
	if (G.LAYER_IS_ANIMATED[9] == true || frameCounter == 1) {data.flen  += frameCounter + " " + layerState[9] + " ";};
}

/*--------------------------------------------------------------------------------------------*/
function storeValueAtCurrentTime_Max (data, frameCounter, layerState, worldScale)
/*--------------------------------------------------------------------------------------------*/
{
	var xpos  = (layerState[0] - G.WORLD_CENTER[0]) * worldScale;
	var ypos	= (-(layerState[1] - G.WORLD_CENTER[1])) * worldScale;
	var zpos	= -layerState[2] * worldScale;
	var xscal	= layerState[3] / 100;
	var yscal	= layerState[4] / 100;
	var zscal	= layerState[5] / 100;
	var xrot 	= layerState[6];
	var yrot 	= -layerState[7];
	var zrot  = -layerState[8];
	var fov   = layerState[9];
	
	var positionLine 	= "";
	var scaleLine 		= "";
	var rotationXLine 	= "";
	var rotationYLine 	= "";
	var rotationZLine 	= "";
	var fovLine		 	= "";
	
	 if (G.LAYER_IS_ANIMATED[0] == true || frameCounter == 1) {positionLine 		= "at time " + (frameCounter-1) + " " + G.SHORT_LAYER_NAME + ".pos = [" + xpos + "," + ypos + "," + zpos+ "]" + G.RET};
	 if (G.LAYER_IS_ANIMATED[3] == true || frameCounter == 1) {scaleLine 			= "at time " + (frameCounter-1) + " " + G.SHORT_LAYER_NAME + ".scale = [" + xscal + "," + yscal + "," + zscal + "]" + G.RET + G.RET;};
	 if (G.LAYER_IS_ANIMATED[6] == true || frameCounter == 1) {rotationXLine 		= "at time " + (frameCounter-1) + " " + G.SHORT_LAYER_NAME + ".rotation.x_rotation = " + xrot + G.RET};
	 if (G.LAYER_IS_ANIMATED[7] == true || frameCounter == 1) {rotationYLine 		= "at time " + (frameCounter-1) + " " + G.SHORT_LAYER_NAME + ".rotation.y_rotation = " + yrot	+ G.RET};
	 if (G.LAYER_IS_ANIMATED[8] == true || frameCounter == 1) {rotationZLine 		= "at time " + (frameCounter-1) + " " + G.SHORT_LAYER_NAME + ".rotation.z_rotation = " + zrot + G.RET};
	 if (G.LAYER_IS_ANIMATED[9] == true || frameCounter == 1) {fovLine		 		= "at time " + (frameCounter-1) + " " + G.SHORT_LAYER_NAME + ".fov = " + fov + G.RET + G.RET;};
	
		if (G.LAYER_TYPE == "Camera")
	{  
		data.keys += positionLine  	+
							rotationXLine 	+
							rotationZLine 	+
							rotationYLine 	+
							fovLine 			;
	}
	else // if Light or Layer
	{  
		data.keys += positionLine 	+
							rotationXLine 	+
							rotationZLine 	+
							rotationYLine 	+
							scaleLine 		;
	}
}

/*-----------------------------------------------------------------------------------------------*/
function storeValueAtCurrentTime_Lightwave (comp, data, frameCounter, layerState, worldScale, t)
/*-----------------------------------------------------------------------------------------------*/
{
	var curTime = t - comp.workAreaStart;
	if (G.LAYER_IS_ANIMATED[0] == true || frameCounter == 1) {data.xpos	 += "  Key " + (layerState[0] - G.WORLD_CENTER[0]) * worldScale 			+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[1] == true || frameCounter == 1) {data.ypos	 += "  Key " + (-((layerState[1] - G.WORLD_CENTER[1]) * worldScale))	 	+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[2] == true || frameCounter == 1) {data.zpos	 += "  Key " + layerState[2]  * worldScale										+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[3] == true || frameCounter == 1) {data.xscal   += "  Key " + layerState[3]  / 100 												+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[4] == true || frameCounter == 1) {data.yscal   += "  Key " + layerState[4] 	/ 100												+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[5] == true || frameCounter == 1) {data.zscal   += "  Key " + layerState[5]	/ 100												+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[6] == true || frameCounter == 1) {data.xrot	 += "  Key " + (-(degreesToRadians(layerState[6])))							+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[7] == true || frameCounter == 1) {data.yrot	 += "  Key " + degreesToRadians(layerState[7])									+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[8] == true || frameCounter == 1) {data.zrot	 += "  Key " + (-(degreesToRadians(layerState[8])))							+ " " + curTime + " 3 0 0 0 0 0 0" + G.RET;};
	if (G.LAYER_IS_ANIMATED[9] == true || frameCounter == 1) {data.flen	 += "  Key " + layerState[9]														+ " " + curTime + " 0 0 0 0 0 0 0" + G.RET;};
}

/*--------------------------------------------------------------------------------------------*/
function checkChannelsForAnimation(layer)
/*--------------------------------------------------------------------------------------------*/
{
	if (G.LAYER_TYPE == "Camera")
	{
		if (layer.position.isTimeVarying == true) {G.LAYER_IS_ANIMATED[0] = true;G.LAYER_IS_ANIMATED[1] = true;G.LAYER_IS_ANIMATED[2] = true;};
		if (layer.orientation.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		if (layer.rotationX.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		if (layer.rotationY.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		if (layer.rotation.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		if (layer.zoom.isTimeVarying == true) {G.LAYER_IS_ANIMATED[9] = true;};
		if (layer.pointOfInterest != null) 
		{
			G.LAYER_IS_ANIMATED[6] = true; G.LAYER_IS_ANIMATED[7] = true; G.LAYER_IS_ANIMATED[8] = true;
		}
	}
	else if (G.LAYER_TYPE == "Light")
	{
		if (layer.position != null)
		{
			if (layer.position.isTimeVarying == true) {G.LAYER_IS_ANIMATED[0] = true;G.LAYER_IS_ANIMATED[1] = true;G.LAYER_IS_ANIMATED[2] = true;};
		}
		if (layer.orientation != null)
		{
			if (layer.orientation.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
			if (layer.rotationX.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
			if (layer.rotationY.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
			if (layer.rotation.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		}
		if (layer.pointOfInterest != null) 
		{
			G.LAYER_IS_ANIMATED[6] = true; G.LAYER_IS_ANIMATED[7] = true; G.LAYER_IS_ANIMATED[8] = true;
		}
	}
	else if (G.LAYER_TYPE == "Layer")
	{
		if (layer.position.isTimeVarying == true) {G.LAYER_IS_ANIMATED[0] = true;G.LAYER_IS_ANIMATED[1] = true;G.LAYER_IS_ANIMATED[2] = true;};
		if (layer.scale.isTimeVarying == true) {G.LAYER_IS_ANIMATED[3] = true;G.LAYER_IS_ANIMATED[4] = true;G.LAYER_IS_ANIMATED[5] = true;};
		if (layer.orientation.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		if (layer.rotationX.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		if (layer.rotationY.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
		if (layer.rotation.isTimeVarying == true) {G.LAYER_IS_ANIMATED[6] = true;G.LAYER_IS_ANIMATED[7] = true;G.LAYER_IS_ANIMATED[8] = true;};
	}
}

/*--------------------------------------------------------------------------------------------*/
function AssumeLayerIsAnimated(layer)
/*--------------------------------------------------------------------------------------------*/
{
	if (layer.parent.name == "WorldCenter") // doesn't count if the parent is this, so consider it unparented
	{
		checkChannelsForAnimation(layer);
	}
	else // since its parented, assume all layers are animated
	{
		for (var j=0;j<=9;j++)
		{
			G.LAYER_IS_ANIMATED[j] = true;
		}
	}
}

/*--------------------------------------------------------------------------------------------*/
function checkForAnimation(layer)
/*--------------------------------------------------------------------------------------------*/
{
	if (layer.parent != null) // if it has a parent
	{
		AssumeLayerIsAnimated(layer);
	}
	else
	{
		checkChannelsForAnimation(layer);
	}
}

/*--------------------------------------------------------------------------------------------*/
function resetComposition (comp, layer)
/*--------------------------------------------------------------------------------------------*/
{
	for (var m=0;m<=9;m++)
	{
		G.LAYER_IS_ANIMATED[m] = false;
	}
	if (G.LAYER_WAS_2D == true)
	{
		layer.threeDLayer = false;
		G.LAYER_WAS_2D = false;
	}
	comp.layer(G.SHORT_LAYER_NAME + "_copy").remove(); 			// remove the cooked layer
	comp.layer(G.SHORT_LAYER_NAME + "_copy_parent").remove(); 	// remove the cooked layer"s parent
}

/*--------------------------------------------------------------------------------------------*/
function totalFramesByChannel(totalFrames)
/*--------------------------------------------------------------------------------------------*/
{
	var totalFramesArray = [];
	for (var n=0;n<=9;n++)
	{
		if (G.LAYER_IS_ANIMATED[n] == false) {totalFramesArray[n] = 1}else{totalFramesArray[n] = totalFrames};
	}
	return totalFramesArray;
}

/*--------------------------------------------------------------------------------------------*/
function getData(comp, data) // grabs the data of each frame and stores it in a set of strings
/*--------------------------------------------------------------------------------------------*/
{
	var worldScale 				= G.WORLD_SCALE[G.RADIOBUTTON_ON-1] * ( Math.pow(10, UI.options.scaleSlider.value) );
	var layerCopyParent 		= comp.layer(G.SHORT_LAYER_NAME + "_copy_parent");
	var layerCopy 				= comp.layer(G.SHORT_LAYER_NAME + "_copy");
	var totalFrames 				= getTotalFrames(comp);
 	var frameCounter 			= 1;

// origin shift

 	if (UI.options.originShift.value == true)
 	{
 		G.WORLD_CENTER = [comp.width/2,comp.height/2,0];
	}
	else
	{
		G.WORLD_CENTER = [0,0,0];
	}
	
// warning   

	if (comp.workAreaDuration > G.SAFE_DUR)
	{
		if (!confirm(G.SAFE_DUR_WNG, true, "AE3D EXPORT"))
       {
			return false;
		}
	}

// process layer

	if (G.RADIOBUTTON_ON == 1) // Maya
	{
		if (G.LAYER_TYPE == "Camera")
		{
			for (var t = comp.workAreaStart; t < comp.workAreaStart + comp.workAreaDuration; t += comp.frameDuration)
			{
				clearOutput();
				UI.main.progress.text="Processing \"" + G.LAYER_NAME + "\" : " + Math.round(((frameCounter/totalFrames)*100)-1) + " %";
				var layerState = collectValueAtCurrentTime_ZYX_Camera (comp, layerCopy, layerCopyParent, t);
				storeValueAtCurrentTime_Maya (data, frameCounter, layerState, worldScale);
				frameCounter++;
			}
		}
		else // layer or light
		{
			for (var t = comp.workAreaStart; t < comp.workAreaStart + comp.workAreaDuration; t += comp.frameDuration)
			{
				clearOutput();
				UI.main.progress.text="Processing \"" + G.LAYER_NAME + "\" : " + Math.round(((frameCounter/totalFrames)*100)-1) + " %";
				var layerState = collectValueAtCurrentTime_ZYX_Layer (comp, layerCopy, layerCopyParent, t);
				storeValueAtCurrentTime_Maya (data, frameCounter, layerState, worldScale);
				frameCounter++;
			}
		}
	}
	else if (G.RADIOBUTTON_ON == 2) // Max
	{
		if (G.LAYER_TYPE == "Camera")
		{
			for (var t = comp.workAreaStart; t < comp.workAreaStart + comp.workAreaDuration; t += comp.frameDuration)
			{
				clearOutput();
				UI.main.progress.text="Processing \"" + G.LAYER_NAME + "\" : " + Math.round(((frameCounter/totalFrames)*100)-1) + " %";
				var layerState = collectValueAtCurrentTime_ZYX_Camera (comp, layerCopy, layerCopyParent, t);
				storeValueAtCurrentTime_Max (data, frameCounter, layerState, worldScale);
				frameCounter++;
			}
		}
		else // layer or light
		{
			for (var t = comp.workAreaStart; t < comp.workAreaStart + comp.workAreaDuration; t += comp.frameDuration)
			{
				clearOutput();
				UI.main.progress.text="Processing \"" + G.LAYER_NAME + "\" : " + Math.round(((frameCounter/totalFrames)*100)-1) + " %";
				var layerState = collectValueAtCurrentTime_ZYX_Layer (comp, layerCopy, layerCopyParent, t)
				storeValueAtCurrentTime_Max (data, frameCounter, layerState, worldScale);
				frameCounter++;
			}
		}
	}
	else if (G.RADIOBUTTON_ON == 3) // Lightwave
	{
		if (G.LAYER_TYPE == "Camera")
		{
			for (var t = comp.workAreaStart; t < comp.workAreaStart + comp.workAreaDuration; t += comp.frameDuration)
			{
				clearOutput();
				UI.main.progress.text="Processing \"" + G.LAYER_NAME + "\" : " + Math.round(((frameCounter/totalFrames)*100)-1) + " %";
				var layerState = collectValueAtCurrentTime_YXZ_Camera (comp, layerCopy, layerCopyParent, t);
				storeValueAtCurrentTime_Lightwave (comp, data, frameCounter, layerState, worldScale, t);
				frameCounter++;
			}
		}
		else // layer or light
		{
			for (var t = comp.workAreaStart; t < comp.workAreaStart + comp.workAreaDuration; t += comp.frameDuration)
			{
				clearOutput();
				UI.main.progress.text="Processing \"" + G.LAYER_NAME + "\" : " + Math.round(((frameCounter/totalFrames)*100)-1) + " %";
				var layerState = collectValueAtCurrentTime_YXZ_Layer (comp, layerCopy, layerCopyParent, t);
				storeValueAtCurrentTime_Lightwave (comp, data, frameCounter, layerState, worldScale, t);
				frameCounter++;
			}
		}	
	}
	clearOutput();
}

/*-----------------------------------------------------------------------------------*/    
function writeHeader(comp)
/*-----------------------------------------------------------------------------------*/ 
{
	var worldScale 		= G.WORLD_SCALE[G.RADIOBUTTON_ON-1] * ( Math.pow(10, UI.options.scaleSlider.value) );
	var totalFrames 		=   getTotalFrames(comp);
	var frameAspect 		=   getFrameAspect(); 
	var fpsName     		=   getFPSName(comp);
	var mayaFB      		=   frameAspect * G.MAYA_FB_H; 
	
	if (G.RADIOBUTTON_ON == 1) // MAYA
	{	
		G.SCENE_STRING = "//Maya ASCII 6.0 scene"																		+ G.RET +
							"//Name: " + G.FILE_NAME																		+ G.RET +
							"//Last modified: " + (new Date()).toString()												+ G.RET +
							"requires maya \"6.0\";"																		+ G.RET +
							"currentUnit -l meter -a degree -t " + fpsName + ";"										+ G.RET +
							""																									+ G.RET ;
		if (UI.options.extraMayaCams.value == true)
		{
			G.SCENE_STRING += "createNode transform -s -n \"persp\";"												+ G.RET +
							"	setAttr \".v\" yes;"																		+ G.RET +
							"	setAttr \".s\" -type \"double3\" 1 1 1 ;"												+ G.RET +
							"	setAttr \".t\" -type \"double3\" " + 5000*worldScale + " " + 3000*worldScale + " " + 5000*worldScale + " ;"+ G.RET +
							"	setAttr \".r\" -type \"double3\" -28 45 0 ;"											+ G.RET +
							"createNode camera -s -n \"perspShape\" -p \"persp\";"									+ G.RET +
							"	setAttr -k off \".v\" no;"																	+ G.RET +
							"	setAttr \".rnd\" no;"																		+ G.RET +
							"	setAttr \".fl\" 35;"																		+ G.RET +
							"	setAttr \".ncp\" 1;"																		+ G.RET +
							"	setAttr \".fcp\" " + 40000*worldScale + ";"												+ G.RET +
							"	setAttr \".coi\" 822 ;"																		+ G.RET +
							"	setAttr \".imn\" -type \"string\" \"persp\";"											+ G.RET +
							"	setAttr \".den\" -type \"string\" \"persp_depth\";"									+ G.RET +
							"	setAttr \".man\" -type \"string\" \"persp_mask\";"									+ G.RET +
							"	setAttr \".hc\" -type \"string\" \"viewSet -p %camera\";"							+ G.RET +
							""																									+ G.RET +
							"createNode transform -n \"front\";"															+ G.RET +
							"	setAttr \".t\" -type \"double3\" 0 0 "+10000*worldScale+" ;"						+ G.RET +
							"createNode camera -s -n \"frontShape\" -p \"front\";"									+ G.RET +
							"	setAttr -k off \".v\" no;"																	+ G.RET +
							"	setAttr \".rnd\" no;"																		+ G.RET +
							"	setAttr \".coi\" 100 ;"																		+ G.RET +
							"	setAttr \".imn\" -type \"string\" \"front\";"											+ G.RET +
							"	setAttr \".den\" -type \"string\" \"front_depth\";"									+ G.RET +
							"	setAttr \".man\" -type \"string\" \"front_mask\";"									+ G.RET +
							"	setAttr \".hc\" -type \"string\" \"viewSet -f %camera\";"							+ G.RET +
							"   setAttr \".o\" yes;"																		+ G.RET +
							"   setAttr \".ow\" 30;"																		+ G.RET +
							""																									+ G.RET +
							"createNode transform -n \"top\";"															+ G.RET +
							"	setAttr \".t\" -type \"double3\" 0 " + 10000*worldScale + " 0 ;"					+ G.RET +
							"	setAttr \".r\" -type \"double3\" -90 0 0 ;"												+ G.RET +
							"createNode camera -s -n \"topShape\" -p \"top\";"										+ G.RET +
							"	setAttr -k off \".v\" no;"																	+ G.RET +
							"	setAttr \".rnd\" no;"																		+ G.RET +
							"	setAttr \".coi\" 100 ;"																		+ G.RET +
							"	setAttr \".imn\" -type \"string\" \"top\";"												+ G.RET +
							"	setAttr \".den\" -type \"string\" \"top_depth\";"										+ G.RET +
							"	setAttr \".man\" -type \"string\" \"top_mask\";"										+ G.RET +
							"	setAttr \".hc\" -type \"string\" \"viewSet -t %camera\";"							+ G.RET +
							"   setAttr \".o\" yes;"																		+ G.RET +
							"   setAttr \".ow\" 30;"																		+ G.RET +
							""																									+ G.RET +
							"createNode transform -n \"side\";"															+ G.RET +
							"	setAttr \".t\" -type \"double3\" " + 10000*worldScale + " 0 0 ;"					+ G.RET +
							"	setAttr \".r\" -type \"double3\" 0 90 0 ;"												+ G.RET +
							"createNode camera -s -n \"sideShape\" -p \"side\";"										+ G.RET +
							"	setAttr -k off \".v\" no;"																	+ G.RET +
							"	setAttr \".rnd\" no;"																		+ G.RET +
							"	setAttr \".coi\" 100 ;"																		+ G.RET +
							"	setAttr \".imn\" -type \"string\" \"side\";"											+ G.RET +
							"	setAttr \".den\" -type \"string\" \"side_depth\";"									+ G.RET +
							"	setAttr \".man\" -type \"string\" \"side_mask\";"										+ G.RET +
							"	setAttr \".hc\" -type \"string\" \"viewSet -s %camera\";"							+ G.RET +
							"   setAttr \".o\" yes;"																		+ G.RET +
							"   setAttr \".ow\" 30;"																		+ G.RET +
							""																									+ G.RET ;
		}
	}
	else if (G.RADIOBUTTON_ON == 2) // MAX
	{
		G.SCENE_STRING = "global frameRate = " + Math.round(comp.frameRate*100)/100								+ G.RET +
							""																									+ G.RET +
							"renderPixelAspect = " + G.ORIGINAL_ASPECT													+ G.RET +
							"renderWidth = " + G.WIDTH																		+ G.RET +
							"renderHeight = " + G.HEIGHT																	+ G.RET +
							"ticksPerFrame = (4800/frameRate)"															+ G.RET +
							""																									+ G.RET ;
	}
	else if (G.RADIOBUTTON_ON == 3) // Lightwave
	{
		G.SCENE_STRING = "LWSC" 																							+ G.RET +
							"3"																									+ G.RET +
							""																									+ G.RET +
							"RenderRangeType 0"																				+ G.RET +
							"FirstFrame 1"																					+ G.RET +
							"LastFrame " + (totalFrames-1)																+ G.RET +
							"FrameStep 1"																						+ G.RET +
							"RenderRangeArbitrary 1-60"																	+ G.RET +
							"PreviewFirstFrame 0"																			+ G.RET +
							"PreviewLastFrame " + (totalFrames-1)														+ G.RET +
							"PreviewFrameStep 1"																			+ G.RET +
							"CurrentFrame 0"																					+ G.RET +
							"FramesPerSecond " + Math.round(comp.frameRate*100)/100									+ G.RET +
							""																									+ G.RET +
							"AmbientColor 1 1 1"																			+ G.RET +
							"AmbientIntensity 0.05"																			+ G.RET +
							""																									+ G.RET +
							"LightColor 1 1 1"																				+ G.RET +
							"LightIntensity 1"																				+ G.RET +
							"AffectCaustics 1"																				+ G.RET +
							"LightType 0"																						+ G.RET +
							"ShadowType 1"																					+ G.RET +
							"ShadowColor 0 0 0"																				+ G.RET +
							""																									+ G.RET ;
	}
}

/*-----------------------------------------------------------------------------------*/    
function writeThisLayerIntoScene(comp, data)
/*-----------------------------------------------------------------------------------*/ 
{
	var totalFrames 		= getTotalFrames(comp);
	var totalFramesBC	= totalFramesByChannel(totalFrames);
	var frameAspect 		= getFrameAspect(); 
	var fpsName     		= getFPSName(comp);
	var mayaFB      		= frameAspect * G.MAYA_FB_H;
	
	if (G.RADIOBUTTON_ON == 1) // MAYA
	{	
		if (G.LAYER_TYPE == "Camera")
		{
			G.SCENE_STRING += "createNode transform -n \"" + G.SHORT_LAYER_NAME + "\";"														+ G.RET +
								"    setAttr \".s\" -type \"double3\" 100 100 100 ;"																+ G.RET +
								"createNode camera -n \"" + G.SHORT_LAYER_NAME + "Shape\" -p \"" + G.SHORT_LAYER_NAME + "\";"				+ G.RET +
								"    setAttr -k off \".v\";"																							+ G.RET +
								"    setAttr \".rnd\" yes;"																							+ G.RET +
								"    setAttr \".ow\" 10.0;"																							+ G.RET +
								"    setAttr \".dof\" no;"																								+ G.RET +
								"    setAttr \".s\" no;"																								+ G.RET +
								"    setAttr \".eo\" 1.0;"																								+ G.RET +
								"    setAttr \".ff\" 1;"																								+ G.RET +
								"    setAttr \".cap\" -type \"double2\" " + mayaFB + " " + G.MAYA_FB_H + ";"									+ G.RET +
								"    setAttr \".fcp\" 40000;"																							+ G.RET +
								"    setAttr \".col\" -type \"float3\" 0.0 0.0 0.0 ;"																+ G.RET +
								"    setAttr \".imn\" -type \"string\" \"" + G.SHORT_LAYER_NAME + "\";"										+ G.RET +
								"    setAttr \".den\" -type \"string\" \"" + G.SHORT_LAYER_NAME + "_Depth\";"								+ G.RET +
								"    setAttr \".man\" -type \"string\" \"" + G.SHORT_LAYER_NAME + "_Mask\";"									+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTL -n \"" + G.SHORT_LAYER_NAME + "_TranslateX\";"										+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[0] + " \".ktv[" + (totalFramesBC[0] > 1 ? " 1:" + totalFramesBC[0] : "0") + "]\" " + data.xpos + ";"  		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTL -n \"" + G.SHORT_LAYER_NAME + "_TranslateY\";"										+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[1] + " \".ktv[" + (totalFramesBC[1] > 1 ? "1:" + totalFramesBC[1] : "0") + "]\" " + data.ypos + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTL -n \"" + G.SHORT_LAYER_NAME + "_TranslateZ\";"										+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[2] + " \".ktv[" + (totalFramesBC[2] > 1 ? "1:" + totalFramesBC[2] : "0") + "]\" " + data.zpos + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_RotateX\";"											+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[6] + " \".ktv[" + (totalFramesBC[6] > 1 ? "1:" + totalFramesBC[6] : "0") + "]\" " + data.xrot + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_RotateY\";"											+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[7] + " \".ktv[" + (totalFramesBC[7] > 1 ? "1:" + totalFramesBC[7] : "0") + "]\" " + data.yrot + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_RotateZ\";"											+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[8] + " \".ktv[" + (totalFramesBC[8] > 1 ? "1:" + totalFramesBC[8] : "0") + "]\" " + data.zrot + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTU -n \"" + G.SHORT_LAYER_NAME + "Shape_FocalLength\";"									+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[9] + " \".ktv[" + (totalFramesBC[9] > 1 ? "1:" + totalFramesBC[9] : "0") + "]\" " + data.flen + ";"		+ G.RET +
								""																															+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_TranslateX.o\" \"" + G.SHORT_LAYER_NAME + ".tx\";"				+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_TranslateY.o\" \"" + G.SHORT_LAYER_NAME + ".ty\";"				+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_TranslateZ.o\" \"" + G.SHORT_LAYER_NAME + ".tz\";"				+ G.RET +
								""																															+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_RotateX.o\" \"" + G.SHORT_LAYER_NAME + ".rx\";"					+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_RotateY.o\" \"" + G.SHORT_LAYER_NAME + ".ry\";"					+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_RotateZ.o\" \"" + G.SHORT_LAYER_NAME + ".rz\";"					+ G.RET +
								""																															+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "Shape_FocalLength.o\"\"" + G.SHORT_LAYER_NAME + "Shape.fl\";"	+ G.RET +
								""																															+ G.RET ;
		}
		else // light or layer
		{
			G.SCENE_STRING += "createNode transform -n \"" + G.SHORT_LAYER_NAME + "\";"														+ G.RET +        
								"createNode locator -n \"" + G.SHORT_LAYER_NAME + "Shape\" -p \"" + G.SHORT_LAYER_NAME + "\";"			+ G.RET +
								"    setAttr -k off \".v\";"																							+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTL -n \"" + G.SHORT_LAYER_NAME + "_TranslateX\";"										+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[0] + " \".ktv[" + (totalFramesBC[0] > 1 ? "1:" + totalFramesBC[0] : "0") + "]\" " + data.xpos + ";"  		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTL -n \"" + G.SHORT_LAYER_NAME + "_TranslateY\";"										+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[1] + " \".ktv[" + (totalFramesBC[1] > 1 ? "1:" + totalFramesBC[1] : "0") + "]\" " + data.ypos + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTL -n \"" + G.SHORT_LAYER_NAME + "_TranslateZ\";"										+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[2] + " \".ktv[" + (totalFramesBC[2] > 1 ? "1:" + totalFramesBC[2] : "0") + "]\" " + data.zpos + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_RotateX\";"											+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[6] + " \".ktv[" + (totalFramesBC[6] > 1 ? "1:" + totalFramesBC[6] : "0") + "]\" " + data.xrot + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_RotateY\";"											+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[7] + " \".ktv[" + (totalFramesBC[7] > 1 ? "1:" + totalFramesBC[7] : "0") + "]\" " + data.yrot + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_RotateZ\";"											+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[8] + " \".ktv[" + (totalFramesBC[8] > 1 ? "1:" + totalFramesBC[8] : "0") + "]\" " + data.zrot + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_ScaleX\";"												+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[3] + " \".ktv[" + (totalFramesBC[3] > 1 ? "1:" + totalFramesBC[3] : "0") + "]\" " + data.xscal + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_ScaleY\";"												+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[4] + " \".ktv[" + (totalFramesBC[4] > 1 ? "1:" + totalFramesBC[4] : "0") + "]\" " + data.yscal + ";"		+ G.RET +
								""																															+ G.RET +
								"createNode animCurveTA -n \"" + G.SHORT_LAYER_NAME + "_ScaleZ\";"												+ G.RET +
								"    setAttr \".tan\" 9;"																								+ G.RET +
								"    setAttr \".wgt\" no;"																								+ G.RET +
								"    setAttr -s " + totalFramesBC[5] + " \".ktv[" + (totalFramesBC[5] > 1 ? "1:" + totalFramesBC[5] : "0") + "]\" " + data.zscal + ";"		+ G.RET +
								""																															+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_TranslateX.o\" \"" + G.SHORT_LAYER_NAME + ".tx\";"				+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_TranslateY.o\" \"" + G.SHORT_LAYER_NAME + ".ty\";"				+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_TranslateZ.o\" \"" + G.SHORT_LAYER_NAME + ".tz\";"				+ G.RET +
								""																															+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_RotateX.o\" \"" + G.SHORT_LAYER_NAME + ".rx\";"					+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_RotateY.o\" \"" + G.SHORT_LAYER_NAME + ".ry\";"					+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_RotateZ.o\" \"" + G.SHORT_LAYER_NAME + ".rz\";"					+ G.RET +
								""																															+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_ScaleX.o\" \"" + G.SHORT_LAYER_NAME + ".sx\";"					+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_ScaleY.o\" \"" + G.SHORT_LAYER_NAME + ".sy\";"					+ G.RET +
								"connectAttr \"" + G.SHORT_LAYER_NAME + "_ScaleZ.o\" \"" + G.SHORT_LAYER_NAME + ".sz\";"					+ G.RET +
								""																															+ G.RET ; 
		}
	}
	else if (G.RADIOBUTTON_ON == 2) // MAX
	{	
		if (G.LAYER_TYPE == "Camera")
		{
			G.SCENE_STRING += G.SHORT_LAYER_NAME + " = freecamera name:\"" + G.SHORT_LAYER_NAME + "\""						+ G.RET +
                           "set animate on"																								+ G.RET +        
                           ""																												+ G.RET +
								data.keys																										+ G.RET ;
		}
		else // light or layer
		{
			G.SCENE_STRING += G.SHORT_LAYER_NAME + " = Dummy()"																		+ G.RET +
								G.SHORT_LAYER_NAME + ".name = \"" + G.SHORT_LAYER_NAME + "\""										+ G.RET +
                           "set animate on"																								+ G.RET +        
                           ""																												+ G.RET +
								data.keys																										+ G.RET ;
		}
	}
	else if (G.RADIOBUTTON_ON == 3) // Lightwave
	{	
		if (G.LAYER_TYPE == "Camera")
		{
			G.SCENE_STRING += "AddCamera"																									+ G.RET +
								"CameraName " + G.SHORT_LAYER_NAME																		+ G.RET +
								"ShowCamera 1 2"																								+ G.RET +
								"CameraMotion"																								+ G.RET +
								"NumChannels 6"																								+ G.RET +
								"Channel 0"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[0]																						+ G.RET +
								data.xpos																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 1"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[1]																						+ G.RET +
								data.ypos																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +	
								"Channel 2"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[2]																						+ G.RET +
								data.zpos																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 3"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[6]																						+ G.RET +
								data.yrot																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 4"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[7]																						+ G.RET +
								data.xrot																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 5"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[8]																						+ G.RET +
								data.zrot																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								""																												+ G.RET +
								"ZoomFactor (envelope)"																						+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[9]																						+ G.RET +
								data.flen																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"ResolutionMultiplier 1.0"																					+ G.RET +
								"FrameSize " + G.WIDTH + " " + G.HEIGHT																	+ G.RET +
								"PixelAspect " + G.ORIGINAL_ASPECT																		+ G.RET +
								"MaskPosition 0 0 " + G.WIDTH + " " + G.HEIGHT															+ G.RET +
								"MotionBlur 0"																								+ G.RET +
								"FieldRendering 0"																							+ G.RET +
								""																												+ G.RET +
								"ApertureHeight 0.015"																						+ G.RET +
								"Antialiasing 0"																								+ G.RET +
								"AntiAliasingLevel -1"																						+ G.RET +
								"ReconstructionFilter 0"																					+ G.RET +
								"AdaptiveSampling 0"																						+ G.RET +
								""																												+ G.RET ;
		}
		else // light or layer
		{
			G.SCENE_STRING += "AddNullObject <" + G.SHORT_LAYER_NAME + ">"															+ G.RET +
								"ShowObject 7 3"																								+ G.RET +
								"ObjectMotion"																								+ G.RET +
								"NumChannels 9"																								+ G.RET +
								"Channel 0"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[0]																						+ G.RET +
								data.xpos																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 1"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[1]																						+ G.RET +
								data.ypos																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +	
								"Channel 2"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[2]																						+ G.RET +
								data.zpos																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 3"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[6]																						+ G.RET +
								data.yrot																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 4"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[7]																						+ G.RET +
								data.xrot																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 5"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[8]																						+ G.RET +
								data.zrot																										+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 6"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[3]																						+ G.RET +
								data.xscal																									+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 7"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[4]																						+ G.RET +
								data.yscal																									+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET +
								"Channel 8"																									+ G.RET +
								"{ Envelope"																									+ G.RET +
								"  " + totalFramesBC[5]																						+ G.RET +
								data.zscal																									+
								"  Behaviors 1 1"																							+ G.RET +
								"}"																												+ G.RET ;		
		}
	}
}

/*-----------------------------------------------------------------------------------*/    
function writeFooter(comp)
/*-----------------------------------------------------------------------------------*/ 
{
	var totalFrames 		=   getTotalFrames(comp);
	var frameAspect 		=   getFrameAspect(); 
	
	if (G.RADIOBUTTON_ON == 1) // MAYA
	{	
		G.SCENE_STRING += "select -ne :time1;"																																		+ G.RET +
							"    setAttr \".o\" 1;"																																		+ G.RET +
							"select -ne :defaultResolution;"																															+ G.RET +
							"    setAttr \".w\" " + G.WIDTH + ";"																													+ G.RET +
							"    setAttr \".h\" " + G.HEIGHT + ";"																													+ G.RET +
							"    setAttr \".dar\" " + frameAspect + ";"																												+ G.RET +
							""																																								+ G.RET +
							"createNode script -n \"uiConfigurationScriptNode\";"																									+ G.RET +
							"    setAttr \".b\" -type \"string\" (\"grid -tgl true -sp 50 -d 50 -s 50\");"																	+ G.RET +
							"    setAttr \".st\" 3;"																																	+ G.RET +
							"createNode script -n \"sceneConfigurationScriptNode\";"																								+ G.RET +
							"    setAttr \".b\" -type \"string\"\"playbackOptions -min 1.0 -max " + (totalFrames+1) + " -ast 1.0 -aet " + (totalFrames+1) + "\";"+ G.RET +
							"    setAttr \".st\" 6;"																																	+ G.RET +
							""																																								+ G.RET +
							"//End of " + G.FILE_NAME;
	}
	else if (G.RADIOBUTTON_ON == 2) // MAX
	{
		G.SCENE_STRING += "animationRange = (interval 0 " + totalFrames + ")";
	}
	else if (G.RADIOBUTTON_ON == 3) // Lightwave
	{
		G.SCENE_STRING += "";
	}
}

/*-----------------------------------------------------------------------------------*/    
function write3DFile() // writes a ASCII file that the 3D softwave can read
/*-----------------------------------------------------------------------------------*/    
{      
	var file = File(G.FILE_PATH);	
	if (!file)
	{
		return;
	}
	if (file.open("w", "TEXT", "????"))
	{                   
		file.writeln(G.SCENE_STRING);
		file.close();
	}
}

/*----------------------------------------------------------------------------------------------------------------*/    
function cookLayer(comp, layer) // create a copy of the layer in After Effects and prepare the transformation data
/*----------------------------------------------------------------------------------------------------------------*/    
{
	G.LAYER_NAME = layer.name;
	G.SHORT_LAYER_NAME = removeForbiddenCharacters (layer.name);
	
// make a copy of the layer
	if (G.LAYER_TYPE == "Camera")
	{
		var layerCopy = comp.layers.addCamera(G.SHORT_LAYER_NAME + "_copy",[0,0]);
		layerCopy.startTime = 0;
		layerCopy.pointOfInterest.expression = "position;";
		layerCopy.position.setValue([comp.width/2,comp.height/2,0]);
	}
	else // light or layer
	{
		var layerCopy = comp.layers.addNull();
		layerCopy.name = G.SHORT_LAYER_NAME + "_copy";
		layerCopy.startTime = 0;
		layerCopy.threeDLayer = true;
		layerCopy.anchorPoint.setValue([50,50,0]);
		layerCopy.position.setValue([comp.width/2,comp.height/2,0]);
	}
	
// make a parent for the layer copy (used for position, for scaling if camera, for Z rotation if rotation is being reversed)
	var layerCopyParent = comp.layers.addNull();
	layerCopyParent.name = G.SHORT_LAYER_NAME + "_copy_parent";
	layerCopyParent.startTime = 0;
	layerCopyParent.threeDLayer = true;
	layerCopyParent.anchorPoint.setValue([50,50,0]);
	layerCopyParent.position.setValue([comp.width/2,comp.height/2,0]);
	layerCopy.parent = layerCopyParent; // attach layer copy to parent

// Expression blocks

	var layerRefExp 		= "L = thisComp.layer(\"" + G.LAYER_NAME + "\");"				+ G.RET;
	
	var unitMatrixExp 	= "c=L.toWorldVec([0,0,0]);"										+ G.RET +
								"u=L.toWorldVec([unit[0],0,0]);"								+ G.RET +
								"v=L.toWorldVec([0,unit[1],0]);"								+ G.RET +
								"w=L.toWorldVec([0,0,unit[2]]);"								+ G.RET;	

	var posExp 			= 	"L.toWorld(A)";
								
	var scaleExp 			= "[1/length(c, u),1/length(c, v),1/length(c, w)]*100";
					  
	
	var ZYXrotExp 		= "hLock=clamp(u[2],-1,1);"										+ G.RET +
								"h=Math.asin(-hLock);"											+ G.RET +
								"cosH=Math.cos(h);"												+ G.RET +
								"if (Math.abs(cosH) > 0.0005){"								+ G.RET +
								"  p=Math.atan2(v[2], w[2]);"									+ G.RET +
								"  b=Math.atan2(u[1],u[0]);"									+ G.RET +
								"}else{"															+ G.RET +
								"  b=Math.atan2(w[1], v[1]);"									+ G.RET +
								" p=0;"															+ G.RET +
								"}"																	+ G.RET;
	
	var YXZrotExp 		= "pLock=clamp(w[1],-1,1);"										+ G.RET +
								"p=Math.asin(-pLock);"											+ G.RET +
								"cosP=Math.cos(p);"												+ G.RET +
								"if (Math.abs(cosP) > 0.0005){"								+ G.RET +
								"  h=Math.atan2(w[0], w[2]);"									+ G.RET +
								"  b=Math.atan2(u[1],v[1]);"									+ G.RET +
								"}else{"															+ G.RET +
								"  h=Math.atan2(u[2], w[2]);"									+ G.RET +
								"  b=0;"															+ G.RET +
								"}"																	+ G.RET;
							
	var zoomExp				= "L.zoom";
	
// write expressions into the layer copy and its parent

	if (G.RADIOBUTTON_ON==1 || G.RADIOBUTTON_ON==2) // for Maya or Max (ZYX rotation)
	{
		if (G.LAYER_TYPE == "Camera")
		{
			layerCopyParent.position.expression 		= layerRefExp + "A=[0,0,0];" + G.RET + posExp;
			layerCopyParent.scale.expression 			= layerRefExp + "unit=[1,1,1];" + G.RET + unitMatrixExp + scaleExp;
			layerCopyParent.rotation.expression 		= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "radiansToDegrees(b)";
			layerCopy.orientation.expression 			= layerRefExp + "unit=thisLayer.parent.scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "[ 0, radiansToDegrees(h), 0 ]";
			layerCopy.rotationX.expression 			= layerRefExp + "unit=thisLayer.parent.scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "radiansToDegrees(p)";
			layerCopy.zoom.expression 					= layerRefExp + zoomExp;
		}
			else if (G.LAYER_TYPE == "Light")
		{
			layerCopyParent.position.expression 		= layerRefExp + "A=[0,0,0];" + G.RET + posExp;
			layerCopyParent.rotation.expression 		= layerRefExp + "unit=thisComp.layer(thisLayer, 1).scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "radiansToDegrees(b)";
			layerCopy.scale.expression 				= layerRefExp + "unit=[1,1,1];" + G.RET + unitMatrixExp + scaleExp;
			layerCopy.orientation.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "[ 0, radiansToDegrees(h), 0 ]";
			layerCopy.rotationX.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "radiansToDegrees(p)";
	
		}
		else if (G.LAYER_TYPE == "Layer")
		{
			layerCopyParent.position.expression 		= layerRefExp + "A=L.anchorPoint;" + G.RET + posExp;
			layerCopyParent.rotation.expression 		= layerRefExp + "unit=thisComp.layer(thisLayer, 1).scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "radiansToDegrees(b)";
			layerCopy.scale.expression 				= layerRefExp + "unit=[1,1,1];" + G.RET + unitMatrixExp + scaleExp;
			layerCopy.orientation.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "[ 0, radiansToDegrees(h), 0 ]";
			layerCopy.rotationX.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + ZYXrotExp + "radiansToDegrees(p)";
	
		}
	}
	else if (G.RADIOBUTTON_ON==3) // for Lightwave (YXZ rotation)
	{
		if (G.LAYER_TYPE == "Camera")
		{
			layerCopyParent.position.expression 		= layerRefExp + "A=[0,0,0];" + G.RET + posExp;
			layerCopyParent.scale.expression 			= layerRefExp + "unit=[1,1,1];" + G.RET + unitMatrixExp + scaleExp;
			layerCopy.orientation.expression 			= layerRefExp + "unit=thisLayer.parent.scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "[ 0, radiansToDegrees(h), 0 ]";
			layerCopy.rotationX.expression 			= layerRefExp + "unit=thisLayer.parent.scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "radiansToDegrees(p)";
			layerCopy.rotation.expression 			= layerRefExp + "unit=thisLayer.parent.scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "radiansToDegrees(b)";
			layerCopy.zoom.expression 					= layerRefExp + zoomExp;
		}
		else if (G.LAYER_TYPE == "Light")
		{
			layerCopyParent.position.expression 		= layerRefExp + "A=[0,0,0];" + G.RET + posExp;
			layerCopy.scale.expression 				= layerRefExp + "unit=[1,1,1];" + G.RET + unitMatrixExp + scaleExp;
			layerCopy.orientation.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "[ 0, radiansToDegrees(h), 0 ]";
			layerCopy.rotationX.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "radiansToDegrees(p)";
			layerCopy.rotation.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "radiansToDegrees(b)";
		}
		else if (G.LAYER_TYPE == "Layer")
		{
			layerCopyParent.position.expression 		= layerRefExp + "A=L.anchorPoint;" + G.RET + posExp;
			layerCopy.scale.expression 				= layerRefExp + "unit=[1,1,1];" + G.RET + unitMatrixExp + scaleExp;
			layerCopy.orientation.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "[ 0, radiansToDegrees(h), 0 ]";
			layerCopy.rotationX.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "radiansToDegrees(p)";
			layerCopy.rotation.expression 			= layerRefExp + "unit=scale/100;" + G.RET + unitMatrixExp + YXZrotExp + "radiansToDegrees(b)";
		}
	}
}

/*---------------------------------------------------------------------------------------------------------    
 MAIN
---------------------------------------------------------------------------------------------------------*/

/*-------------------*/
function main()
/*-------------------*/
{
	UI.main.progress.text="Checking...";									// initial error checks after pressing the export button
	var proj = app.project;
	if (!proj)
   {
		alert("Open a project first.");
		UI.main.progress.text="Ready.";
		return;
	}
	var comp = proj.activeItem;
	if (!comp || !(comp instanceof CompItem))
	{
		alert("A composition must be open and active");
		UI.main.progress.text="Ready.";
		return;
	}
	var selLayers = comp.selectedLayers;
	if (selLayers.length == 0)
	{
		alert("Please select the layers you want to export");
		UI.main.progress.text="Ready.";
		return;
	}
	var AllowAccess = app.preferences.getPrefAsLong("Main Pref Section", "Pref_SCRIPTING_FILE_NETWORK_SECURITY");
	if (AllowAccess == 0)
	{
		alert("ALERT!"+G.RET+
				"You need to check \"Allow Scripts to Write Files"+G.RET+
				"and Access Network\" in the General Preferences"+G.RET+
				"in order to use this plug in.");
		UI.main.progress.text="Ready.";
		return;
	}

	storeOriginalLayerNames (selLayers);										// the names of layers might need to be changed
	checkForBadLayerNames (selLayers);										// repeated names and long layer names are not allowed

	G.ORIGINAL_ASPECT = getPreciseCompPAR(comp);							// store original size (important for non square comps)
	G.WIDTH = comp.width;
	G.HEIGHT = comp.height;

	app.beginUndoGroup("AE3D Export");
// ------------------------------------------------------------------------------------------------------------------------------------------------------- 
		UI.main.progress.text="Processing...";
		nonSquareToSquare(comp); 												// if comp is non-square, pin all unparented layers to world center and make it square
		writeHeader(comp); 														// write header into scene string
		for (var k=0; k<selLayers.length; k++) 								// go through selected layers one at a time
		{
			var layer = selLayers[k];
			checkLayerType(layer); 												// what type of layer is it?
			checkForAnimation (layer);											// what channels are animated?
			cookLayer (comp, layer); 											// make a copy of the selected layer, with world space values
			var data = new DataContainer(); 									// temporary storage for the keyframe data
			getData(comp, data); 												// get data from cooked layer and store it
			UI.main.progress.text="Writing...";
			writeThisLayerIntoScene(comp, data); 							// write data for this layer into the scene string
			resetComposition (comp, layer);									// restore original values, erase layer copies
		}		
		writeFooter(comp); 														// write footer into scene string
		UI.main.progress.text="Exporting...";
		write3DFile(); 															// take the scene string and put it into an ASCII file for 3D packages
		restoreLayerNames (selLayers)	;										// restores the layer names if they were changed
		squareToNonSquare(comp); 												// if it was non-square, return it to original size, and erase the center pin
		UI.main.progress.text="Done.";
// ------------------------------------------------------------------------------------------------------------------------------------------------------- 
	app.endUndoGroup();
}

/*---------------------------------------------------------------------------------------------------------    
 Entry Point - initialize global variables and load user interface
---------------------------------------------------------------------------------------------------------*/  
var G = new Object();
initGlobals(G);

var UI = new Object();
initUI(UI);
    
//****************************** END    
}
