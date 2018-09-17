import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QGridLayout, QLabel, QFileDialog, QStatusBar, QMenu, QListWidget, QListWidgetItem, QVBoxLayout, QDockWidget, QCheckBox, QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import os
import os.path
import time


class myFileList(QListWidget):

   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())

class MainWidget(QWidget):

    def __init__(self, parent, path):
        QWidget.__init__(self, parent)
        self.initUI(path)

    def initUI(self,path):
        src = QLabel('Source')
        dest = QLabel('Destination')

        self.srcEdit = QLineEdit()
        selectButton = QPushButton('...', self)
        self.destEdit = QLineEdit()
        selectButton2 = QPushButton('...', self)
        button = QPushButton('Start Copy', self)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(src, 1, 0)
        grid.addWidget(self.srcEdit, 1, 1)
        grid.addWidget(selectButton, 1, 2)

        grid.addWidget(dest, 2, 0)
        grid.addWidget(self.destEdit, 2, 1)
        grid.addWidget(selectButton2, 2, 2)

        grid.addWidget(button, 3, 1)
        self.setLayout(grid)

        self.srcEdit.setText(path)

        button.clicked.connect(self.on_click)
        selectButton.clicked.connect(self.showDirectory)
        selectButton2.clicked.connect(self.showDirectory2)

        self.show()

    @pyqtSlot()
    def on_click(self):
        src = self.srcEdit.text()
        dest = self.destEdit.text()

        button = QMessageBox.question(self, 'Message', "Copy from: " + src + " To " + dest, QMessageBox.Ok,
                             QMessageBox.Cancel)
        if button == QMessageBox.Ok:
            print("Copy file!")
            dest = os.path.join(dest, self.getCurTime())
            if self.copyFiles(src, dest):
                QMessageBox.question(self, 'Message', "Copy completed!", QMessageBox.Ok,
                                    QMessageBox.Ok)
                #self.removeFile(src)
            else:
                QMessageBox.question(self, 'Message', "Copy failed!", QMessageBox.Ok,
                                     QMessageBox.Ok)
    def showDirectory(self):
        dir = QFileDialog.getExistingDirectory(self, 'Open file directory', './')
        self.srcEdit.setText(dir)

    def showDirectory2(self):
        dir2 = QFileDialog.getExistingDirectory(self, 'Open file directory', './')
        self.destEdit.setText(dir2)

    def copyFiles(self, sourceDir, targetDir):
        if sourceDir == '' or targetDir == '':
            QMessageBox.question(self, 'Message', "source or target directory cannot be empty!", QMessageBox.Ok,
                                 QMessageBox.Ok)
            return False
        else:
            for file in os.listdir(sourceDir):
                sourceFile = os.path.join(sourceDir, file)
                targetFile = os.path.join(targetDir, file)
                if os.path.isfile(sourceFile):
                    if not os.path.exists(targetDir):
                        os.makedirs(targetDir)
                    if not os.path.exists(targetFile) or (
                            os.path.exists(targetFile) and (os.path.getsize(targetFile) != os.path.getsize(sourceFile))):
                        open(targetFile, "wb").write(open(sourceFile, "rb").read())
                if os.path.isdir(sourceFile):
                    self.copyFiles(sourceFile, targetFile)

            return True

    def removeFile(self, targetDir):
        for file in os.listdir(targetDir):
            targetFile = os.path.join(targetDir, file)
        if os.path.isfile(targetFile):
            os.remove(targetFile)

    def getCurTime(self):
        return time.strftime("%Y-%m-%d", time.localtime())

class MainWindow(QMainWindow):
    def __init__(self):
        #self.add_hello_context_menu()
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.desktopPath = open("config.txt", "r+").read()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('About')
        aboutAct = QAction('Things about us', self)
        fileMenu.addAction(aboutAct)
        aboutAct.triggered.connect(self.showAbout)
        self.statusBar()

        # Create a widget for tool dock
        # Add some of widgets to listLayout
        listLayout = QVBoxLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)

        # Create and add a widget for showing current label items
        self.labelList = QListWidget()
        labelListContainer = QWidget()
        labelListContainer.setLayout(listLayout)
        listLayout.addWidget(self.labelList)

        self.dock = QDockWidget(u'工具', self)
        self.dock.setObjectName(u'Labels')
        self.dock.setWidget(labelListContainer)

        # create the labelList widget here
        self.labelList = myFileList(self)
        self.populate(self.labelList)

        self.fileListWidget = myFileList(self)
        self.populate(self.fileListWidget)
        filelistLayout = QVBoxLayout()
        filelistLayout.setContentsMargins(0, 0, 0, 0)
        filelistLayout.addWidget(self.fileListWidget)
        fileListContainer = QWidget()
        fileListContainer.setLayout(filelistLayout)
        self.filedock = QDockWidget(u'图片列表', self)
        self.filedock.setObjectName(u'Files')
        self.filedock.setWidget(fileListContainer)

        self.setCentralWidget(self.labelList)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filedock)
        self.dockFeatures = QDockWidget.DockWidgetClosable \
                            | QDockWidget.DockWidgetFloatable
        self.dock.setFeatures(self.dock.features() ^ self.dockFeatures)
        self.filedock.setFeatures(self.filedock.features() ^ self.dockFeatures)

        self.setGeometry(400, 200, 950, 600)
        self.setWindowTitle('Desktop Backup')
        self.statusBar().showMessage("Program started.")

        self.show()

    def populate(self, fileList):
        for file in os.listdir(self.desktopPath):
            print(file)
            myQListWidgetItem = QListWidgetItem(fileList)
            myQListWidgetItem.setText(file)
            fileList.addItem(myQListWidgetItem)

    def showAbout(self):
        self.statusBar().showMessage("About us!!!")
        QMessageBox.question(self, 'About', "emmmmmmmmmmm", QMessageBox.Ok,
                             QMessageBox.Ok)

class MainWindowDirectLoad(QMainWindow):
    def __init__(self):
        #self.add_hello_context_menu()
        super(MainWindowDirectLoad, self).__init__()
        self.initUI()

    def initUI(self):
        self.desktopPath = path = os.path.expanduser("~/Desktop")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('About')
        aboutAct = QAction('Things about us', self)
        fileMenu.addAction(aboutAct)
        aboutAct.triggered.connect(self.showAbout)
        self.statusBar()

        # Create a widget for tool dock
        # Add some of widgets to listLayout
        listLayout = QVBoxLayout()
        listLayout.setContentsMargins(0, 0, 0, 0)

        # Create and add a widget for showing current label items
        self.labelList = QListWidget()
        labelListContainer = QWidget()
        labelListContainer.setLayout(listLayout)
        listLayout.addWidget(self.labelList)

        self.dock = QDockWidget(u'工具', self)
        self.dock.setObjectName(u'Labels')
        self.dock.setWidget(labelListContainer)

        # create the labelList widget here
        self.labelList = myFileList(self)
        self.populate(self.labelList)

        self.fileListWidget = myFileList(self)
        self.populate(self.fileListWidget)
        filelistLayout = QVBoxLayout()
        filelistLayout.setContentsMargins(0, 0, 0, 0)
        filelistLayout.addWidget(self.fileListWidget)
        fileListContainer = QWidget()
        fileListContainer.setLayout(filelistLayout)
        self.filedock = QDockWidget(u'图片列表', self)
        self.filedock.setObjectName(u'Files')
        self.filedock.setWidget(fileListContainer)

        self.setCentralWidget(self.labelList)
        self.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.filedock)
        self.dockFeatures = QDockWidget.DockWidgetClosable \
                            | QDockWidget.DockWidgetFloatable
        self.dock.setFeatures(self.dock.features() ^ self.dockFeatures)
        self.filedock.setFeatures(self.filedock.features() ^ self.dockFeatures)

        self.setGeometry(400, 200, 950, 600)
        self.setWindowTitle('Desktop Backup')
        self.statusBar().showMessage("Program started.")

        self.show()

    def populate(self, fileList):
        for file in os.listdir(self.desktopPath):
            print(file)
            myQListWidgetItem = QListWidgetItem(fileList)
            myQListWidgetItem.setText(file)
            fileList.addItem(myQListWidgetItem)

    def showAbout(self):
        self.statusBar().showMessage("About us!!!")
        QMessageBox.question(self, 'About', "emmmmmmmmmmm", QMessageBox.Ok,
                             QMessageBox.Ok)

class Preview(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.path = None

        src = QLabel('Path')
        self.srcEdit = QLineEdit()
        selectButton = QPushButton('...', self)
        confirmButton = QPushButton('OK', self)

        selectButton.clicked.connect(self.showDirectory)
        confirmButton.clicked.connect(self.on_click)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(src, 1, 0)
        grid.addWidget(self.srcEdit, 1, 1)
        grid.addWidget(selectButton, 1, 2)
        grid.addWidget(confirmButton,2, 1)

        self.setLayout(grid)
        self.setGeometry(500, 300, 550, 200)
        self.setWindowTitle('Please tell me your desktop path')

        self.show()




    @pyqtSlot()
    def on_click(self):
        self.setVisible(False)
        self.path = self.srcEdit.text()

        configFile = open("config.txt", "r+")
        configFile.write(self.path)
        configFile.close()

        self.SW = MainWindow()
        self.SW.show()

    def showDirectory(self):
        dir = QFileDialog.getExistingDirectory(self, 'Open file directory', './')
        self.srcEdit.setText(dir)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # path = ""
    # path = open("config.txt", "r+").read()
    # if path is not "":
    #     ex = MainWindow()
    # else:
    #     ex = Preview()
    ex = MainWindowDirectLoad()
    sys.exit(app.exec_())