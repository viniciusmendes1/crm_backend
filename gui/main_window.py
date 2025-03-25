import sys
import os
import json

# Adicionar o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QFileDialog, QListWidget, QListWidgetItem, QMenu, QAction
from PyQt5.QtGui import QIcon
import qtawesome as qta
from modules.contacts import save_contact, list_contacts, remove_contact, update_contact, search_contacts, export_contacts
from modules.reports import generate_report
from gui.admin_register_window import AdminRegisterWindow
from modules.email_importer import import_releases
from modules.releases_manager import ReleasesManager
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

KEYWORDS_FILE = "keywords.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRM para Revista")
        self.setGeometry(100, 100, 1200, 800)

        self.releases_manager = ReleasesManager()
        self.keywords = self.load_keywords()

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
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                font-family: Arial, sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003d80;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #2c3e50;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-family: Arial, sans-serif;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                color: #333;
                padding: 5px;
                border: none;
                font-family: Arial, sans-serif;
            }
        """)

        self.initUI()

    def initUI(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard_tab = QWidget()
        self.contacts_tab = QWidget()
        self.releases_tab = QWidget()
        self.settings_tab = QWidget()

        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.contacts_tab, "Contatos")
        self.tabs.addTab(self.releases_tab, "Releases")
        self.tabs.addTab(self.settings_tab, "Configurações")

        self.initDashboardTab()
        self.initContactsTab()
        self.initReleasesTab()
        self.initSettingsTab()
        self.initMenuBar()

    def initMenuBar(self):
        menubar = self.menuBar()

        # Menu Contatos
        contact_menu = menubar.addMenu('Contatos')

        add_contact_action = QAction(qta.icon('fa5s.plus', color='black'), 'Adicionar Contato', self)
        add_contact_action.triggered.connect(self.show_add_contact_form)
        contact_menu.addAction(add_contact_action)

        list_contacts_action = QAction(qta.icon('fa5s.list', color='black'), 'Listar Contatos', self)
        list_contacts_action.triggered.connect(self.show_contacts_list)
        contact_menu.addAction(list_contacts_action)

        # Menu Relatórios
        report_menu = menubar.addMenu('Relatórios')

        generate_report_action = QAction(qta.icon('fa5s.file-alt', color='black'), 'Gerar Relatório', self)
        generate_report_action.triggered.connect(self.generate_report)
        report_menu.addAction(generate_report_action)

        # Menu Exportar
        export_menu = menubar.addMenu('Exportar')

        export_contacts_action_csv = QAction(qta.icon('fa5s.file-csv', color='black'), 'Exportar Contatos CSV', self)
        export_contacts_action_csv.triggered.connect(lambda: self.export_contacts('csv'))
        export_menu.addAction(export_contacts_action_csv)

        export_contacts_action_excel = QAction(qta.icon('fa5s.file-excel', color='black'), 'Exportar Contatos Excel', self)
        export_contacts_action_excel.triggered.connect(lambda: self.export_contacts('excel'))
        export_menu.addAction(export_contacts_action_excel)

        export_contacts_action_pdf = QAction(qta.icon('fa5s.file-pdf', color='black'), 'Exportar Contatos PDF', self)
        export_contacts_action_pdf.triggered.connect(lambda: self.export_contacts('pdf'))
        export_menu.addAction(export_contacts_action_pdf)

        # Menu Usuários
        user_menu = menubar.addMenu('Usuários')

        add_user_action = QAction(qta.icon('fa5s.user-plus', color='black'), 'Adicionar Usuário', self)
        add_user_action.triggered.connect(self.show_admin_register_window)
        user_menu.addAction(add_user_action)

    def show_add_contact_form(self):
        self.add_contact_widget = QWidget()
        self.add_contact_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nome")
        self.add_contact_layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.add_contact_layout.addWidget(self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefone")
        self.add_contact_layout.addWidget(self.phone_input)

        self.save_contact_button = QPushButton("Salvar Contato")
        self.save_contact_button.setIcon(qta.icon('fa5s.save', color='white'))
        self.save_contact_button.clicked.connect(self.save_contact)
        self.add_contact_layout.addWidget(self.save_contact_button)

        self.add_contact_widget.setLayout(self.add_contact_layout)
        self.contacts_tab.layout().addWidget(self.add_contact_widget)

    def save_contact(self):
        name = self.name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        if not name or not email or not phone:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios")
            return

        save_contact(name, email, phone)
        QMessageBox.information(self, "Sucesso", "Contato salvo com sucesso")
        self.name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()

    def show_contacts_list(self):
        contacts = list_contacts()
        self.contacts_table.setRowCount(len(contacts))
        self.contacts_table.setColumnCount(4)
        self.contacts_table.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefone"])

        for row, contact in enumerate(contacts):
            self.contacts_table.setItem(row, 0, QTableWidgetItem(str(contact[0])))
            self.contacts_table.setItem(row, 1, QTableWidgetItem(contact[1]))
            self.contacts_table.setItem(row, 2, QTableWidgetItem(contact[2]))
            self.contacts_table.setItem(row, 3, QTableWidgetItem(contact[3]))

    def initDashboardTab(self):
        layout = QVBoxLayout()

        # Aqui você pode adicionar gráficos e estatísticas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.update_dashboard()

        self.dashboard_tab.setLayout(layout)

    def update_dashboard(self):
        # Exemplo de atualização do gráfico
        self.ax.clear()
        releases_received = len(self.releases_manager.releases)
        releases_archived = len([r for r in self.releases_manager.releases if r.get("archived")])
        users_registered = len(list_contacts())

        self.ax.bar(["Recebidos", "Arquivados", "Usuários"], [releases_received, releases_archived, users_registered])
        self.ax.set_title("Estatísticas do CRM")
        self.canvas.draw()

    def initContactsTab(self):
        layout = QVBoxLayout()

        self.search_contact_input = QLineEdit()
        self.search_contact_input.setPlaceholderText("Pesquisar Contatos")
        layout.addWidget(self.search_contact_input)

        self.search_contact_button = QPushButton("Pesquisar")
        self.search_contact_button.setIcon(qta.icon('fa5s.search', color='white'))
        self.search_contact_button.clicked.connect(self.search_contacts)
        layout.addWidget(self.search_contact_button)

        self.contacts_table = QTableWidget()
        layout.addWidget(self.contacts_table)

        self.edit_contact_input = QLineEdit()
        self.edit_contact_input.setPlaceholderText("ID do Contato para Editar")
        layout.addWidget(self.edit_contact_input)

        self.edit_contact_button = QPushButton("Editar Contato")
        self.edit_contact_button.setIcon(qta.icon('fa5s.edit', color='white'))
        self.edit_contact_button.clicked.connect(self.show_edit_contact_form)
        layout.addWidget(self.edit_contact_button)

        self.remove_contact_input = QLineEdit()
        self.remove_contact_input.setPlaceholderText("ID do Contato para Remover")
        layout.addWidget(self.remove_contact_input)

        self.remove_contact_button = QPushButton("Remover Contato")
        self.remove_contact_button.setIcon(qta.icon('fa5s.trash', color='white'))
        self.remove_contact_button.clicked.connect(self.remove_contact)
        layout.addWidget(self.remove_contact_button)

        self.contacts_tab.setLayout(layout)

    def initReleasesTab(self):
        layout = QVBoxLayout()

        self.import_button = QPushButton("Importar Releases")
        self.import_button.setIcon(qta.icon('fa5s.download', color='white'))
        self.import_button.clicked.connect(self.import_releases)
        layout.addWidget(self.import_button)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filtrar por Categoria")
        layout.addWidget(self.filter_input)

        self.filter_button = QPushButton("Filtrar")
        self.filter_button.setIcon(qta.icon('fa5s.filter', color='white'))
        self.filter_button.clicked.connect(self.filter_releases)
        layout.addWidget(self.filter_button)

        self.releases_table = QTableWidget()
        layout.addWidget(self.releases_table)

        self.archive_button = QPushButton("Arquivar")
        self.archive_button.setIcon(qta.icon('fa5s.archive', color='white'))
        self.archive_button.clicked.connect(self.archive_release)
        layout.addWidget(self.archive_button)

        self.releases_tab.setLayout(layout)

    def initSettingsTab(self):
        layout = QVBoxLayout()

        self.keywords_input = QLineEdit()
        self.keywords_input.setPlaceholderText("Adicionar palavra-chave")
        layout.addWidget(self.keywords_input)

        self.add_keyword_button = QPushButton("Adicionar")
        self.add_keyword_button.setIcon(qta.icon('fa5s.plus', color='white'))
        self.add_keyword_button.clicked.connect(self.add_keyword)
        layout.addWidget(self.add_keyword_button)

        self.keywords_list = QListWidget()
        layout.addWidget(self.keywords_list)

        self.load_keywords_to_list()

        self.settings_tab.setLayout(layout)

    def add_keyword(self):
        keyword = self.keywords_input.text().strip()
        if keyword and keyword not in self.keywords:
            self.keywords.append(keyword)
            self.keywords_list.addItem(QListWidgetItem(keyword))
            self.keywords_input.clear()
            self.save_keywords()

    def load_keywords(self):
        if os.path.exists(KEYWORDS_FILE):
            with open(KEYWORDS_FILE, 'r') as file:
                return json.load(file)
        return []

    def save_keywords(self):
        with open(KEYWORDS_FILE, 'w') as file:
            json.dump(self.keywords, file)

    def load_keywords_to_list(self):
        for keyword in self.keywords:
            self.keywords_list.addItem(QListWidgetItem(keyword))

    def show_edit_contact_form(self):
        contact_id = self.edit_contact_input.text()

        if not contact_id:
            QMessageBox.warning(self, "Erro", "ID do contato é obrigatório")
            return

        contact_id = int(contact_id)
        contacts = list_contacts()
        contact = next((c for c in contacts if c[0] == contact_id), None)

        if not contact:
            QMessageBox.warning(self, "Erro", "Contato não encontrado")
            return

        self.edit_contact_widget = QWidget()
        self.edit_contact_layout = QVBoxLayout()

        self.edit_name_input = QLineEdit(contact[1])
        self.edit_contact_layout.addWidget(self.edit_name_input)

        self.edit_email_input = QLineEdit(contact[2])
        self.edit_contact_layout.addWidget(self.edit_email_input)

        self.edit_phone_input = QLineEdit(contact[3])
        self.edit_contact_layout.addWidget(self.edit_phone_input)

        self.update_contact_button = QPushButton("Atualizar Contato")
        self.update_contact_button.setIcon(qta.icon('fa5s.save', color='white'))
        self.update_contact_button.clicked.connect(lambda: self.update_contact(contact_id))
        self.edit_contact_layout.addWidget(self.update_contact_button)

        self.edit_contact_widget.setLayout(self.edit_contact_layout)
        self.contacts_tab.layout().addWidget(self.edit_contact_widget)

    def update_contact(self, contact_id):
        name = self.edit_name_input.text()
        email = self.edit_email_input.text()
        phone = self.edit_phone_input.text()

        if not name or not email or not phone:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios")
            return

        update_contact(contact_id, name, email, phone)
        QMessageBox.information(self, "Sucesso", "Contato atualizado com sucesso")
        self.show_contacts_list()

    def remove_contact(self):
        contact_id = self.remove_contact_input.text()

        if not contact_id:
            QMessageBox.warning(self, "Erro", "ID do contato é obrigatório")
            return

        remove_contact(int(contact_id))
        QMessageBox.information(self, "Sucesso", "Contato removido com sucesso")
        self.remove_contact_input.clear()
        self.show_contacts_list()

    def search_contacts(self):
        keyword = self.search_contact_input.text()
        if not keyword:
            QMessageBox.warning(self, "Erro", "Por favor, insira um termo de pesquisa")
            return

        contacts = search_contacts(keyword)
        self.contacts_table.setRowCount(len(contacts))
        self.contacts_table.setColumnCount(4)
        self.contacts_table.setHorizontalHeaderLabels(["ID", "Nome", "Email", "Telefone"])

        for row, contact in enumerate(contacts):
            self.contacts_table.setItem(row, 0, QTableWidgetItem(str(contact[0])))
            self.contacts_table.setItem(row, 1, QTableWidgetItem(contact[1]))
            self.contacts_table.setItem(row, 2, QTableWidgetItem(contact[2]))
            self.contacts_table.setItem(row, 3, QTableWidgetItem(contact[3]))

    def export_contacts(self, file_format):
        options = QFileDialog.Options()
        file_types = {
            'csv': "CSV Files (*.csv);;All Files (*)",
            'excel': "Excel Files (*.xlsx);;All Files (*)",
            'pdf': "PDF Files (*.pdf);;All Files (*)"
        }
        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Contatos", "", file_types[file_format], options=options)

        if file_path:
            export_contacts(file_path, file_format)
            QMessageBox.information(self, "Sucesso", f"Contatos exportados com sucesso para {file_format.upper()}")

    def generate_report(self):
        generate_report()
        QMessageBox.information(self, "Sucesso", "Relatório gerado com sucesso")

    def show_admin_register_window(self):
        self.admin_register_window = AdminRegisterWindow()
        self.admin_register_window.show()

    def import_releases(self):
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        imap_server = os.getenv("IMAP_SERVER")
        imap_port = int(os.getenv("IMAP_PORT"))

        print(f"EMAIL_USER: {email_user}, EMAIL_PASS: {email_pass}, IMAP_SERVER: {imap_server}, IMAP_PORT: {imap_port}")  # Adicione esta linha para verificar as credenciais
        releases = import_releases(email_user, email_pass, self.keywords, imap_server, imap_port)
        for release in releases:
            self.releases_manager.add_release(release)
        self.show_releases()
        self.update_dashboard()

    def filter_releases(self):
        category = self.filter_input.text()
        filtered_releases = self.releases_manager.filter_releases(category)
        self.show_releases(filtered_releases)

    def show_releases(self, releases=None):
        if releases is None:
            releases = self.releases_manager.releases

        self.releases_table.setRowCount(len(releases))
        self.releases_table.setColumnCount(3)
        self.releases_table.setHorizontalHeaderLabels(["Assunto", "Remetente", "Conteúdo"])

        for row, release in enumerate(releases):
            self.releases_table.setItem(row, 0, QTableWidgetItem(release["subject"]))
            self.releases_table.setItem(row, 1, QTableWidgetItem(release["from"]))
            self.releases_table.setItem(row, 2, QTableWidgetItem(release["body"]))

    def archive_release(self):
        selected_row = self.releases_table.currentRow()
        if selected_row != -1:
            release = self.releases_manager.releases[selected_row]
            self.releases_manager.archive_release(release)
            self.show_releases()
            self.update_dashboard()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())