DicomTreeQT5 ver 0.12 Readme file 
(c) 2019 AC Chamberlain

1) Introduction
There are many DICOM tag viewers available. None of them seem to do exactly what I want, therefore this simple app.

2) Licence
Please read the file Licence.txt. This means that if as a result of using this program you fry your patients, trash your linac, nuke the cat, blow the city power in a ten block radius and generally cause global thermonuclear meltdown! Sorry, I did warn you!

3) System Requirements
Currently running on Fedora 28/KDE 5.13/QT 5.11
Windows users will need to install a python stack (such as anaconda) and QT5.
Note: If you use anaconda you must install PySide2 using conda and not Pip as the paths will not be correct.

4) Dependencies
* PySide2
* pydicom

5) Installation
Copy the files into a directory

6) Use
Open a console window, change to the above directory and run:

python3 DicomTreeQT5.pyw

Open a DICOM file either from the menu or toolbar. Drag and drop from your
favourite file manager is also supported.

7) Release notes
Latest release
Added the ability to insert, delete and modify DICOM tags and save the resulting file. Note: No checking is done on the tag values and it is not well tested.

Version 0.11
Added about package with licence details, credits and this readme.

8) History
13/03/2019 version 0.1
20/05/2019 tidy up for GitHub
15/07/2019 change open close icons
           add about package
16/7/2019  fix Windows font
17/9/2019  Add Save DICOM file
19/9/2019  Add insert, edit and delete DICOM tags
12/11/2019 Fix open file from command line
14/11/2019 Fix edit decimal string tag



