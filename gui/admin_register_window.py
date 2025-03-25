import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QWidget, QMessageBox
from modules.users import register_user, generate_activation_key, get_activation_keys


class AdminRegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerenciamento de Usuários e Chaves de Ativação")
        self.setGeometry(400, 150, 600, 400)

        layout = QVBoxLayout()

        title_label = QLabel("Gerenciamento de Usuários e Chaves de Ativação")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(title_label)

        form_layout = QVBoxLayout()

        self.username_label = QLabel("Nome de Usuário:")
        form_layout.addWidget(self.username_label)

        self.username_input = QLineEdit()
        form_layout.addWidget(self.username_input)

        self.password_label = QLabel("Senha:")
        form_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        form_layout.addWidget(self.password_input)

        self.activation_key_label = QLabel("Chave de Ativação:")
        form_layout.addWidget(self.activation_key_label)

        self.activation_key_input = QLineEdit()
        form_layout.addWidget(self.activation_key_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.register_button = QPushButton("Registrar Usuário")
        self.register_button.clicked.connect(self.register_user)
        button_layout.addWidget(self.register_button)

        self.generate_key_button = QPushButton("Gerar Chave de Ativação")
        self.generate_key_button.clicked.connect(self.generate_activation_key)
        button_layout.addWidget(self.generate_key_button)

        self.view_keys_button = QPushButton("Ver Chaves de Ativação")
        self.view_keys_button.clicked.connect(self.view_activation_keys)
        button_layout.addWidget(self.view_keys_button)

        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        activation_key = self.activation_key_input.text()
        result = register_user(username, password, activation_key)
        QMessageBox.information(self, "Resultado", result)

    def generate_activation_key(self):
        key = generate_activation_key()
        QMessageBox.information(self, "Chave de Ativação Gerada", f"Chave: {key}")

    def view_activation_keys(self):
        keys = get_activation_keys()
        keys_str = "\n".join([f"Chave: {key[0]}, Usada: {key[1]}, Criada em: {key[2]}" for key in keys])
        QMessageBox.information(self, "Chaves de Ativação", keys_str)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminRegisterWindow()
    window.show()
    sys.exit(app.exec_())