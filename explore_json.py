import argparse
import json
import os
import sys
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QAction, QApplication, QLabel, QLineEdit,
                               QMainWindow, QPushButton, QTreeWidget, QTreeWidgetItem,
                               QVBoxLayout, QWidget, QHeaderView)


class JsonTreeWidget(QTreeWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data

        self.setColumnCount(2)
        self.setHeaderLabels(['path', 'value'])
        # self.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # self.header().setStretchLastSection(False)

        self.add_object(data)
        self.expandAll()

    def add_object(self, obj, parent=None):
        if parent is None:
            parent = self

        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (list, dict)):
                    item = QTreeWidgetItem(parent, [k])
                    self.add_object(v, item)
                else:
                    # TODO Fix label so it works for numbers rather than just str(v)
                    item = QTreeWidgetItem(parent, [k, str(v)])
        elif isinstance(obj, list):
            for index, element in enumerate(obj):
                if isinstance(element, (list, dict)):
                    item = QTreeWidgetItem(parent, [str(index)])
                    self.add_object(element, item)
                else:
                    item = QTreeWidgetItem(parent, [str(index), str(element)])
        else:
            item = QTreeWidgetItem(parent, [str(obj)])
            raise ValueError("Tree add_object expects a collection")


class ExplorerWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        self.tree = JsonTreeWidget(data)

        self.quit = QPushButton("Quit")
        self.search_box = QLineEdit()

        # QWidget Layout
        self.layout = QVBoxLayout()
        self.layout.setMargin(10)
        self.layout.addWidget(QLabel("Search"))
        self.layout.addWidget(self.search_box)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.quit)

        # Set the layout to the QWidget
        self.setLayout(self.layout)

        # Signals and Slots
        self.quit.clicked.connect(self.quit_application)
        self.search_box.textChanged[str].connect(self.update_search)

    @Slot()
    def update_search(self, s):
        print(s)

    @Slot()
    def quit_application(self):
        QApplication.quit()


class ExplorerWindow(QMainWindow):
    def __init__(self, filename):
        super().__init__()
        self.setWindowTitle("Json Explorer")

        # Menu
        self.menu = self.menuBar()
        self.menu.setNativeMenuBar(False)
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.exit_app)

        self.file_menu.addAction(exit_action)
        filename = os.path.expanduser(filename)
        try:
            with open(filename) as data_file:
                widget_data = json.load(data_file)
        except json.JSONDecodeError:
            print("Invalid json")
            self.exit_app()
        except OSError:
            print("Couldn't open file: {}".format(filename))
            self.exit_app()
        widget = ExplorerWidget(widget_data)
        self.setCentralWidget(widget)

    @Slot()
    def exit_app(self):
        QApplication.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Explore a json object')
    parser.add_argument('file', metavar='JSON_FILE', nargs='?')

    args = parser.parse_args(['./sample.json'])

    app = QApplication([])
    window = ExplorerWindow(args.file)
    window.resize(1000, 800)
    window.show()

    sys.exit(app.exec_())
