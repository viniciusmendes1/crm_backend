import sys
from PyQt5.QtWidgets import QApplication
from gui.login_window import LoginWindow


def main():
    app = QApplication(sys.argv)

    with open("gui/style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())

    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()