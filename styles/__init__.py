from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QApplication
from os.path import pardir, join, dirname
from enum import Enum

#default_style = join(pardir(dirname(__file__)), 'styles')
default_style = join(dirname(__file__), 'light_theme.qss')

def loadStylesheet(filename:str=default_style):
    """
    Loads an qss stylesheet to current QApplication instance

    :param filename: Filename of qss stylesheet
    :type filename: str
    """
    print('STYLE loading:', filename)
    file = QFile(filename)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))


class ButtonStyle(Enum):
    TOGGLE_OFF = """
        QPushButton {
            background-color: transparent;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: transparent;
            font: bold 14px;
            color: #6F7070;
            min-width: 10em;
            padding: 15px;
            text-align:left;
        }
        
        QPushButton:pressed {
            background-color: #AED8F2;
            border-style: inset;
        }
        
        QPushButton:hover:!pressed {
            background-color: #E2E2E3;
        }
    """
    TOGGLE_ON = """
        QPushButton {
            background-color: #AED8F2;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
            border-color: transparent;
            font: bold 14px;
            color: #6F7070;
            min-width: 10em;
            padding: 15px;
            text-align:left;
        }
        
        QPushButton:pressed {
            background-color: #AED8F2;
            border-style: inset;
        }
        
        QPushButton:hover:!pressed {
            background-color: #A0C7DF;
        }
    """

    def __call__(self):
        return self.value
