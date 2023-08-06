propeller_design_tools (PDT)
============================
---
**Work in progress / incomplete documentation**

Note: The graphical user interface for this should be functional for Linux users as well very soon!!!

Eventually I do plan to create better docs, but for now it's just what you see below and the source code itself.

---

Description
===========
Python 3.7 package that provides exactly what it sounds 
like by automating usage of the GPL-licensed 
CLI-utilities XFOIL and XROTOR.

Both utilities are published by professor Mark Drela (MIT).
- XFOIL: for arbitrary 2D airfoil analysis
- XROTOR: for arbitrary propeller design schemes

IMPORTANT NOTE: to potentially aid in realizing errors are coming from XFOIL or XROTOR rather than this source code ->
currently this source code implements these as executables installed when pip installing this package -> this means if
you are having pip install errors and are on Linux it might be caused by that.  Actually, if you are having any errors,
even in the GUI, and you are on Linux it might be caused by me not understanding until now much about Linux.  If this 
is the case and you think you know what is causing the error, please feel free to reach out to me to let me know.

CONTINUED: additionally, very soon I will be implementing a fix to automatically install all dependencies, which should
fix many issues for Linux users, if not all of the current ones.  I also HIGHLY RECOMMEND to use only the "constant" 
blade cl distribution target option for the first time you ever use this code, and then only venture into other options
once you are familiar with the code more and can explain to me even what exactly Mark Drela means by this parameter.  I
think it's just his way of saying the parameter that controls what you want each target section's operating AoA to be,
which in all honestly I have personally found to not really affect the outputs all that much with the exception
(obviously) of what each section's chord length will end up being.  It doesn't seem to impact overall realized efficiency
of the design very much (< ~5-10 percent in all my experiences).

For this same exact reason, it is also HIGHLY RECOMMENDED to use only the 'grad' or 'pot' solver options until you know
you have the code at least generating an output without failing.  My personal favorite solver is obviously the 'vrtx'
option, but XROTOR seems to be much less stable and take much, much longer to arrive at solutions when using 'vrtx'.
Thank you all that is my TED talk.

Purpose
=======
PDT seeks to provide the user a set of python3 utilities
that can be used for arbitrary scripting efforts to automate
usage of both XFOIL and XROTOR while implementing its own 
unique python3.7-native algorithms to maintain local
input files, meta files, databases, and results files and
weave everything together for the user in a simple,
meaningful way to aid in the initial / investigatory 
stage of well-behaved propeller designs.

Getting Started
===============
Installation
------------
`pip install propdes`

General Operation
-----------------
`import propeller_design_tools as pdt`

PDT operates on two different "database" directories, defined
by the user with:

    pdt.set_airfoil_database(path: str)
    pdt.set_propeller_database(path: str)

**The user must set these two directories at the top 
of every script right after the imports**

*The airfoil directory will be used to store any foil / 
XFOIL- related support files, and the propeller directory
will be used similarly to store any propeller / XROTOR - 
related support files.*

Pre-Requisite: XFOIL and XROTOR Executables
-------------------------------------------
(soon this section will be obsolete as I plan to implement a pure-python
version of both XFOIL and XROTOR in the source code)

In order to utilize any PDT functionality that depends on 
running XFOIL, the "xfoil.exe" executable file needs to be
in the user-set "airfoil_database" location. *Current pip 
installations include the xfoil.exe file in the foil_database,
there should theoretically be no need to download it manually.*

[XFOIL executable and docs](https://web.mit.edu/drela/Public/web/xfoil/)

Likewise, in order to utilize any PDT functionality that
depends on running XROTOR, the "xrotor.exe" executable file
needs to be in the user-set "propeller_database" location.
*Current pip installations include the xrotor.exe file in the 
default prop_database, there should theoretically be no need to 
download it manually.*

[CROTOR executable and docs](http://www.esotec.org/sw/crotor.html#download)
*(this is actually a link to "CROTOR", which I find is
the easiest way to obtain a windows-executable of XROTOR)*

[actual XROTOR docs](https://web.mit.edu/drela/Public/web/xrotor/xrotor_doc.txt)

Example Scripts / Workflow
--------------------------
At a high-level, the current concept for PDT workflow is as 
follows (after obtaining the required executables and pip-installing 
the PDT package):

0. Try out the (currently extremely buggy and incomplete) user interface!
[example0_user_interface.py](
   https://github.com/helloDestroyerOfWorlds/propeller_design_tools/blob/master/tests/example0_user_interface.py
   )

   ![ex0-1.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex0-1.png)
   ![ex0-2.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex0-2.png)
   ![ex0-3.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex0-3.png)

1. Obtain normalized airfoil coordinate files from
[UIUC Database](https://m-selig.ae.illinois.edu/ads/coord_database.html)
-> save these files into the "airfoil_database" directory


2. Use PDT to run XFOIL across ranges of Reynolds Numbers in order to
populate database data for the desired foil sections -> see 
[example1_airfoil_analysis.py](
   https://github.com/helloDestroyerOfWorlds/propeller_design_tools/blob/master/tests/example1_airfoil_analysis.py
   )

   ![ex1-1.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex1-1.png)
   ![ex1-2.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex1-2.png)


3. Once the required 2D airfoil data is generated, PDT can then be used
to automatically generate all the required 2D foil definition parameters
required by XROTOR (these "station parameters" are essentially what 
allow XROTOR to model the performance of well-behaved, arbitrarily-lofted 
blade geometries) -> see
[example2_radialstation_creation.py](
   https://github.com/helloDestroyerOfWorlds/propeller_design_tools/blob/master/tests/example2_radialstation_creation.py
   )

   ![ex2-1.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex2-1.png)
   
   But this step is also automated & displayed by PDT when the user uses
the builtin PDT propeller creation function -> see
[example3_prop_creation.py](
   https://github.com/helloDestroyerOfWorlds/propeller_design_tools/blob/master/tests/example3_prop_creation.py
   )

   ![ex3-1.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex3-1.png)

   NOTE: It is highly recommended to first run XROTOR using either the 'grad' 
or the 'pot' vortex formulation in order to get your design "tweaked in" -> 
these are much faster than the (more accurate) 'vrtx' formulation, which you 
can then move on to.

   ![ex3-2.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex3-2.png)


4. PDT's Propeller() object instances can generate 3D geometry files 
including profle xyz coordinate listings, and .stl 3D geometry files -> see
[example4_stl_generation.py](
   https://github.com/helloDestroyerOfWorlds/propeller_design_tools/blob/master/tests/example4_stl_generation.py
   )

   ![ex4-1.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex4-1.png)

Note: It is known that currently there is an issue with these .stl files opening in SolidWorks -> try converting them
using anything (first idea is MS Paint, I think the new version can save STL files as well).  As far as I can tell this 
is only an issue for SolidWorks users on Windows, these files open and display fine in every other application.

5. Analyze a given Propeller() instance across a sweep of operating points -> see 
[example5_prop_analysis.py](
   https://github.com/helloDestroyerOfWorlds/propeller_design_tools/blob/master/tests/example5_prop_analysis.py
   )

   ![ex5-1.png](https://raw.githubusercontent.com/helloDestroyerOfWorlds/propeller_design_tools/master/tests/ex5-1.png)


6. **WIP** Prop optimization (grid-search style generic optimizer for "optimal"
prop design generation by means of maximizing or minimizing a given output / 
calculated metric based on outputs, optionally taking into account different
propeller operating points via the ability to define the propeller's "duty-cycle"
-> coming soon! This should elimiate the user's need to even input a value for the
desired blade cl distribution altogether.)