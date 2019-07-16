"""
=========================================
Show a dicom file using hierarchical tree
=========================================

Show a dicom file using a hierarchical tree using Pyside and QT5.
Usage: python3 DicomTreeQT5.pyw dicom_filename
Or drag and drop from your file manager.

"""

# author : AC Chamberlain <alanphys@yahoo.co.uk>
# copyright: AC Chamberlain (c) 2019
# based on the scripts by Guillaume Lemaitre and Padraig Looney
# license : pydicom (https://github.com/pydicom/pydicom/blob/master/LICENSE)

import sys
from platform import system
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2.QtCore import SIGNAL, QObject, Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem, QFont
from ui_mainwindow import Ui_DCMTreeForm
from aboutpackage import About
import pydicom
from pydicom import compat
import os


class DCMTreeForm(QMainWindow):
    def __init__(self):
        super(DCMTreeForm, self).__init__()
        self.ui = Ui_DCMTreeForm()
        self.ui.setupUi(self)
        font = QFont()
        os = system()
        if os == 'Linux':
            font.setFamily("Monospace")
        elif os == 'Windows':
            font.setFamily("Courier New")
        else:
            font.setFamily("Courier")
        self.ui.treeView.setFont(font)
        self.ui.statusbar.showMessage('Open DICOM file or drag and drop')
        QObject.connect(self.ui.action_Open, SIGNAL('triggered()'), self.openfile)
        QObject.connect(self.ui.action_About, SIGNAL('triggered()'), self.showabout)

    def openfile(self):
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            filename = os.path.realpath(__file__)
        dirpath = os.path.dirname(os.path.realpath(filename))
        filename = QFileDialog.getOpenFileName(self, 'Open DICOM file', dirpath, 'DICOM files (*.dcm);;All files (*.*)')[0]
        self.show_tree(filename)

    def show_tree(self, filename):
        ds = self.dicom_to_dataset(filename)
        model = self.dataset_to_model(ds, filename)
        self.display(model)

    def dicom_to_dataset(self, filename):
        dataset = pydicom.read_file(filename, force=True)
        return dataset

    def display(self, model):
        self.ui.treeView.setModel(model)
        self.ui.treeView.show()

    def dataset_to_model(self, dataset, filename):
        model = QStandardItemModel()
        model_header = list()
        model_header.append(filename)
        model.setHorizontalHeaderLabels(model_header)
        parent_item = model.invisibleRootItem()
        self.recurse_tree(model, dataset, parent_item)
        return model

    def recurse_tree(self, model, dataset, parent):
        # order the dicom tags
        for data_element in dataset:
            if isinstance(data_element.value, compat.text_type):
                item = QStandardItem(compat.text_type(data_element))
            else:
                item = QStandardItem(str(data_element))
            parent.appendRow(item)
            if data_element.VR == "SQ":   # a sequence
                for i, dataset in enumerate(data_element.value):
                    sq_item_description = data_element.name.replace(" Sequence", "")  # XXX not i18n
                    item_text = "{0:s} {1:d}".format(sq_item_description, i + 1)
                    item = QStandardItem(item_text)
                    parent.appendRow(item)
                    self.recurse_tree(model, dataset, item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            url = event.mimeData().text()
            filename = url.split('/',2)[2]
            if os.path.isfile(filename):
                self.show_tree(filename)

    def showabout(self):
        about = About()
        about.exec()


def main():
    app = QApplication(sys.argv)
    window = DCMTreeForm()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        window.show_tree(filename)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
