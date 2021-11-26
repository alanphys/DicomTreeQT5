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
from PySide2.QtCore import SIGNAL, QObject, Qt, QSortFilterProxyModel
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
        self.ds = None
        self.filename = None
        self.source_model = QStandardItemModel()
        self.proxy_model = QSortFilterProxyModel()
        font = QFont()
        os = system()
        if os == 'Linux':
            font.setFamily("Monospace")
        elif os == 'Windows':
            font.setFamily("Courier New")
        else:
            font.setFamily("Courier")
        self.ui.treeView.setFont(font)
        self.ui.fsearchbar.setVisible(False)
        self.ui.treeView.addAction(self.ui.action_Copy)
        self.ui.treeView.addAction(self.ui.actionSelect_All)
        self.ui.treeView.addAction(self.ui.actionClear_selection)
        self.ui.treeView.addAction(self.ui.action_Find_tag)
        self.ui.statusbar.showMessage('Open DICOM file or drag and drop')
        self.ui.action_Open.triggered.connect(self.openfile)
        self.ui.action_Save.triggered.connect(self.savefile)
        self.ui.actionSave_As.triggered.connect(self.savefileas)
        self.ui.action_Copy.triggered.connect(self.copy_tag)
        self.ui.actionSelect_All.triggered.connect(self.selectall_tags)
        self.ui.actionClear_selection.triggered.connect(self.clearall_tags)
        self.ui.action_Find_tag.triggered.connect(self.find_tag)
        self.ui.qle_filter_tag.textChanged.connect(self.filter_tag)
        self.ui.action_Insert.triggered.connect(self.insert_tag)
        self.ui.action_Edit.triggered.connect(self.edit_tag)
        self.ui.action_Delete.triggered.connect(self.del_tag)
        self.ui.action_About.triggered.connect(self.showabout)

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

    def copy_tag(self):
        clipboard = QApplication.clipboard()
        selected_tags = ''
        for index in self.ui.treeView.selectedIndexes():
            selected_tags = selected_tags + self.ui.treeView.model().itemData(index)[0] + '\n'
        clipboard.setText(selected_tags)

    def selectall_tags(self):
        self.ui.treeView.selectAll()

    def clearall_tags(self):
        self.ui.treeView.clearSelection()

    def find_tag(self):
        if self.ui.fsearchbar.isEnabled():
            self.ui.qle_filter_tag.setText('')
            self.ui.fsearchbar.setVisible(False)
            self.ui.fsearchbar.setEnabled(False)
            self.ui.action_Find_tag.setText('Show &Filter bar')
        else:
            self.ui.fsearchbar.setVisible(True)
            self.ui.fsearchbar.setEnabled(True)
            self.ui.action_Find_tag.setText('Hide &Filter bar')

    def filter_tag(self):
        """Select tags that contain requested text"""
        tag_to_find = self.ui.qle_filter_tag.text()
        if tag_to_find != '':
            self.proxy_model.setFilterRegularExpression(tag_to_find)
        else:
            self.proxy_model.setFilterRegularExpression('')

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
        tag_vr = tagtext.split(':')[0][-2:]
        tag_keyword = tagtext.split(':')[0][13:-2].strip()
        InputDlg = QInputDialog(self)
        InputDlg.setInputMode(QInputDialog.TextInput)
        InputDlg.resize(500, 100)
        InputDlg.setLabelText('Change value for (' + tag_group + ', ' + tag_element + ') ' + tag_keyword + ' ' + tag_vr + ':')
        InputDlg.setTextValue(str(self.ds[tag_group_int,tag_element_int].value))
        InputDlg.setWindowTitle('Change DICOM tag')
        ok = InputDlg.exec_()
        tagtext = InputDlg.textValue()
        if ok and tagtext != '':
            if tag_vr == 'DS':
                if tagtext[0] == '[':
                    tagtext = tagtext.translate({ord(i): None for i in "[]'"}).split(',')
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
        self.dataset_to_model()
        self.proxy_model.setSourceModel(self.source_model)
        self.ui.treeView.setModel(self.proxy_model)
        self.ui.treeView.show()

    def dataset_to_model(self):
        self.source_model.clear()
        model_header = list()
        model_header.append(self.filename)
        self.source_model.setHorizontalHeaderLabels(model_header)
        parent_item = self.source_model.invisibleRootItem()
        self.write_header(self.source_model, self.ds, parent_item)
        self.recurse_tree(self.source_model, self.ds, parent_item)
        return

    def write_header(self, model, ds, parent):
        # write meta data
        fm = ds.file_meta
        for data_element in fm:
            if isinstance(data_element.value, compat.text_type):
                item = QStandardItem(compat.text_type(data_element))
            else:
                item = QStandardItem(str(data_element))
            parent.appendRow(item)

    def recurse_tree(self, model, ds, parent):
        # order the dicom tags
        # write data elements
        for data_element in ds:
            if isinstance(data_element.value, compat.text_type):
                item = QStandardItem(compat.text_type(data_element))
            else:
                item = QStandardItem(str(data_element))
            parent.appendRow(item)
            if data_element.VR == "SQ":   # a sequence
                for i, ds in enumerate(data_element.value):
                    sq_item_description = data_element.name.replace(" Sequence", "")  # XXX not i18n
                    item_text = "{0:s} {1:d}".format(sq_item_description, i + 1)
                    item = QStandardItem(item_text)
                    parent.appendRow(item)
                    self.recurse_tree(model, ds, item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            if len(event.mimeData().urls()) > 1:
                self.ui.statusbar.showMessage('Warning! More than one file was passed.')
            filename = str(event.mimeData().urls()[0].toLocalFile())
            if os.path.isfile(filename):
                self.filename = filename
                self.ds = pydicom.read_file(self.filename, force=True)
                self.show_tree()
            else:
                self.ui.statusbar.showMessage("Sorry, couldn't open the file!")

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
