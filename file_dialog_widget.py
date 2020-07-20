import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from enum import Enum

from bhub_io import add_project


class FileBrowserMode(Enum):
    OPEN = 0
    OPEN_MULTIPLE = 1
    SAVE = 2

class BlendFileBrowser(QWidget):

    def __init__(self, wnd=None, mode=FileBrowserMode.OPEN_MULTIPLE):
        super().__init__()
        self.window = wnd
        self.title = 'File Browser (*.blend)'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI(mode)

    def initUI(self, mode):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        if mode == FileBrowserMode.OPEN:
            self.openFileNameDialog()
        elif FileBrowserMode.OPEN_MULTIPLE:
            self.openFileNamesDialog()
        elif FileBrowserMode.SAVE:
            self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open *.blend file", "",
                                                  "Blender Files (*.blend);;All Files (*)", options=options)
        if fileName:
            # print(fileName)
            # return fileName
            data = add_project(fileName)
            if data:
                self.parent.add_project_box(self.window.projects_content_layout, data[0], data[1], 0)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Open multiple *.blend files", "",
                                                "Blender Files (*.blend);;All Files (*)", options=options)
        if files:
            # print(files)
            # return files
            for file in files:
                # Wait for generation and callback function to update.
                add_project(file, True, self.window.redraw_projects_list)
                #if data:
                #    self.parent.add_project_box(self.parent.content_layout, data[0], data[1], 0)


    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save *.blend file", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)
            return fileName
