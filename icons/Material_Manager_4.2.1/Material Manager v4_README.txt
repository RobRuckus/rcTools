---------------------------------------------------
--------- Material Manager v4.x for Maya ----------
---------------------------------------------------
Authored and maintained by Dennis "Bartalon" Porter
Forward your feedback to Dennis.Porter.3D@gmail.com
---------------------------------------------------

The Material Manager is designed to facilitate quick interaction with all materials in a scene.
This script will give you automated control over assigning and removing texture maps to the
most common material channels, as well as various cleanup and maintenance features to keep your
time spent working with your scene instead of wasted in the Hypershade, Channel Box, or Marking
Menus!

This tool works with Maya 2013, 2014, 2015, 2016, LT editions, and should continue to work in all 
future versions of Maya.  May not work with older versions.

An overview of the plugin can be watched here:
	Material Manager - https://www.youtube.com/watch?v=epuTr47Y8LA
	Smart Exporter   - https://www.youtube.com/watch?v=6Bj6JNrUA9Y

Updates can be found here at either of these sites, if available:
	http://www.creativecrash.com/maya/script/material-manager
	https://gumroad.com/products/QSvJh
	http://dennisporter3d.com/mel.htm#ddo

---------------------------------------------------
-----------  Installation Instructions  -----------
---------------------------------------------------

1) Fully exit Maya.

2) Delete any old versions of the Material Manager plugin (file name could have changed slightly
	from older versions).

3) Paste the following files into "C:\Users\[account name]\Documents\maya\2013-x64\prefs\scripts" or equivalent directory:

	dp_MaterialManager.mel
	dp_SmartExport.mel

	NOTE:  DO NOT extract the files to the C:\Users\[account name]\Documents\maya\scripts folder, otherwise the
		   script may not work properly.  You can confirm it is the correct scripts directory by making sure the 
		   version of Maya you use is part of the file path.


4) Paste the "MaterialManager" folder inside "C:\Users\Owner\Documents\maya\2013-x64\prefs\icons" directory.

5) Open Maya.

6) In Maya's MEL command line (or in the Script Editor), type in the following, then press CTRL + Enter:

source dp_MaterialManager.mel; materialManager;


---------------------------------------------------
--------------  Version Information  --------------
---------------------------------------------------


-----------------------------------------
--  October 11 2016  --  Version 4.2.0 --

1)  New Tool:  Colorize Materials - This tool will colorize all materials assigned to a model for quick visualization.  Read button annotation for more information
2)  Fixed an oversight where the "Multiple Materials Detected" window functionality was incomplete
3)  Auto Color ID Tool:  Fixed an issue that was causing the tool to fail in Maya LT
4)  ID Map Baker:  Loading objects with children into the High Poly slot will now automatically select children to ensure a proper bake
5)  Quick Materials:  While holding CTRL to skip the naming prompt, the new material will now automatically assign to your selection
6)  Fixed an issue where using the Marking tools on individual, unmarked materials would sometimes not work
7)  Nameplates now correctly highlight after changing their size
8)  Renaming multiple materials at once will now prompt you in the order they appear in the Current Scene list
9)  Various impretinent warnings have been suppressed
10) Smart Exporter:  Fixed an issue when checking a custom naming convention against materials only would not actually check the names



--------------------------------------------
--  September 10 2016  --  Version 4.1.1  --

1)  Fixed an oversight where the ID Map Baker would not work if loading more than one mesh into the Low Poly slot.  The bake currently will only work with 
	one model assigned to the Low Poly slot.  The High Poly slot can still have as many pieces as needed
2)  Added a prompt to warn the user if the user attempts to load more than one mesh into the Low Poly slot
3)  Added a prompt for if the user attempts to load both the High Poly and Low Poly slots with the same mesh
4)  Changed the color of the Auto-assign Color IDs button to make it more obvious that it's a button
5)  Removed the specular reflection from the Quick Checker material



-----------------------------------------
--  August 12 2016  --  Version 4.1.0  --

1)  New Feature! Holding CTRL while clicking a material nameplate will now automatically match assigned polygons/meshes.  Use the marking boxes and the
	Match button as usual to match multiple materials at once
2)  Fixed a crash that would occur when attempting to bake a material ID map while the low poly mesh had more than 1 material assigned to it
3)	Fixed a bug where an error would occur when using Channel Control commands on a mesh with multiple materials assigned and with a docked MM window
4)  Fixed a bug that was preventing the second column of the Presets tab to display properly when using a search filter
5)	Fixed a bug that was causing "Sort Assigned Materials First" to display in reverse order when combined with alphabetical sorting
6)  The space bar will now choose "Proceed" instead of "Abort" if the Auto-assign color ID tool prompts the user about there being more than 15 elements



----------------------------------------
--  August 4 2016  --  Version 4.0.3  --

1)  Maya 2017 LT:  Fixed a bug that caused intermittent crashes when using the Dock menu
2)  Added a link to the Polycount thread under the Help menu
3)  Updated the Gumroad icon in the Help menu


---------------------------------------
--  July 19 2016  --  Version 4.0.2  --

1)  Smart Exporter:  Fixed a bug where the Smart Exporter would not recognize when UVs were selected
2)  Smart Exporter:  Added "blinn" to the list of export flags to check for


---------------------------------------
--  July 18 2016  --  Version 4.0.1  --


1) 	Added a missing icon for Gumroad
2)  Updated installation instructions


---------------------------------------
--  July 17 2016  --  Version 4.0.0  --


General

1)  UI has been revamped to look sleeker and improved top-to-bottom flow of use.
	*  The banner area may now be hidden for optimal window space.
	*  Indicators have been removed and now material name plates highlight instead.
	*  Indicators now work on a per-component basis; you can now see exactly which material is assigned to individual faces.
	*  You are now also able to limit material matching to your active selection only
	*  An interactively-updating Tangent Coordinate System is now visible as a toggleable icon which allows you to switch a model's handedness.
2)  New Features:
	*  Counters have been added to the frames to keep track of materials in scene and on selection.
	*  Nameplates can now be resized to some degree.
	*  The "Smart Exporter" tool has been implemented to provide for quick name and material checks (with some neat features) for outgoing models.
	*  Assigned materials can now be sorted to the top of the material list.  This setting stacks with alphabetical or chronological sorting.
	*  Added a toggle option which allows material assignments to affect instance objects.  Default setting is on.
	*  Added a button to auto-harden UV seams, useful if planning to bake a normal map.
	*  Added a "relate" tool under the Cleanup menu which will scrub any scene and give all utility, shadingEngine, file, and texture nodes correct names 
	   using the material name as a base
	*  Added a Bonus Setting to reveal/hide particleCloud objects since they are technically materials.
	*  Added a tool to quickly remove namespaces that sometimes come with imported OBJ files.  This works with all object types including models/materials.
	*  Window docking is now fully functional!
3)  Color ID Map baker has been revamped and given its own tab.
	*  New feature available to assign color IDs automatically (up to 15 unique colors).
	*  Multiple objects are now supported when loading high, low, and cage meshes into the baker.
4)  Presets tab has been improved.
	*  Search filtering now works on presets.
	*  Custom colors have been improved to fit a more optimal color selection for color ID maps

Bug Fixes

1)  Material Manager 4 will no longer prevent you from using it if using it in a version it was not written for.  Additionally,
	compatibility has been maxmimzed so the script should continue working in versions of Maya that haven't come out yet (but still no guarantees).
2)	Fixed a bug where some commands would execute more than once at a time.
3)  Alphabetical sorting now ignores capitalization and will order properly.
4)  All warnings and errors that are impertinent to the user have been concealed.

Other Notes

1)	Maya 2012 and older is no longer supported and the script is not expected to work in those versions.







-----------------------------------------
--  January 25 2015 --  Version 3.2.0  --


1)  Added a section under the Presets tab to automatically bake out a color ID map!
2)  Added a help menu for baking color ID maps.
3)  Fixed a bug where deleting a material channel that was not occupied would not result in a "does not exist" warning.


---------------------
--  August 19 2014 --


1)  Fixed an error which was preventing the plugin from working for Maya 2011 (2012 version now v3.0.4)


--------------------------------------
--  July 21 2014 --  Version 3.1.0  --


1)  Updated the main banner and Channel Control icons with a fresh new look!
2)  Fixed a typo in the Version Information that stated this version was meant for 2012 and older instead of 2013 and newer
3)  A marker will now automatically be placed at your selection if less than two markers exist in the Material List
4)  Fixed a bug that would produce errors when lambert1 was part of a marked list
5)  Markers will now remain after renaming materials
6)  Markers will now clear properly when Maya opens a new scene
7)  Fixed a bug where assigning a Preset to nothing, or another material, would produce an error
8)  Assigning a normal map to a material no longer produces an "already connected" warning


---------------------------------------
--  April 30 2014 --  Version 3.0.0  --


1)  Completely overhauled the code!  Hopefully it's easier to read now
2)  Enhanced compatability between versions
3)  Revamped how selection/rename/delete works.  Read more on this under the window's Help menu
4)  It is now quicker and easier to select and modify multiple materials.  Hold SHIFT to toggle material selections, hold CTRL to clear markers
5)  Updated help menus to reflect changes
6)  Holding ALT while clicking a material in the list will now show that material in the Attribute Editor without losing your current selection
7)  Material search bar added!
8)  Alphabetical sorting will now properly order lower- and upper-case materials
9)  Indicator added in Sorting menu to display the active sorting mode
10) Colorized the frame layouts for aesthetics and easier visual separation of sections
11) Removed quick material "Checker".  In Maya 2015, a checker shader comes built into the UV editor window
12) Relocated New Custom Material to the Quick Materials frame
13) Relocated hypershade/graph network buttons to the Quick Materials frame
14) Main listing now updates after assigning a new material from the Assign New Material window
15) Updated Contact/Update frame contents
16) Removed many superfluous warnings when deleting materials.  Some may still occur but should not affect functionality
17) Indicators should now properly display even when more complex materials are assigned to an object (such as car paint, misss, etc.)
18) Material list and indicators should now update after importing and opening a new scene.


-----------------------------------------
--  February 3 2014 --  Version 2.7.4  --


1)  Fixed the misleading destination path in step 3 of the Installation Instructions.
2)	Clicking on a material name now updates textures!
3)  Added a Sort Z-A sorting method.
4)  Fixed an issue where deleting a selected material (regular and multi mode) would prevent the Material List from updating.
5)	Fixed an issue where assigning Quick Materials didn't work on more than one object.
6)  Fixed an issue where deleting a material resulted in the loss of the current selection.


----------------------------------------
--  January 6 2014 --  Version 2.7.3  --


1)  Assigning a hotkey for "dDo Manager" using the menu option will now function as an open/close toggle.  Press once to open; press
	again to close.
2)  Add Materials tab now properly updates when deleting a preset from Material List and immediately switching to Add Materials.
3)  Material List tab should no longer break if there are identically named shape objects (under separate hierarchies).
4)  If attempting to use the Assign/Delete Material Channels to assign a channel which is already occupied, the material will be
	displayed along with a warning instead of just warning about a full channel, if possible.
5)  Increased the minimum window height slightly.


-----------------------------------------
--  December 4 2013 --  Version 2.7.1  --


1)	Deleting materials from the Material List tab and creating materials from the Add Materials tab no longer causes the scroll position
	to reset
2)	Selecting mesh components (vertex, edge, face) will now update Material List indicators for the parent shape.
3)  Creating and assigning material presets is now faster and more similar to applying existing materials from the Material List tab.
4)  The Detach Alpha button (adjacent to the Delete Transparency Channel button) should now work when a single material is in question.
5)  Assigning a material now updates the Material List indicators.
6)  Warning messages for nonexistent or already-empty channels have been disabled.  Warnings for occupied channels still enabled.
7)  The update button which redirects to my Website now takes you to the appropriate page.
8)  Changed some initialization code around; if you happened to bind a hotkey using Tools > Assign Hotkey: dDo Manager, please re-bind
	your hotkey to avoid any issues related to the changes.
9)  Using the Cleanup tools will now also update the preset list if you have that tab selected.


------------------------------------------
--  October 27 2013  --  Version 2.6.1  --


1)  The window can now scale vertically to whatever side you would like
2) 	Fixed an issue where reloading the screen caused your selection to clear
3)	Cleaned up the code a bit (but it's still probably messy)
4)  Added a help menu option explaining the Add Materials tab
5)  Redesigned how the Add Materials presets list
6)  The Del All button under Assign/Delete Material Channels button no longer deletes the material from the scene
7)  Adding or deleting a diffuse map to a material will automatically refresh the material listing


------------------------------------------
--  October 21 2013  --  Version 2.5.2  --


After much testing, some elements were decided to be inefficiently positioned or superfluous.

1)  Layout reduced to two tabs.
2)	Selecting an object now automatically detects and updates material indicators without having to redraw the window.
3) 	Several selection errors have been fixed.
4)  Global values for color, spec, cosine power, etc. no longer attempt to reinitialize.
5)  Quick Materials and Assign/Delete Material Channels tools have been moved to the bottom of the first tab.
6)  Added a button next to the Delete Transparency button which disconnects alpha channels from a material's diffuse channel
	which may have inadvertently or undesirably loaded as a transparency channel.
7)  The Select and Delete buttons for Multi Select Mode have been relocated to the lambert1 line in order to free up UI real estate
8)  Ramp Shaders, Fluid Shapes, and Env Fog now successfully loads into the material listing, however some features may not be available
	for these material types, such as the Assign/Delete Material Channels tools.
9)  Colorized indicator arrows for easier visibility.
10) Moved Create Shelf Button button to the Tool menu.
11) Added Import and Export buttons.


------------------------
--  September 9 2013  --


Version 2 is here!  With a newly renovated and streamlined UI, the Material Manager now
offers quicker access to material creation and modification.  An all-new material presets
tab offers all the dDo materials without having to load every material into your
scene.  Create and apply only what you need as you go!

Thanks to Polycount.com users passerby and Froyok for coding assistance.