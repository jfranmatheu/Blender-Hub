from enum import Enum
from os.path import join, dirname

icons_dir = join(dirname(__file__), 'icons')

class Icon(Enum):
    Icon = 'app_icon'
    Projects = 'projects'
    Learn = 'learn'
    Community = 'community'
    Installs = 'installs'

    def __call__(self):
        return join(icons_dir, self.value)
