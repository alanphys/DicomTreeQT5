"""
=========================
Show a tabbed help window
=========================

Show a tabbed help window displaying the readme, licence and credits
"""
# author : AC Chamberlain <alanphys@yahoo.co.uk>
# copyright: AC Chamberlain (c) 2019-2023

from .aboutformui import Ui_AboutForm
from PySide2.QtWidgets import QDialog
import os


class About(QDialog):
    def __init__(self):
        super(About, self).__init__()
        self.ui = Ui_AboutForm()
        self.ui.setupUi(self)
        textpath = os.path.join(os.path.dirname(__file__), os.pardir)

        try:
            infile = open(os.path.join(textpath, "readme.txt"))
            try:
                self.ui.qlAbout.setText(infile.read())
            finally:
                infile.close()
        except IOError:
            self.ui.qlAbout.setText("Sorry! No readme available.")

        try:
            infile = open(os.path.join(textpath, "licence.txt"))
            try:
                self.ui.qlLicence.setText(infile.read())
            finally:
                infile.close()
        except IOError:
            self.ui.qlLicence.setText("Sorry! No licence available.")

        try:
            infile = open(os.path.join(textpath, "credits.txt"))
            try:
                self.ui.qlCredits.setText(infile.read())
            finally:
                infile.close()
        except IOError:
            self.ui.qlCredits.setText("Sorry! No credits available.")
