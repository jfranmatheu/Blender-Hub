
from PyQt5.QtCore import QSize, QRect, Qt, QPoint, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTabWidget, QWidget

from bhub_button import bHubProjectButton
from bhub_project_widget import bHubProjectWidget
from file_dialog_widget import BlendFileBrowser, FileBrowserMode
from flow_grid_layout import FlowLayout
from icons import Icon
from bhub_io import launch_blender, add_project
from styles import ButtonStyle
from enum import Enum
from os.path import basename


class Section(Enum):
    Projects = "Projects"
    Learn = "Learn"
    Community = "Community"
    Installs = "Installs"

    def __call__(self):
        return self.value


class bHubWindow(QMainWindow):
    left_widget: QWidget
    right_widget: QTabWidget

    def __init__(self, parent=None):
        super().__init__(parent)

        # Projects Section Settings.
        self.items_per_row = 3
        self.must_refresh = False

        # set the title of main window
        self.setWindowTitle("Blender Hub")
        self.setWindowIcon(QIcon(Icon.Icon()))

        # set the size of window
        self.setGeometry(200, 200, 850, 600)  # x, y, w, h

        # opening window in maximized size
        # self.showMaximized()

        # Create buttons.
        self.btn_1 = QPushButton('Projects', self)
        self.btn_1.setIcon(QIcon(Icon.Projects()))
        self.btn_2 = QPushButton('Learn', self)
        self.btn_2.setIcon(QIcon(Icon.Learn()))
        self.btn_3 = QPushButton('Community', self)
        self.btn_3.setIcon(QIcon(Icon.Community()))
        self.btn_4 = QPushButton('Installs', self)
        self.btn_4.setIcon(QIcon(Icon.Installs()))

        # Set icons.
        icon_size = QSize(40, 20)
        self.btn_1.setIconSize(icon_size)
        self.btn_2.setIconSize(icon_size)
        self.btn_3.setIconSize(icon_size)
        self.btn_4.setIconSize(icon_size)

        # Set click events.
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # Active Button. Setting style.
        self.section_name = Section.Projects()
        self.btn_1.setObjectName('sidebar_active')
        self.active_button = self.btn_1
        # self.active_button.setStyleSheet(ButtonStyle.TOGGLE_ON())

        # Set tabs.
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        self.initUI()
        self.show()

    def initUI(self):
        # self.init_menuBar()
        # self.init_statusBar()

        # Setup left widget/layout. (sidebar)
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(15)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        self.left_widget = left_widget

        # Setup right widget/layout.
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        # self.right_widget.setCurrentIndex(0)  # Activate first section.

        # Comentar esto para hacer los tabs encima en vez de sidebar.
        # Debe de estar harcoded.
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        # Setup main widget/layout.
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def init_menuBar(self):
        exitAct = QAction('&Exit', self)  # QIcon('exit.png')
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        menu = self.menuBar()
        fileMenu = menu.addMenu('&File')
        fileMenu.addAction(exitAct)

    def init_statusBar(self):
        self.statusBar().showMessage('Welcome to Blender Hub! :-)')

    # -----------------
    # buttons

    def button1(self):
        if self.update_active_button(self.btn_1):
            self.right_widget.setCurrentIndex(0)

    def button2(self):
        if self.update_active_button(self.btn_2):
            self.right_widget.setCurrentIndex(1)

    def button3(self):
        if self.update_active_button(self.btn_3):
            self.right_widget.setCurrentIndex(2)

    def button4(self):
        if self.update_active_button(self.btn_4):
            self.right_widget.setCurrentIndex(3)

    def update_active_button(self, active):
        # Avoid to refresh when clicking current one.
        if self.active_button == active:
            return False
        self.active_button.setStyleSheet(ButtonStyle.TOGGLE_OFF())
        active.setStyleSheet(ButtonStyle.TOGGLE_ON())
        self.active_button = active
        return True

    # -----------------
    # pages

    # Header
    def draw_header(self):
        #print("Draw header")
        widget = QWidget()
        widget.setObjectName("section_header")
        layout = QHBoxLayout()
        lbl_header = QLabel(self.section_name)
        lbl_header.setObjectName("section_header_label")
        layout.addWidget(lbl_header)
        return widget, layout

    def draw_content(self):
        #print("Draw content")
        # Define content widget and layout.
        content_widget = QWidget()
        content_widget.setObjectName("section_content")
        content_layout = QGridLayout()
        return content_widget, content_layout

    def draw(self, header_widget, header_layout, content_widget, content_layout, scroll_area=False):
        #print("Draw")
        main_layout = QVBoxLayout()

        if scroll_area:
            scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
            widget = QWidget()  # Widget that contains the collection of Vertical Box
            vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        # Set Layouts.
        header_widget.setLayout(header_layout)
        content_widget.setLayout(content_layout)

        main_layout.addWidget(header_widget)

        if scroll_area:
            vbox.addWidget(content_widget)

            vbox.addStretch(5)

            widget.setLayout(vbox)

            # Scroll Area Properties
            scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            scroll.setWidgetResizable(True)
            scroll.setWidget(widget)

            main_layout.addWidget(scroll)
        else:
            # Add widgets to main layout.
            main_layout.addWidget(content_widget)
            main_layout.addStretch(5)

        # Create main widget and set main layout to it.
        main = QWidget()
        main.setObjectName("section_main")
        main.setLayout(main_layout)
        self.main = main

        return self.main

    # Projects Section.
    def ui1(self):
        self.section_name = Section.Projects()
        header_widget, header_layout = self.draw_header()

        self.projects_content_widget = QWidget()
        self.projects_content_widget.setObjectName("section_content")
        self.projects_content_layout = FlowLayout()  # QGridLayout()
        # self.projects_content_widget, self.projects_content_layout = self.draw_content()

        self.draw_projects_header(header_layout)
        self.draw_projects_list()  # content_widget, content_layout)

        return self.draw(header_widget, header_layout, self.projects_content_widget, self.projects_content_layout, True)

    def on_click(self):
        print('PyQt5 button click')

    def add_projects(self):
        print("Open File Browser.")
        BlendFileBrowser(self, FileBrowserMode.OPEN_MULTIPLE)
        print("Close File Browser.")

    def new_project(self):
        # BlendFileBrowser(FileBrowserMode.SAVE)
        name, ok = self.get_text_input()
        if ok:
            if name != '' and not name.endswith('.blend'):
                name += '.blend'
            print("%s project has been created." % name)
            launch_blender(name)

    def get_text_input(self):
        return QInputDialog.getText(self, "New project", "Project name:", QLineEdit.Normal, "")

    def draw_projects_header(self, layout):
        add_button = QPushButton("ADD", self)
        add_button.setObjectName("section_header")
        add_button.clicked.connect(self.add_projects)
        layout.addWidget(add_button)

        add_button = QPushButton("NEW", self)
        add_button.setObjectName("section_header")
        add_button.clicked.connect(self.new_project)
        layout.addWidget(add_button)

    def refresh_projects_list(self):
        self.must_refresh = True

    def redraw_projects_list(self):
        print("Re-Draw projects list")
        count = self.projects_content_layout.count()
        # print("Count Before:", count)
        if count > 1:
            for i in reversed(range(count)):
                # wdg = self.projects_content_layout.itemAt(i).widget()
                # wdg.setParent(None)
                # self.projects_content_layout.removeWidget(wdg)
                # del wdg
                self.projects_content_layout.itemAt(i).widget().deleteLater()
            self.draw_projects_list()
            self.projects_content_widget.update()

            print("Count After:", self.projects_content_layout.count())

    def draw_projects_list(self):  # , content_widget, content_layout):
        print("Draw projects list")
        from bhub_io import projects_list, exists
        if not exists(projects_list):
            return
        import json
        idx = 0
        with open(projects_list, 'r') as file:
            raw_data = file.read()
            if not raw_data or raw_data == '' or raw_data == ' ':
                return
            data = json.loads(raw_data)
            if data is None or data == {}:
                return
            num_cols = 0
            num_rows = 0
            for name, props in data.items():
                self.add_project_box(name, props, num_rows, num_cols)  # content_widget, content_layout,
                num_cols += 1
                if num_cols >= self.items_per_row:
                    num_cols = 0
                    num_rows += 1
                idx += 1

    def add_project_box(self, name, props, col, row):  # , content_widget, content_layout
        box = bHubProjectWidget(self, name, props)  # QGroupBox("My Awesome Project")
        self.projects_content_layout.addWidget(box)  # col, row)

    def ui2(self):
        self.section_name = Section.Learn()
        header_widget, header_layout = self.draw_header()
        content_widget, content_layout = self.draw_content()

        return self.draw(header_widget, header_layout, content_widget, content_layout)

    def ui3(self):
        self.section_name = Section.Community()
        header_widget, header_layout = self.draw_header()
        content_widget, content_layout = self.draw_content()

        return self.draw(header_widget, header_layout, content_widget, content_layout)

    def ui4(self):
        self.section_name = Section.Installs()
        header_widget, header_layout = self.draw_header()
        content_widget, content_layout = self.draw_content()

        self.draw_installs_list(content_layout)

        return self.draw(header_widget, header_layout, content_widget, content_layout)

    def draw_installs_list(self, content_layout):
        box = QWidget()  # QGroupBox("My Awesome Project")
        box.setObjectName("section_item")
        layout = QHBoxLayout()

        buttonBlue = QPushButton('My awesome .blend project', self)
        buttonBlue.clicked.connect(self.on_click)
        layout.addWidget(buttonBlue)

        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(0, 0, 0, 0)

        box.setLayout(layout)
        content_layout.addWidget(box)
