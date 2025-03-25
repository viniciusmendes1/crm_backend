import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import qtawesome as qta
from modules.users import authenticate_user
from gui.main_window import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(400, 150, 400, 500)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 16px;
                color: #333;
                font-family: Arial, sans-serif;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #ffffff;
                color: #2c3e50;
                font-family: Arial, sans-serif;
            }
            QPushButton {
                padding: 10px;
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #666666;
            }
        """)

        layout = QVBoxLayout()

        # Adicionar logo da empresa
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("images/company_logo.png")
        logo_label.setPixmap(logo_pixmap.scaled(200, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Adicionar título
        title_label = QLabel("Bem-vindo ao CRM")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center; color: #333;")
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        self.username_label = QLabel("Nome de Usuário:")
        form_layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        form_layout.addWidget(self.username_input)

        self.password_label = QLabel("Senha:")
        form_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.setIcon(qta.icon('fa5s.sign-in-alt', color='white'))
        self.login_button.clicked.connect(self.login)
        button_layout.addWidget(self.login_button)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if authenticate_user(username, password):
            QMessageBox.information(self, "Sucesso", "Login realizado com sucesso")
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Erro", "Nome de usuário ou senha incorretos")

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())