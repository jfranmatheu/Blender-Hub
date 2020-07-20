from PyQt5.QtWidgets import QApplication
import sys
from bhub_window import bHubWindow
from checking import check_folders, check_projects, load_style

if __name__ == "__main__":
    print("Starting Blender Hub...")
    check_folders()
    #check_projects()

    app = QApplication(sys.argv)
    win = bHubWindow()

    # Load Style.
    load_style()

    sys.exit(app.exec())
