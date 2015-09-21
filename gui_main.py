
# -*- coding:utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class TreeItem:
    def __init__(self, data, parent=None):
        self.m_parent_item = parent
        self.m_item_data = data
        self.m_child_items = []

    def append_child(self, item):
        self.m_child_items.append(item)

    def child_count(self):
        return len(self.m_child_items)

    def column_count(self):
        return len(self.m_item_data)

    def child(self, row):
        return self.m_child_items[row]

    def data(self, column):
        try:
            return self.m_item_data[column]
        except IndexError:
            return None

    def parent(self):
        return self.m_parent_item

    def row(self):
        if self.m_parent_item:
            return self.m_parent_item.childItems.index(self)

        return 0


class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.m_root_item = TreeItem(("name", "address", "delay", "lost", "average"))
        self.setup_model_data(data, self.m_root_item)

    def setup_model_data(self, data, parent):
        configs = []
        f = open(data, "r")
        for line in f:
            line = line.decode('utf8')
            if line[0] == '#':
                continue
            a = line.split()
            configs.append(a)
        f.close()

        i = 0
        for config in configs:
            name = config[0]
            address = config[1]
            parent.append_child(TreeItem((name, address, "-", "-", "-"), parent))
            i += 1

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item = self.m_root_item
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()
        parent_item = child_item.parent()

        if parent_item == self.m_root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.m_root_item.column_count()

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self.m_root_item
        else:
            parent_item = parent.internalPointer()

        return parent_item.child_count()

class DataTable(QTreeView):
    def __init__(self, parent=None):
        super(DataTable, self).__init__(parent)

        model = TreeModel("config.txt")
        self.setModel(model)

        return

        self.setColumnCount(5)
        self.setHeaderItem(0, QTreeWidgetItem(self.tr('name')))
        self.setHeaderItem(1, QTreeWidgetItem(self.tr('address')))
        self.setHeaderItem(2, QTreeWidgetItem(self.tr('delay')))
        self.setHeaderItem(3, QTreeWidgetItem(self.tr('lost')))
        self.setHeaderItem(4, QTreeWidgetItem(self.tr('average')))
        self.setShowGrid(False)

        self.configs = []

    def load_data(self, file_name):
        configs = self.configs
        f = open(file_name, "r")
        for line in f:
            line = line.decode('utf8')
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
        #table.load_data("config.txt")
        layout.addWidget(table)

        #button = QPushButton("Quit")
        #button.resize(100, 50)
        #QObject.connect(button, SIGNAL("clicked()"), QtGui.qApp, SLOT("quit()"))
        #layout.addWidget(button)

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

