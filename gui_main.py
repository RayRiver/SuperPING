
# -*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class DataTable(QTableWidget):
    def __init__(self, parent=None):
        super(DataTable, self).__init__(parent)
        self.setColumnCount(5)
        self.setRowHeight(10, 10)
        self.setHorizontalHeaderItem(0, QTableWidgetItem(QString(u'名字')))
        self.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr('address')))
        self.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr('delay')))
        self.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr('lost')))
        self.setHorizontalHeaderItem(4, QTableWidgetItem(self.tr('average')))
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)

        self.configs = []

    def load_data(self, file_name):
        configs = self.configs
        f = open(file_name, "r")
        for line in f:
            if line[0] == '#':
                continue
            a = line.split()
            configs.append(a)
        f.close()

        i = 0
        for config in configs:
            name = config[0]
            address = config[1]
            self.insertRow(i)
            self.setItem(i, 0, QTableWidgetItem(QString(name)))
            self.setItem(i, 1, QTableWidgetItem(address))
            self.setItem(i, 2, QTableWidgetItem(self.tr("-")))
            self.setItem(i, 3, QTableWidgetItem(self.tr("-")))
            self.setItem(i, 4, QTableWidgetItem(self.tr("-")))
            i += 1


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        self.create_actions()
        self.create_status_bar()
        self.create_menu_bar()

        layout = self.create_center_widget()

        table = DataTable()
        table.load_data("config.txt")
        layout.addWidget(table)

        button = QPushButton("Quit")
        button.resize(100, 50)
        QObject.connect(button, SIGNAL("clicked()"), QtGui.qApp, SLOT("quit()"))
        layout.addWidget(button)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("title")

    def create_center_widget(self):
        center_widget = QWidget()
        layout = QVBoxLayout()
        center_widget.setLayout(layout)
        self.setCentralWidget(center_widget)
        return layout

    def create_actions(self):
        self.new_action = QAction(self.tr('&New'), self)
        self.connect(self.new_action, SIGNAL("triggered()"), QtGui.qApp.quit)

        self.quit_action = QAction(self.tr('&Quit'), self)
        self.connect(self.quit_action, SIGNAL("triggered()"), QtGui.qApp.quit)

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu(self.tr('&File'))
        file_menu.addAction(self.new_action)
        if sys.platform != "darwin":
            file_menu.addAction(self.quit_action)

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

