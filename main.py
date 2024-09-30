from application import Application
import sys
import sys
from PySide6.QtWidgets import QApplication

#sys.exit(app.exec())


def main():
    win = Application()

    win.load_config() 
    win.setup()
    win.start()
    win.save_config()

if __name__ == "__main__":
    main()
