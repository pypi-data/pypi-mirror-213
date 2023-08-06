#!/usr/bin/env python
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


import argparse, fnmatch, sys, platform, os, copy, logging, pickle, random, traceback, scipy, signal, subprocess, time
from sound_source_id.pyqtver import*

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QFont, QIcon, QPainter, QDesktopServices
    from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QDesktopWidget, QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout, QFileDialog, QInputDialog, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
    from PyQt5.QtCore import QRect
    from PyQt5.QtCore import Qt, QEvent, QDate, QDateTime, QTime
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QAction, QFont, QIcon, QPainter, QDesktopServices
    from PyQt6.QtWidgets import QAbstractItemView, QApplication, QDialogButtonBox, QFrame, QGridLayout, QHBoxLayout, QFileDialog, QInputDialog, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QSizePolicy, QSplitter, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
    from PyQt6.QtCore import QRect
    from PyQt6.QtCore import Qt, QEvent, QDate, QDateTime, QTime

from numpy import sin, cos, pi, sqrt, abs, arange, zeros, mean, concatenate, convolve, angle, real, log2, log10, int_, linspace, repeat, ceil, unique, hamming, hanning, blackman, bartlett, round, transpose
from numpy.fft import rfft, irfft, fft, ifft
from numpy import ceil, concatenate, floor, float32, int16, int32, mean, sqrt, transpose, zeros


import pandas as pd
import numpy as np
from tempfile import mkstemp
from sound_source_id.audio_manager import*
from sound_source_id.sndlib import*
from sound_source_id.global_parameters import*
from sound_source_id.dialog_edit_preferences import*
from sound_source_id.dialog_edit_transducers import*
from sound_source_id import qrc_resources
from sound_source_id._version_info import*
from sound_source_id.utils import*
if platform.system() == 'Windows':
    import winsound

__version__ = sound_source_id_version
signal.signal(signal.SIGINT, signal.SIG_DFL)

if platform.system() == "Linux":
    try:
        import alsaaudio
    except ImportError:
        pass
try:
    import pyaudio
except ImportError:
    pass

local_dir = os.path.expanduser("~") +'/.local/share/data/sound_source_id/'
if os.path.exists(local_dir) == False:
    os.makedirs(local_dir)
stderrFile = os.path.expanduser("~") +'/.local/share/data/sound_source_id/sound_source_id_stderr_log.txt'

logging.basicConfig(filename=stderrFile,level=logging.DEBUG,)


#the except hook allows to see most startup errors in a window
#rather than the console
def excepthook(except_type, except_val, tbck):
    """ Show errors in message box"""
    # recover traceback
    tb = traceback.format_exception(except_type, except_val, tbck)
    def onClickSaveTbButton():
        ftow = QFileDialog.getSaveFileName(None, 'Choose where to save the traceback', "traceback.txt", 'All Files (*)')[0]
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            fName = open(ftow, 'w')
            fName.write("".join(tb))
            fName.close()
    
    diag = QDialog(None, Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)
    diag.window().setWindowTitle("Critical Error!")
    siz = QVBoxLayout()
    lay = QVBoxLayout()
    saveTbButton = QPushButton("Save Traceback", diag)
    saveTbButton.clicked.connect(onClickSaveTbButton)
    lab = QLabel("Sorry, something went wrong. The attached traceback can help you troubleshoot the problem: \n\n" + "".join(tb))
    lab.setMargin(10)
    lab.setWordWrap(True)
    lab.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    lab.setStyleSheet("QLabel { background-color: white }");
    lay.addWidget(lab)

    sc = QScrollArea()
    sc.setWidget(lab)
    siz.addWidget(sc) #SCROLLAREA IS A WIDGET SO IT NEEDS TO BE ADDED TO A LAYOUT

    buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)

    buttonBox.accepted.connect(diag.accept)
    buttonBox.rejected.connect(diag.reject)
    siz.addWidget(saveTbButton)
    siz.addWidget(buttonBox)
    diag.setLayout(siz)
    diag.exec()

    timeStamp = ''+ time.strftime("%d/%m/%y %H:%M:%S", time.localtime()) + ' ' + '\n'
    logMsg = timeStamp + ''.join(tb)
    logging.debug(logMsg)


class applicationWindow(QMainWindow):
    """main window"""
    def __init__(self, prm):
        QMainWindow.__init__(self)
        self.setAcceptDrops(True)
        self.prm = prm
        self.currBlock = 0
        #self.sampFreq = 48000
        #self.nbits = 32
        self.prm['version'] = __version__
        self.prm['builddate'] = sound_source_id_builddate
        
        self.saveResFile = ""
        self.listenerID = ""
        self.audioManager = audioManager(self)

        try:
            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]
        ##if all previously stored transducers have been removed use the first of the new ones
        except:
            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][0]
            
        self.trialRunning = False
        self.currLocale = prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.setWindowTitle(self.tr("sound_source_id"))
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
       
        self.f2_sizer = QVBoxLayout()
        self.f2_sizer.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.f1 = QFrame()
        self.f1.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        self.f2 = QFrame()
        self.f2.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        self.splitter = QSplitter(QtCore.Qt.Orientation.Horizontal)

        self.statusBar()
        #MENU-----------------------------------
        self.menubar = self.menuBar()
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('&File'))

        loadPrmButton = QAction(self.tr('Load Parameters'), self)
        loadPrmButton.setShortcut('Ctrl+L')
        loadPrmButton.setStatusTip(self.tr('Load Parameters File'))
        loadPrmButton.triggered.connect(self.onClickLoadParameters)
        self.statusBar()
        self.fileMenu.addAction(loadPrmButton)

        exitButton = QAction(QIcon.fromTheme("application-exit", QIcon(':/exit')), self.tr('Exit'), self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip(self.tr('Exit application'))
        exitButton.triggered.connect(self.close)
        self.statusBar()
        self.fileMenu.addAction(exitButton)

        #EDIT MENU
        self.editMenu = self.menubar.addMenu(self.tr('&Edit'))
        self.editPrefAction = QAction(self.tr('Preferences'), self)
        self.editMenu.addAction(self.editPrefAction)
        self.editPrefAction.triggered.connect(self.onEditPref)

        self.editTransducersAction = QAction(QIcon.fromTheme("audio-headphones", QIcon(":/audio-headphones")), self.tr('Transducers'), self)
        self.editMenu.addAction(self.editTransducersAction)
        self.editTransducersAction.triggered.connect(self.onEditTransducers)

        #HELP MENU
        self.helpMenu = self.menubar.addMenu(self.tr('&Help'))

        self.onShowModulesDocAction = QAction(self.tr('Manual (html)'), self)
        self.helpMenu.addAction(self.onShowModulesDocAction)
        self.onShowModulesDocAction.triggered.connect(self.onShowModulesDoc)

        self.onShowManualPdfAction = QAction(self.tr('Manual (pdf)'), self)
        self.helpMenu.addAction(self.onShowManualPdfAction)
        self.onShowManualPdfAction.triggered.connect(self.onShowManualPdf)

        self.onAboutAction = QAction(QIcon.fromTheme("help-about", QIcon(":/help-about")), self.tr('About sound_source_id'), self)
        self.helpMenu.addAction(self.onAboutAction)
        self.onAboutAction.triggered.connect(self.onAbout)

        self.showPlayBtnAction = QAction(self.tr('Show Play Buttons'), self, checkable=True)
        self.editMenu.addAction(self.showPlayBtnAction)
        self.showPlayBtnAction.triggered.connect(self.onToggleShowPlayBtnAction)
      
        # self.listenerTF = QLineEdit("")
        # self.top_widg_sizer.addWidget(self.listenerTF)

        if os.path.exists(prm["pref"]["default_prm_file"]):
            try:
                self.loadParameters(prm["pref"]["default_prm_file"])
            except:
                self.angles = [-70, 70]
                self.labels = ["1", "2"]
                self.channels = [1, 2]
                self.n_chan = 2
                self.n_blocks = 0
                self.stimListFile = ""
                self.randomizeTrialList = "true"
                self.demo_stim = ""
                self.demo_stim_lev = 0
                self.show()
                QMessageBox.warning(self, self.tr("Warning"), self.tr("There was an issue loading your default parameter file. It is likely to contain an error. Please select a new default parameters file and restart the program."))
                self.onEditPref()
        else:
            self.angles = [-70, 70]
            self.labels = ["1", "2"]
            self.channels = [1, 2]
            self.n_chan = 2
            self.n_blocks = 0
            self.stimListFile = ""
            self.randomizeTrialList = "true"
            self.demo_stim = ""
            self.demo_stim_lev = 0
            self.show()
            QMessageBox.warning(self, self.tr("Warning"), self.tr("The default parameters file could not be found. Please select a new default parameters file and restart the program."))
            self.onEditPref()


        self.statusButton = QPushButton(self.tr("Start"), self)
        self.f2_sizer.addWidget(self.statusButton)
        #self.statusButton.setGeometry(QRect(rad+100, rad, 180, 40))
        self.statusButton.clicked.connect(self.onClickStatusButton)
        self.statusButton.setStyleSheet('font-size: 16pt; font-weight: bold')
        #self.statusButton.show()

        self.runDemoButton = QPushButton(self.tr("Run Demo"), self)
        self.f2_sizer.addWidget(self.runDemoButton)
        #self.runDemoButton.setGeometry(QRect(rad*2+100, rad, 120, 40))
        self.runDemoButton.clicked.connect(self.onClickRunDemoButton)
        self.runDemoButton.setStyleSheet('font-size: 16pt; font-weight: bold')
        self.runDemoButton.show()
        
        

        self.f2.setLayout(self.f2_sizer)
        self.splitter.addWidget(self.f1)
        self.splitter.addWidget(self.f2)

        self.setCentralWidget(self.splitter)
        self.setGeometry(0, 0, int(screen.width()*3/4), screen.height())
        self.splitter.splitterMoved.connect(self.updateInterface)
        self.splitter.setSizes([int((5/6)*screen.width()), int((1/6)*screen.width())])

        self.setupInterface(clearPrev=False)
        
        self.audioManager.initializeAudio()
        self.show()
        self.updateInterface() #needed to get correct layout on Windows when program starts
        
    def onToggleShowPlayBtnAction(self):
        for pb in self.play_btn:
            if self.showPlayBtnAction.isChecked() == True:
                pb.show()
            else:
                pb.hide()

    def loadParameters(self, fName):
        self.parametersFile = fName
        fStream = open(fName, 'r')
        allLines = fStream.readlines()
        fStream.close()
        self.angles = []
        self.labels = []
        self.channels = []
        
        for i in range(len(allLines)):
            if allLines[i].split(':')[0].strip() == 'angles':
                angles_list = allLines[i].split(':')[1].strip().split(',')
                for li in angles_list:
                    self.angles.append(int(li))
            elif allLines[i].split(':')[0].strip() == 'labels':
                labels_list = allLines[i].split(':')[1].strip().split(',')
                for li in labels_list:
                    self.labels.append(li.strip())
            elif allLines[i].split(':')[0].strip() == 'channels':
                channels_list = allLines[i].split(':')[1].strip().split(',')
                for li in channels_list:
                    self.channels.append(int(li.strip()))
            elif allLines[i].split(':')[0].strip() == 'n_chan':
                self.n_chan = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'n_blocks':
                self.n_blocks = int(allLines[i].split(':')[1].strip())
            elif allLines[i].split(':')[0].strip() == 'stim_list_file':
                self.stimListFile = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'randomize':
                self.randomizeTrialList = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'demo_stim':
                self.demo_stim = allLines[i].split(':')[1].strip()
            elif allLines[i].split(':')[0].strip() == 'demo_stim_lev':
                self.demo_stim_lev = float(allLines[i].split(':')[1].strip())

        
        fDir = fName.split('/')[0:-1]
        fDir = "/".join([el for el in fDir]) + "/"
        os.chdir(fDir)
        self.stimList = pd.read_csv(self.stimListFile, sep=";")
        self.statusBar().showMessage(self.tr("Loaded ") + fName + self.tr(" parameter file"))

        
    def onClickLoadParameters(self):
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose parameters file to load"), '', self.tr("All Files (*)"))[0]
        if len(fName) > 0: #if the user didn't press cancel
            self.loadParameters(fName)
            self.setupInterface(clearPrev=True)
            
    def setupInterface(self, clearPrev):
        if clearPrev == True:
            #self.statusButton.deleteLater()
            #self.runDemoButton.deleteLater()
            for btn in self.rsp_btn:
                btn.deleteLater()
            for btn in self.play_btn:
                btn.deleteLater()
            for lgt in self.rsp_light:
                lgt.deleteLater()

        theta = 2 * np.pi  / 10
        bt_wd = 40; bt_ht = 40
        base_rad = np.minimum(self.f1.height(), self.f1.width())
        rad_l = base_rad #560
        rad = rad_l - 60 #500
        rad_pb = rad - 60  #radius play button
        self.rsp_btn = []
        self.play_btn = []
        self.rsp_light = []
        dxl = []; dyl = []
        dx_pb = []; dy_pb = []
        for i in range(len(self.angles)):
            angle = deg2rad(self.angles[i])
            dx = int(rad*np.sin(angle))+rad+100
            dy = -int(rad*np.cos(angle))+rad+100
            dxl.append(int(rad_l*np.sin(angle))+rad+100)
            dyl.append(-int(rad_l*np.cos(angle))+rad+100)
            dx_pb.append(int(rad_pb*np.sin(angle))+rad+100)
            dy_pb.append(-int(rad_pb*np.cos(angle))+rad+100)
            self.rsp_btn.append(QPushButton(self.labels[i], parent = self.f1))
            self.rsp_btn[i].setGeometry(QRect(dx, dy, bt_wd, bt_ht))
            self.rsp_btn[i].clicked.connect(self.on_click_response_button)
            self.rsp_btn[i].show()

            self.play_btn.append(QPushButton('>'+self.labels[i], parent = self.f1))
            self.play_btn[i].setGeometry(QRect(dx_pb[i], dy_pb[i], bt_wd, bt_ht))
            self.play_btn[i].clicked.connect(self.on_click_play_button)
            self.play_btn[i].hide()
     
            self.rsp_light.append(responseLight(self.f1, self.prm))
            self.rsp_light[i].setGeometry(QRect(dxl[i], dyl[i], bt_wd, bt_ht))
            self.rsp_light[i].move(dxl[i], dyl[i])
            self.rsp_light[i].show()

        self.resizeEvent(QtGui.QResizeEvent(self.size(), QtCore.QSize()))
        

    def updateInterface(self):
        #self.splitter.setSizes([int((5/6)*self.width()), int((1/6)*self.width())])
        theta = 2 * np.pi  / 10
        bt_wd = 40; bt_ht = 40
        base_rad = np.minimum(int(self.f1.height()/2), int(self.f1.width()/2))-25
        rad_l = base_rad #560
        rad = rad_l - 60 #500
        rad_pb = rad - 60  #radius play button

        dxl = []; dyl = []
        dx_pb = []; dy_pb = []
        x_offset = 50
        y_offset = 75
        for i in range(len(self.angles)):
            angle = deg2rad(self.angles[i])
            dx = int(rad*np.sin(angle))+rad+x_offset
            dy = -int(rad*np.cos(angle))+rad+y_offset
            dxl.append(int(rad_l*np.sin(angle))+rad+x_offset)
            dyl.append(-int(rad_l*np.cos(angle))+rad+y_offset)
            dx_pb.append(int(rad_pb*np.sin(angle))+rad+x_offset)
            dy_pb.append(-int(rad_pb*np.cos(angle))+rad+y_offset)

            self.rsp_btn[i].move(dx, dy)
            self.play_btn[i].move(dx_pb[i], dy_pb[i])
            self.rsp_light[i].move(dxl[i], dyl[i])

    def resizeEvent(self, event):
        self.updateInterface()
        #self.splitter.setSizes([int((5/6)*self.width()), int((1/6)*self.width())])
        QMainWindow.resizeEvent(self, event)
  
    def onClickStatusButton(self):
        if self.currBlock == 0:
            if self.saveResFile == "":
                ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "", self.tr('All Files (*)'), "")[0]
                # if len(ftow) > 0:
                #     if fnmatch.fnmatch(ftow, '*.csv') == False:
                #         ftow = ftow + '.csv'
                if ftow != "":
                    self.saveResPath = ftow #file where results are saved
                    self.saveResDir = os.path.dirname(str(ftow)) + '/' #directory where results are saved
                    self.saveResFile = open(self.saveResPath, "w")
                    self.saveResFile.write("listener" + self.prm['pref']['csvSeparator'] +
                                           "condition" + self.prm['pref']['csvSeparator'] +
                                           "block" + self.prm['pref']['csvSeparator'] +
                                           "trial" + self.prm['pref']['csvSeparator'] +
                                           "angle" + self.prm['pref']['csvSeparator'] +
                                           "response" + self.prm['pref']['csvSeparator'] +
                                           "error" + self.prm['pref']['csvSeparator'] +
                                           "sound_file" + self.prm['pref']['csvSeparator'] +
                                           "base_level" + self.prm['pref']['csvSeparator'] +
                                           "rove" + self.prm['pref']['csvSeparator'] +
                                           "actual_level" + self.prm['pref']['csvSeparator'] +
                                           "date" + self.prm['pref']['csvSeparator'] +
                                           "time\n")
                else:
                    QMessageBox.warning(self, self.tr("Warning"), self.tr("You need to select a file where to save the results to proceed"))
                return
            
            if self.listenerID == "":
                msg = self.tr("Please, enter the listener's name:") 
                text, ok = QInputDialog.getText(self, self.tr("Input Dialog:") , msg)
                if ok:
                    self.listenerID = text
                return

            self.currBlock = 1
            self.statusButton.setText(self.tr("Running"))
            self.do_block()
          
        elif self.currBlock > 0 and self.currBlock < self.n_blocks:
            self.statusButton.setText(self.tr("Running"))
            self.currBlock = self.currBlock + 1
            self.do_block()

    def onClickRunDemoButton(self):
        if self.trialRunning == True:
            return
        self.trialRunning = True
        for i in range(len(self.angles)):
            self.prep_sound(self.demo_stim, i+1, self.demo_stim_lev)
            self.rsp_light[i].setStatus('neutral')
            self.audioManager.playSound(self.curr_stim_multi, self.sampFreq, self.nbits, False, "tmp.wav") 
            self.rsp_light[i].setStatus('off')
            time.sleep(0.5)
        QApplication.processEvents()
        self.trialRunning = False
        
    def do_block(self):
        self.nTrials = self.stimList.shape[0]
        if self.randomizeTrialList == "true":
            self.stimList = self.stimList.sample(frac=1)
        self.currTrialN = 1
        self.do_trial()
        
    def do_trial(self):
        self.trialRunning = True

        self.curr_ang = self.stimList['angle'].values[self.currTrialN-1]
        self.currIdx = self.angles.index(self.curr_ang)
        self.curr_chan = self.channels[self.currIdx]
        self.curr_stim_file = self.stimList['sound_file'].values[self.currTrialN-1]
        self.curr_stim_lev = self.stimList['level'].values[self.currTrialN-1]
        self.curr_rove = self.stimList['roving'].values[self.currTrialN-1]
        self.curr_lev = self.curr_stim_lev + random.uniform(-self.curr_rove, self.curr_rove)
        self.giveFeedback = self.stimList['feedback'].values[self.currTrialN-1]
        self.curr_cnd = self.stimList['condition'].values[self.currTrialN-1]
        
        self.prep_sound(self.curr_stim_file, self.curr_chan, self.curr_lev)
        self.audioManager.playSound(self.curr_stim_multi, self.sampFreq, self.nbits, False, "tmp.wav")

        QApplication.processEvents()
        self.trialRunning = False

    def on_click_play_button(self):
        try:
            buttonClicked = self.play_btn.index(self.sender())+1
        except:
            buttonClicked = 0

        ang = self.angles[buttonClicked-1]
        chan = self.channels[buttonClicked-1]
        stim_file = self.demo_stim 
        lev = self.demo_stim_lev

        self.prep_sound(stim_file, chan, lev)
        self.audioManager.playSound(self.curr_stim_multi, self.sampFreq, self.nbits, False, "tmp.wav")

    def prep_sound(self, stim_file, chan, lev):
        curr_stim_mono, sf, nbits = self.audioManager.loadWavFile(stim_file, lev, self.maxLevel, channel="Original")

        if curr_stim_mono.ndim > 1:
            curr_stim_mono = curr_stim_mono[:,0]
        curr_stim_mono  = curr_stim_mono.reshape(curr_stim_mono.shape[0], 1)

        self.curr_stim_multi = np.zeros((curr_stim_mono.shape[0], self.n_chan))
        self.curr_stim_multi[:, chan-1] = curr_stim_mono[:,0]
        if self.prm["pref"]["sound"]["prependSilence"] > 0:
            duration = self.prm["pref"]["sound"]["prependSilence"]/1000 #convert from ms to sec
            nSamples = int(round(duration * sf))
            silenceToPrepend = zeros((nSamples, self.n_chan))
            self.curr_stim_multi = concatenate((silenceToPrepend, self.curr_stim_multi), axis=0)
        if self.prm["pref"]["sound"]["appendSilence"] > 0:
            duration = self.prm["pref"]["sound"]["appendSilence"]/1000 #convert from ms to sec
            nSamples = int(round(duration * sf))
            silenceToAppend = zeros((nSamples, self.n_chan))
            self.curr_stim_multi = concatenate((self.curr_stim_multi, silenceToAppend), axis=0)
        self.sampFreq = sf
        self.nbits = nbits
            
    def on_click_response_button(self):
        #the try-except is here because when the interface is updating between blocks
        #the sender may be missing (participants press multiple times response button when interface is changing)
        try:
            buttonClicked = self.rsp_btn.index(self.sender())+1
        except:
            buttonClicked = 0
        self.sortResponse(buttonClicked)

    def sortResponse(self, buttonClicked):
        if buttonClicked == 0: #0 is not a response option
            return
        if self.statusButton.text() != self.tr("Running"):
            return
        if self.trialRunning == True: # do not accept responses while the trial is running
            return

        rsp_ang = self.angles[buttonClicked-1]

        if self.giveFeedback == True:
            if rsp_ang == self.curr_ang:
                self.rsp_light[self.currIdx].giveFeedback('correct', '')
            else:
                self.rsp_light[self.currIdx].giveFeedback('incorrect', '')
       
            
        currTime = QTime.toString(QTime.currentTime(), self.currLocale.timeFormat(self.currLocale.ShortFormat)) 
        currDate = QDate.toString(QDate.currentDate(), self.currLocale.dateFormat(self.currLocale.ShortFormat)) 

        #listener
        self.saveResFile.write(self.listenerID + self.prm['pref']["csvSeparator"])
        #condition
        self.saveResFile.write(str(self.curr_cnd) + self.prm['pref']["csvSeparator"])
        #block
        self.saveResFile.write(str(self.currBlock) + self.prm['pref']["csvSeparator"])
        #trial
        self.saveResFile.write(str(self.currTrialN) + self.prm['pref']["csvSeparator"])
        #angle
        self.saveResFile.write(str(self.curr_ang) + self.prm['pref']["csvSeparator"])
        #response
        self.saveResFile.write(str(rsp_ang) + self.prm['pref']["csvSeparator"])
        #error
        self.saveResFile.write(str(self.curr_ang-rsp_ang) + self.prm['pref']["csvSeparator"])
        #sound file
        self.saveResFile.write(self.curr_stim_file + self.prm['pref']["csvSeparator"])
        #base level
        self.saveResFile.write(str(self.curr_stim_lev) + self.prm['pref']["csvSeparator"])
        #rove
        self.saveResFile.write(str(self.curr_rove) + self.prm['pref']["csvSeparator"])
        #level
        self.saveResFile.write(str(self.curr_lev) + self.prm['pref']["csvSeparator"])
        #date
        self.saveResFile.write(currDate + self.prm['pref']["csvSeparator"])
        #time
        self.saveResFile.write(currTime)
        self.saveResFile.write('\n')
        self.saveResFile.flush()

        if self.currTrialN == self.nTrials:
            if self.currBlock < self.n_blocks:
                self.statusButton.setText(self.tr("Run Block"))
            else:
                self.saveResFile.close()
                self.statusButton.setText(self.tr("Finished"))
                dats = pd.read_csv(self.saveResPath, sep=self.prm['pref']["csvSeparator"])
                  
                rms_err = dats.groupby("listener")[["error"]].agg(lambda x: rms_fun(x))
                rms_err_by_block = dats.groupby(["listener", "block"])[["error"]].agg(lambda x: rms_fun(x))
                rms_err_by_cnd = dats.groupby(["listener", "condition"])[["error"]].agg(lambda x: rms_fun(x))
                rms_err_by_cnd_block = dats.groupby(["listener", "condition", "block"])[["error"]].agg(lambda x: rms_fun(x))

                rms_err =  rms_err.rename(columns={"error": "rms_err"})
                rms_err_by_block =  rms_err_by_block.rename(columns={"error": "rms_err"})
                rms_err_by_cnd = rms_err_by_cnd.rename(columns={"error": "rms_err"})
                rms_err_by_cnd_block = rms_err_by_cnd_block.rename(columns={"error": "rms_err"})

                rms_err.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err.csv", sep=";")
                if rms_err_by_block.empty == False:
                    rms_err_by_block.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err_by_block.csv", sep=";")
                if rms_err_by_cnd.empty == False:
                    rms_err_by_cnd.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err_by_cnd.csv", sep=";")
                if rms_err_by_cnd_block.empty == False:
                    rms_err_by_cnd_block.to_csv(self.saveResPath.split(".csv")[0] + "_" + "rms_err_by_cnd_block.csv", sep=";")
                    
        else:
            self.currTrialN = self.currTrialN +1
            self.do_trial()
    
    def onEditPref(self):
        dialog = preferencesDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]
            self.audioManager.initializeAudio()
            
    def onEditTransducers(self):
        dialog = transducersDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            ##if all previously stored transducers have been removed use the first of the new ones
            try:
                currTransducerIdx = self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])
            except:
                currTransducerIdx = 0
            self.prm["pref"]["sound"]["transducers"] = self.prm["transducers"]["transducersChoices"][currTransducerIdx]
            self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]

            self.maxLevel = self.prm["transducers"]["transducersMaxLevel"][self.prm["transducers"]["transducersChoices"].index(self.prm["pref"]["sound"]["transducers"])]

    def onShowManualPdf(self):
        fileToOpen = os.path.abspath(self.prm['rootDirectory']) + '/doc/_build/latex/sound_source_id.pdf'
        print(fileToOpen)
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        
    def onShowModulesDoc(self):
        fileToOpen = os.path.abspath(self.prm['rootDirectory']) + '/doc/_build/html/index.html'
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))

    def createAppShortcut(self):
        from pyshortcuts import make_shortcut
        make_shortcut(script="sound_source_id", name='sound_source_id', icon=os.path.dirname(__file__)+"icons/point-right.ico", terminal=False, executable=None)

    def onAbout(self):
        qt_compiled_ver = QtCore.QT_VERSION_STR
        qt_runtime_ver = QtCore.qVersion()
        qt_pybackend_ver = QtCore.PYQT_VERSION_STR
        qt_pybackend = "PyQt"


        QMessageBox.about(self, self.tr("About sound_source_id"),
                              self.tr("""<b>sound_source_id - Python app for sound localization experiments</b> <br>
                              - version: {0}; <br>
                              - build date: {1} <br>
                              <p> Copyright &copy; 2022-2023 Samuele Carcagno. <a href="mailto:sam.carcagno@gmail.com">sam.carcagno@gmail.com</a> 
                              All rights reserved. <p>
                              This program is free software: you can redistribute it and/or modify
                              it under the terms of the GNU General Public License as published by
                              the Free Software Foundation, either version 3 of the License, or
                              (at your option) any later version.
                              <p>
                              This program is distributed in the hope that it will be useful,
                              but WITHOUT ANY WARRANTY; without even the implied warranty of
                              MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                              GNU General Public License for more details.
                              <p>
                              You should have received a copy of the GNU General Public License
                              along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>
                              <p>Python {2} - {3} {4} compiled against Qt {5}, and running with Qt {6} on {7}""").format(__version__, self.prm['builddate'], platform.python_version(), qt_pybackend, qt_pybackend_ver, qt_compiled_ver, qt_runtime_ver, platform.system()))

            
class responseLight(QWidget):
    def __init__(self, parent, prm):
        super(responseLight, self).__init__(parent)
        # self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
        #                                QSizePolicy.Expanding))
        #self.cw = self.parent().parent() #control window
        self.RL_prm = prm
        self.correctLightColor = QColor(*self.RL_prm["pref"]["correctLightColor"])
        self.incorrectLightColor = QColor(*self.RL_prm["pref"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.RL_prm["pref"]["neutralLightColor"])
        self.offLightColor = QColor(*self.RL_prm["pref"]["offLightColor"])
        
        self.borderColor = Qt.GlobalColor.black
        self.lightColor = self.offLightColor#Qt.black
        self.feedbackText = ""
        self.responseLightType = self.tr("Light & Text") #this is just for inizialization purposes
        self.penColor = QColor(255,255,255) #this is just for inizialization purposes
        

        self.correctSmiley = QIcon.fromTheme("face-smile", QIcon(":/face-smile"))
        self.incorrectSmiley = QIcon.fromTheme("face-sad", QIcon(":/face-sad"))
        self.neutralSmiley = QIcon.fromTheme("face-plain", QIcon(":/face-plain"))
        self.offSmiley = QIcon() #create just a null icon
        self.feedbackSmiley = self.offSmiley
        
    def giveFeedback(self, feedback, feedbackText):
        self.feedbackText = feedbackText
        ##currBlock = 'b'+ str(self.RL_prm['currentBlock'])
        self.responseLightType = self.tr("Light & Text") ##self.parent().self.RL_prm[currBlock]['responseLightType']
        self.setStatus(feedback)
        self.parent().repaint()
        QApplication.processEvents()
        time.sleep(self.RL_prm["pref"]["responseLightDuration"]/1000) ##self.parent().self.RL_prm["pref"]
        self.setStatus('off')
        self.parent().repaint()
        QApplication.processEvents()
        
    def setStatus(self, status):
        self.correctLightColor = QColor(*self.RL_prm["pref"]["correctLightColor"])
        self.incorrectLightColor = QColor(*self.RL_prm["pref"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.RL_prm["pref"]["neutralLightColor"])
        self.offLightColor = QColor(*self.RL_prm["pref"]["offLightColor"])
        if self.responseLightType in [self.tr("Light"), self.tr("Light & Text"), self.tr("Light & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                self.lightColor = self.correctLightColor#Qt.green
            elif status == 'incorrect':
                self.lightColor = self.incorrectLightColor #Qt.red
            elif status == 'neutral':
                self.lightColor = self.neutralLightColor #Qt.white
            elif status == 'off':
                self.lightColor = self.offLightColor #Qt.black
        if self.responseLightType in [self.tr("Text"), self.tr("Light & Text"), self.tr("Text & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                # if self.RL_prm["pref"]["correctTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetCorrectTextFeedback"]
                # else:
                #     self.feedbackText = self.RL_prm['rbTrans'].translate('rb', self.RL_prm["pref"]["correctTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["correctTextColor"])
            elif status == 'incorrect':
                # if self.RL_prm["pref"]["incorrectTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetIncorrectTextFeedback"]
                # else:
                #     self.feedbackText = self.RL_prm['rbTrans'].translate('rb', self.RL_prm["pref"]["incorrectTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["incorrectTextColor"])
            elif status == 'neutral':
                # if self.RL_prm["pref"]["neutralTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetNeutralTextFeedback"]
                # else:
                self.feedbackText = self.tr(self.RL_prm["pref"]["neutralTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["neutralTextColor"])
            elif status == 'off':
                # if self.RL_prm["pref"]["offTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.RL_prm["pref"]["userSetOffTextFeedback"]
                # else:
                self.feedbackText = self.tr(self.RL_prm["pref"]["offTextFeedback"])
                self.penColor = QColor(*self.RL_prm["pref"]["offTextColor"])
        if self.responseLightType in [self.tr("Smiley"), self.tr("Light & Smiley"), self.tr("Text & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                self.feedbackSmiley = self.correctSmiley
            elif status == 'incorrect':
                self.feedbackSmiley = self.incorrectSmiley
            elif status == 'neutral':
                self.feedbackSmiley = self.neutralSmiley
            elif status == 'off':
                self.feedbackSmiley = self.offSmiley
        self.parent().repaint()

    def paintEvent(self, event=None):
        if self.responseLightType == self.tr("Light"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
        elif self.responseLightType == self.tr("Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Light & Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), int(self.width()+self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0,0,self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), int(self.width()+self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), int(self.width()-self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0,0,self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.RL_prm["pref"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)

            
def main():
    
    prm = {}
    prm['appData'] = {}
    # create the GUI application
    qApp = QApplication(sys.argv)
    sys.excepthook = excepthook

    # prm['calledWithWAVFiles'] = False
    # parser = argparse.ArgumentParser()
    
    # parser.add_argument("-f", "--file", help="Load WAV file", nargs='*', default='')
    # args = parser.parse_args()
    # if len(args.file) > 0:
    #     prm['calledWithWAVFiles'] = True
    #     prm['WAVFilesToLoad'] = args.file

    if getattr(sys, "frozen", False):
         # The application is frozen
         prm['rootDirectory'] = os.path.dirname(sys.executable)
    else:
        prm['rootDirectory'] = os.path.dirname(__file__)

    prm = get_prefs(prm)
    prm = global_parameters(prm)
 
    #first read the locale settings
    locale = QtCore.QLocale().system().name() #returns a string such as en_US
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_" + locale, ":/translations/"):
        qApp.installTranslator(qtTranslator)
    appTranslator = QtCore.QTranslator()
    if appTranslator.load("sound_source_id_" + locale, ":/translations/"):
        qApp.installTranslator(appTranslator)
    prm['appData']['currentLocale'] = QtCore.QLocale(locale)
    QtCore.QLocale.setDefault(prm['appData']['currentLocale'])
    
    
    #then load the preferred language
    if prm['pref']['country'] != "System Settings":
        locale =  prm['pref']['language']  + '_' + prm['pref']['country']
        qtTranslator = QtCore.QTranslator()
        if qtTranslator.load("qt_" + locale, ":/translations/"):
            qApp.installTranslator(qtTranslator)
        appTranslator = QtCore.QTranslator()
        if appTranslator.load("sound_source_id_" + locale, ":/translations/") or locale == "en_US":
            qApp.installTranslator(appTranslator)
            prm['appData']['currentLocale'] = QtCore.QLocale(locale)
            QtCore.QLocale.setDefault(prm['appData']['currentLocale'])
            prm['appData']['currentLocale'].setNumberOptions(prm['appData']['currentLocale'].NumberOption.OmitGroupSeparator | prm['appData']['currentLocale'].NumberOption.RejectGroupSeparator)

            
    qApp.setWindowIcon(QIcon(":/point-right"))
    ## Look and feel changed to CleanLooks
    #QApplication.setStyle(QStyleFactory.create("QtCurve"))
    #QApplication.setPalette(QApplication.style().standardPalette())
    #qApp.currentLocale = locale
    # instantiate the ApplicationWindow widget
    qApp.currentLocale = locale
    qApp.setApplicationName('sound_source_id')
    aw = applicationWindow(prm)


    # show the widget
    #aw.show()
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
    sys.exit(qApp.exec())
if __name__ == "__main__":
    main()
   
