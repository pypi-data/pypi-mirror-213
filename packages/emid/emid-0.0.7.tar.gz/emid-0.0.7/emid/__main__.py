#!/usr/bin/python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2022-2023 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of emid

#    emid is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    emid is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with emid.  If not, see <http://www.gnu.org/licenses/>.

import fnmatch, logging, os, random, signal, time, traceback
import numpy as np
import pandas as pd
from emid.pyqtver import*
from emid import qrc_resources
from emid._version_info import*

from emid.audio_manager import*
from emid.global_parameters import*
from emid.dialog_edit_preferences import*
from emid.dialog_edit_phones import*

if pyqtversion == 5:
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtCore import Qt, QEvent, QDate, QDateTime, QTime
    from PyQt5.QtWidgets import QAction, QCheckBox, QComboBox, QDesktopWidget, QDialog, QDialogButtonBox, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QScrollArea, QSizePolicy, QSlider, QSpacerItem, QSplitter, QPushButton, QToolButton, QVBoxLayout, QWhatsThis, QWidget
    from PyQt5.QtGui import QColor, QDesktopServices, QDoubleValidator, QIcon, QPainter, QIntValidator
elif pyqtversion == 6:
    from PyQt6 import QtCore, QtGui
    from PyQt6.QtCore import Qt, QEvent, QDate, QDateTime, QTime
    from PyQt6.QtWidgets import  QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFrame, QFileDialog, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLayout, QLineEdit, QMainWindow, QMessageBox, QScrollArea, QSizePolicy, QSlider, QSpacerItem, QSplitter, QPushButton, QToolButton, QVBoxLayout, QWhatsThis, QWidget
    from PyQt6.QtGui import QAction, QColor, QDesktopServices, QDoubleValidator, QIcon, QPainter, QIntValidator
    
QtCore.Signal = QtCore.pyqtSignal
QtCore.Slot = QtCore.pyqtSlot

signal.signal(signal.SIGINT, signal.SIG_DFL)

local_dir = os.path.expanduser("~") +'/.local/share/data/emid/'
if os.path.exists(local_dir) == False:
    os.makedirs(local_dir)
stderrFile = os.path.expanduser("~") +'/.local/share/data/emid/emid_stderr_log.txt'

logging.basicConfig(filename=stderrFile,level=logging.DEBUG,)

# def excepthook(except_type, except_val, tbck):
#     """ Show errors in message box"""
#     # recover traceback
#     tb = traceback.format_exception(except_type, except_val, tbck)
#     ret = QMessageBox.critical(None, "Critical Error! Something went wrong, the following info may help you troubleshooting",
#                                     ''.join(tb),
#                                     QMessageBox.StandardButton.Ok)
#     timeStamp = ''+ time.strftime("%d/%m/%y %H:%M:%S", time.localtime()) + ' ' + '\n'
#     logMsg = timeStamp + ''.join(tb)
#     logging.debug(logMsg)

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

class mainWin(QMainWindow):
    def __init__(self, prm=None):
        QMainWindow.__init__(self)
        self.prm = prm
        self.currLocale = prm['appData']['currentLocale'] 
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
        self.setGeometry(80, 100, int((1/2)*screen.width()), int((7/10)*screen.height()))
        ##self.main_frame = QFrame()
        self.cw = QFrame()
        self.cw.setFrameStyle(QFrame.Shape.StyledPanel|QFrame.Shadow.Sunken)
        self.main_sizer = QVBoxLayout()
        self.hbox1_sizer = QHBoxLayout()
        self.grid1_sizer = QGridLayout()
        self.setWindowTitle(self.tr("emid"))
        
        self.audioManager = audioManager(self)
        self.sessionRunning = False
        self.listenerID = ""
        self.currentTrialN = 1
        ##self.nTrials = 3

        try:
            self.maxLevel = self.prm["phones"]["phonesMaxLevel"][self.prm["phones"]["phonesChoices"].index(self.prm["pref"]["sound"]["phones"])]
        ##if all previously stored phones have been removed use the first of the new ones
        except:
            self.maxLevel = self.prm["phones"]["phonesMaxLevel"][0]


        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu(self.tr('-'))
        
        self.editPhonesAction = QAction(QIcon.fromTheme("audio-headphones", QIcon(":/audio-headphones")), self.tr('Phones'), self)
        self.fileMenu.addAction(self.editPhonesAction)
        self.editPhonesAction.triggered.connect(self.onEditPhones)
        
        self.editPrefAction = QAction(QIcon.fromTheme("preferences-other", QIcon(":/preferences-other")), self.tr('Preferences'), self)
        self.fileMenu.addAction(self.editPrefAction)
        self.editPrefAction.triggered.connect(self.onEditPref)

        self.onShowManualHtmlAction = QAction(self.tr('Manual (html)'), self)
        self.fileMenu.addAction(self.onShowManualHtmlAction)
        self.onShowManualHtmlAction.triggered.connect(self.onShowManualHtml)

        self.onShowManualPdfAction = QAction(self.tr('Manual (pdf)'), self)
        self.fileMenu.addAction(self.onShowManualPdfAction)
        self.onShowManualPdfAction.triggered.connect(self.onShowManualPdf)

        self.onAboutAction = QAction(QIcon.fromTheme("help-about", QIcon(":/help-about")), self.tr('About emid'), self)
        self.fileMenu.addAction(self.onAboutAction)
        self.onAboutAction.triggered.connect(self.onAbout)

        self.iconButtonWidth = 200
        self.iconButtonHeight = 200
        self.happySmiley = QIcon.fromTheme("oem-face-smiling", QIcon(":/oem-face-smiling"))
        self.sadSmiley = QIcon.fromTheme("oem-face-frowning", QIcon(":/oem-face-frowning"))
        self.neutralSmiley = QIcon.fromTheme("oem-face-neutral", QIcon(":/oem-face-neutral"))
        self.scaredSmiley = QIcon.fromTheme("oem-face-anguished", QIcon(":/oem-face-anguished"))
        self.angrySmiley = QIcon.fromTheme("oem-face-angry", QIcon(":/oem-face-angry"))

        self.setupListenerButton = QPushButton(self.tr("Setup Listener"), self)
        self.setupListenerButton.clicked.connect(self.onClickSetupListenerButton)
        self.setupListenerButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.setupListenerButton.setStyleSheet('font-size: 32pt; font-weight: bold')
        self.hbox1_sizer.addWidget(self.setupListenerButton)
        self.main_sizer.addLayout(self.hbox1_sizer)
        
        self.statusButton = QPushButton(self.tr("Start"), self)
        self.statusButton.clicked.connect(self.onClickStatusButton)
        self.statusButton.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.main_sizer.addWidget(self.statusButton)
        self.statusButton.setStyleSheet('font-size: 32pt; font-weight: bold')
        self.statusButton.hide()
        self.cw.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.main_sizer.addItem(QSpacerItem(-1, 10, QSizePolicy.Policy.Expanding))
        self.sentenceLabel = QLabel("")
        self.sentenceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sentenceLabel.setStyleSheet('font-size: 36pt; font-weight: bold; color: blue')
        self.main_sizer.addWidget(self.sentenceLabel)
        self.main_sizer.addItem(QSpacerItem(-1, 10, QSizePolicy.Policy.Expanding))

        self.responseLight = responseLight(self)
        self.responseLight.setMaximumSize(screen.width(), screen.height())
        self.responseLight.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.main_sizer.addItem(QSpacerItem(-1, 10, QSizePolicy.Policy.Expanding))
        self.main_sizer.addWidget(self.responseLight)
        
        self.responseButton = []
        self.responseButtonLabel = []
        self.nAlternatives = 5
        self.buttonLabels = [self.tr("Happy"), self.tr("Sad"), self.tr("Neutral"), self.tr("Angry"), self.tr("Scared")]
        self.buttonIcons = [self.happySmiley, self.sadSmiley, self.neutralSmiley, self.angrySmiley, self.scaredSmiley]
        for i in range(self.nAlternatives):
            self.responseButton.append(QPushButton(self.tr(""), self))
            self.responseButton[i].setIcon(self.buttonIcons[i])
            self.responseButton[i].setIconSize(QtCore.QSize(self.iconButtonWidth,self.iconButtonHeight))
            self.responseButton[i].clicked.connect(self.sortResponseButton)
            self.responseButton[i].setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
            self.grid1_sizer.addWidget(self.responseButton[i], 0, i)
            self.responseButton[i].setStyleSheet('font-size: 26pt; font-weight: bold')
            self.responseButton[i].setStyleSheet("QPushButton::focus"
                                                 "{"
                                                 "background-color : lightblue;"
                                                 "}"
                                                 )
            self.cw.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.responseButtonLabel.append(QLabel(self.buttonLabels[i]))
            self.responseButtonLabel[i].setStyleSheet('font-size: 26pt; font-weight: bold')
            self.responseButtonLabel[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid1_sizer.addWidget(self.responseButtonLabel[i], 1, i)
            
        self.main_sizer.addLayout(self.grid1_sizer)
      
        self.cw.setLayout(self.main_sizer)
    

        self.setCentralWidget(self.cw)
        self.show()

    def onClickStatusButton(self):
        if self.statusButton.text() == self.tr("Next") and self.responseGiven == False:
            return
        if self.statusButton.text() == self.tr("Finished"):
            return
        if self.statusButton.text() == self.tr("Start"):
            self.nCorrect = 0
            self.sessionRunning = True
            self.statusButton.setText(self.tr("Running"))
            QApplication.processEvents()
        if self.listenerID == "":
            text, ok = QInputDialog.getText(self, "" , self.tr("Listener ID: "))
            if ok:
                self.listenerID = text
                self.statusButton.setText(self.tr("Start"))
            return

        # if self.currentTrialN > 1:
        #     self.storeResponse()
        if self.tr(self.statusButton.text()) == self.tr("Next"):
            self.correctOptionText = self.trialList[(self.currentTrialN-1)].split(';')[2].strip()
            self.storeResponse()
            if self.giveFeedbackOpt == True:
                if self.thisResponseCorrect == "True":
                    self.responseLight.giveFeedback("correct", self.correctOptionText)
                else:
                    self.responseLight.giveFeedback("incorrect", self.correctOptionText)
            self.statusButton.setText(self.tr("Running"))
            QApplication.processEvents()
            
        if self.currentTrialN <= self.nTrials :
            self.doTrial()
        else:
            print("% correct: " + str((self.nCorrect/self.nTrials)*100))
            self.statusButton.setText(self.tr("Finished"))
     
            
    def doTrial(self):
        self.statusButton.setText(self.tr("Running"))
        self.sentenceLabel.setText(self.trialList[(self.currentTrialN-1)].split(';')[1].strip())
        QApplication.processEvents()
        thisFName = self.trialList[(self.currentTrialN-1)].split(';')[0].strip()
        lev = float(self.trialList[(self.currentTrialN-1)].split(';')[3].strip())
        ##print("Playing " + thisFName + " at " + str(lev) + " dB")
        snd, SF, nbits = self.audioManager.loadWavFile(thisFName, lev, self.maxLevel, channel="Original")
        
        rms1 = sqrt(mean(snd[:,0]*snd[:,0]))
        rms2 = sqrt(mean(snd[:,1]*snd[:,1]))
        # print("------------")
        # print(10*log10(rms1))
        # print(10*log10(rms2))
        
        self.trialRunning = True
        time.sleep(self.currLocale.toInt(self.prm['pref']['startDelay'])[0]/1000)
        self.audioManager.playSound(snd, SF, 32, True, "snd_.wav")
        QApplication.processEvents()
        self.trialRunning = False
        self.statusButton.setText(self.tr("Next"))
        self.responseGiven = False
        QApplication.processEvents()

    def storeResponse(self):

        currTime = QTime.toString(QTime.currentTime(), self.currLocale.timeFormat(self.currLocale.ShortFormat)) 
        currDate = QDate.toString(QDate.currentDate(), self.currLocale.dateFormat(self.currLocale.ShortFormat)) 

        #listener
        self.thisPageFile.write(self.listenerID + self.prm['pref']["general"]["csvSeparator"])
        #emotion
        self.thisPageFile.write(self.trialList[(self.currentTrialN-1)].split(';')[2].strip() + self.prm['pref']["general"]["csvSeparator"])
        #response
        self.thisPageFile.write(self.thisResponse + self.prm['pref']["general"]["csvSeparator"])
        #correct
        self.thisPageFile.write(self.thisResponseCorrect + self.prm['pref']["general"]["csvSeparator"])
        #sentence
        self.thisPageFile.write(self.tr(self.trialList[(self.currentTrialN-1)].split(';')[1].strip()) + self.prm['pref']["general"]["csvSeparator"])
        #file
        self.thisPageFile.write(self.tr(self.trialList[(self.currentTrialN-1)].split(';')[0].strip()) + self.prm['pref']["general"]["csvSeparator"])
        #date
        self.thisPageFile.write(currDate + self.prm['pref']["general"]["csvSeparator"])
        #time
        self.thisPageFile.write(currTime)
        self.thisPageFile.write('\n')
        self.thisPageFile.flush()
        self.currentTrialN = self.currentTrialN+1
        

    def onClickSetupListenerButton(self):
        text, ok = QInputDialog.getText(self, "" , self.tr("Listener ID: "))
        if ok:
            self.listenerID = text
        else:
            return
        fName = QFileDialog.getOpenFileName(self, self.tr("Choose trial list file"), '', self.tr("CSV (*.csv *CSV *Csv);;All Files (*)"))[0]
        if len(fName) > 0: #if the user didn't press cancel
            self.trialListFile = fName
            fStream = open(fName, 'r')
            allLines = fStream.readlines()
            if allLines[0].split(":")[1].strip() == "True":
                randomizeTrialList = True
            else:
                randomizeTrialList = False
            if allLines[1].split(":")[1].strip() == "True":
                self.giveFeedbackOpt = True
            else:
                self.giveFeedbackOpt = False
            allLines.pop(0)
            allLines.pop(0)
            self.trialList = allLines
            if randomizeTrialList == True:
                random.shuffle(self.trialList)
            self.nTrials = len(allLines)
            fStream.close()
           
        ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write results'), "", self.tr('CSV (*.csv *CSV *Csv);;All Files (*)'), "")[0]
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.csv') == False:
                ftow = ftow + '.csv'
            self.thisPagePath = ftow #file where results are saved
            self.thisPageDir = os.path.dirname(str(ftow)) + '/' #directory where results are saved
            self.thisPageFile = open(self.thisPagePath, "w")
            self.thisPageFile.write("listener" + self.prm['pref']['general']['csvSeparator'] +
                                    "emotion" + self.prm['pref']['general']['csvSeparator'] +
                                    "response" + self.prm['pref']['general']['csvSeparator'] +
                                    "correct" + self.prm['pref']['general']['csvSeparator'] +
                                    "sentence" + self.prm['pref']['general']['csvSeparator'] +
                                    "sound_file" + self.prm['pref']['general']['csvSeparator'] +
                                    "date" + self.prm['pref']['general']['csvSeparator'] +
                                    "time\n")

            self.setupListenerButton.hide()
            self.statusButton.show()
        else:
            return

    def sortResponseButton(self):
        try:
            buttonClicked = self.responseButton.index(self.sender())+1
        except:
            buttonClicked = 0

        self.sortResponse(buttonClicked)

    def sortResponse(self, buttonClicked):
        if self.statusButton.text() not in [self.tr("Running"), self.tr("Next")]:
            return
        if self.trialRunning == True:
            print("Trial running, discarding response")
            return

        ##print(self.tr(self.buttonLabels[(buttonClicked-1)]))
        ##print(self.trialList[(self.currentTrialN-1)].split(';')[2].strip())
        self.thisResponse = self.tr(self.buttonLabels[(buttonClicked-1)])
        self.responseGiven = True
        if self.tr(self.buttonLabels[(buttonClicked-1)]) == self.trialList[(self.currentTrialN-1)].split(';')[2].strip():
            self.thisResponseCorrect = "True"
            self.nCorrect = self.nCorrect + 1
        else:
            self.thisResponseCorrect = "False"

    def onEditPref(self):
        dialog = preferencesDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            self.audioManager.initializeAudio()
            self.maxLevel = self.prm["phones"]["phonesMaxLevel"][self.prm["phones"]["phonesChoices"].index(self.prm["pref"]["sound"]["phones"])]
    def onEditPhones(self):
        dialog = phonesDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            ##if all previously stored phones have been removed use the first of the new ones
            try:
                currPhoneIdx = self.prm["phones"]["phonesChoices"].index(self.prm["pref"]["sound"]["phones"])
            except:
                currPhoneIdx = 0
            self.prm["pref"]["sound"]["phones"] = self.prm["phones"]["phonesChoices"][currPhoneIdx]
            self.prm["phones"]["phonesMaxLevel"][self.prm["phones"]["phonesChoices"].index(self.prm["pref"]["sound"]["phones"])]

    def onShowManualPdf(self):
        fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/latex/emid.pdf'
        print(fileToOpen)
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))
        
    def onShowManualHtml(self):
        fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/html/index.html'
        QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))

    def onAbout(self):
        qt_compiled_ver = QtCore.QT_VERSION_STR
        qt_runtime_ver = QtCore.qVersion()
        qt_pybackend_ver = QtCore.PYQT_VERSION_STR
        qt_pybackend = "PyQt"


        QMessageBox.about(self, self.tr("About emid"),
                              self.tr("""<b>emid - Python app for sound localization experiments</b> <br>
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
                              <p>Python {2} - {3} {4} compiled against Qt {5}, and running with Qt {6} on {7}""").format(emid_version, emid_builddate, platform.python_version(), qt_pybackend, qt_pybackend_ver, qt_compiled_ver, qt_runtime_ver, platform.system()))




class responseLight(QWidget):
    def __init__(self, parent):
        super(responseLight, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding,
                                       QSizePolicy.Policy.Expanding))
        self.correctLightColor = QColor(*self.parent().prm["pref"]["appearance"]["correctLightColor"]) #* explode tuple
        self.incorrectLightColor = QColor(*self.parent().prm["pref"]["appearance"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.parent().prm["pref"]["appearance"]["neutralLightColor"])
        self.offLightColor = QColor(*self.parent().prm["pref"]["appearance"]["offLightColor"])
        
        self.borderColor = Qt.GlobalColor.black
        self.lightColor = self.offLightColor#Qt.black
        self.feedbackText = ""
        self.responseLightType = self.tr("Light & Text") #this is just for inizialization purposes
        self.penColor = QColor(255,255,255) #this is just for inizialization purposes
        self.cw = self.parent() #control window

        self.correctSmiley = QIcon.fromTheme("face-smile", QIcon(":/face-smile"))
        self.incorrectSmiley = QIcon.fromTheme("face-sad", QIcon(":/face-sad"))
        self.neutralSmiley = QIcon.fromTheme("face-plain", QIcon(":/face-plain"))
        self.offSmiley = QIcon() #create just a null icon
        self.feedbackSmiley = self.offSmiley
        
    def giveFeedback(self, feedback, feedbackText):
        self.feedbackText = feedbackText
        ##currBlock = 'b'+ str(self.parent().prm['currentBlock'])
        self.responseLightType = self.tr("Light & Text") ##self.parent().prm[currBlock]['responseLightType']
        self.setStatus(feedback)
        self.parent().repaint()
        QApplication.processEvents()
        time.sleep(self.parent().parent().prm["pref"]["general"]["responseLightDuration"]/1000) ##self.parent().prm["pref"]
        self.setStatus('off')
        self.parent().repaint()
        QApplication.processEvents()
        
    def setStatus(self, status):
        self.correctLightColor = QColor(*self.cw.prm["pref"]["appearance"]["correctLightColor"])
        self.incorrectLightColor = QColor(*self.cw.prm["pref"]["appearance"]["incorrectLightColor"])
        self.neutralLightColor = QColor(*self.cw.prm["pref"]["appearance"]["neutralLightColor"])
        self.offLightColor = QColor(*self.cw.prm["pref"]["appearance"]["offLightColor"])
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
                # if self.cw.prm["pref"]["appearance"]["correctTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.cw.prm["pref"]["appearance"]["userSetCorrectTextFeedback"]
                # else:
                #     self.feedbackText = self.cw.prm['rbTrans'].translate('rb', self.cw.prm["pref"]["appearance"]["correctTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["appearance"]["correctTextColor"])
            elif status == 'incorrect':
                # if self.cw.prm["pref"]["appearance"]["incorrectTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.cw.prm["pref"]["appearance"]["userSetIncorrectTextFeedback"]
                # else:
                #     self.feedbackText = self.cw.prm['rbTrans'].translate('rb', self.cw.prm["pref"]["appearance"]["incorrectTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["appearance"]["incorrectTextColor"])
            elif status == 'neutral':
                # if self.cw.prm["pref"]["appearance"]["neutralTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.cw.prm["pref"]["appearance"]["userSetNeutralTextFeedback"]
                # else:
                self.feedbackText = self.tr(self.cw.prm["pref"]["appearance"]["neutralTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["appearance"]["neutralTextColor"])
            elif status == 'off':
                # if self.cw.prm["pref"]["appearance"]["offTextFeedbackUserSet"] == True:
                #     self.feedbackText = self.cw.prm["pref"]["appearance"]["userSetOffTextFeedback"]
                # else:
                self.feedbackText = self.tr(self.cw.prm["pref"]["appearance"]["offTextFeedback"])
                self.penColor = QColor(*self.cw.prm["pref"]["appearance"]["offTextColor"])
        if self.responseLightType in [self.tr("Smiley"), self.tr("Light & Smiley"), self.tr("Text & Smiley"), self.tr("Light & Text & Smiley")]:
            if status == 'correct':
                self.feedbackSmiley = self.correctSmiley
            elif status == 'incorrect':
                self.feedbackSmiley = self.incorrectSmiley
            elif status == 'neutral':
                self.feedbackSmiley = self.neutralSmiley
            elif status == 'off':
                self.feedbackSmiley = self.offSmiley

    def paintEvent(self, event=None):
        if self.responseLightType == self.tr("Light"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
        elif self.responseLightType == self.tr("Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["appearance"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Light & Text"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setPen(self.borderColor)
            painter.setBrush(self.lightColor)
            painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            r = QtCore.QRectF(0,0,self.width(),self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["appearance"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rect = QRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            self.feedbackSmiley.paint(painter, rect, Qt.AlignmentFlag.AlignCenter)
        elif self.responseLightType == self.tr("Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.offLightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), self.width()+int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0,0,self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["appearance"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)
        elif self.responseLightType == self.tr("Light & Text & Smiley"):
            painter = QPainter(self)
            painter.setViewport(0,0,self.width(),self.height())
            painter.setBrush(self.lightColor)
            rect = painter.drawRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/30), self.height())
            rectRight = QRect(int(self.width()/60), int(self.height()/60), self.width()+int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectRight, Qt.AlignmentFlag.AlignCenter)
            rectLeft = QRect(int(self.width()/60), int(self.height()/60), self.width()-int(self.width()/2), self.height())
            self.feedbackSmiley.paint(painter, rectLeft, Qt.AlignmentFlag.AlignCenter)
            r = QtCore.QRectF(0,0,self.width(), self.height())
            painter.setPen(self.penColor)
            qfont = QFont()
            qfont.fromString(self.cw.prm["pref"]["appearance"]["responseLightFont"])
            painter.setFont(qfont)
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.feedbackText)



    
def main():
    prm = {}
    prm['appData'] = {}
    prm = get_prefs(prm)
    prm = set_global_parameters(prm)
    qApp = QApplication(sys.argv)
    sys.excepthook = excepthook
    #qApp.setWindowIcon(QtGui.QIcon(":/app_icon"))
 

    #first read the locale settings
    locale = QtCore.QLocale().system().name() #returns a string such as en_US
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_" + locale, ":/translations/"):
        qApp.installTranslator(qtTranslator)
    appTranslator = QtCore.QTranslator()
    if appTranslator.load("emid_" + locale, ":/translations/"):
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
        if appTranslator.load("emid_" + locale, ":/translations/") or locale == "en_US":
            qApp.installTranslator(appTranslator)
            prm['appData']['currentLocale'] = QtCore.QLocale(locale)
            QtCore.QLocale.setDefault(prm['appData']['currentLocale'])
            prm['appData']['currentLocale'].setNumberOptions(prm['appData']['currentLocale'].NumberOption.OmitGroupSeparator | prm['appData']['currentLocale'].NumberOption.RejectGroupSeparator)


    qApp.setWindowIcon(QIcon(":/oem-face-neutral"))
    ## Look and feel changed to CleanLooks
    #QApplication.setStyle(QStyleFactory.create("QtCurve"))
    ##QApplication.setPalette(QApplication.style().standardPalette())
    qApp.currentLocale = locale
    # instantiate the ApplicationWindow widget
    qApp.setApplicationName('emid')
    #qApp.setStyle('Breeze')
    x = mainWin(prm=prm)
    sys.exit(qApp.exec())

if __name__ == "__main__":
    main()
