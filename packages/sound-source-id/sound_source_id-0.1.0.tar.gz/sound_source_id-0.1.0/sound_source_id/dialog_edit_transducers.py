# -*- coding: utf-8 -*-

#   Copyright (C) 2022-2023 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of sound_source_id

#    sound_source_id is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    sound_source_id is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with sound_source_id.  If not, see <http://www.gnu.org/licenses/>.

from .pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import QLocale, QThread
    from PyQt5.QtWidgets import QAbstractItemView, QComboBox, QDesktopWidget, QDialog, QDialogButtonBox, QGridLayout, QInputDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
    from PyQt5.QtGui import QDoubleValidator, QIcon
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale, QThread
    from PyQt6.QtWidgets import QAbstractItemView, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QInputDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
    from PyQt6.QtGui import QDoubleValidator, QIcon
    
import copy, pickle
from numpy import unique
##from .audio_manager import*
#from .default_experiments.generate_stimuli import pureTone
#from .default_experiments.generate_stimuli import*
##from .sndlib import*

class transducersDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = self.parent().prm
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
        self.resize(int(screen.width()/2.5), int(screen.height()/3))
        self.isPlaying = False
        #self.audioManager = audioManager(self)
        #self.playThread = threadedPlayer(self)
   
        self.sizer = QGridLayout() 
        self.v1Sizer = QVBoxLayout()
        self.v2Sizer = QVBoxLayout()
        self.calibSizer = QGridLayout()
        
        self.transducersTableWidget = QTableWidget()
        self.transducersTableWidget.setColumnCount(3)
        self.transducersTableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.transducersTableWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        self.transducersTableWidget.setHorizontalHeaderLabels([self.tr('Transducers'), self.tr('Max Level'), 'id'])
        self.transducersTableWidget.hideColumn(2)
        self.transducersTableWidget.cellDoubleClicked[int,int].connect(self.onCellDoubleClicked)

        #RENAME Transducers BUTTON
        self.renameTransducersButton = QPushButton(self.tr("Rename Transducers"), self)
        self.renameTransducersButton.clicked.connect(self.onEditLabel)
        #Change Level Transducers BUTTON
        self.changeLevelTransducersButton = QPushButton(self.tr("Change Max Level"), self)
        self.changeLevelTransducersButton.clicked.connect(self.onEditMaxLevel)
        
        #ADD Transducers BUTTON
        self.addTransducersButton = QPushButton(self.tr("Add Transducers"), self)
        self.addTransducersButton.clicked.connect(self.onClickAddTransducersButton)
        #REMOVE Transducers BUTTON
        self.removeTransducersButton = QPushButton(self.tr("Remove Transducers"), self)
        self.removeTransducersButton.clicked.connect(self.onClickRemoveTransducersButton)

        self.v1Sizer.addWidget(self.renameTransducersButton)
        self.v1Sizer.addWidget(self.changeLevelTransducersButton)
        self.v1Sizer.addWidget(self.addTransducersButton)
        self.v1Sizer.addWidget(self.removeTransducersButton)
        self.v1Sizer.addStretch()
        self.transducersList = {}
    
        for i in range(len(self.prm['transducers']['transducersChoices'])):
            currCount = i+1
            thisID = self.prm['transducers']['transducersID'][i]
            self.transducersList[thisID] = {}
            self.transducersList[thisID]['label'] = self.prm['transducers']['transducersChoices'][i]
            self.transducersList[thisID]['maxLevel'] = self.prm['transducers']['transducersMaxLevel'][i]
            self.transducersTableWidget.setRowCount(currCount)
            newItem = QTableWidgetItem(self.transducersList[thisID]['label'])
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.transducersTableWidget.setItem(currCount-1, 0, newItem)
            newItem = QTableWidgetItem(self.currLocale.toString(self.transducersList[thisID]['maxLevel']))
            newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.transducersTableWidget.setItem(currCount-1, 1, newItem)
            self.transducersList[thisID]['qid'] = QTableWidgetItem(thisID)
            self.transducersTableWidget.setItem(currCount-1, 2, self.transducersList[thisID]['qid'])

        # ##CALIBRATION TONE
        # n = 0
        # self.calLabel = QLabel(self.tr('Calibration Tone:'), self)
        # self.calibSizer.addWidget(self.calLabel, n, 0, 1, 2)
        # n = n+1
        # self.toneFreqLabel = QLabel(self.tr('Frequency (Hz)'), self)
        # self.toneFreqTF = QLineEdit("1000")
        # self.toneFreqTF.setValidator(QDoubleValidator(self))
        # self.calibSizer.addWidget(self.toneFreqLabel, n, 0)
        # self.calibSizer.addWidget(self.toneFreqTF, n, 1)
        # n = n+1
        # self.toneLevLabel = QLabel(self.tr('Level (dB)'), self)
        # self.toneLevTF = QLineEdit("60")
        # self.toneLevTF.setValidator(QDoubleValidator(self))
        # self.calibSizer.addWidget(self.toneLevLabel, n, 0)
        # self.calibSizer.addWidget(self.toneLevTF, n, 1)
        # n = n+1
        # self.toneDurLabel = QLabel(self.tr('Duration (ms)'), self)
        # self.toneDurTF = QLineEdit("4980")
        # self.toneDurTF.setValidator(QDoubleValidator(self))
        # self.calibSizer.addWidget(self.toneDurLabel, n, 0)
        # self.calibSizer.addWidget(self.toneDurTF, n, 1)
        # n = n+1
        # self.toneRampsLabel = QLabel(self.tr('Ramps (ms)'), self)
        # self.toneRampsTF = QLineEdit("10")
        # self.toneRampsTF.setValidator(QDoubleValidator(self))
        # self.calibSizer.addWidget(self.toneRampsLabel, n, 0)
        # self.calibSizer.addWidget(self.toneRampsTF, n, 1)
        # n = n+1
        # self.earLabel = QLabel(self.tr('Ear:'), self)
        # self.earChooser = QComboBox()
        # self.earChooser.addItems([self.tr("Right"), self.tr("Left"), self.tr("Both")])
        # self.calibSizer.addWidget(self.earLabel, n, 0)
        # self.calibSizer.addWidget(self.earChooser, n, 1)
        # n = n+1
        # self.playCalibButton = QPushButton(self.tr("Play"), self)
        # self.playCalibButton.clicked.connect(self.onClickPlayCalibButton)
        # self.playCalibButton.setIcon(QIcon.fromTheme("media-playback-start", QIcon(":/media-playback-start")))
        # self.calibSizer.addWidget(self.playCalibButton, n, 0, 1, 2)
        # n = n+1
        # self.stopCalibButton = QPushButton(self.tr("Stop"), self)
        # self.stopCalibButton.clicked.connect(self.onClickStopCalibButton)
        # self.stopCalibButton.setIcon(QIcon.fromTheme("media-playback-stop", QIcon(":/media-playback-stop")))
        # self.calibSizer.addWidget(self.stopCalibButton, n, 0, 1, 2)
        # if self.prm['pref']['sound']['playCommand'] in ["alsaaudio","pyaudio"]:
        #     self.stopCalibButton.show()
        # else:
        #     self.stopCalibButton.hide()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.permanentApply)

        self.sizer.addLayout(self.v1Sizer, 0, 0)
        self.v2Sizer.addLayout(self.calibSizer)
        self.v2Sizer.addStretch()
        self.sizer.addWidget(self.transducersTableWidget, 0, 1)
        self.sizer.addLayout(self.v2Sizer, 0, 2)
        self.sizer.addWidget(buttonBox, 1,1,1,2)
        self.sizer.setColumnStretch(1,2)
        self.setLayout(self.sizer)
        self.setWindowTitle(self.tr("Edit Transducers"))
        self.show()

    def onCellDoubleClicked(self, row, col):
        if col == 0:
            self.onEditLabel()
        elif col == 1:
            self.onEditMaxLevel()

    def onEditLabel(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one label can be renamed at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            msg = self.tr('New name:')
            text, ok = QInputDialog.getText(self, self.tr('Input Dialog'), msg)
            if ok:
                self.transducersTableWidget.item(self.transducersList[selectedSound]['qid'].row(), 0).setText(text)
                self.transducersList[selectedSound]['label'] = text
    def onEditMaxLevel(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one item can be edited at a time'))
        elif len(ids) < 1:
            pass
        else:
            selectedSound = ids[0]
            msg = self.tr('Level:')
            text, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.transducersList[selectedSound]['maxLevel'])
            if ok:
                self.transducersTableWidget.item(self.transducersList[selectedSound]['qid'].row(), 1).setText(self.currLocale.toString(text))
                self.transducersList[selectedSound]['maxLevel'] = text

    def findSelectedItemIds(self):
        selItems = self.transducersTableWidget.selectedItems()
        selItemsRows = []
        for i in range(len(selItems)):
            selItemsRows.append(selItems[i].row())
        selItemsRows = unique(selItemsRows)
        selItemsIds = []
        for i in range(len(selItemsRows)):
            selItemsIds.append(str(self.transducersTableWidget.item(selItemsRows[i], 2).text()))
        return selItemsIds

    def permanentApply(self):
        self.prm['transducers']['transducersChoices'] = []
        self.prm['transducers']['transducersMaxLevel'] = []
        self.prm['transducers']['transducersID'] = []

        keys = sorted(self.transducersList.keys())
        for key in keys:
            self.prm['transducers']['transducersChoices'].append(str(self.transducersList[key]['label']))
            self.prm['transducers']['transducersMaxLevel'].append(self.transducersList[key]['maxLevel'])
            self.prm['transducers']['transducersID'].append(key)
        f = open(self.parent().prm['transducersPrefFile'], 'wb')
        pickle.dump(self.parent().prm['transducers'], f)
        f.close()

    def onClickAddTransducersButton(self):
        keys = sorted(self.transducersList.keys())
        thisID = str(int(keys[-1])+1)
        currCount = self.transducersTableWidget.rowCount() + 1

        self.transducersList[thisID] = {}
        self.transducersList[thisID]['label'] = 'Transducers' + ' ' + str(currCount)
        self.transducersList[thisID]['maxLevel'] = 100
        self.transducersTableWidget.setRowCount(currCount)
        newItem = QTableWidgetItem(self.transducersList[thisID]['label'])
        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.transducersTableWidget.setItem(currCount-1, 0, newItem)
        newItem = QTableWidgetItem(self.currLocale.toString(self.transducersList[thisID]['maxLevel']))
        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.transducersTableWidget.setItem(currCount-1, 1, newItem)
        self.transducersList[thisID]['qid'] = QTableWidgetItem(thisID)
        self.transducersTableWidget.setItem(currCount-1, 2, self.transducersList[thisID]['qid'])
      

    def onClickRemoveTransducersButton(self):
        if self.transducersTableWidget.rowCount() == 1:
            ret = QMessageBox.warning(self, self.tr("Warning"),
                                            self.tr("Only one transducer left. Cannot remove!"),
                                            QMessageBox.StandardButton.Ok)
        else:
            ids = self.findSelectedItemIds()
            for i in range(len(ids)):
                selectedTransducers = ids[i]
                self.transducersTableWidget.removeRow(self.transducersList[selectedTransducers]['qid'].row())
                del self.transducersList[selectedTransducers]


    # def onClickPlayCalibButton(self):
    #     ids = self.findSelectedItemIds()
    #     if len(ids) > 1:
    #         QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one label can be renamed at a time'))
    #         return
    #     elif len(ids) < 1:
    #         QMessageBox.warning(self, self.tr('Warning'), self.tr('Please, select a transducer in the table'))
    #         return
    #     else:
    #         selectedSound = ids[0]
    #         calMaxLev = self.transducersList[selectedSound]['maxLevel']
    #         frequency = self.currLocale.toDouble(self.toneFreqTF.text())[0]
    #         level = self.currLocale.toDouble(self.toneLevTF.text())[0]
    #         duration = self.currLocale.toDouble(self.toneDurTF.text())[0]
    #         ramp = self.currLocale.toDouble(self. toneRampsTF.text())[0]
    #         channel =  self.earChooser.currentText()
    #         fs = 48000#self.currLocale.toInt(self.parent().sampRateTF.text())[0]
    #         nBits = 32#self.currLocale.toInt(self.parent().nBitsChooser.currentText())[0]
    #         calTone = pureTone(frequency, 0, level, duration, ramp, channel, fs, calMaxLev)
    #         self.isPlaying = True
    #         if self.prm['pref']['sound']['playCommand'] in ["alsaaudio","pyaudio"]:
    #             self.playThread = threadedAudioPlayer(self.parent())
    #         else:
    #             self.playThread = threadedExternalAudioPlayer(self.parent())
    #         self.playThread.playThreadedSound(calTone, fs, nBits, self.prm['pref']['sound']['playCommand'], True, 'calibrationTone.wav')
    #         if self.playThread.isFinished() == True:
    #             self.isPlaying = False

    # def onClickStopCalibButton(self):
    #     if self.isPlaying == True:
    #         self.playThread.terminate()
    #         #self.playThread.__del__()

    def closeEvent(self, event):
        if self.isPlaying == True:
            #self.playThread.__del__()
            self.playThread.terminate()
        event.accept()
        
    def accept(self): #reimplement accept (i.e. ok button)
        if self.isPlaying == True:
            #self.playThread.__del__()
            self.playThread.terminate()
        QDialog.accept(self)
    def reject(self): #reimplement reject
        if self.isPlaying == True:
            #self.playThread.__del__()
            self.playThread.terminate()
        QDialog.reject(self)

   
