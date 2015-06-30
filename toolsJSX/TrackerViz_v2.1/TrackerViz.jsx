/*
    Name............TrackerViz.jsx    
    Version.........2.1   
    Author..........www.nabscripts.com
    Description.....This script provides several tools for working with trackers (or layers) such as averaging, rototracking and more.
    Support.........CS3
    Thanks to.......Sean Kennedy (www.mackdadd.com) and Jeff Almasol (www.redefinery.com)
*/

{
    
    /*-------------------------------------------------------------------------------------*/
    function initGlobals(G)
    /*-------------------------------------------------------------------------------------*/
    {        
        G.SCRIPT_NAME               =   "TrackerViz";
        G.VERSION					=	"2.1";
        
        // Min version
        G.APP_VERSION				=	parseFloat(app.version);
        G.MIN_VERSION				=	8.0;

        // DEFAULTS
        G.LAYER_NAME_DFLT           =   "Tracker";
        G.LAYER_COLOR_DFLT          =   [1,0,0];    // red
        G.CYCLE_COLORS_DFLT         =   false;
        G.LAYER_WIDTH_DFLT          =   20;
        G.LAYER_HEIGHT_DFLT         =   20;
        G.GUIDE_LAYER_DFLT          =   true;
        G.SAVE_PREFS_DFLT           =   true;
        G.LT2S_KRATE_DFLT           =   1;
        G.LT2S_ORIGINAL_DFLT        =   false;		// keep initial tangents (when a Shape has been stored)
        G.LT2S_ROTOB_DFLT           =   false;      // rotobezier mask 
        G.LT2S_CLOSED_DFLT        	=   true;		// closed mask
        G.PRECOMPOSE_PINNED_DFLT	=	false;		// precompose pinned layer
        G.BAKING_SAFE_DUR_DFLT      =   180;        // 3 minutes

        // Roto shape
        G.ROTOSHAPE_NAME_DFLT       =   "RotoShape";
        G.ROTOSHAPE_COLOR_DFLT      =   [1,1,1];    // white 
        
        // Linking shape 
        G.LINKINGSHAPE_NAME_DFLT    =   "Linking Shape";
        G.LINKINGSHAPE_COLOR_DFLT   =   [1,1,1];    // white 

        // Track combine
        G.CORRECTED_TRACKER_NAME    =   "Fixed ";   // tracker's name is added to the end of this string
        
        // Corner Pin
        G.CORNER_PINNED_NAME_DFLT	=	"Corner Pinned";
        G.CORNER_PINNED_COLOR_DFLT	=	[1,1,1];	// white
        G.PRECOMP_NAME_DFLT			=	" - Precomp"; // Pinned layer name is added at the beginning of this string

        // Carriage return
        G.CR                        =   "\r";
        
        // Icon?
        G.ICON_EXTENSION			= 	".png";
        G.FOUND_ICON				=	File(G.SCRIPT_NAME + G.ICON_EXTENSION).exists; 
        
        // ABOUT DIALOG
        G.ABOUT_TITLE               =   "About" + " " + G.SCRIPT_NAME + " v" + G.VERSION;
        G.AUTHOR_PNL_NAME           =   "Author";
        G.AUTHOR                    =   "(C) 2008 www.nabscripts.com";
        
        G.DESCRIPTION_PNL_NAME      =   "Description";
        G.DESCRIPTION               =   "Averaging, tracking, rototracking and more." + G.CR + G.CR +                                        
                                        "Functions are: " + G.CR +
                                        "--------------------------------------------------------------" + G.CR +
                                        "* Average Position:" + G.CR +
                                        "Creates a new solid layer at the center of the selected trackers/layers." + G.CR + G.CR +
                                        "* Position + Rotation:" + G.CR +
                                        "Creates a new solid layer at the first selected tracker/layer position, " +
                                        "and rotates it towards the second selected tracker/layer." + G.CR + G.CR +
                                        "* Position + Scale:" + G.CR +
                                        "Creates a new solid layer at the first selected tracker/layer position, " +
                                        "and scales it so that its size matches the distance between the first and " +
                                        "second selected tracker/layer." + G.CR + G.CR +
                                        "* Position + Rotation + Scale:" + G.CR +
                                        "Creates a new solid layer at the first selected tracker/layer position, " +
                                        "rotates it towards the second selected tracker/layer and scales it so " +
                                        "that its size matches the distance between the two trackers/layers." + G.CR + G.CR +
                                        "* Track Combine:" + G.CR +
                                        "Creates a new layer that combines the selected layer position with the position of its parent." + G.CR + G.CR +
                                        "* Corner Pin:" + G.CR +
                                        "Creates a new comp-sized solid with the Corner Pin effect applied to it. The four corners are animated according to the selected trackers/layers position." + G.CR + G.CR +
                                        "* CC Power Pin:" + G.CR +
                                        "Same as above except that the CC Power Pin effect is used instead of the Corner Pin effect." + G.CR + G.CR +
                                        "* Shape To Tracker:" + G.CR +
                                        "Associates each vertex of the selected mask shape/path with track points." + G.CR + G.CR +
                                        "* Shape To Layers:" + G.CR +
                                        "Creates a new solid at each mask vertex (the mask shape/path can be animated)." + G.CR + G.CR +
                                        "* Tracker To Shape:" + G.CR +
                                        "Transforms an animated (or analyzed) tracker into an animated mask shape/path." + G.CR + G.CR +
                                        "* Layers To Shape:" + G.CR +
                                        "Creates an new mask shape/path such that its vertices follow the position " +
                                        "of the selected layers." + G.CR + G.CR +
                                        "Animation methods are:" + G.CR +
                                        "--------------------------------------------------------------" + G.CR +
                                        "* Expression:" + G.CR +
                                        "Property value is dynamically linked to other properties (no keys)." + G.CR + G.CR +
                                        "* Keyframes:" + G.CR +
                                        "Property values are specified by standard keyframes." + G.CR + G.CR +
										"Shape-related options are:" + G.CR +
										"--------------------------------------------------------------" + G.CR +
                                        "* Keys Rate:" + G.CR +
                                        "Indicates the rate at which keyframes are created. For example, the default value 1 creates " +
                                        "a keyframe at every frame, a value of 2 creates a keyframe every two frames." + G.CR + G.CR +
                                        "* RotoB:" + G.CR +
                                        "The mask will be created in rotobezier mode." + G.CR + G.CR +
                                        "* Original:" + G.CR +
                                        "When Shape To Tracker/Layers is executed, tangents of the mask vertices are strored. Later on if Tracker/Layers to Shape is executed, then this option allows to reuse the same customized tangents for the new mask." + G.CR + G.CR +
                                        "* Closed:" + G.CR +
                                        "If this option is checked, the new mask will be a closed mask." + G.CR + G.CR +
                                        "Notes:" + G.CR +
                                        "--------------------------------------------------------------" + G.CR +
                                        "* Every function supports 2D/3D data and parenting." + G.CR + G.CR +
                                        "* The comp work area is taken into account when generating keyframes." + G.CR + G.CR +
                                        "";
        
        G.VIEW_CODE_BTN_NAME        =   "View Code";
        G.VIEW_CODE_ST1             =   "The code was written in TextPad and may not be displayed nicely";
        G.VIEW_CODE_ST2             =   "if your system associates jsx files with ExtendScript ToolKit."
        
        
        // ERROR/WARNING MESSAGES
        // errors
        G.BAD_VERSION_ERR           =   "This script requires AE CS3 or later.";
        G.NO_ICON_ERR				=	"The script cannot find the icon file (\"TrackerViz.png\"). Make sure that the icon file is located in the same folder as the script.";
        G.NO_COMP_ERR               =   "There is no active composition.";
        G.DIM_ERR                   =   "Select 2D or 3D layers but not both.";
        G.SEL_AL2T_ERR              =   "Select at least two trackers having only one track point.";
        G.SEL_AL2L_ERR              =   "Select at least two layers.";
        G.SEL_EX2T_ERR              =   "Select exactly two trackers having only one track point.";
        G.SEL_EX4T_ERR              =   "Select exactly four trackers having only one track point.";
        G.SEL_BAD_TYPE_ERR          =   "Track Motion cannot be applied to the selected layer.";
        G.SEL_BAD_SIZE_ERR          =   "Layer must be comp-sized for this function.";
        G.SEL_BAD_TRANS_ERR         =   "Some Transform properties have been modified. This function requires the default Transform.";
        G.SEL_EX2L_ERR              =   "Select exactly two layers.";
        G.SEL_EX4L_ERR              =   "Select exactly four layers.";
        G.SEL_EX1S_ERR              =   "Select exactly one mask path.";
        G.SEL_2DL_ERR               =   "This function works with 2D layers.";
        G.SEL_ANIMS_ERR             =   "The selected mask path must not be animated.";
        G.SEL_EX1T_ERR              =   "Select exactly one tracker (having normally multiple track points).";
        G.SEL_EX1L_ERR              =   "Select exactly one layer.";
        G.ON_SAME_LAYER_ERR			=	"Make sure that the selected trackers belong to the same layer.";
        G.SEL_WWL_MODE_ERR          =   "Select \"Work With Layers\" to use this function.";
        G.BAD_WIDTH_ERR             =   "Layer width is out of range (1-30000).";
        G.BAD_HEIGHT_ERR            =   "Layer height is out of range (1-30000).";

        // warnings & messages
        G.SEL_NO_ANIMT_WNG          =   "Track points of the selected tracker do not seem to be animated.";
        G.SEL_NO_ANIML_WNG          =   "Selected layers must contain at least one position keyframe.\r\r" +
                                        "Note: if they are animated with expression, you must convert the expression to keyframes";
        G.ALLOW_RENAME_LAYERS_MSG	=	"Some layers have the same name (or the layer that will be created will have the same name as existing layers). Do you allow the script to rename some of the layers to avoid confusion ?";
        G.ALLOW_RENAME_TRACKERS_MSG	=	"Some trackers have the same name. Do you allow the script to rename some of the trackers to avoid confusion ?";
        G.BAKE_KEYS_WNG            	=   "The script is going to generate %s keyframes, do you really want to continue ?\r\r"
                                        + "If you click \"No\" the script will stop, then you can \"Undo\" it "
                                        + "and reduce the work area before trying again.";                                     

        // MAIN PALETTE
        G.SCRIPT_TITLE              =   "TrackerViz";
        
        // static text
        G.WORK_WITH_ST_NAME         =   "Work With:";
        G.FUNCTION_ST_NAME          =   "Function:";
        G.ANIMATION_ST_NAME         =   "Animation:";
        G.KEYS_RATE_ST_NAME        	=   "Keys Rate:";

        // buttons
        G.ABOUT_BTN_NAME            =   "?";
        G.SETTINGS_BTN_NAME         =   "Settings";
        G.PROCEED_BTN_NAME          =   "Proceed";       

        // list items
        G.WORK_WITH_CHOICES         =   '["Layers", "Trackers"]';
        G.FUNCTION_CHOICES          =   '["Average Position", "Position+Rotation", "Position+Scale", "Position+Rotation+Scale", "Track Combine", "Corner Pin (UL-UR-LL-LR)", "CC Power Pin (UL-UR-LL-LR)", "-", "Shape To Layers", "Layers To Shape"]';                
		G.ANIMATION_CHOICES         =   '["Expression", "Keyframes"]';

        // shape to layers/tracker
        G.S2L_NAME                  =   "Shape To Layers";
        G.S2T_NAME                  =   "Shape To Tracker";

        // layers/tracker to shape
        G.L2S_NAME                  =   "Layers To Shape";
        G.T2S_NAME                  =   "Tracker To Shape";

        G.LT2S_ROTOB_CB_NAME        =   "RotoB";
        G.LT2S_ORIGINAL_CB_NAME     =   "Original";
        G.LT2S_CLOSED_CB_NAME		=	"Closed";
        
        // precompose pinned layer
        G.PRECOMPOSE_CB_NAME		=	"Precompose Pinned Layer";
        
        // initial selection
        G.WORK_WITH_INIT            =   0;      // Layers
        G.FUNCTION_INIT             =   0;      // Average Position
        G.ANIMATION_INIT            =   1;      // Keyframes

        // SETTINGS PALETTE 
        G.SETTINGS_TITLE            =   "Settings";    

        // static text
        G.LAYER_NAME_ST_NAME        =   "Layer Name:";
        G.LAYER_COLOR_ST_NAME       =   "Layer Color:";
        G.LAYER_WIDTH_ST_NAME       =   "Layer Width:";
        G.LAYER_HEIGHT_ST_NAME      =   "Layer Height:";    

        // checkboxes
        G.CYCLE_COLORS_CB_NAME      =   "Cycle Colors";
        G.GUIDE_LAYER_CB_NAME       =   "Guide Layer:";
        G.SAVE_PREFS_CB_NAME        =   "Save Prefs";

        // buttons
        G.PICK_COLOR_BTN_NAME       =   "¤";
        G.OK_BTN_NAME               =   "Ok";   

        // STRINGS IN PREFS
        G.TITLE_PRF_NAME            =   "TrackerViz";  // "Settings_TrackerViz" in prefs file
        G.LAYER_NAME_PRF_NAME       =   "Layer Name";
        G.LAYER_RED_PRF_NAME        =   "Layer Red Color";    
        G.LAYER_GREEN_PRF_NAME      =   "Layer Green Color";
        G.LAYER_BLUE_PRF_NAME       =   "Layer Blue Color";
        G.CYCLE_COLORS_PRF_NAME     =   "Cycle Colors";
        G.LAYER_WIDTH_PRF_NAME      =   "Layer Width";
        G.LAYER_HEIGHT_PRF_NAME     =   "Layer Height";
        G.GUIDE_LAYER_PRF_NAME      =   "Guide Layer";

        // a) Safe margin for keyTime
        // b) Faking tangents to activate rotoBezier
        G.EPSILON                   =   1e-3;
        
        // this stores shape value 
        // (it is used for retrieving original tangents when Layers/Tracker to Shape 
        // is applied after Shape to Layers/Tracker)
        G.SHAPE_VAL                 =   null;
        //G.SHAPE_VALS                = new Array()

        // Layer name numbering
        G.LAYER_COUNTER             =   1;          // starts at 1

        // Cycle colors
        G.COLOR_COUNTER             =   0;                                        
        G.CYCLE_COLOR_PRESETS       =   [   [0.710, 0.220, 0.220],      // red
                                            [0.894, 0.847, 0.298],      // yellow
                                            [0.663, 0.796, 0.780],      // aqua
                                            [0.898, 0.737, 0.788],      // pink
                                            [0.663, 0.663, 0.792],      // lavender
                                            [0.906, 0.757, 0.620],      // peach
                                            [0.702, 0.780, 0.702],      // sea foam
                                            [0.404, 0.490, 0.878],      // blue
                                            [0.290, 0.643, 0.298],      // green
                                            [0.557, 0.173, 0.604],      // purple
                                            [0.910, 0.573, 0.051],      // orange
                                            [0.498, 0.271, 0.165],      // brown
                                            [0.957, 0.427, 0.839],      // fuchsia
                                            [0.239, 0.635, 0.647],      // cyan
                                            [0.659, 0.588, 0.467]   ];  // sandstone
    }
              
    /*-------------------------------------------------------------------------------------*/
    function initUI(thisObj)
    /*-------------------------------------------------------------------------------------*/
    {        
		var pal = (thisObj instanceof Panel) ? thisObj : new Window("palette", G.SCRIPT_TITLE, undefined, {resizeable:true});

		var res = 
		"group { \
			orientation:'column', alignment:['fill','top'], \
			header: Group { \
				alignment:['fill','top'], \
				iconBtn: IconButton { icon:'" + G.SCRIPT_NAME + G.ICON_EXTENSION + "', alignment:['fill','center'] }, \
			}, \
			gr1: Group { \
				alignment:['fill','top'], \
				workWithSt: StaticText { text:'" + G.WORK_WITH_ST_NAME + "' }, \
				workWithLst: DropDownList { properties:{items:" + G.WORK_WITH_CHOICES + "}, alignment:['fill','top'], maximumSize:[180,20] }, \
			}, \
			gr2: Group { \
				alignment:['fill','top'], \
				functionSt: StaticText { text:'" + G.FUNCTION_ST_NAME + "' }, \
				functionLst: DropDownList { properties:{items:" + G.FUNCTION_CHOICES + "}, alignment:['fill','top'], maximumSize:[180,20] }, \
			}, \
			gr3: Group { \
				alignment:['fill','top'], \
				animSt: StaticText { text:'" + G.ANIMATION_ST_NAME + "' }, \
				animLst: DropDownList { properties:{items:" + G.ANIMATION_CHOICES + "}, alignment:['fill','top'], maximumSize:[180,20] }, \
			}, \
			gr4: Group { \
				alignment:['fill','top'], \
				kRateSt: StaticText { text:'" + G.KEYS_RATE_ST_NAME + "' }, \
				kRateEdt: EditText { text:'" + G.LT2S_KRATE_DFLT + "', characters:3, alignment:['left','center'] }, \
			}, \
			gr5: Group { \
				alignment:['fill','top'], orientation:'stack', \
				gr5a: Group { \
					alignment:['fill','top'], alignChildren:['fill','top'], \
					dummySt: StaticText { text:'', alignment:['left','center'] }, \
					rotoBezierCb: Checkbox { text:'" + G.LT2S_ROTOB_CB_NAME + "', alignment:['fill','center'] }, \
					originalCb: Checkbox { text:'" + G.LT2S_ORIGINAL_CB_NAME + "', alignment:['fill','center'] }, \
					closedCb: Checkbox { text:'" + G.LT2S_CLOSED_CB_NAME + "', alignment:['fill','center'] }, \
				}, \
				gr5b: Group { \
					alignment:['fill','top'], alignChildren:['fill','top'], \
					dummySt: StaticText { text:'', alignment:['left','center'] }, \
					precomposeCb: Checkbox { text:'" + G.PRECOMPOSE_CB_NAME + "', alignment:['fill','center'] }, \
				}, \
			}, \
			cmds: Group { \
				alignment:['left','top'], \
				dummySt: StaticText { text:'', alignment:['left','center'] }, \
				settingsBtn: Button { text:'" + G.SETTINGS_BTN_NAME + "', alignment:['fill','center'] }, \
				proceedBtn: Button { text:'" + G.PROCEED_BTN_NAME + "', alignment:['fill','center'], preferredSize:[90,20] }, \
			}, \
		}";
		pal.grp = pal.add(res);
		
		pal.grp.gr1.workWithLst.graphics.foregroundColor = 
		pal.grp.gr2.functionLst.graphics.foregroundColor = 
		pal.grp.gr3.animLst.graphics.foregroundColor = 
		pal.grp.gr4.kRateEdt.graphics.foregroundColor = pal.graphics.newPen(pal.graphics.BrushType.SOLID_COLOR, [0,0,0], 1);

		pal.grp.gr1.workWithLst.selection = G.WORK_WITH_INIT;
		pal.grp.gr2.functionLst.selection = G.FUNCTION_INIT;
		pal.grp.gr3.animLst.selection = G.ANIMATION_INIT;
		
		pal.grp.gr2.functionSt.preferredSize.width += 15;
		
		pal.grp.gr1.workWithSt.preferredSize.width = 		
		pal.grp.gr3.animSt.preferredSize.width = 
		pal.grp.gr4.kRateSt.preferredSize.width = 
		pal.grp.gr5.gr5a.dummySt.preferredSize.width = 
		pal.grp.gr5.gr5b.dummySt.preferredSize.width = 
		pal.grp.cmds.dummySt.preferredSize.width = pal.grp.gr2.functionSt.preferredSize.width;
		
		pal.grp.gr4.visible = false;
		pal.grp.gr5.visible = false;
		
		/*-----------------------------------------------------------------------------*/
		pal.grp.header.iconBtn.onClick = function () 
		/*-----------------------------------------------------------------------------*/
		{
            var aboutUI = new Object();
            
            aboutUI.dlg = new Window("dialog", G.ABOUT_TITLE, [0,0,520,470]);
            
            aboutUI.dlg.authPnl = aboutUI.dlg.add("panel", [25,25,490,85], G.AUTHOR_PNL_NAME);
            aboutUI.dlg.authPnl.add("statictext", [30,21,450,41], G.AUTHOR);
                        
            aboutUI.dlg.descrPnl = aboutUI.dlg.add("panel", [25,100,490,400], G.DESCRIPTION_PNL_NAME);
            aboutUI.dlg.descrPnl.descrEdt = aboutUI.dlg.descrPnl.add("edittext", [25,30,435,260], G.DESCRIPTION, {multiline:true})
            
            aboutUI.dlg.okBtn = aboutUI.dlg.add("button", [390,435,490,455], G.OK_BTN_NAME);
            aboutUI.dlg.okBtn.onClick = function () { this.parent.close(); };
            
            aboutUI.dlg.add("statictext", [25,405,355,420], G.VIEW_CODE_ST1); 
            aboutUI.dlg.add("statictext", [25,420,355,435], G.VIEW_CODE_ST2); 
            aboutUI.dlg.viewCodeBtn = aboutUI.dlg.add("button", [25,435,125,455], G.VIEW_CODE_BTN_NAME);
                
            aboutUI.dlg.viewCodeBtn.onClick = function () { new File($.fileName).execute(); };
            
            aboutUI.dlg.center();
            aboutUI.dlg.show();
		};
		
		/*-----------------------------------------------------------------------------*/
		pal.grp.gr1.workWithLst.onChange = function () 
        /*-----------------------------------------------------------------------------*/
        {
            // Change function's list according to the current selection
            if (this.selection.index == 0)
            {   
                // layers to shape / shape to layers
                pal.grp.gr2.functionLst.items[8].text = G.S2L_NAME;
                pal.grp.gr2.functionLst.items[9].text = G.L2S_NAME;
                
            }
            else if (this.selection.index == 1)
            {
                // tracker to shape / shape to tracker
                pal.grp.gr2.functionLst.items[8].text = G.S2T_NAME;
                pal.grp.gr2.functionLst.items[9].text = G.T2S_NAME;
            }
            if (pal.grp.gr2.functionLst.selection.toString() == G.S2T_NAME || 
                pal.grp.gr2.functionLst.selection.toString() == G.L2S_NAME ||
                pal.grp.gr2.functionLst.selection.toString() == G.T2S_NAME)
            {
                pal.grp.cmds.settingsBtn.enabled = false;
            }
            else
            {
                pal.grp.cmds.settingsBtn.enabled = true;
            }              			
		}

		/*-----------------------------------------------------------------------------*/
		pal.grp.gr2.functionLst.onChange = function () 
        /*-----------------------------------------------------------------------------*/
        {            
            if (this.selection.toString() == G.S2L_NAME || this.selection.toString() == G.S2T_NAME)
            { 
                pal.grp.gr3.animLst.selection       = 1;                // indicates we'll use keyframes
                pal.grp.gr3.animLst.enabled         = false;
                
                pal.grp.gr4.visible					= false;
                pal.grp.gr5.visible					= false;                
                
                pal.grp.cmds.settingsBtn.enabled	= this.selection.toString() == G.S2L_NAME;
            }            
            else if (this.selection.toString() == G.L2S_NAME || this.selection.toString() == G.T2S_NAME)
            {                
                pal.grp.gr3.animLst.selection       = 1;                // indicates we'll use keyframes
                pal.grp.gr3.animLst.enabled         = false;
                
                pal.grp.gr4.visible					= true;
                pal.grp.gr5.visible					= true;
                pal.grp.gr5.gr5a.visible			= true;
                pal.grp.gr5.gr5b.visible			= false;
                
                pal.grp.gr4.kRateEdt.value      	= G.LT2S_KRATE_DFLT;
                pal.grp.gr5.gr5a.rotoBezierCb.value	= G.LT2S_ROTOB_DFLT;                
                pal.grp.gr5.gr5a.originalCb.value	= G.LT2S_ORIGINAL_DFLT;
                pal.grp.gr5.gr5a.closedCb.value		= G.LT2S_CLOSED_DFLT;
                
                pal.grp.cmds.settingsBtn.enabled	= false;
            }
            else if (this.selection.toString().indexOf("Pin") != -1)
            {
				pal.grp.gr4.visible					= false;
				pal.grp.gr5.visible					= true;
				pal.grp.gr5.gr5a.visible			= false;				
				pal.grp.gr5.gr5b.visible			= true;
				pal.grp.gr5.gr5b.precomposeCb.value	= G.PRECOMPOSE_PINNED_DFLT;
				
				pal.grp.cmds.settingsBtn.enabled	= false;
			}
            else
            {
                pal.grp.gr3.animLst.enabled         = true;
                
                pal.grp.gr4.visible					= false;
                pal.grp.gr5.visible					= false;
                
                pal.grp.cmds.settingsBtn.enabled	= true;
            }
        }

		/*-----------------------------------------------------------------------------*/
		pal.grp.gr4.kRateEdt.onChange = function () 
        /*-----------------------------------------------------------------------------*/
        {
            var dataIn = this.text;
            if (isNaN(dataIn) || parseInt(dataIn) < 1)
            {
                this.text = G.LT2S_KRATE_DFLT;
                return;
            }
            G.LT2S_KRATE_DFLT = Math.round(parseFloat(dataIn));
            this.text = G.LT2S_KRATE_DFLT;
        }     

		/*-----------------------------------------------------------------------------*/
		pal.grp.gr5.gr5a.rotoBezierCb.onClick = function () 
        /*-----------------------------------------------------------------------------*/
        {
            G.LT2S_ROTOB_DFLT					= this.value;
            G.LT2S_ORIGINAL_DFLT				= false;
            pal.grp.gr5.gr5a.originalCb.value	= false;            
        }         

		/*-----------------------------------------------------------------------------*/
		pal.grp.gr5.gr5a.originalCb.onClick = function () 
        /*-----------------------------------------------------------------------------*/
        {
            G.LT2S_ORIGINAL_DFLT        		= this.value;
            G.LT2S_ROTOB_DFLT           		= false; 
            pal.grp.gr5.gr5a.rotoBezierCb.value	= false;                        
        }

		/*-----------------------------------------------------------------------------*/
		pal.grp.gr5.gr5a.closedCb.onClick = function () 
        /*-----------------------------------------------------------------------------*/
        {
            G.LT2S_CLOSED_DFLT = this.value;            
        }         

		/*-----------------------------------------------------------------------------*/
		pal.grp.gr5.gr5b.precomposeCb.onClick = function () 
        /*-----------------------------------------------------------------------------*/
        {
            G.PRECOMPOSE_PINNED_DFLT = this.value;            
        }         
        
		/*-----------------------------------------------------------------------------*/
		pal.grp.cmds.settingsBtn.onClick = function () 
        /*-----------------------------------------------------------------------------*/
        {            
            var settingsUI = new Object();
            
            // Palette
            settingsUI.pal = new Window("palette", G.SETTINGS_TITLE, [900,390+15,1090,620+15]);   
            
            settingsUI.pal.add("statictext", [15,24,90,40], G.LAYER_NAME_ST_NAME); 
            settingsUI.pal.layerNameEdt = settingsUI.pal.add("edittext", [95,20,175,40], G.LAYER_NAME_DFLT);            
            
            settingsUI.pal.add("statictext", [15,54,90,70], G.LAYER_COLOR_ST_NAME); 
            settingsUI.pal.layerColEdt;
               
            settingsUI.pal.grp = settingsUI.pal.add("group", [95,50,135,70]); 
            settingsUI.pal.pickColorBtn = settingsUI.pal.add("button", [150,50,175,70], G.PICK_COLOR_BTN_NAME);
                
            var colorInt = 255 * (  65536 * G.LAYER_COLOR_DFLT[0] 
                                    + 256 * G.LAYER_COLOR_DFLT[1] 
                                    +       G.LAYER_COLOR_DFLT[2]   );
                
            setColor(settingsUI.pal.grp, G.LAYER_COLOR_DFLT);
                   
            settingsUI.pal.pickColorBtn.onClick = pickColorBtn_OnClick;                

			/*-------------------------------------------------------------------------*/
			function pickColorBtn_OnClick()
			/*-------------------------------------------------------------------------*/                
			{   
				var c = $.colorPicker(colorInt);    // open color selection dialog

				if (c == -1) return;                // cancel button has been clicked

				var r = ((c >> 16) & 0xFF) / 255;
				var g = ((c >> 8) & 0xFF) / 255;
				var b = (c & 0xFF) / 255;

				setColor(settingsUI.pal.grp, [r,g,b]);

				colorInt = c;                       // update default color picker

				G.LAYER_COLOR_DFLT = [r,g,b];                    
			}

			/*-------------------------------------------------------------------------*/
			function setColor(obj, color)
			/*-------------------------------------------------------------------------*/
			{
				var gfx = obj.graphics;
				try
				{
					gfx.backgroundColor = gfx.newBrush(gfx.BrushType.SOLID_COLOR, color);   
				}
				catch(e)
				{
					// miam-miam
				}
			}                

            settingsUI.pal.cycleColorsCb = settingsUI.pal.add("checkbox", [95,80,175,105], G.CYCLE_COLORS_CB_NAME);
            settingsUI.pal.cycleColorsCb.value = G.CYCLE_COLORS_DFLT;
            
            settingsUI.pal.add("statictext", [15,114,90,130], G.LAYER_WIDTH_ST_NAME); 
            settingsUI.pal.layerWidthEdt = settingsUI.pal.add("edittext", [95,110,175,130], G.LAYER_WIDTH_DFLT);            
            
            settingsUI.pal.add("statictext", [15,144,90,160], G.LAYER_HEIGHT_ST_NAME); 
            settingsUI.pal.layerHeightEdt = settingsUI.pal.add("edittext", [95,140,175,160], G.LAYER_HEIGHT_DFLT);   
            
            settingsUI.pal.add("statictext", [15,174,90,190], G.GUIDE_LAYER_CB_NAME); 
            settingsUI.pal.guideLayerCb = settingsUI.pal.add("checkbox", [95,170,175,190]);
            settingsUI.pal.guideLayerCb.value = G.GUIDE_LAYER_DFLT;

            settingsUI.pal.savePrefsCb = settingsUI.pal.add("checkbox", [15,200,85,225], G.SAVE_PREFS_CB_NAME);
            settingsUI.pal.savePrefsCb.value = G.SAVE_PREFS_DFLT;
            
            settingsUI.pal.okBtn = settingsUI.pal.add("button", [95,200,175,220], G.OK_BTN_NAME);
            
            // Display palette
            //settingsUI.pal.center();
            settingsUI.pal.show();
            
            // Events
            settingsUI.pal.okBtn.onClick            = okBtn_OnClick;
            settingsUI.pal.layerNameEdt.onChange    = layerNameEdt_OnChange;            
            settingsUI.pal.cycleColorsCb.onClick    = cycleColorsCb_OnClick;
            settingsUI.pal.layerWidthEdt.onChange   = layerWidthEdt_OnChange;
            settingsUI.pal.layerHeightEdt.onChange  = layerHeightEdt_OnChange;
            settingsUI.pal.guideLayerCb.onClick     = guideLayerCb_OnClick;
            settingsUI.pal.savePrefsCb.onClick      = savePrefsCb_OnClick;
            
            // Secondary palette's functions
            /*-----------------------------------------------------------------------------*/
            function okBtn_OnClick()
            /*-----------------------------------------------------------------------------*/
            {
                if (settingsUI.pal.savePrefsCb.value)
                {                    
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.LAYER_NAME_PRF_NAME,   G.LAYER_NAME_DFLT             );
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.LAYER_RED_PRF_NAME,    G.LAYER_COLOR_DFLT[0]         );
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.LAYER_GREEN_PRF_NAME,  G.LAYER_COLOR_DFLT[1]         );
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.LAYER_BLUE_PRF_NAME,   G.LAYER_COLOR_DFLT[2]         );
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.CYCLE_COLORS_PRF_NAME, G.CYCLE_COLORS_DFLT ? 1 : 0   );
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.LAYER_WIDTH_PRF_NAME,  G.LAYER_WIDTH_DFLT            );
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.LAYER_HEIGHT_PRF_NAME, G.LAYER_HEIGHT_DFLT           );
                    app.settings.saveSetting(G.TITLE_PRF_NAME, G.GUIDE_LAYER_PRF_NAME,  G.GUIDE_LAYER_DFLT ? 1 : 0    );
                }
                this.parent.close();
            }
 
            /*-----------------------------------------------------------------------------*/
            function layerNameEdt_OnChange()
            /*-----------------------------------------------------------------------------*/
            {
                this.text = this.text.substring(0,31);
                G.LAYER_NAME_DFLT = this.text;
            }
            
            /*-----------------------------------------------------------------------------*/
            function layerColEdt_OnChange()
            /*-----------------------------------------------------------------------------*/
            {                
                var colorStr = this.text;
                
                var colorArray = colorStr.split(",");
                if (colorArray.length != 3)
                {
                    throwErr(G.BAD_COLOR_ERR);
                    this.text = G.LAYER_COLOR_DFLT[0] + "," + G.LAYER_COLOR_DFLT[1] + "," + G.LAYER_COLOR_DFLT[2];
                    return;
                }
                for (var i = 0; i < colorArray.length; i++)
                {
                    if (isNaN(colorArray[i]) || colorArray[i] < 0.0 || colorArray[i] > 1.0)
                    {
                        throwErr(G.BAD_COLOR_ERR);
                        this.text = G.LAYER_COLOR_DFLT[0] + "," + G.LAYER_COLOR_DFLT[1] + "," + G.LAYER_COLOR_DFLT[2];
                        return;
                    }
                }                
                G.LAYER_COLOR_DFLT = colorArray;
            }

            /*-----------------------------------------------------------------------------*/
            function cycleColorsCb_OnClick()
            /*-----------------------------------------------------------------------------*/
            {
                G.CYCLE_COLORS_DFLT = this.value;
            } 
            
            /*-----------------------------------------------------------------------------*/
            function layerWidthEdt_OnChange()
            /*-----------------------------------------------------------------------------*/
            {
                var dataIn = this.text;
                if (isNaN(dataIn) || parseInt(dataIn) < 1 || parseInt(dataIn) > 30000)
                {
                    throwErr(G.BAD_WIDTH_ERR);
                    this.text = G.LAYER_WIDTH_DFLT;
                    return;
                }
                G.LAYER_WIDTH_DFLT = Math.round(parseFloat(dataIn));                
            }
            
            /*-----------------------------------------------------------------------------*/
            function layerHeightEdt_OnChange()
            /*-----------------------------------------------------------------------------*/
            {
                var dataIn = this.text;
                if (isNaN(dataIn) || parseInt(dataIn) < 1 || parseInt(dataIn) > 30000)
                {
                    throwErr(G.BAD_HEIGHT_ERR);
                    this.text = G.LAYER_HEIGHT_DFLT;
                    return;
                }
                G.LAYER_HEIGHT_DFLT = Math.round(parseFloat(dataIn));                
            }
            
            /*-----------------------------------------------------------------------------*/
            function guideLayerCb_OnClick()
            /*-----------------------------------------------------------------------------*/
            {
                G.GUIDE_LAYER_DFLT = this.value;
            } 

            /*-----------------------------------------------------------------------------*/
            function savePrefsCb_OnClick()
            /*-----------------------------------------------------------------------------*/
            {
                G.SAVE_PREFS_DFLT = this.value;
            }  
        }
        
        /*-----------------------------------------------------------------------------*/
        pal.grp.cmds.proceedBtn.onClick = function ()
        /*-----------------------------------------------------------------------------*/
        { 
			var workWithLayersFlag      = (pal.grp.gr1.workWithLst.selection.index == 0);
            var workWithTrackersFlag    = (pal.grp.gr1.workWithLst.selection.index == 1);
            var avgPosFlag              = (pal.grp.gr2.functionLst.selection.index == 0);
            var posRotFlag              = (pal.grp.gr2.functionLst.selection.index == 1);
            var posScaFlag              = (pal.grp.gr2.functionLst.selection.index == 2);
            var posRotScaFlag           = (pal.grp.gr2.functionLst.selection.index == 3);
            var tCombiFlag              = (pal.grp.gr2.functionLst.selection.index == 4);
            var cPinFlag				= (pal.grp.gr2.functionLst.selection.index == 5);
            var pPinFlag				= (pal.grp.gr2.functionLst.selection.index == 6);
            var s2ltFlag                = (pal.grp.gr2.functionLst.selection.index == 8); // 7 is separator
            var lt2sFlag                = (pal.grp.gr2.functionLst.selection.index == 9);
            var allowExprFlag           = (pal.grp.gr3.animLst.selection.index == 0);
            var bakeKeysFlag            = (pal.grp.gr3.animLst.selection.index == 1);            
            //var progressBar             = pal.grp.gr7.pgsBar;
			
            Main(   workWithTrackersFlag, 
                    workWithLayersFlag, 
                    avgPosFlag, 
                    posRotFlag,
                    posScaFlag,
                    posRotScaFlag,
                    tCombiFlag,
                    cPinFlag,
                    pPinFlag,
                    s2ltFlag,
                    lt2sFlag,                    
                    allowExprFlag, 
                    bakeKeysFlag/*, 
                    progressBar*/);    
        }               
				
		return pal;
	}
		
		

    
    /*-------------------------------------------------------------------------------------*/
    // Some data structures
    /*-------------------------------------------------------------------------------------*/
    
    /*-------------------------------------------------------------------------------------*/
    function TrackersContainer()
    /*-------------------------------------------------------------------------------------*/
    {
        var container               = new Object();
        
        container.containingLayers  = new Array();  // [       layer1          ,        layer2         ,...]
        container.trackers          = new Array();  // [[tracker1,tracker2,...], [tracker1,tracker2,..],...]        
        container.trackPoints       = new Array();  // [[trackPt1,trackPt2,...], [trackPt1,trackPt2,..],...]        
        container.attachPoints 		= new Array();  // [[attachPt1,attachPt2,...], [attachPt1,attachPt2,..],...]        
        container.selAL2TErr        = false;        // error flag  
        container.selEX2TErr        = false;        // error flag
        container.dimErr            = false;        // error flag
        
        return container;
    }    

    /*-------------------------------------------------------------------------------------*/
    function TrackersContainer2()
    /*-------------------------------------------------------------------------------------*/
    {
        var container               = new Object();
        
        container.containingLayers  = new Array();  // [       layer1          ,        layer2         ,...] /* only one layer in this version */
        container.trackers          = new Array();  // [[tracker1,tracker2,...], [tracker1,tracker2,..],...]        
        container.trackPoints       = new Array();  // [[trackPt1,trackPt2,...], [trackPt1,trackPt2,..],...]        
        container.attachPoints 		= new Array();  // [[attachPt1,attachPt2,...], [attachPt1,attachPt2,..],...]        
        container.selEX4TErr        = false;        // error flag
        container.onSameLayerErr	= false;		// error flag
        //container.dimErr            = false;        // error flag
        
        return container;
    }    
    
    /*-------------------------------------------------------------------------------------*/
    function LayersContainer()
    /*-------------------------------------------------------------------------------------*/
    {
        var container               = new Object();
        
        container.layers            = new Array();  // array of layer
        container.positions         = new Array();  // array of position property
        container.selAL2LErr        = false;        // error flag
        container.selEX2LErr        = false;        // error flag
        container.dimErr            = false;        // error flag
        
        return container;
    }

    /*-------------------------------------------------------------------------------------*/
    function LayersContainer2()
    /*-------------------------------------------------------------------------------------*/
    {
        var container               = new Object();
        
        container.layers            = new Array();  // array of layer
        container.positions         = new Array();  // array of position property
        container.selEX4LErr        = false;        // error flag
        container.dimErr            = false;        // error flag
        
        return container;
    }
    
    /*-------------------------------------------------------------------------------------*/
    function NameWng()
    /*-------------------------------------------------------------------------------------*/
    {
        var nameWng                 = new Object();
        
        nameWng.layersNameWng       = false;        // warning flag
        nameWng.trackersNameWng     = false;        // warning flag
        
        return nameWng;
    } 

    /*-------------------------------------------------------------------------------------*/
    function S2LTContainer()
    /*-------------------------------------------------------------------------------------*/
    {
        var container               = new Object();
        
        container.shapes            = new Shape();  // array of mask shape (value)
        container.shape             = new Shape();  // mask shape (value)
        container.vertices          = new Array();  // array of vertex (tracker)
                                                    // array of array of vertex (layers, animation allowed)
        container.start             = 0;            // time indicator
        container.end               = 0;            // time indicator
        container.selEX1SErr        = false;        // error flag
        container.selAnimSErr       = false;        // error flag
        container.selBadTypeErr     = false;        // error flag
        container.selBadSizeErr     = false;        // error flag
        container.selBadTransErr    = false;        // error flag        
        
        return container;
    }

    /*-------------------------------------------------------------------------------------*/
    function LT2SContainer()
    /*-------------------------------------------------------------------------------------*/
    {
        var container               = new Object();
        
        container.layers            = new Array();  // array of layers
        container.trackPoints       = new Array();  // array of trackPoints
        container.earliest          = 0;            // key time
        container.latest            = 0;            // key time
        container.incr              = 0;            // time increment
        container.selEX1TErr        = false;        // error flag
        container.selAL2LErr        = false;        // error flag
        container.selNoAnimTWng     = false;        // warning flag
        container.selNoAnimLWng     = false;        // warning flag
        
        return container;
    }
    
    /*-------------------------------------------------------------------------------------*/
    function TrackCombineContainer()
    /*-------------------------------------------------------------------------------------*/
    {
        var container               = new Object();
        
        container.pos               = null;         // position stream of the selected layer
        container.selEX1LErr        = false;
        
        return container;
    }
    
    /*-------------------------------------------------------------------------------------*/
    // Script functions
    /*-------------------------------------------------------------------------------------*/
    
    /*-------------------------------------------------------------------------------------*/
    function throwErr(err)
    /*-------------------------------------------------------------------------------------*/
    {
        alert(G.SCRIPT_NAME + " error: \r\r" + err, G.SCRIPT_NAME);
    }

    /*-------------------------------------------------------------------------------------*/
    function throwWng(wng)
    /*-------------------------------------------------------------------------------------*/
    {
        alert(G.SCRIPT_NAME + " warning: \r\r" + wng, G.SCRIPT_NAME);
    }
    
    /*-------------------------------------------------------------------------------------*/
    function getLayerFromProp(prop)
    /*-------------------------------------------------------------------------------------*/
    {
        var layer;
        
        while (prop = prop.propertyGroup(1))
        {
            layer = prop;
        }
        
        return layer;
    }

    /*-------------------------------------------------------------------------------------*/
    function getEarliestLatestAttachPointKeyTime(tracker)
    /*-------------------------------------------------------------------------------------*/
    {
        var earliest = 3*3600 + G.EPSILON;    
        var latest   = -earliest;
		var curLayer = getLayerFromProp(tracker);
		
        for (var i = 1; i <= tracker.numProperties; i++)
        {
            var curTrackPoint = tracker.property(i);            
            var curAttachPoint = curTrackPoint.property("ADBE MTracker Pt Attach Pt");
            
            if (curAttachPoint.numKeys)
            {
                // Check only the first and last key to speed things up
                if (curAttachPoint.keyTime(1) < earliest)
                    earliest = curAttachPoint.keyTime(1);

                if (curAttachPoint.keyTime(curAttachPoint.numKeys) > latest)
                    latest = curAttachPoint.keyTime(curAttachPoint.numKeys);
            }

            if (curAttachPoint.expressionEnabled) // when expression is enabled we take in/out points 
            {                                     // which are supposed to be earlier/later than the first/last key
                if (curLayer.inPoint < earliest)
                    earliest = curLayer.inPoint;
                
                if (curLayer.outPoint > latest)
                    latest = curLayer.outPoint;
            }            
        }
        
        // Something weird occurred
        if (earliest == 3*3600 + G.EPSILON)
        {
            return null;
        }            

        return [earliest, latest];
    }

    /*-------------------------------------------------------------------------------------*/
    function getEarliestLatestPositionKeyTime(layers)
    /*-------------------------------------------------------------------------------------*/
    {
        var earliest = 3*3600 + G.EPSILON;    
        var latest   = -earliest;

        for (var i = 0; i < layers.length; i++)
        {
            var curLayer = layers[i];
            var curPosition = curLayer.position;
            
            if (curPosition.numKeys)
            {
                // Check only the first and last key to speed things up
                if (curPosition.keyTime(1) < earliest)
                    earliest = curPosition.keyTime(1);

                if (curPosition.keyTime(curPosition.numKeys) > latest)
                    latest = curPosition.keyTime(curPosition.numKeys);
            }
            
            if (curPosition.expressionEnabled)  // when expression is enabled we take in/out points 
            {                                   // which are supposed to be earlier/later than the first/last key
                if (curLayer.inPoint < earliest)
                    earliest = curLayer.inPoint;
                
                if (curLayer.outPoint > latest)
                    latest = curLayer.outPoint;
            }
        }
        
        // Something weird occurred
        if (earliest == 3*3600 + G.EPSILON)
        {
            return null;
        }            

        return [earliest, latest];
    }
    
    /*-------------------------------------------------------------------------------------*/
    function getS2LTContainer(  comp, 
                                workWithTrackersFlag, 
                                workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {
        var container = new S2LTContainer();
        
        // Make sure there is exactly one mask selected
        if (comp.selectedProperties.length != 2) // mask + mask shape
        {
            container.selEX1SErr = true;
            return container;
        }
        if (comp.selectedProperties[1].matchName != "ADBE Mask Shape")
        {
            container.selEX1SErr = true;
            return container;
        }
        
        // Retrieve containing layer
        var layer = getLayerFromProp(comp.selectedProperties[0]);
        
        if (workWithTrackersFlag)
        {
            // Make sure the selected layer is ok for Track Motion
            if (layer instanceof AVLayer && layer.canSetTimeRemapEnabled) 
            {
                // do nothing, we get a footage or a comp, that's fine
            }
            else
            {
                container.selBadTypeErr = true;
                return container;
            }
        }
        else if (workWithLayersFlag)
        {
            // Make sure the selected layer is comp-sized
            if (layer.width != comp.width || layer.height != comp.height)
            {
                container.selBadSizeErr = true;
                return container;
            }            
            // Make sure transform properties have not been modified
            var transGroup = layer.property("ADBE Transform Group");
            for (var i = 1; i <= transGroup.numProperties; i++)
            {
				if (transGroup.property(i).matchName != "ADBE Opacity" && transGroup.property(i).isModified)
                {
                    container.selBadTransErr = true;
                    return container;
                }
            }            
        }
                
        // Mask data
        var mask = comp.selectedProperties[0];
        var shape = mask.property("ADBE Mask Shape");
        var numKeys = shape.numKeys;     
        
        if (workWithTrackersFlag)
        {
            // Make sure the mask shape isn't animated
            if (numKeys)
            {
                container.selAnimSErr = true
                return container;
            }
            // Store shape data
            else
            {
                container.shape = shape.value;
                container.vertices = shape.value.vertices;
                
                G.SHAPE_VAL = shape.value;
            }
        }
        else if (workWithLayersFlag)
        {            
            if (numKeys) // Store each shape
            {
                var start = Math.max(shape.keyTime(1), comp.workAreaStart);
                var end = Math.min(shape.keyTime(shape.numKeys), comp.workAreaStart + comp.workAreaDuration);
                                
                container.start = start;
                container.end = end;
                
                var k = 0;
                for (var i = start; i <= end + G.EPSILON; i += comp.frameDuration)
                {                
                    container.shapes[k] = shape.valueAtTime(i, false);
                    container.vertices[k] = shape.valueAtTime(i, false).vertices;
                    
                    //G.SHAPE_VALS[k] = shape.valueAtTime(i, false);
                    
                    k++;
                }
            }
            else // Store current shape
            {   
                container.shapes[0] = shape.value;
                container.vertices[0] = shape.value.vertices;
                
                G.SHAPE_VAL = shape.value;
            }
        }
        
        return container;
    }

    /*-------------------------------------------------------------------------------------*/
    function getLT2SContainer(  comp,
                                workWithTrackersFlag,
                                workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {           
        var container = new LT2SContainer();
        
        var tracker;
        var layers;
        
        var earliestLatest;
        var earliest;
        var latest;
        var incr;
        
        if (workWithTrackersFlag)
        {
            // Make sure there is exactly one tracker selected 
            if (comp.selectedProperties.length != 1) 
            {
                container.selEX1TErr = true;
                return container;
            }
            if (comp.selectedProperties[0].matchName != "ADBE MTracker")
            {
                container.selEX1TErr = true;
                return container;
            }
            tracker = comp.selectedProperties[0];
            
            // Retrieve first and last key time
            earliestLatest = getEarliestLatestAttachPointKeyTime(tracker);
            if (!earliestLatest)
            {
                container.selNoAnimTWng = true;
                return container;
            }
                
            // Loop through each track point
            for (var j = 1; j <= tracker.numProperties; j++)
            {
                container.trackPoints.push(tracker.property(j)); // store trackPoint
            }
        }
        else if (workWithLayersFlag) 
        {
            layers = comp.selectedLayers;
            
            // Make sure we have at least two layers selected (mask with less than 2 points are too boring!)
            if (layers.length < 2)
            {
                container.selAL2LErr = true;
                return container;
            }
            
            // Retrieve first and last key time
            earliestLatest = getEarliestLatestPositionKeyTime(layers); 
            if (!earliestLatest)
            {
                container.selNoAnimLWng = true;
                return container;
            }
            
            // Store layers            
            container.layers = layers;
        }

        // Take work area into account
        earliest = Math.max(earliestLatest[0], comp.workAreaStart);
        latest = Math.min(earliestLatest[1], comp.workAreaStart + comp.workAreaDuration);
        incr = G.LT2S_KRATE_DFLT * comp.frameDuration;
        
        container.earliest = earliest;
        container.latest = latest;
        container.incr = incr; 
        
        return container;
    }
    
    /*-------------------------------------------------------------------------------------*/
    function searchIdenticalNames(  comp,
                                    workWithTrackersFlag, 
                                    workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {        
        var nameWng = new NameWng(); // stores warnings

        var layers = comp.layers;    // index starts at 1
        
        // Name of the layer we'll add to comp
        var newLayerName = (G.LAYER_NAME_DFLT + " " + G.LAYER_COUNTER).substring(0,31);
        
        // Look at each pair of layers
        for (var i = 1; !nameWng.layersNameWng && i < layers.length; i++)
        {
            for (var j = i + 1; !nameWng.layersNameWng && j <= layers.length; j++)            
            {
                if (layers[i].name == layers[j].name)
                {
                    nameWng.layersNameWng = true;
                }
            }
            // Also look at the layer we'll create
            if (layers[i].name == newLayerName) 
            {
                nameWng.layersNameWng = true;
            }
        }
        // The last one
        if (layers[layers.length].name == newLayerName)
        {
            nameWng.layersNameWng = true;
        }
        
        // Look at each pair of trackers on a given layer (for all layers)  
        if (workWithTrackersFlag)
        {
            err = false; // reset flag            
            
            for (var i = 1; !nameWng.trackersNameWng && i <= layers.length; i++)
            {
                var curLayer = layers[i];
                
                for (var j = 1; !nameWng.trackersNameWng && j <= curLayer.numProperties; j++)
                {
                    var curGroup = curLayer.property(j);
                    
                    if (curGroup.matchName == "ADBE MTrackers") // trackers group
                    {
                        for (var k = 1; !nameWng.trackersNameWng && k < curGroup.numProperties; k++) 
                        {               
                            var  curTrackerA = curGroup.property(k);
                            
                            if (curTrackerA.matchName == "ADBE MTracker") // we got a tracker
                            {   
                                for (var t = k + 1; !nameWng.trackersNameWng && t <= curGroup.numProperties; t++) 
                                {
                                    var curTrackerB = curGroup.property(t);
                                    
                                    if (curTrackerB.matchName == "ADBE MTracker") // we got another tracker
                                    {
                                        if (curTrackerA.name == curTrackerB.name)
                                        {
                                            nameWng.trackersNameWng = true;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            } 
        }
        
        return nameWng;
    }
    
    /*-------------------------------------------------------------------------------------*/
    function autoRenameLayers(comp)
    /*-------------------------------------------------------------------------------------*/
    {
		var newLayerName = (G.LAYER_NAME_DFLT + " " + G.LAYER_COUNTER).substring(0,31);
		
		for (var i = 1; i < comp.numLayers; i++)
		{
			var layerA = comp.layer(i);

			for (var j = i + 1; j <= comp.numLayers; j++)
			{
				var layerB = comp.layer(j);

				if (layerA.name == layerB.name)
				{
					layerB.name += " ";
				}
			}
			
			if (layerA == newLayerName)
			{
				G.LAYER_NAME_DFLT += " ";
			}				
		}		
	}
	
    /*-------------------------------------------------------------------------------------*/
    function autoRenameTrackers(comp)
    /*-------------------------------------------------------------------------------------*/
    {
		for (var i = 1; i <= comp.numLayers; i++)
		{
			var curLayer = comp.layer(i);		                
			
			for (var p = 1; p <= curLayer.numProperties; p++)
			{
				var curGroup = curLayer.property(p);		                    
				
				if (curGroup.matchName == "ADBE MTrackers") // trackers group
				{
					for (var m = 1; m < curGroup.numProperties; m++) 
					{               
						var curTrackerA = curGroup.property(m);		                            
						
						if (curTrackerA.matchName == "ADBE MTracker") // we got a tracker
						{   
							for (var n = m + 1; n <= curGroup.numProperties; n++) 
							{
								var curTrackerB = curGroup.property(n);		                                    
								
								if (curTrackerB.matchName == "ADBE MTracker") // we got another tracker
								{
									if (curTrackerA.name == curTrackerB.name)
									{
										curTrackerB.name += " ";
                                    }
								}
							}
						}
					}
				}
			}
		}
	}
	
    /*-------------------------------------------------------------------------------------*/
    function getTrackersContainer(  comp, 
                                    avgPosFlag, 
                                    posRotFlag, 
                                    posScaFlag, 
                                    posRotScaFlag)
    /*-------------------------------------------------------------------------------------*/
    {   
        // Data container
        var container = new TrackersContainer();
         
        for (var i = 0; i < comp.selectedLayers.length; i++)
        {
            var curLayer = comp.selectedLayers[i]; 
            container.containingLayers[i] = curLayer; // store layer
             
            // Make sure layers have same dimension
            if (curLayer.threeDLayer != comp.selectedLayers[0].threeDLayer)
            {
                container.dimErr = true;
                
                return container;
            }
            
            container.trackers[i] = new Array(); // stores trackers for the i-th layer
            
            for (var j = 1; j <= curLayer.numProperties; j++)
            {
                var curGroup = curLayer.property(j); 
                
                if (curGroup.matchName == "ADBE MTrackers") // trackers group
                {
                    for (var k = 1; k <= curGroup.numProperties; k++)
                    {
                        var curProp = curGroup.property(k);                                                                                        
                        
                        if (curProp.selected && curProp.matchName == "ADBE MTracker") // we got a selected tracker
                        {
                            container.trackers[i].push(curProp); // add tracker to our container
                        }
                    }
                }
            }
        }
		    
        // Retrieve the number of selected trackers
        var numSelTrackers = 0;
        for (var i = 0; i < container.trackers.length; i++)
        {
            numSelTrackers += container.trackers[i].length;
        }                      
        
        // Make sure enough trackers are selected
        
        // Need at least two
        if (avgPosFlag && numSelTrackers < 2) 
        {
            container.selAL2TErr = true;
            return container;
        }
        // Need exactly two
        else if ((posRotFlag || posScaFlag || posRotScaFlag) && numSelTrackers != 2)
        {
            container.selEX2TErr = true;
            return container;
        }
        
        // Make sure trackers have only one track point
        for (var i = 0; i < container.trackers.length; i++)
        {
            for (var j = 0; j < container.trackers[i].length; j++)
            {
                if (container.trackers[i][j].numProperties != 1)
                {
                    if (avgPosFlag)
                    {
                        container.selAL2TErr = true;
                    }
                    else if (posRotFlag || posScaFlag || posRotScaFlag)
                    {
                        container.selEX2TErr = true;
                    }
                    
                    return container;
                }
            }
        }
              
        // Retrieve track points and attach points
        for (var i = 0; i < container.trackers.length; i++)
        {
            container.trackPoints[i] = new Array();    
            container.attachPoints[i] = new Array(); 
            
            for (var j = 0; j < container.trackers[i].length; j++)
            {
                var curTracker = container.trackers[i][j];
                var curTrackPoint = curTracker.property("ADBE MTracker Pt");
                var curAttachPoint = curTracker.property("ADBE MTracker Pt Attach Pt");            
                
                container.trackPoints[i].push(curTrackPoint);
                container.attachPoints[i].push(curAttachPoint);
            }
        }
         
        return container;  
    }
	
	// second version of this function
	// this is used for Corner Pin
    /*-------------------------------------------------------------------------------------*/
    function getTrackersContainer2(comp)
    /*-------------------------------------------------------------------------------------*/
    {   
        // Data container
        var container = new TrackersContainer();
        
        // Make sure the selected trackers belong to the same layer
        // This could be changed in future versions, so we keep the 2D arrays stuff (trackers[][])
        if (comp.selectedLayers.length > 1)
        {
			container.onSameLayerErr = true;
			
			return container;
		}
		
        var curLayer = comp.selectedLayers[0]; 
        container.containingLayers[0] = curLayer; // store layer
                        
        container.trackers[0] = new Array(); // stores trackers for the layer
            
		for (var j = 1; j <= curLayer.numProperties; j++)
		{
			var curGroup = curLayer.property(j); 

			if (curGroup.matchName == "ADBE MTrackers") // trackers group
			{
				for (var k = 1; k <= curGroup.numProperties; k++)
				{
					var curProp = curGroup.property(k);                                                                                        

					if (curProp.selected && curProp.matchName == "ADBE MTracker") // we got a selected tracker
					{
						container.trackers[0].push(curProp); // add tracker to our container
					}
				}
			}
		}
		    
        // Retrieve the number of selected trackers
        var numSelTrackers = 0;
        for (var i = 0; i < container.trackers.length; i++)
        {
            numSelTrackers += container.trackers[0].length;
        }                      
        
        // Make sure enough trackers are selected
        
        // Need exactly four
        if (numSelTrackers != 4) 
        {
            container.selEX4TErr = true;
            return container;
        }        
        
        // Make sure trackers have only one track point
        for (var j = 0; j < container.trackers[0].length; j++)
		{
			if (container.trackers[0][j].numProperties != 1)
			{
				container.selEX4TErr = true;

				return container;
			}
		}
              
        // Retrieve track points and attach points
		container.trackPoints[0] = new Array();    
		container.attachPoints[0] = new Array(); 

		for (var j = 0; j < container.trackers[0].length; j++)
		{
			var curTracker = container.trackers[0][j];
			var curTrackPoint = curTracker.property("ADBE MTracker Pt");
			var curAttachPoint = curTracker.property("ADBE MTracker Pt Attach Pt");            

			container.trackPoints[0].push(curTrackPoint);
			container.attachPoints[0].push(curAttachPoint);
		}
         
        return container;  
    }
    
    /*-------------------------------------------------------------------------------------*/
    function getLayersContainer(comp,
                                avgPosFlag, 
                                posRotFlag, 
                                posScaFlag, 
                                posRotScaFlag)
    /*-------------------------------------------------------------------------------------*/
    {
        // Data container
        var container = new LayersContainer();
        
        for (var i = 0; i < comp.selectedLayers.length; i++)
        {
            var curLayer = comp.selectedLayers[i]; 
            container.layers[i] = curLayer; // store layer
            container.positions[i] = curLayer.position; // store position
             
            // Make sure layers have same dimension
            if (curLayer.threeDLayer != comp.selectedLayers[0].threeDLayer)
            {
                container.dimErr = true;
                
                return container;
            }
        }
        
        // Make sure enough trackers are selected
        if (container.layers.length < 2)
        {
            // Need at least two
            if (avgPosFlag) 
            {
                container.selAL2LErr = true;
            }
            // Need exactly two
            else if (posRotFlag || posScaFlag || posRotScaFlag)
            {
                container.selEX2LErr = true;
            }
            
            return container;
        }
            
        return container;
    }
	
	// second version of this function
	// this is used for Corner Pin
    /*-------------------------------------------------------------------------------------*/
    function getLayersContainer2(comp)
    /*-------------------------------------------------------------------------------------*/
    {
        // Data container
        var container = new LayersContainer();
        
        for (var i = 0; i < comp.selectedLayers.length; i++)
        {
            var curLayer = comp.selectedLayers[i]; 
            container.layers[i] = curLayer; // store layer
            container.positions[i] = curLayer.position; // store position
             
            // Make sure layers have same dimension
            if (curLayer.threeDLayer != comp.selectedLayers[0].threeDLayer)
            {
                container.dimErr = true;
                
                return container;
            }
        }
        
        // Make sure enough trackers are selected
        
        // Need exactly four
        if (container.layers.length != 4)
        {            
            container.selEX4LErr = true;
            
            return container;
        }
            
        return container;
    }

    /*-------------------------------------------------------------------------------------*/
    function getTrackCombineContainer(comp)
    /*-------------------------------------------------------------------------------------*/
    {
        // Data container
        var container = new TrackCombineContainer();
        
        // Make sure there are two selected layers
        if (comp.selectedLayers.length != 1)
        {
            container.selEX1LErr = true;
            
            return container;
        }
        
        var selLayer = comp.selectedLayers[0];
        
        container.pos = selLayer.position;
        
        return container;
    }
        
    /*-------------------------------------------------------------------------------------*/
    function createNewSolid(comp)
    /*-------------------------------------------------------------------------------------*/
    {            
        var layerColor  = G.CYCLE_COLORS_DFLT ? 
                          G.CYCLE_COLOR_PRESETS[(G.COLOR_COUNTER++) % G.CYCLE_COLOR_PRESETS.length] : 
                          G.LAYER_COLOR_DFLT;
        var layerName   = (G.LAYER_NAME_DFLT + " " + (G.LAYER_COUNTER++)).substring(0,31);
        var layerWidth  = G.LAYER_WIDTH_DFLT
        var layerHeight = G.LAYER_HEIGHT_DFLT
        var layerPAR    = comp.pixelAspect;
        var layerDur    = comp.duration;        
        
        return comp.layers.addSolid(layerColor, 
                                    layerName, 
                                    layerWidth,
                                    layerHeight,
                                    layerPAR,
                                    layerDur);
    }

    /*-------------------------------------------------------------------------------------*/
    function getAvgPosExpr( comp, 
                            container, 
                            workWithTrackersFlag, 
                            workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {
        var avgPosExpr = "";
                
        var layers;         // array of layers
        var streams;        // array of position (layers mode) 
                            // or array of array of trackers (trackers mode)                     
        var substreams;     // array of array of track points (trackers mode only)
        
        var numStreams = 0;
        
        // Retrieve data from the container
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers; 
            streams = container.trackers;
            substreams = container.trackPoints;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
            streams = container.positions;
        }
        
        // Set up expression variables
        for (var i = 0; i < layers.length; i++)
        {
            if (workWithTrackersFlag)
            {                    
                avgPosExpr += "L" + (i+1) + " = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[i].name + "\");\r";
                
                // Loop through each tracker of the i-th layer
                for (var j = 0; j < streams[i].length; j++)
                {
                    avgPosExpr += "AtPt" + (numStreams+1) + " = L" + (i+1) + ".motionTracker(\"" 
                                  + streams[i][j].name + "\")" + "(\"" 
                                  + substreams[i][j].name + "\").attachPoint;\r" +
                                  "P" + (numStreams+1) + " = L" + (i+1) + ".toWorld(AtPt" + (numStreams+1) + ");\r";
                    
                    numStreams++;
                }
            }
            else if (workWithLayersFlag)
            {
                avgPosExpr += "L" + (i+1) + " = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[i].name + "\");\r" + 
                              "P" + (i+1) + " = L" + (i+1) + ".toWorld(L" + (i+1) + ".anchorPoint);\r";
                           
                numStreams++;
            }
        }
        // Calculate the sum and divide by numStreams
        avgPosExpr += "(";
        for (var i = 0; i < numStreams; i++)
        {
            if (i < numStreams - 1)
            {
                avgPosExpr += "P" + (i+1) + " + ";
            }
            else
            {
                avgPosExpr += "P" + (i+1) + ") / " + numStreams + ";";                    
            }
        }
        
        return avgPosExpr;
    }

    /*-------------------------------------------------------------------------------------*/
    function getPosExpr(container, 
                        workWithTrackersFlag, 
                        workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {        
        var posExpr = "";
        
        // Position of the first tracker point or the first layer
        if (workWithTrackersFlag)
        {                    
            posExpr += "L = comp(\"" + container.containingLayers[0].containingComp.name + "\").layer(\"" + container.containingLayers[0].name + "\");\r" +
                       "AtPt = L.motionTracker(\"" + container.trackers[0][0].name + "\")" 
                       + "(\"" + container.trackPoints[0][0].name + "\").attachPoint;\r" +
                       "L.toWorld(AtPt);";
        }
        else if (workWithLayersFlag)
        {  
			posExpr += "L = comp(\"" + container.layers[0].containingComp.name + "\").layer(\"" + container.layers[0].name + "\");\r" + 
                       "L.toWorld(L.anchorPoint);";
        }
        
        return posExpr;
    }

    // Second version of this function used for mask shape animation.
    /*-------------------------------------------------------------------------------------*/
    function getPosExpr2(   prop,
                            workWithTrackersFlag, 
                            workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {
        var posExpr = "";
        
        if (workWithTrackersFlag)
        {                    
            // prop = trackPoint
            posExpr += "L = comp(\"" + getLayerFromProp(prop).containingComp.name + "\").layer(\"" + getLayerFromProp(prop).name + "\");\r" +
                       "AtPt = L.motionTracker(\"" + prop.propertyGroup(1).name + "\")" 
                       + "(\"" + prop.name + "\").attachPoint;\r" +
                       "L.toComp(AtPt);";
        }
        else if (workWithLayersFlag)
        {
            // prop = layer.position
            posExpr += "L = comp(\"" + getLayerFromProp(prop).containingComp.name + "\").layer(\"" + getLayerFromProp(prop).name + "\");\r" +
                       "L.toComp(L.anchorPoint);";
        }
        
        return posExpr;
    }
    
    /*-------------------------------------------------------------------------------------*/
    function getRotExpr(container, 
                        workWithTrackersFlag, 
                        workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {        
        var rotExpr = "";
        
        var layers;         // array of layers
        var streams;        // array of position (layers mode) 
                            // or array of array of trackers (trackers mode)                     
        var substreams;     // array of array of track points (trackers mode only)
                
        // Retrieve data from the container
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers; 
            streams = container.trackers;
            substreams = container.trackPoints;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
            streams = container.positions;
        }
        
        // 2D rotation
        if (!layers[0].threeDLayer)
        {
            if (workWithTrackersFlag)
            {   
                if (layers.length > 1) // the two trackers are on different layers
                {                    
                    rotExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                               "L2 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[1].name + "\");\r" +
                               "AtPt1 = L1.motionTracker(\"" 
                               + streams[0][0].name + "\")" + "(\"" 
                               + substreams[0][0].name + "\").attachPoint;\r" +
                               "P1 = L1.toWorld(AtPt1);\r" +
                               "AtPt2 = L2.motionTracker(\""
                               + streams[1][0].name + "\")" + "(\"" 
                               + substreams[1][0].name + "\").attachPoint;\r" +
                               "P2 = L2.toWorld(AtPt2);\r";
                }
                else // only one layer so we reference it once
                {
                    rotExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                               "AtPt1 = L1.motionTracker(\"" 
                               + streams[0][0].name + "\")" + "(\"" 
                               + substreams[0][0].name + "\").attachPoint;\r" +
                               "P1 = L1.toWorld(AtPt1);\r" +
                               "AtPt2 = L1.motionTracker(\""
                               + streams[0][1].name + "\")" + "(\"" 
                               + substreams[0][1].name + "\").attachPoint;\r" +
                               "P2 = L1.toWorld(AtPt2);\r";
                 }
                 
                 rotExpr += "delta = P2 - P1;\r" +
                            "radiansToDegrees(Math.atan2(delta[1],delta[0]));"; 
            }
            else if (workWithLayersFlag)
            {   
                rotExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                           "L2 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[1].name + "\");\r" +                           
                           "P1 = L1.toWorld(L1.anchorPoint);\r" +
                           "P2 = L2.toWorld(L2.anchorPoint);\r" +
                           "delta = P2 - P1;\r" +
                           "radiansToDegrees(Math.atan2(delta[1],delta[0]));";    
            }
        }
        // 3D orientation
        else
        {            
            if (workWithTrackersFlag)
            {
                if (layers.length > 1) // the two trackers are on different layers
                {                    
                    rotExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                               "L2 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[1].name + "\");\r" +
                               "AtPt1 = L1.motionTracker(\"" 
                               + streams[0][0].name + "\")" + "(\"" 
                               + substreams[0][0].name + "\").attachPoint;\r" +
                               "P1 = L1.toWorld(AtPt1);\r" +
                               "AtPt2 = L2.motionTracker(\""
                               + streams[1][0].name + "\")" + "(\"" 
                               + substreams[1][0].name + "\").attachPoint;\r" +
                               "P2 = L2.toWorld(AtPt2);\r";
                }
                else // only one layer so we reference it once
                {
                    rotExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                               "AtPt1 = L1.motionTracker(\"" 
                               + streams[0][0].name + "\")" + "(\"" 
                               + substreams[0][0].name + "\").attachPoint;\r" +
                               "P1 = L1.toWorld(AtPt1);\r" +
                               "AtPt2 = L1.motionTracker(\""
                               + streams[0][1].name + "\")" + "(\"" 
                               + substreams[0][1].name + "\").attachPoint;\r" +
                               "P2 = L1.toWorld(AtPt2);\r";
                 }
            }
            else if (workWithLayersFlag)
            {
                rotExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                           "L2 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[1].name + "\");\r" +
                           "P1 = L1.toWorld(L1.anchorPoint);\r" +                           
                           "P2 = L2.toWorld(L2.anchorPoint);\r";
            }
             
            rotExpr += "lookAt(P1,P2);";
        }
                
        return rotExpr;
    }
    
    /*-------------------------------------------------------------------------------------*/
    function getScaExpr(container,
                        workWithTrackersFlag,
                        workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {   
        var scaExpr = "";
                
        var layers;         // array of layers
        var streams;        // array of position (layers mode) 
                            // or array of array of trackers (trackers mode)                     
        var substreams;     // array of array of track points (trackers mode only)
                
        // Retrieve data from the container
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers; 
            streams = container.trackers;
            substreams = container.trackPoints;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
            streams = container.positions;
        }

        if (workWithTrackersFlag)
        {
            if (layers.length > 1) // the two trackers are on different layers
            {                    
                scaExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                           "L2 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[1].name + "\");\r" +
                           "AtPt1 = L1.motionTracker(\"" 
                           + streams[0][0].name + "\")" + "(\"" 
                           + substreams[0][0].name + "\").attachPoint;\r" +
                           "P1 = L1.toWorld(AtPt1);\r" +
                           "AtPt2 = L2.motionTracker(\""
                           + streams[1][0].name + "\")" + "(\"" 
                           + substreams[1][0].name + "\").attachPoint;\r" +
                           "P2 = L2.toWorld(AtPt2);\r";
            }
            else // only one layer so we reference it once
            {
                scaExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                           "AtPt1 = L1.motionTracker(\"" 
                           + streams[0][0].name + "\")" + "(\"" 
                           + substreams[0][0].name + "\").attachPoint;\r" +
                           "P1 = L1.toWorld(AtPt1);\r" +
                           "AtPt2 = L1.motionTracker(\""
                           + streams[0][1].name + "\")" + "(\"" 
                           + substreams[0][1].name + "\").attachPoint;\r" +
                           "P2 = L1.toWorld(AtPt2);\r";
             }
        }
        else if (workWithLayersFlag)
        {
            scaExpr += "L1 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" +
                       "L2 = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[1].name + "\");\r" +
                       "P1 = L1.toWorld(L1.anchorPoint);\r" +                           
                       "P2 = L2.toWorld(L2.anchorPoint);\r";
        }

        scaExpr += "D = length(P2 - P1);\r" +
                   "[100 * (D / width), 100 * (D / width)";  
         
        // 2D scale
        if (!layers[0].threeDLayer)
        {
            scaExpr += "];";
        }
        // 3D scale
        else
        {
            scaExpr += ", 100 * (D / width)];"; 
        }        
        
        return scaExpr;
    }    

    /*-------------------------------------------------------------------------------------*/
    function getTrackCombinePosExpr(selLayer)
    /*-------------------------------------------------------------------------------------*/
    {
        return "L = comp(\"" + selLayer.containingComp.name + "\").layer(\"" + selLayer.name + "\");\r" +
               "L.toWorld(L.anchorPoint);"; 
    }

    /*-------------------------------------------------------------------------------------*/
    function getCornerPinExpr(	comp, 
    							container, 
    							workWithTrackersFlag, 
    							workWithLayersFlag)
    /*-------------------------------------------------------------------------------------*/
    {
        var cornerPinExpr = new Array();	// array of expressions
        									// one for each corner
                
        var layers;         // array of layers
        var streams;        // array of position (layers mode) 
                            // or array of array of trackers (trackers mode)                     
        var substreams;     // array of array of track points (trackers mode only)
                
        // Retrieve data from the container
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers; 
            streams = container.trackers;
            substreams = container.trackPoints;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
            streams = container.positions;
        }
                
        for (var i = 0; i < 4; i++)
		{	
			if (workWithTrackersFlag)
			{				
				cornerPinExpr[i] =	"L = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[0].name + "\");\r" + 
									"AtPt = L.motionTracker(\"" 
									+ streams[0][i].name + "\")" + "(\"" 
									+ substreams[0][i].name + "\").attachPoint;\r" +
									"L.toComp(AtPt);";				    
			}
			else if (workWithLayersFlag)
			{
				cornerPinExpr[i] = 	"L = comp(\"" + layers[0].containingComp.name + "\").layer(\"" + layers[i].name + "\");\r" + 
									"L.toComp(L.anchorPoint);";				
			}				
		}        
        
        return cornerPinExpr;
    }
    
    /*-------------------------------------------------------------------------------------*/
    function setStreamData(stream, data)
    /*-------------------------------------------------------------------------------------*/
    {
         stream.setValuesAtTimes(data[0], data[1]);   
    }

    /*-------------------------------------------------------------------------------------*/
    function setStreamExpression(stream, expr)
    /*-------------------------------------------------------------------------------------*/
    {
         stream.expression = expr;
    }

    /*-------------------------------------------------------------------------------------*/
    function convertExprToKeys(comp, layer, stream)
    /*-------------------------------------------------------------------------------------*/
    {
        var data        = new Array();
        var timeVals    = new Array();
        var keyVals     = new Array();
        
        // (currently inpoint is always 0, outpoint is always compdur) 
        var start       = Math.max(comp.workAreaStart, layer.inPoint); 
        var end         = Math.min(comp.workAreaStart + comp.workAreaDuration, layer.outPoint);
        
        // Throw a warning message if too many keyframes
        if (end - start > G.BAKING_SAFE_DUR_DFLT)
        {
            var isOk = confirm(G.BAKE_KEYS_WNG.replace(/%s/, Math.round((end-start) / comp.frameDuration)),true); // no_as_default
            if (!isOk) return;
        }        
        
        for (var t = start; t < end; t += comp.frameDuration)
        {
            timeVals.push(t);
            keyVals.push(stream.valueAtTime(t, false));
        }                
        data = [timeVals, keyVals];                                
        
        setStreamData(stream, data);
        
        // At this point we can disable or remove the expression
        // comment out (comment) what you want (don't want)
        
        //stream.expressionEnabled = false;  // disable expression
        stream.expression = "";              // remove expression        
    }

    /*-------------------------------------------------------------------------------------*/
    function removeExtraKeys(prop, start, end)
    /*-------------------------------------------------------------------------------------*/
    {
        while (prop.keyTime(1) < start) 
        {
            prop.removeKey(1);
        }        
        while (prop.keyTime(prop.numKeys) > end) 
        {
            prop.removeKey(prop.numKeys);
        }
    }

    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Average_Position(   comp,
                                            container,
                                            workWithTrackersFlag, 
                                            workWithLayersFlag,
                                            allowExprFlag, 
                                            bakeKeysFlag/*,
                                            progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    {   
		/*
		var numSteps            = 1 + (bakeKeysFlag ? 1 : 0);
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/
        
        // Retrieve data from the container
        var layers;
        
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
        }
    
        // (1)
        var layer           = createNewSolid(comp);                 
        layer.guideLayer    = G.GUIDE_LAYER_DFLT;
        layer.threeDLayer   = layers[0].threeDLayer;
            
        var posExpr = getAvgPosExpr(comp, 
                                    container,
                                    workWithTrackersFlag, 
                                    workWithLayersFlag);    
        
        setStreamExpression(layer.position, posExpr);
        
        //progressBar.value++;
        
        // (2)
        if (bakeKeysFlag)
        {
            convertExprToKeys(comp, layer, layer.position);

            //progressBar.value++;
        }
        
        //progressBar.hide();
    }

    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Position_Rotation(  comp,
                                            container, 
                                            workWithTrackersFlag, 
                                            workWithLayersFlag,
                                            allowExprFlag, 
                                            bakeKeysFlag/*,
                                            progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    { 
		/*
		var numSteps            = 1 + (bakeKeysFlag ? 2 : 0);
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/

        // Retrieve data from the container
        var layers;
        
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
        }

        // (1)
        var layer           = createNewSolid(comp);
        layer.guideLayer    = G.GUIDE_LAYER_DFLT;
        layer.threeDLayer   = layers[0].threeDLayer;
        layer.anchorPoint.setValue([0, layer.height / 2]); // reposition AnchP 
        
        var posExpr = getPosExpr(   container,
                                    workWithTrackersFlag,
                                    workWithLayersFlag);
                                    
        var rotExpr = getRotExpr(   container,
                                    workWithTrackersFlag,
                                    workWithLayersFlag);

        setStreamExpression(layer.position, posExpr);
        
        if (!layer.threeDLayer)                
        {
            setStreamExpression(layer.rotation, rotExpr);
        }
        else             
        {
             setStreamExpression(layer.orientation, rotExpr);                                             
             layer.rotationY.setValue(-90); 
        }
        
        //progressBar.value++;
        
        if (bakeKeysFlag)
        {
            // (2)
            convertExprToKeys(comp, layer, layer.position); 
            
            //progressBar.value++;
 
            if (!layer.threeDLayer)
            {
                // (3)
                convertExprToKeys(comp, layer, layer.rotation);

                //progressBar.value++;
            }
            else
            {
                // (3)
                convertExprToKeys(comp, layer, layer.orientation);
               
                //progressBar.value++;
            }
        }
        
        //progressBar.hide();
    }
    
    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Position_Scale( comp,
                                        container, 
                                        workWithTrackersFlag, 
                                        workWithLayersFlag,
                                        allowExprFlag, 
                                        bakeKeysFlag/*,
                                        progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    { 
		/*
		var numSteps            = 1 + (bakeKeysFlag ? 2 : 0);
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/

        // Retrieve data from the container
        var layers;
        
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
        }
        
        // (1)
        var layer           = createNewSolid(comp);
        layer.guideLayer    = G.GUIDE_LAYER_DFLT;
        layer.threeDLayer   = layers[0].threeDLayer;
        layer.collapseTransformation = true;               // in case scale > 100
        layer.anchorPoint.setValue([0, layer.height / 2]); // reposition AnchP 

        var posExpr = getPosExpr(   container,
                                    workWithTrackersFlag,
                                    workWithLayersFlag);

        var scaExpr = getScaExpr(   container,
                                    workWithTrackersFlag,
                                    workWithLayersFlag);

        setStreamExpression(layer.position, posExpr);
        setStreamExpression(layer.scale, scaExpr);
        
        //progressBar.value++;
        
        if (bakeKeysFlag)
        {
            // (2)
            convertExprToKeys(comp, layer, layer.position);            
            
            //progressBar.value++;           
                
            // (3)
            convertExprToKeys(comp, layer, layer.scale);               
            
            //progressBar.value++;
        }
        
        //progressBar.hide();
    }    

    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Position_Rotation_Scale(comp,
                                                container, 
                                                workWithTrackersFlag, 
                                                workWithLayersFlag,
                                                allowExprFlag, 
                                                bakeKeysFlag/*,
                                                progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    {
		/*
		var numSteps            = 1 + (bakeKeysFlag ? 3 : 0);
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/
        
        // Retrieve data from the container
        var layers;
        
        if (workWithTrackersFlag)
        {
            layers = container.containingLayers;
        }
        else if (workWithLayersFlag)
        {
            layers = container.layers;
        }
        
        // (1)
        var layer           = createNewSolid(comp);
        layer.guideLayer    = G.GUIDE_LAYER_DFLT;
        layer.threeDLayer   = layers[0].threeDLayer;
        layer.collapseTransformation = true;               // in case scale > 100
        layer.anchorPoint.setValue([0, layer.height / 2]); // reposition AnchP 
        
        var posExpr = getPosExpr(   container,
                                    workWithTrackersFlag,
                                    workWithLayersFlag);
        
        var rotExpr = getRotExpr(   container,
                                    workWithTrackersFlag,
                                    workWithLayersFlag);

        var scaExpr = getScaExpr(   container,
                                    workWithTrackersFlag,
                                    workWithLayersFlag);
		
		setStreamExpression(layer.position, posExpr);
        
        if (!layer.threeDLayer)                
        {
            setStreamExpression(layer.rotation, rotExpr);
        }
        else             
        {
             setStreamExpression(layer.orientation, rotExpr);                                             
             layer.rotationY.setValue(-90); 
        }
        
        setStreamExpression(layer.scale, scaExpr);
        
        //progressBar.value++;
        
        if (bakeKeysFlag)
        {
            // (2)
            convertExprToKeys(comp, layer, layer.position);
            
            //progressBar.value++;
            
            if (!layer.threeDLayer)
            {
                // (3)
                convertExprToKeys(comp, layer, layer.rotation);

                //progressBar.value++;
            }
            else
            {
                // (3)
                convertExprToKeys(comp, layer, layer.orientation);
                
                //progressBar.value++;
            }
            
            // (4)
            convertExprToKeys(comp, layer, layer.scale);
            
            //progressBar.value++;
        } 
		
        
        //progressBar.hide();
    }
        
    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Shape_To_Tracker(   comp,
                                            s2lt_container/*,
                                            progressBar*/)    
    /*-------------------------------------------------------------------------------------*/
    {
		/*
		var numSteps            = s2lt_container.vertices.length;
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/

        // If this function has been called there is exactly one mask shape selected
        
        // Retrieve containing layer        
        var layer = getLayerFromProp(comp.selectedProperties[0]);
        
        // Add tracker to the layer 
        var trackersGroup = layer.property("ADBE MTrackers");
        var tracker = trackersGroup.addProperty("ADBE MTracker");
        
        // Add track point at each mask vertex location
        var trackPoint;
        var featureCenter;
        var attachPoint;
        for (var i = 0; i < s2lt_container.vertices.length; i++)
        {
            trackPoint = tracker.addProperty("ADBE MTracker Pt");
            featureCenter = trackPoint.property("ADBE MTracker Pt Feature Center");
            attachPoint = trackPoint.property("ADBE MTracker Pt Attach Pt");
            
            featureCenter.setValue(s2lt_container.vertices[i]);
            attachPoint.setValue(s2lt_container.vertices[i]);
            
            //progressBar.value++;           
        }
        
        //progressBar.hide();        
    }    
    
    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Shape_To_Layers(comp,
                                        s2lt_container/*,
                                        progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    {
        // We are in layers mode, the mask is possibly animated
        
        var start = s2lt_container.start;
        var end = s2lt_container.end;
        
        // Throw a warning message if too many keyframes
        if (end - start > G.BAKING_SAFE_DUR_DFLT)
        {
            var isOk = confirm(G.BAKE_KEYS_WNG.replace(/%s/,s2lt_container.vertices[0].length*Math.round((end-start) / comp.frameDuration)),true);  // no_as_default
            if (!isOk) return;
        }   
        
        /*
        var numSteps            = ((end - start) / comp.frameDuration) * s2lt_container.vertices[0].length;
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/
        
        // Store selected mask because creating new layers will deselect it
        var mask = comp.selectedProperties[0];

        // Create a layer at each vertex of the mask
        var layer;
        var numVerts = s2lt_container.vertices[0].length; // assume constant number of vertices
                
        for (var i = 0; i < numVerts; i++) 
        {
            layer = createNewSolid(comp);            
            
            var k = 0; // frame iterator;
            
            // Animate layer's position based on current vertex position
            for (var t = start; t <= end + G.EPSILON; t += comp.frameDuration)
            {   
                layer.position.setValueAtTime(t, s2lt_container.vertices[k++][i]);

                //progressBar.value++;           
            }            
        }
        
        // Deselect last created layer
        layer.selected = false;
        
        // Now we can reselect the mask
        mask.selected = true;
        
        //progressBar.hide();                
    }
    
    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Create_Shape(   comp,
                                        lt2s_container,
                                        workWithTrackersFlag, 
                                        workWithLayersFlag/*,
                                        progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    {        
        var earliest    = lt2s_container.earliest;
        var latest      = lt2s_container.latest;
        var incr        = lt2s_container.incr;        
        
        /*
		var numSteps            = (latest - earliest) / incr;
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/
		
        // Send a warning if too many keyframes
        if (latest - earliest > G.BAKING_SAFE_DUR_DFLT)
        {
            var isOk = confirm(G.BAKE_KEYS_WNG.replace(/%s/,Math.round(numSteps)),true); // no_as_default
            if (!isOk) return;
        }
       
        // Retrieve number of properties from container
        var numStreams;        
        if (workWithTrackersFlag)
        {
            numStreams = lt2s_container.trackPoints.length;
        }
        else if (workWithLayersFlag)
        {
            numStreams = lt2s_container.layers.length;
        }
            
        // Get position expressions
        var posExprs = new Array();
        for (var i = 0; i < numStreams; i++)
        {
            if (workWithTrackersFlag)
            {
                posExprs[i] = getPosExpr2(lt2s_container.trackPoints[i], workWithTrackersFlag, workWithLayersFlag);
            }
            else if (workWithLayersFlag)
            {
                posExprs[i] = getPosExpr2(lt2s_container.layers[i].position, workWithTrackersFlag, workWithLayersFlag);
            }
        }
        
        // Create new solid
        var layerColor;
        var layerName;
        if (workWithTrackersFlag)
        {
            layerColor = G.ROTOSHAPE_COLOR_DFLT;
            layerName = G.ROTOSHAPE_NAME_DFLT;
        }
        else if (workWithLayersFlag)
        {
            layerColor = G.LINKINGSHAPE_COLOR_DFLT;
            layerName = G.LINKINGSHAPE_NAME_DFLT;
        }
        var layer = comp.layers.addSolid(   layerColor,        
                                            layerName,
                                            comp.width,
                                            comp.height,
                                            comp.pixelAspect,
                                            comp.duration);
        // Add temporary point controls
        var ptCtrl;
        var pt;
        for (var i = 0; i < numStreams; i++)
        {
            ptCtrl = layer.Effects.addProperty("ADBE Point Control");
            ptCtrl.name = "Temp Point Control " + (i+1);
            
            pt = ptCtrl.property(1);
            pt.expression = posExprs[i];
        } 
        
        // Create mask
        var mask = layer.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        
        // These will store shape keyframes
        var keyTimes = new Array();
        var keyValues = new Array();        
 
        // Shape animation          
        for (var i = earliest; i <= latest + G.EPSILON; i+=incr)
        {   
            var shape = new Shape();
            var vertices = new Array();
            for (var j = 0; j < numStreams; j++)
            {
                vertices[j] = layer.Effects.property("Temp Point Control " + (j+1)).property(1).valueAtTime(i, false);
            }    
            
            shape.vertices = vertices;    
            shape.closed = G.LT2S_CLOSED_DFLT;
            
            // To make rotoBezier active we must create fake tangents
            // (something close to zero but NOT zero)
            if (G.LT2S_ROTOB_DFLT)
            {
                var inTangents = new Array();
            
                for (var j = 0; j < shape.vertices.length; j++)
                {
                    inTangents.push([G.EPSILON,G.EPSILON]); // inTangents are enough
                }
                
                shape.inTangents = inTangents;
            }
            else if (G.LT2S_ORIGINAL_DFLT && G.SHAPE_VAL)
            {            
                shape.inTangents = G.SHAPE_VAL.inTangents;
                shape.outTangents = G.SHAPE_VAL.outTangents;
            }
                        
            keyTimes.push(i);
            keyValues.push(shape);
            
            //progressBar.value++; 
        }    

        // Set keyframes        
        setStreamData(mask.maskShape, [keyTimes,keyValues])
        
        // Set rotoBezier mode AFTER setting shape value
        if (G.LT2S_ROTOB_DFLT)
        {
            mask.rotoBezier = true;  
        }
       
        // Remove point controls
        for (var i = 0; i < numStreams; i++)
        {
            layer.Effects.property("Temp Point Control " + (i+1)).remove();
        }
                
        //progressBar.hide();
    }
    
    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Track_Combine(  comp,
                                        tc_container,
                                        allowExprFlag, 
                                        bakeKeysFlag/*,
                                        progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    {
        var selLayer = getLayerFromProp(tc_container.pos);        
        var pos = tc_container.pos;
        
        /*
		var numSteps            = 1 + (bakeKeysFlag ? 1 : 0);
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/
        
        // Create new layer        
        var layer           = createNewSolid(comp);                 
        layer.guideLayer    = G.GUIDE_LAYER_DFLT;
        layer.threeDLayer   = selLayer.threeDLayer;
        layer.name          = (G.CORRECTED_TRACKER_NAME + selLayer.name).substring(0,31);
                        
        // Add position expression
        var posExpr = getTrackCombinePosExpr(selLayer);
        setStreamExpression(layer.position, posExpr);
        
        // Bake keys if necessary     
        if (bakeKeysFlag)
        {
            // Convert expression to keyframes
            convertExprToKeys(comp, layer, layer.position);
            
            //progressBar.value++; 
        }
        
        //progressBar.hide();                                
    }
    
    /*-------------------------------------------------------------------------------------*/
    function trackerViz_Corner_Pin(	comp, 
            						container, 
            						workWithTrackersFlag,
            						workWithLayersFlag,
            						allowExprFlag, 
            						bakeKeysFlag,
            						cPinFlag,
            						pPinFlag/*,
            						progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    {
		/*
		var numSteps            = 1 + (bakeKeysFlag ? 4 : 0);
		progressBar.value       = 0;
		progressBar.maxvalue    = numSteps;
		progressBar.show();
		*/
        
        // (1)
        var layer = comp.layers.addSolid(	G.CORNER_PINNED_COLOR_DFLT,        
                                            G.CORNER_PINNED_NAME_DFLT,
                                            comp.width,
                                            comp.height,
                                            comp.pixelAspect,
                                            comp.duration);
            
        var cornerPinExpr 	= getCornerPinExpr(	comp, 
        										container,
        										workWithTrackersFlag, 
        										workWithLayersFlag);    
        
        var cornerPinEffect;
        
        if (cPinFlag)
        {
			cornerPinEffect	= layer.Effects.addProperty("ADBE Corner Pin");
			
        	for (var i = 1; i <= 4; i++)
        	{
				setStreamExpression(cornerPinEffect.property(i), cornerPinExpr[i-1]);
			}
		}
		else if (pPinFlag)
		{				
			cornerPinEffect	= layer.Effects.addProperty("CC Power Pin");
			
			for (var i = 2; i <= 5; i++)
			{			
				setStreamExpression(cornerPinEffect.property(i), cornerPinExpr[i-2]);
			}
		}
        
        //progressBar.value++;
        
        // (2)
        if (bakeKeysFlag)
        {
			if (cPinFlag)
        	{
				for (var i = 1; i <= 4; i++)
				{
					convertExprToKeys(comp, layer, cornerPinEffect.property(i));
					
					//progressBar.value++;
				}
			}
			else if (pPinFlag)
			{										
				for (var i = 2; i <= 5; i++)
				{
					convertExprToKeys(comp, layer, cornerPinEffect.property(i));				
					
					//progressBar.value++;
				}
			}
        }
        
        // precompose 
        if (G.PRECOMPOSE_PINNED_DFLT)
        {
			comp.layers.precompose([1],(layer.name + G.PRECOMP_NAME_DFLT).substring(0,31),false); // false := "Leave all attributes in"			
		}
        
        //progressBar.hide();		
	}
	
    /*-------------------------------------------------------------------------------------*/
    function Main(  workWithTrackersFlag, 
                    workWithLayersFlag, 
                    avgPosFlag, 
                    posRotFlag,
                    posScaFlag,
                    posRotScaFlag,
                    tCombiFlag,
                    cPinFlag,
                    pPinFlag,
                    s2ltFlag,
                    lt2sFlag,                    
                    allowExprFlag, 
                    bakeKeysFlag/*,
                    progressBar*/)
    /*-------------------------------------------------------------------------------------*/
    {  
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem))
        {
            throwErr(G.NO_COMP_ERR);
            return;
        }
        
        if (!lt2sFlag)
        {
        	// Make sure layers and trackers have unique names
        	var nameWng = new NameWng();
        	nameWng = searchIdenticalNames(comp, workWithTrackersFlag, workWithLayersFlag);
        	
        	if (nameWng.layersNameWng)
        	{
        	    if (confirm(G.ALLOW_RENAME_LAYERS_MSG))
        	    {
					autoRenameLayers(comp);
				}
				else
				{
					return;
				}
        	}   
        	else if (nameWng.trackersNameWng)
        	{
        	    if (confirm(G.ALLOW_RENAME_TRACKERS_MSG))
        	    {
					autoRenameTrackers(comp);
				}
				else
				{
					return;
				}				
			}
		}
         
        app.beginUndoGroup(G.SCRIPT_NAME);
        
        // 'SHAPE' FUNCTIONS
                
        if (s2ltFlag || lt2sFlag)
        {
            var s2lt_container; // stores useful stuff
            var lt2s_container; // ""
            
            // shape to layers/tracker
            if (s2ltFlag)
            {
                s2lt_container = new S2LTContainer();
                s2lt_container = getS2LTContainer(  comp,
                                                    workWithTrackersFlag,
                                                    workWithLayersFlag);                                
                // Make sure selection is ok
                if (s2lt_container.selEX1SErr)
                {
                    throwErr(G.SEL_EX1S_ERR);
                    return;
                }
                if (s2lt_container.selAnimSErr)
                {
                    throwErr(G.SEL_ANIMS_ERR);
                    return;
                }
                if (workWithTrackersFlag && s2lt_container.selBadTypeErr)
                {
                    throwErr(G.SEL_BAD_TYPE_ERR);
                    return;
                }
                if (workWithLayersFlag && s2lt_container.selBadSizeErr)
                {
                    throwErr(G.SEL_BAD_SIZE_ERR);
                    return;
                }
                if (workWithLayersFlag && s2lt_container.selBadTransErr)
                {
                    throwErr(G.SEL_BAD_TRANS_ERR);
                    return;
                }
                
                // Perform operations
                if (workWithTrackersFlag)
                {
                    trackerViz_Shape_To_Tracker(comp,
                                                s2lt_container/*,
                                                progressBar*/);
                }
                else if (workWithLayersFlag)
                {
                    trackerViz_Shape_To_Layers( comp,
                                                s2lt_container/*,
                                                progressBar*/);
                }
                
                return;
            }
            // layers/tracker to shape
            else if (lt2sFlag)
            {
                lt2s_container = new LT2SContainer();
                lt2s_container = getLT2SContainer(  comp,
                                                    workWithTrackersFlag, 
                                                    workWithLayersFlag);                                                                    
				// Make sure selection is ok
                if (workWithTrackersFlag) 
                {
                    if (lt2s_container.selEX1TErr)
                    {
                        throwErr(G.SEL_EX1T_ERR);
                        return;
                    }
                    else if (lt2s_container.selNoAnimTWng)
                    {
                        throwWng(G.SEL_NO_ANIMT_WNG);
                        return;
                    }
                }
                else if (workWithLayersFlag)
                {
                    if (lt2s_container.selAL2LErr)
                    {
                        throwErr(G.SEL_AL2L_ERR);
                        return;
                    }
                    else if (lt2s_container.selNoAnimLWng)
                    {
                        throwWng(G.SEL_NO_ANIML_WNG);
                        return;
                    }
                }
                
                // Perform operation
                trackerViz_Create_Shape(comp,
                                        lt2s_container,
                                        workWithTrackersFlag, 
                                        workWithLayersFlag/*,
                                        progressBar*/);
                                        
                return;
            }
        }
        
        // MAIN FUNCTIONS
        
        // corner pin
        if (cPinFlag || pPinFlag)
        {
			var container;  // stores useful stuff
			
			// Retrieve data
			if (workWithTrackersFlag)
			{            
				container = new TrackersContainer2();
				container = getTrackersContainer2(comp); 
			}
			else
			{
				container = new LayersContainer2();
				container = getLayersContainer2(comp);         
			}
			
			// Make sure selected trackers belong to the same layer
			if (container.onSameLayerErr)
			{
				throwErr(G.ON_SAME_LAYER_ERR);
				return;
			} 

			// Make sure selection is ok
			if (workWithTrackersFlag && container.selEX4TErr)
			{
				throwErr(G.SEL_EX4T_ERR);
				return;
			}
			else if (workWithLayersFlag && container.selEX4LErr)
			{
				throwErr(G.SEL_EX4L_ERR);
				return;
			}
			
			// Perform operation
            trackerViz_Corner_Pin(	comp, 
            						container, 
            						workWithTrackersFlag,
            						workWithLayersFlag,
            						allowExprFlag, 
            						bakeKeysFlag,
            						cPinFlag,
            						pPinFlag/*,
            						progressBar*/);
            return;
		}
		
        // track combine
        if (tCombiFlag)
        {
            // Make sure WorkWithLayers is selected
            if (workWithTrackersFlag)
            {
                throwErr(G.SEL_WWL_MODE_ERR);
                return;
            }
            
            var tc_container = new TrackCombineContainer();
            tc_container = getTrackCombineContainer(comp);
            
            // Make sure there is only layer selected
            if (tc_container.selEX1LErr)
            {
                throwErr(G.SEL_EX1L_ERR);
                return;
            }
            
            // Perform operation
            trackerViz_Track_Combine(   comp,
                                        tc_container,
                                        allowExprFlag, 
                                        bakeKeysFlag/*,
                                        progressBar*/);            
            
            return;
        }
        
        // pos / pos_rot / pos_sca / pos_rot_sca
        
        var container;  // stores useful stuff
        
        // Retrieve data
        if (workWithTrackersFlag)
        {            
            container = new TrackersContainer();
            container = getTrackersContainer(   comp, 
                                                avgPosFlag, 
                                                posRotFlag, 
                                                posScaFlag, 
                                                posRotScaFlag); 
        }
        else
        {
            container = new LayersContainer();
            container = getLayersContainer( comp, 
                                            avgPosFlag,
                                            posRotFlag, 
                                            posScaFlag, 
                                            posRotScaFlag);         
        }
                
        // Make sure 2D and 3D data are not both selected
        if (container.dimErr)
        {
            throwErr(G.DIM_ERR);
            return;
        } 
        
        // Make sure selection is ok
        if (avgPosFlag)
        {
            if (workWithTrackersFlag && container.selAL2TErr)
            {
				throwErr(G.SEL_AL2T_ERR);
				return;
            }
            else if (workWithLayersFlag && container.selAL2LErr)
            {
				throwErr(G.SEL_AL2L_ERR);
				return;
            }
        }
        else if (posRotFlag || posScaFlag || posRotScaFlag)
        {
            if (workWithTrackersFlag && container.selEX2TErr)
            {
                throwErr(G.SEL_EX2T_ERR);
                return;
            }
            else if (workWithLayersFlag && container.selEX2LErr)
            {
                throwErr(G.SEL_EX2L_ERR);
                return;
            }
        }

        // At this point we should have everything we need
        // to perform operations
        
        if (avgPosFlag)
        {
            trackerViz_Average_Position(comp, 
                                        container, 
                                        workWithTrackersFlag,
                                        workWithLayersFlag,
                                        allowExprFlag, 
                                        bakeKeysFlag/*,
                                        progressBar*/);
        }
        else if (posRotFlag)
        {
            trackerViz_Position_Rotation(comp, 
                                        container, 
                                        workWithTrackersFlag,
                                        workWithLayersFlag,
                                        allowExprFlag, 
                                        bakeKeysFlag/*,
                                        progressBar*/);
        }
        else if (posScaFlag)
        {
            trackerViz_Position_Scale(  comp, 
                                        container, 
                                        workWithTrackersFlag,
                                        workWithLayersFlag,
                                        allowExprFlag, 
                                        bakeKeysFlag/*,
                                        progressBar*/);
        }        
        else if (posRotScaFlag)
        {
            trackerViz_Position_Rotation_Scale( comp, 
                                                container, 
                                                workWithTrackersFlag,
                                                workWithLayersFlag,
                                                allowExprFlag, 
                                                bakeKeysFlag/*,
                                                progressBar*/);
        }
        
        // reset these variables for future use
        G.SHAPE_VAL  = null;
        //G.SHAPE_VALS = new Array();
        
        app.endUndoGroup();
    }

    /*-------------------------------------------------------------------------------------*/
    // Entry point
    /*-------------------------------------------------------------------------------------*/
    var G = new Object(); // stores all global variables
    initGlobals(G);
    
    if (G.APP_VERSION < G.MIN_VERSION)
    {
        throwErr(G.BAD_VERSION_ERR);     
    }
    else if (!G.FOUND_ICON)
    {
		throwErr(G.NO_ICON_ERR);
	}
	else
	{		
		var WND = initUI(this);

		if (WND instanceof Window)
		{
			// Show the palette
			WND.center();
			WND.show();
		}
		else
		{
			WND.layout.layout(true);
		}
    }
    
}
