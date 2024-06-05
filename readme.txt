DicomTreeQT5 ver 0.13 Readme file (c) 2019 AC Chamberlain

Note: The DicomTreeQT5 code has been incorporated in LinaQA and this repository is deprecated.

1) Introduction
There are many DICOM tag viewers available. None of them seem to do exactly what I want, therefore this simple app.

2) Licence
Please read the file Licence.txt. This means that if as a result of using this program you fry your patients, trash your linac, nuke the cat, blow the city power in a ten block radius and generally cause global thermonuclear meltdown! Sorry, you were warned!

3) System Requirements
Currently running on Fedora 28/KDE 5.13/QT 5.13
Windows users will need to install a python stack (such as anaconda) and QT5.
Note: If you use anaconda you must install PySide2 using conda and not Pip as the paths will not be correct.

4) Dependencies
* PySide2 >= 5.11
* pydicom

5) Installation
Copy the files into a directory

6) Use
Open a console window, change to the above directory and run:

python3 DicomTreeQT5.pyw

Open a DICOM file either from the menu or toolbar. Drag and drop from your favourite file manager is also supported.

7) Release notes
Latest release
Adds DICOM tag filtering on any string. Adds the ability to copy multiple tags to the clipboard, select all visible tags and clear all selected tags.

Version 0.12
Added the ability to insert, delete and modify DICOM tags and save the resulting file. Note: No checking is done on the tag values and it is not well tested.

Version 0.11
Added about package with licence details, credits and this readme.

8) History
13/03/2019 version 0.10
20/05/2019 tidy up for GitHub
15/07/2019 change open close icons
           add about package
16/7/2019  fix Windows font
17/9/2019  add Save DICOM file
19/9/2019  add insert, edit and delete DICOM tags
12/11/2019 fix open file from command line
14/11/2019 fix edit decimal string tag
22/11/2019 add copy to clipboard, select all and clear selection
25/11/2019 change signal/slot connections to new pythonistic form
           add DICOM tag filter bar
26/11/2019 fix drag and drop




