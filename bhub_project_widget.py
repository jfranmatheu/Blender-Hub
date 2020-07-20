import shutil

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QBoxLayout, QGroupBox, QPushButton, QFrame

from bhub_button import bHubProjectButton, NAME_LENGTH_THRESHOLD, NAME_LENGTH
from bhub_io import launch_blender, get_thumbnail_path
from utils import trucate_string


class bHubProjectWidget(QFrame):

    def __init__(self, window=None, name='My Project', props={}):
        super().__init__()
        self.setObjectName("project")
        # self.parent = parent  # content_widget/layout
        self.window = window
        self.name = name
        self.props = props
        self.file_path = self.props['file_path']
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)

        ##################
        # INIT THUMBNAIL #
        ##################
        self.setAcceptDrops(True)
        self.thumbnail = None

        ok, self.thumbnail_path = get_thumbnail_path(self.file_path)

        print("Init Button:: file_path:", self.file_path)
        print("Init Button:: thumbnail_path:", self.thumbnail_path)

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        self.button = QPushButton()
        self.button.setObjectName("project")
        self.button.clicked.connect(self.open_project)
        if self.thumbnail_path:
            self.thumbnail = QIcon(self.thumbnail_path)
            self.button.setIcon(self.thumbnail)
            self.button.setIconSize(QSize(128, 128))
        vbox.addWidget(self.button)

        label = QLabel(self.name if len(self.name) < NAME_LENGTH_THRESHOLD else
                       trucate_string(self.name, NAME_LENGTH, NAME_LENGTH))
        label.setObjectName("project")
        vbox.addWidget(label)

        self.setLayout(vbox)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            print("Drop Image:", file_path)
            # self.set_icon(file_path, True)
            if file_path:
                # self.button_widget.set_icon(file_path, True)
                if self.thumbnail:
                    self.thumbnail.swap(QIcon(file_path))
                else:
                    self.thumbnail = QIcon(file_path)
                self.button.setIcon(self.thumbnail)
                shutil.copyfile(file_path, self.thumbnail_path)

    def open_project(self):
        if launch_blender(self.file_path, True):
            self.update_grid()

    def update_grid(self):
        # scroll_area = self.parentWidget().parentWidget().parentWidget().parentWidget()
        # wnd = widget.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        # wnd.redraw_projects_list()
        self.window.redraw_projects_list()
