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
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QLineEdit
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
        ds = None
        filename = None
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
        QObject.connect(self.ui.action_Save, SIGNAL('triggered()'), self.savefile)
        QObject.connect(self.ui.actionSave_As, SIGNAL('triggered()'), self.savefileas)
        QObject.connect(self.ui.action_Insert, SIGNAL('triggered()'), self.insert_tag)
        QObject.connect(self.ui.action_Edit, SIGNAL('triggered()'), self.edit_tag)
        QObject.connect(self.ui.action_Delete, SIGNAL('triggered()'), self.del_tag)
        QObject.connect(self.ui.action_About, SIGNAL('triggered()'), self.showabout)

    def openfile(self):
        if len(sys.argv) > 1:
            self.filename = sys.argv[1]
        else:
            self.filename = os.path.realpath(__file__)
        dirpath = os.path.dirname(os.path.realpath(self.filename))
        self.filename = QFileDialog.getOpenFileName(self, 'Open DICOM file', dirpath, 'DICOM files (*.dcm);;All files (*.*)')[0]
        self.ds = pydicom.read_file(self.filename, force=True)
        self.show_tree()

    def savefile(self):
        self.ds.save_as(self.filename)

    def savefileas(self):
        self.filename = QFileDialog.getSaveFileName(self, 'Save DICOM file', self.filename,  'DICOM files (*.dcm);;All files (*.*)')[0]
        self.ds.save_as(self.filename)

    def insert_tag(self):
        index = self.ui.treeView.currentIndex()
        tagtext = self.ui.treeView.model().itemData(index)[0]
        InputDlg = QInputDialog(self)
        InputDlg.setInputMode(QInputDialog.TextInput)
        InputDlg.resize(500,100)
        InputDlg.setLabelText('Create new tag as: (Group, Element) Keyword VR: Value')
        InputDlg.setTextValue('')
        InputDlg.setWindowTitle('Change DICOM tag')
        ok = InputDlg.exec_()
        tagtext = InputDlg.textValue()
        if ok and tagtext != '':
            tag_no = '0x' + tagtext[1:5] + tagtext[7:11]
            VR = tagtext.split(':')[0][-2:]
            tag_value = tagtext.split(':')[1][1:].strip("'")
            if tag_value[0] == '[':
                tag_value = tag_value.translate({ord(i): None for i in "[]'"}).split(',')
            print(VR, tag_value)
            self.ds.add_new(tag_no, VR, tag_value)
            self.show_tree()

    def edit_tag(self):
        index = self.ui.treeView.currentIndex()
        tagtext = self.ui.treeView.model().itemData(index)[0]
        tag_group = '0x' + tagtext[1:5]
        tag_element = '0x' + tagtext[7:11]
        tag_group_int = int(tag_group, 16)
        tag_element_int = int(tag_element, 16)
        InputDlg = QInputDialog(self)
        InputDlg.setInputMode(QInputDialog.TextInput)
        InputDlg.resize(500, 100)
        InputDlg.setLabelText('Change value:')
        InputDlg.setTextValue(str(self.ds[tag_group_int,tag_element_int].value))
        InputDlg.setWindowTitle('Change DICOM tag')
        ok = InputDlg.exec_()
        tagtext = InputDlg.textValue()
        if ok and tagtext != '':
            self.ds[tag_group_int,tag_element_int].value = tagtext
            self.show_tree()

    def del_tag(self):
        index = self.ui.treeView.currentIndex()
        tagtext = self.ui.treeView.model().itemData(index)[0]
        tag_group = '0x' + tagtext[1:5]
        tag_element = '0x' + tagtext[7:11]
        tag_group_int = int(tag_group, 16)
        tag_element_int = int(tag_element, 16)
        if tagtext != '':
            del self.ds[tag_group_int,tag_element_int]
            self.show_tree()

    def show_tree(self):
        model = self.dataset_to_model(self.ds, self.filename)
        self.display(model)

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
        window.filename = sys.argv[1]
        window.ds = pydicom.read_file(window.filename, force=True)
        window.show_tree()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
