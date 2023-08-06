#
# Change Log of pypos3d library
# 
# **SVN** : Refer to SVN database for details
#
1.1 (2021-06-19)
------------------
This version includes some functional enhancement needed by new validation tests.


PyPos3DLO (v0.7):
- CreateMechanical:
  * Capacity to import a material and rename it in the destination figure. Usefull when using
    your 3D modeller you have renamed some material
  * New channel type: "shaderNodeParm" is a new type of channel to drive Material behavior

pypos3dv (v0.6):
- FIX/Enhancement : Now support Geometries with non homogeneous texture/normal presence

pypos3d.wftk:
- class GeomGroup : 
  * New internal design
  * **New** class FaceAttr to store Face (and line) attributs

- class WaveGeom:
  Previously WaveGeom was not able to manage geometries with non homogeneous presence of
  texture (or normal) at face level.

  * Internal texture / normal management upgrade.  
  * Change in write method to use the more modern f-strings

pypos3d.pftk:
- Change in write methods to use the more modern f-strings
- Few bug fixes


1.0.2 (2021-05-20)
------------------
First finalized version: Provide the means to easily create mechanical Poser Characters.


PyPos3DLO (v0.6):
- **New** 'CreateMechanical' command to create character from a 'simple' description sheet.
- **New** 'InitMecha' command to initialize mechanical character description sheet.
- **New** 'UnTriangularize' command to simplify groups of a geometry by merging adjacent triangles
- **New** 'Check Dir' button: in sheet 'Glob', this action checks if directories exist and mark in red bad ones
- **New** 'Select Dir' button: in sheet 'Glob', this action provides the means to select a directory with the standard dialog.
- **New** 'Import/Migrate' button: in sheet 'Glob', this action provides the means to migrate the data of an existing document to the current one.
- **New** 'Show Algorithm Param' checkbox: in sheet Main, this option activates a helper in the action table. When you enter/select an operation, PyPos3DLO prints in the required cells a short parameter description.
- Some bug fixes

pypos3dv (v0.5):
- FIX/Enhancement : Now support legacy computers with only GLES 1.20 (Intel GM45 for example)

pypos3d.wftk:
- class GeomGroup : 
  * **New** method 'UnTriangularize': simplify a geometry group by merging adjacent triangles
  * Method fusion() : fixed to manage normals

- class WFMat : Extension to manage ka and ks colors

- class WaveGeom:
  * Method OptimizeGroups: Refactoring for performance. Optimized from O(n2) to O(n.log(n))
  * Method CleanDupVert: Refactoring for performance. Optimized from O(n2) to O(n.log(n))
  * Method extractSortJonction: Refactoring for performance. Optimized from O(n2) to O(n.log(n))
  * **New** method 'UnTriangularize': simplify all groups of the geometry by merging adjacent triangles

pypos3d.pftk:
- class Figure:
  * **New** Method createMechanical: create a new figure with articulated parts (without bad effects
    of Poser imports)
  * Method importChannels: Refactoring to be more generic and to support 'createMechanic' method

- class PoserFile:
  * **New** Method createFigure: create an empty new figure in the current PoserFile.

- class PoserMaterial: Enhanced to match more accuratetly Poser's syntax and to support createMechanical method.

- Few bug fixes

- Port/Validations: Validated on Python 3.9.5 / scipy 1.6 on Linux

0.5 (2021-03-20)
----------------
Enhancement of v0.4.0 (thanks to PyPos3DLO returns):

PyPos3DLO:
- delete functions supports channel deletion
- ReportAltMorph can take into account deltas in adjacent others actors.
  Useful when the alternate geometry has been created with parts fusions.
- ImportChannel: New option to hide created dials when they are calculated
- addMaster : New function - Provides the means to create a valueParm at root
  level (BODY) for any actor's dial
- createMorph : New function - Provides the means to create a morph by importing
  a Wavefront file (like Poser). Morph can apply to the default geometry of
  the actor OR to any alternate geometry of it. An optional 'master' dial
  can be specified to control the morph from the character's root (BODY)
- New Button **Open** : Open a file selection window to select any managed file
  and edit it. 
- New Button **View Log** : Read the log file into a dedicated sheets named 'Logs'

pypos3d:
- Extensions to support the new functions above
- Refactoring of WaveGeom.cleanDupVert (now O(n.logn) instead of O(n2))
- Enhancement of Unit Tests coverage and some useless methods removed
- Few bug fixes

Dependencies:
- Tested with GLFW 2.1.0

0.4.0 (2021-02-17)
------------------
This version of this global project delivers an OpenGL 3D viewer for Wavefront files.
This viewer provides the means to observe geometries with simple coloring and texturing
capabilities.

Changes in pypos3d.wftk:
  - Class WFMat added to support simple viewer renderings
  - WaveGeom can read material files (.mtl)

Changes in pypos3d.pftk:
  - Poser customData management added for Figure, PoserMeshedObject


0.3.0 (2020-12-05)
------------------
New decimation function added. The package 'propslim' contains the port of the QSlim algorithm initially developed and distributed by Michael Garland in July 2004 within the "SlimKit Surface Modeling Tools".
This decimate function applies to "WaveGeom" and preserves 'texture' coordinates.

**WARNING**
Original copyrights and credentials are delivered within this independant module.
The original C++ code was GPL2. I don't know about my partial port, I suspect it to be _copylefted_ by it.
If it's not the case, I would choose for 'New BSD license'
For commercial usage in a closed source program, I suggest to remove the package: pypos3d.propslim

Other changes: Few new unit tests to foster relialability.


0.2.0 (2020-11-16)
------------------

Internal structure optim: (for a better code maintenability and few speed improvements)
- Do not differentiate Props and Actors in a Figure (do avoid some Misses)
- Delete class "channels" : Shall disappear after read, attributs inlined in PoserMeshedObject
- Delete Class "FigureDescription" --> inlined in Figure
- Delete class "AddChildSA" and "weld" and "linkParam"
- Add a consistency method on links

PoserFileParser refactoring:
  --> Read Speed x 6

Channel Cleaning Improved (and fixed)

New method (for pypos3dapp) : printChannelLinks

Take into account deformers : 
  waveDeformerProp
  coneForceField

And few bug fixes

0.1.8 (2020-11-04)
------------------
* valueOp computation enhancement to support all kind of operations (for ApplyDelta)
* Channels dependencies new algorithm (for pypos3dapp 0.2 needs)

0.1.7 (2020-10-23)
------------------
* Delivery error fixed (on setup.py and setup-tu.py)

0.1.6 (2020-10-22)
------------------
* First Release of pypos3d
* First Release of PyPos3dLO : The LibreOffice based GUI for pypos3d
* Langage support : Poser4 to Poser9


0.1.1 (2020-Oct)
----------------
  Test version (for PyPI and for the libreoffice application installer)


