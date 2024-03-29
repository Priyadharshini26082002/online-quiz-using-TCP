from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import socket
import sip
import time
import os

FORMAT = 'utf-8'
WAIT_TIME = 30

sys.path.append(os.path.normpath("../socket/"))
from client import *

class Ui_MainWindow1(object):
    response = ""
    client = ""
    elapsed_time = 0
    start_time = 0
    index = 1
    def setupUi_1(self,MainWindow,ques,options,client,ui):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(580,319)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 10, 321, 41))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(40, 10, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 20, 20))
        self.label_2.setStyleSheet("background-color: rgb(0, 255, 0)")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(190, 10, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(130, 70, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(80, 110, 99, 21))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(80, 140, 99, 21))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_3.setGeometry(QtCore.QRect(80, 170, 99, 21))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_4.setGeometry(QtCore.QRect(80, 200, 99, 21))
        self.radioButton_4.setObjectName("radioButton_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 242, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(380, 240, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(440, 20, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 580, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # print(ques, options)
        self.retranslateUi(MainWindow,ques,options)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.client = client
        self.elapsed_time = 0

        # start time
        self.start_time = time.time()

        # a timer to update the timer label
        timer = QtCore.QTimer(MainWindow)
        timer.timeout.connect(lambda: self.updateTimer(client,ui,MainWindow,timer))
        timer.start(1000)

        self.pushButton.clicked.connect(lambda: self.onSubmit(client,ui,MainWindow,timer))

    def updateTimer(self,client,ui,MainWindow,timer):
        self.elapsed_time = self.elapsed_time + 1
        curr_time = WAIT_TIME - self.elapsed_time
        timer_txt = "Time Left: "+str(curr_time)
        self.label_6.setText(timer_txt)
        if(curr_time == 0):
            self.elapsed_time = 0
            self.onSubmit(client,ui,MainWindow,timer)

    def updateQuestionIndex(self):
        question_index = self.label_3.text()
        question_index = question_index.split(" ")[1].split(":")[0]
        question_index = int(question_index) + self.index
        self.index = self.index + 1
        self.label_3.setText("Question "+str(question_index)+":")

    def onSubmit(self,client,ui,MainWindow,timer):
        timer.stop()
        end_time = time.time()
        self.disableButtons()
        response = "e"
        if(self.radioButton.isChecked() == True):
            response = "a"
        elif(self.radioButton_2.isChecked() == True):
            response = "b"
        elif(self.radioButton_3.isChecked() == True):
            response = "c"
        elif(self.radioButton_4.isChecked() == True):
            response = "d"

        print(response)
        # time.sleep(1)
        client.send(response.encode(FORMAT))

        # get end time and send to server
        duration = end_time - self.start_time
        duration_str = str(duration)
        time.sleep(0.5)
        client.send(duration_str.encode(FORMAT))

        # call the receive message defined in the client code
        recvMessageF(client,ui,MainWindow)

    def disableButtons(self):
        self.radioButton.setEnabled(False)
        self.radioButton_2.setEnabled(False)
        self.radioButton_3.setEnabled(False)
        self.radioButton_4.setEnabled(False)
        self.pushButton.setEnabled(False)

    def retranslateUi(self, MainWindow,ques,options):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Status: Connected"))
        self.label_7.setText(_translate("MainWindow", SERVER))
        self.label_3.setText(_translate("MainWindow", "Question 1:"))

        # Wrap the word - manually
        ques_words = ques.split(" ")
        print(ques)
        if(len(ques_words) > 8):
            ques = ' '.join(map(str, ques_words[:8])) + "\n" + ' '.join(map(str, ques_words[8:])) +"\n"
            self.radioButton.setStyleSheet("padding:15px")
            self.radioButton_2.setStyleSheet("padding:15px")
            self.radioButton_3.setStyleSheet("padding:15px")
            self.radioButton_4.setStyleSheet("padding:15px")

            
        self.label_4.setText(_translate("MainWindow", ques))
        self.radioButton.setText(_translate("MainWindow", options[0]))
        self.radioButton_2.setText(_translate("MainWindow", options[1]))
        self.radioButton_3.setText(_translate("MainWindow", options[2]))
        self.radioButton_4.setText(_translate("MainWindow", options[3]))
        self.pushButton.setText(_translate("MainWindow", "Submit"))
        self.label_5.setText(_translate("MainWindow", ""))
        self.label_6.setText(_translate("MainWindow", "Time Left: 30:00"))

        # MainWindow.adjustSize()
        self.label.adjustSize()
        self.label_3.adjustSize()
        self.label_4.adjustSize()
        self.radioButton.adjustSize()
        self.radioButton_2.adjustSize()
        self.radioButton_3.adjustSize()
        self.radioButton_4.adjustSize()
