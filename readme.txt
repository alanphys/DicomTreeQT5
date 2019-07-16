DicomTreeQT5 Readme file 
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

7) History
13/03/2019 version 0.1
20/05/2019 tidy up for GitHub
15/07/2019 change open close icons
           add about package
16/7/2019  fix Windows font



