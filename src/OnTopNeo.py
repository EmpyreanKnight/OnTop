# -*- coding: utf8 -*-
import win32gui
import win32con
import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class CheckItemModel(QtGui.QStandardItemModel):
    def __init__(self, parent, callback):
        super(CheckItemModel, self).__init__(parent)
        self.itemChanged.connect(self.onItemChanged)
        self.callback = callback

    def addItem(self, title):
        item = QtGui.QStandardItem(title)
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
        item.setData(QtCore.QVariant(QtCore.Qt.Unchecked), QtCore.Qt.CheckStateRole)
        self.appendRow(item)

    def removeItem(self, title):
        for item in self.findItems(title):
            self.removeRow(item.row())

    def check(self, index):
        self.item(index, 0).setData(QtCore.QVariant(QtCore.Qt.Checked), QtCore.Qt.CheckStateRole)

    def setItems(self, titles):
        for i in reversed(range(self.rowCount())):
            self.removeRow(i)
        for title in titles:
            self.addItem(title)

    def onItemChanged(self, item):
        self.callback(item.text(), item.data(QtCore.Qt.CheckStateRole) > 0)


class OnTop(QtWidgets.QWidget):
    def __init__(self):
        super(OnTop, self).__init__()
        self.titles = []   # currently opened window titles
        self.topList = []  # currently on-topped window titles
        self.model = None  # check item model to show titles

        self.initUI()

    # set up UI widgets
    def initUI(self):
        self.setWindowTitle('OnTop Neo')
        self.setWindowIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon))

        refreshButton = QtWidgets.QPushButton('Refresh')
        resetButton = QtWidgets.QPushButton('Reset')
        refreshButton.clicked.connect(self.onRefresh)
        resetButton.clicked.connect(self.onReset)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(refreshButton)
        buttonLayout.addWidget(resetButton)

        # tick-box list of opened windows
        view = QtWidgets.QListView(self)
        self.model = CheckItemModel(self, self.onChanged)
        view.setModel(self.model)
        hLayout = QtWidgets.QHBoxLayout(self)
        hLayout.addWidget(view)
        groupBox = QtWidgets.QGroupBox('Tick a window to on top it.', self)
        groupBox.setLayout(hLayout)

        layout = QtWidgets.QGridLayout(self)
        layout.addLayout(buttonLayout, 0, 0)
        layout.addWidget(groupBox, 1, 0)

        self.onRefresh()
        self.setLayout(layout)
        self.setCenter(800, 600)

    def closeEvent(self, event):
        self.resetAll()

    def onRefresh(self):
        self.titles = self.getTitles()
        self.model.setItems(self.titles)
        self.setOnTopStatus()

    def onReset(self):
        self.resetAll()

    def onChanged(self, title, status):
        self.setTopWindows(title, status)

    # check all top-windows in checklist
    def setOnTopStatus(self):
        for index, text in enumerate(self.titles):
            hwnd = win32gui.FindWindow(None, text)
            if (win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                    & win32con.WS_EX_TOPMOST):
                self.model.check(index)

    def resetAll(self):
        for title in self.topList:
            self.setTopWindows(title, False)

    @staticmethod
    # callback function defined for Win32 API EnumWindows
    # this function append window name to title list
    def enumCallBack(hwnd, titles):
        # skip empty titled, invisible or disabled windows
        if win32gui.GetWindowText(hwnd) != '' \
                and win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            titles.append(win32gui.GetWindowText(hwnd))

    # get all title names of current front windows
    def getTitles(self):
        titles = []
        win32gui.EnumWindows(self.enumCallBack, titles)
        return titles

    # enable/disable a window as top-window by its name
    def setTopWindows(self, title, enable):
        hwnd = win32gui.FindWindow(None, title)
        if not win32gui.IsWindow(hwnd):
            return

        if enable:
            self.topList.append(title)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,
                                  0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        else:
            self.topList.remove(title)
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST,
                                  0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    # call this function before set window visible
    # to place the window at the middle of screen
    def setCenter(self, width, height):
        size = self.rect()
        size.setSize(QtCore.QSize(width, height))
        xCoord = QtWidgets.QApplication.desktop().screen().rect().center().x() - size.center().x()
        yCoord = QtWidgets.QApplication.desktop().screen().rect().center().y() - size.center().y()
        self.setGeometry(xCoord, yCoord, width, height)


# set up the UI style
def setTheme(mainApp):
    mainApp.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    mainApp.setPalette(palette)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    setTheme(app)
    window = OnTop()
    window.show()
    sys.exit(app.exec_())
