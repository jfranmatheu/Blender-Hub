import shutil

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton
from bhub_io import launch_blender, generate_preview, get_thumbnail_path
from utils import trucate_string


NAME_LENGTH = 12
NAME_LENGTH_2 = 24
NAME_LENGTH_THRESHOLD = 28


class bHubProjectButton(QWidget):
    def __init__(self, parent=None, name="Project", filepath='', index=0):
        QWidget.__init__(self, parent)
        self.parent = parent

        # ALLOW DRAG&DROP
        self.setAcceptDrops(True)

        ##################
        # INIT THUMBNAIL #
        ##################
        self.thumbnail = None
        ok, self.thumbnail_path = get_thumbnail_path(filepath)

        print("Init Button:: filepath:", filepath)
        print("Init Button:: thumbnail:", self.thumbnail_path)

        ##################
        #  INIT BUTTON   #
        ##################
        #self.button = \
        #    QPushButton(name if len(name) < NAME_LENGTH_THRESHOLD
        #                else trucate_string(name, NAME_LENGTH, NAME_LENGTH), self)
        self.button = QPushButton('', self)
        self.button.setObjectName("project")
        self.filepath = filepath = filepath[:-6]
        self.button.clicked.connect(self.open_project)

        if ok:
            self.set_icon(self.thumbnail_path)

        self.index = index

    def set_icon(self, image, external=False):
        if self.thumbnail:
            self.thumbnail.swap(QIcon(image))
        else:
            self.thumbnail = QIcon(image)
        self.button.setIcon(self.thumbnail)
        self.button.setIconSize(QSize(128, 128))
        if external:
            shutil.copyfile(image, self.thumbnail_path)
        # Update widget.
        self.update()


    def open_project(self):
        if launch_blender(self.filepath, True, self):
            self.update_grid()

        '''count = content_layout.count()
        if count > 1:
            # last = content_layout.itemAt(count - 1)
            item = content_layout.itemAt(0).widget  # first
            content_layout.itemAt(0).widget = content_layout.itemAt(count - 1).widget  # first = last
            for i in range(2, count):
                content_layout.itemAt(i - 1).widget = item
                item = content_layout.itemAt(i).widget
            content_widget.update()'''

    def update_grid(self):
        #########################
        # Update projects grid. #
        #########################
        # (Nº parent widget from bHubProjectButton)
        # 1 => QWidget (box)
        # 2 => QWidget (grid) 'section_content'
        # 3 => QWidget (content)
        # 4 => QStackedWidget
        # 5 => tab widget
        # 6 => QWidget
        # 7 => bHubWindow
        # grid_content = self.parentWidget().parentWidget()
        wnd = self.parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget().parentWidget()
        # print(wnd)
        # print(grid_content)
        # print(grid_content.layout())
        wnd.redraw_projects_list()
