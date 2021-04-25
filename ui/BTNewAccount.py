# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/BTNewAccount.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormNewAccount(object):
    def setupUi(self, FormNewAccount):
        FormNewAccount.setObjectName("FormNewAccount")
        FormNewAccount.resize(500, 234)
        FormNewAccount.setMinimumSize(QtCore.QSize(500, 0))
        FormNewAccount.setMaximumSize(QtCore.QSize(500, 16777215))
        self.gridLayout = QtWidgets.QGridLayout(FormNewAccount)
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(FormNewAccount)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.editAccountName = QtWidgets.QLineEdit(FormNewAccount)
        self.editAccountName.setObjectName("editAccountName")
        self.horizontalLayout.addWidget(self.editAccountName)
        spacerItem = QtWidgets.QSpacerItem(150, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.buttonSaveProfile = QtWidgets.QPushButton(FormNewAccount)
        self.buttonSaveProfile.setObjectName("buttonSaveProfile")
        self.gridLayout.addWidget(self.buttonSaveProfile, 7, 0, 1, 1)
        self.toolBox = QtWidgets.QToolBox(FormNewAccount)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolBox.setFont(font)
        self.toolBox.setObjectName("toolBox")
        self.page1 = QtWidgets.QWidget()
        self.page1.setGeometry(QtCore.QRect(0, 0, 482, 95))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.page1.setFont(font)
        self.page1.setObjectName("page1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.page1)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.editURI = QtWidgets.QLineEdit(self.page1)
        self.editURI.setObjectName("editURI")
        self.gridLayout_2.addWidget(self.editURI, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.toolBox.addItem(self.page1, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 482, 95))
        self.page_2.setObjectName("page_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.page_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.comboDigest = QtWidgets.QComboBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboDigest.sizePolicy().hasHeightForWidth())
        self.comboDigest.setSizePolicy(sizePolicy)
        self.comboDigest.setObjectName("comboDigest")
        self.comboDigest.addItem("")
        self.comboDigest.addItem("")
        self.comboDigest.addItem("")
        self.comboDigest.addItem("")
        self.horizontalLayout_2.addWidget(self.comboDigest)
        spacerItem2 = QtWidgets.QSpacerItem(66, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_5 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.spinDigits = QtWidgets.QSpinBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinDigits.sizePolicy().hasHeightForWidth())
        self.spinDigits.setSizePolicy(sizePolicy)
        self.spinDigits.setMinimum(1)
        self.spinDigits.setMaximum(32)
        self.spinDigits.setObjectName("spinDigits")
        self.horizontalLayout_2.addWidget(self.spinDigits)
        spacerItem3 = QtWidgets.QSpacerItem(61, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.label_6 = QtWidgets.QLabel(self.page_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.spinInterval = QtWidgets.QSpinBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinInterval.sizePolicy().hasHeightForWidth())
        self.spinInterval.setSizePolicy(sizePolicy)
        self.spinInterval.setMinimum(0)
        self.spinInterval.setMaximum(59)
        self.spinInterval.setObjectName("spinInterval")
        self.horizontalLayout_2.addWidget(self.spinInterval)
        self.horizontalLayout_2.setStretch(1, 1)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 4)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 3, 0, 1, 1)
        self.editSecret = QtWidgets.QLineEdit(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editSecret.sizePolicy().hasHeightForWidth())
        self.editSecret.setSizePolicy(sizePolicy)
        self.editSecret.setObjectName("editSecret")
        self.gridLayout_3.addWidget(self.editSecret, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.comboSecretBase = QtWidgets.QComboBox(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboSecretBase.sizePolicy().hasHeightForWidth())
        self.comboSecretBase.setSizePolicy(sizePolicy)
        self.comboSecretBase.setMinimumSize(QtCore.QSize(120, 0))
        self.comboSecretBase.setMaximumSize(QtCore.QSize(300, 16777215))
        self.comboSecretBase.setObjectName("comboSecretBase")
        self.comboSecretBase.addItem("")
        self.comboSecretBase.addItem("")
        self.comboSecretBase.addItem("")
        self.gridLayout_3.addWidget(self.comboSecretBase, 0, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_3.addItem(spacerItem5, 1, 0, 1, 1)
        self.toolBox.addItem(self.page_2, "")
        self.gridLayout.addWidget(self.toolBox, 5, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 4, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem6, 8, 0, 1, 1)

        self.retranslateUi(FormNewAccount)
        self.toolBox.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(FormNewAccount)

    def retranslateUi(self, FormNewAccount):
        _translate = QtCore.QCoreApplication.translate
        FormNewAccount.setWindowTitle(_translate("FormNewAccount", "Form"))
        self.label_2.setText(_translate("FormNewAccount", "Account Name"))
        self.buttonSaveProfile.setText(_translate("FormNewAccount", "Save Account"))
        self.label.setText(_translate("FormNewAccount", "URI:"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page1), _translate("FormNewAccount", "Load from URI"))
        self.label_4.setText(_translate("FormNewAccount", "Hash"))
        self.comboDigest.setItemText(0, _translate("FormNewAccount", "SHA-1"))
        self.comboDigest.setItemText(1, _translate("FormNewAccount", "SHA-256"))
        self.comboDigest.setItemText(2, _translate("FormNewAccount", "SHA-512"))
        self.comboDigest.setItemText(3, _translate("FormNewAccount", "MD5"))
        self.label_5.setText(_translate("FormNewAccount", "Digits"))
        self.label_6.setText(_translate("FormNewAccount", "Interval"))
        self.label_3.setText(_translate("FormNewAccount", "Secret"))
        self.comboSecretBase.setItemText(0, _translate("FormNewAccount", "Base 32"))
        self.comboSecretBase.setItemText(1, _translate("FormNewAccount", "Base 64"))
        self.comboSecretBase.setItemText(2, _translate("FormNewAccount", "Exadecimal"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("FormNewAccount", "Insert Account Information"))
