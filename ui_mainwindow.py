# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dicomtreeQT5.ui',
# licensing of 'dicomtreeQT5.ui' applies.
#
# Created: Mon Jul 15 14:16:14 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_DCMTreeForm(object):
    def setupUi(self, DCMTreeForm):
        DCMTreeForm.setObjectName("DCMTreeForm")
        DCMTreeForm.resize(800, 600)
        DCMTreeForm.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(DCMTreeForm)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Monospace")
        self.treeView.setFont(font)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDragDropOverwriteMode(True)
        self.treeView.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.treeView.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)
        DCMTreeForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DCMTreeForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        DCMTreeForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DCMTreeForm)
        self.statusbar.setObjectName("statusbar")
        DCMTreeForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(DCMTreeForm)
        self.toolBar.setObjectName("toolBar")
        DCMTreeForm.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_Open = QtWidgets.QAction(DCMTreeForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/Icons/ImageOpen.xpm"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Open.setIcon(icon)
        self.action_Open.setObjectName("action_Open")
        self.action_Exit = QtWidgets.QAction(DCMTreeForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/Icons/exit.xpm"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Exit.setIcon(icon1)
        self.action_Exit.setObjectName("action_Exit")
        self.action_About = QtWidgets.QAction(DCMTreeForm)
        self.action_About.setObjectName("action_About")
        self.menuFile.addAction(self.action_Open)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_Exit)
        self.menuHelp.addAction(self.action_About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.action_Open)
        self.toolBar.addAction(self.action_Exit)

        self.retranslateUi(DCMTreeForm)
        QtCore.QObject.connect(self.action_Exit, QtCore.SIGNAL("triggered()"), DCMTreeForm.close)
        QtCore.QMetaObject.connectSlotsByName(DCMTreeForm)

    def retranslateUi(self, DCMTreeForm):
        DCMTreeForm.setWindowTitle(QtWidgets.QApplication.translate("DCMTreeForm", "Dicom Tree Viewer", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("DCMTreeForm", "&File", None, -1))
        self.menuHelp.setTitle(QtWidgets.QApplication.translate("DCMTreeForm", "&Help", None, -1))
        self.toolBar.setWindowTitle(QtWidgets.QApplication.translate("DCMTreeForm", "toolBar", None, -1))
        self.action_Open.setText(QtWidgets.QApplication.translate("DCMTreeForm", "&Open", None, -1))
        self.action_Open.setToolTip(QtWidgets.QApplication.translate("DCMTreeForm", "Open dicom file", None, -1))
        self.action_Exit.setText(QtWidgets.QApplication.translate("DCMTreeForm", "E&xit", None, -1))
        self.action_Exit.setToolTip(QtWidgets.QApplication.translate("DCMTreeForm", "Exit program", None, -1))
        self.action_About.setText(QtWidgets.QApplication.translate("DCMTreeForm", "&About", None, -1))

import dicomtreeQT5_rc
