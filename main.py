from PyQt5.QtGui import QIntValidator

from SerialTools import readSerialNew
from PyQt5.uic import loadUi
from PyQt5.QtCore import QObject, QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
)
import time

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)
        self.type = ""
        self.port = ""
        self.baud = ""
        self.destination = ""
        self.sectionSize = ""
        self.testLimiter = ""
        self.count = 0

    Tfinished = pyqtSignal()

    def init(self, Limitertype, port, baud, destination, sectionSize, testLimiter):
        print("init")
        self.type = Limitertype
        self.port = port
        self.baud = baud
        self.destination = destination
        self.sectionSize = sectionSize
        self.testLimiter = testLimiter
        self.tag = ""

        loadUi("files/TestWindow.ui", self)
        self.setWindowTitle(f"Test section {self.count + 1}")
        self.TestStartButton.clicked.connect(self.getData)
        self.TagLineEdit.setPlaceholderText(f"insert tag {self.count + 1}")
        self.show()

    def getData(self):
        #print("sleeping...")
        #time.sleep(5)
        self.tag = self.TagLineEdit.text()
        readSerialNew(self.type, self.port, self.baud, self.destination, self.tag, self.testLimiter)


        self.count = self.count + 1
        self.setWindowTitle(f"Test section {self.count + 1}")
        self.TagLineEdit.setText("")
        self.TagLineEdit.setPlaceholderText(f"insert tag {self.count + 1}")
        if self.count >= int(self.sectionSize):
            self.Tfinished.emit()
            self.close()

class Worker(QObject):
    finished = pyqtSignal()

    def run(self, type, port, baud, destination, sectionSize, testLimiter):

        try:
            print("in")
            self.dialog = TestWindow()
            self.dialog.init(type, port, baud, destination, sectionSize, testLimiter)
            self.dialog.Tfinished.connect(self.finished.emit)
        except Exception as ex:
            print(ex)

        print("type: ")
        print(type)
        print("port: ")
        print(port)
        print("baud: ")
        print(baud)
        print("destination: ")
        print(destination)
        print("sectionSize: ")
        print(sectionSize)
        print("testLimiter: ")
        print(testLimiter)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.sampleMode = "time"

    def initUI(self):
        loadUi("files/MainWindow.ui", self)
        self.setWindowTitle("IR Grid")
        self.TestLimiterLineEdit.setPlaceholderText("...")
        self.TestLimiterLineEdit.setValidator(QIntValidator(1, 99999, self))
        self.TestSectionsLineEdit.setPlaceholderText("...")
        self.TestSectionsLineEdit.setValidator(QIntValidator(1, 99999, self))
        self.DirectoryLineEdit.setPlaceholderText("...")
        self.SaveButton.clicked.connect(self.chooseDir)
        self.SampleModeComboBox.currentIndexChanged.connect(self.changeMode)
        self.StartButton.clicked.connect(lambda: self.execute(self.sampleMode))
        self.show()

    def chooseDir(self):
        response = QFileDialog.getExistingDirectory(self, caption='Select a folder')
        self.DirectoryLineEdit.setText(response)

    def changeMode(self):
        item = self.SampleModeComboBox.currentText()
        if item == "Sample for time":
            self.TestLimiterLabel.setText("Test section duration (in seconds)")
            self.sampleMode = "time"
        elif item == "Fixed sample number":
            self.TestLimiterLabel.setText("Number of samples")
            self.sampleMode = "number"
        else:
            pass

    def execute(self, mode):
        port = self.PortLineEdit.text()
        baud = self.BaudComboBox.currentText()
        destination = self.DirectoryLineEdit.text()
        sectionSize = self.TestSectionsLineEdit.text()
        testLimiter = self.TestLimiterLineEdit.text()

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(lambda: self.worker.run(mode, port, baud, destination, sectionSize, testLimiter))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(lambda: self.PortLineEdit.setEnabled(True))
        self.worker.finished.connect(lambda: self.BaudComboBox.setEnabled(True))
        self.worker.finished.connect(lambda: self.TestSectionsLineEdit.setEnabled(True))
        self.worker.finished.connect(lambda: self.SampleModeComboBox.setEnabled(True))
        self.worker.finished.connect(lambda: self.TestLimiterLineEdit.setEnabled(True))
        self.worker.finished.connect(lambda: self.SaveButton.setEnabled(True))
        self.worker.finished.connect(lambda: self.DirectoryLineEdit.setEnabled(True))
        self.worker.finished.connect(lambda: self.StartButton.setEnabled(True))

        if port != "" and baud != "" and destination != "" and sectionSize != "" and testLimiter != "":
            self.thread.start()
            self.PortLineEdit.setEnabled(False)
            self.BaudComboBox.setEnabled(False)
            self.TestSectionsLineEdit.setEnabled(False)
            self.SampleModeComboBox.setEnabled(False)
            self.TestLimiterLineEdit.setEnabled(False)
            self.SaveButton.setEnabled(False)
            self.DirectoryLineEdit.setEnabled(False)
            self.StartButton.setEnabled(False)
        else:
            print("INVALID")



app = QApplication([])
window = MainWindow()
app.exec_()