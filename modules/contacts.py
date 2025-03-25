import csv
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import sqlite3

class Contacts:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_contact(self, name, email, phone, tags):
        query = """
        INSERT INTO contacts (name, email, phone, tags)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(query, (name, email, phone, tags))
        self.conn.commit()

    def get_contacts(self, filter_by=None):
        query = "SELECT * FROM contacts"
        if filter_by:
            query += f" WHERE {filter_by}"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def remove_contact(self, contact_id):
        query = """
        DELETE FROM contacts WHERE id = ?
        """
        self.conn.execute(query, (contact_id,))
        self.conn.commit()

    def update_contact(self, contact_id, name, email, phone, tags):
        query = """
        UPDATE contacts
        SET name = ?, email = ?, phone = ?, tags = ?
        WHERE id = ?
        """
        self.conn.execute(query, (name, email, phone, tags, contact_id))
        self.conn.commit()

    def search_contacts(self, keyword):
        query = """
        SELECT * FROM contacts
        WHERE name LIKE ? OR email LIKE ? OR phone LIKE ?
        """
        cursor = self.conn.execute(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        return cursor.fetchall()

    def export_contacts(self, file_path, file_format='csv'):
        contacts = self.get_contacts()
        if file_format == 'csv':
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Nome", "Email", "Telefone", "Tags", "Data de Criação"])
                writer.writerows(contacts)
        elif file_format == 'excel':
            df = pd.DataFrame(contacts, columns=["ID", "Nome", "Email", "Telefone", "Tags", "Data de Criação"])
            df.to_excel(file_path, index=False)
        elif file_format == 'pdf':
            c = canvas.Canvas(file_path, pagesize=letter)
            width, height = letter
            c.drawString(100, height - 40, "Contatos")
            c.drawString(100, height - 60, "ID, Nome, Email, Telefone, Tags, Data de Criação")
            y = height - 80
            for contact in contacts:
                c.drawString(100, y, f"{contact[0]}, {contact[1]}, {contact[2]}, {contact[3]}, {contact[4]}, {contact[5]}")
                y -= 20
            c.save()

# Funções para compatibilidade com o código existente
def save_contact(name, email, phone):
    contacts = Contacts('database/crm_revista.db')
    contacts.add_contact(name, email, phone, '')

def list_contacts():
    contacts = Contacts('database/crm_revista.db')
    return contacts.get_contacts()

def remove_contact(contact_id):
    contacts = Contacts('database/crm_revista.db')
    contacts.remove_contact(contact_id)

def update_contact(contact_id, name, email, phone):
    contacts = Contacts('database/crm_revista.db')
    contacts.update_contact(contact_id, name, email, phone, '')

def search_contacts(keyword):
    contacts = Contacts('database/crm_revista.db')
    return contacts.search_contacts(keyword)

def export_contacts(file_path, file_format='csv'):
    contacts = Contacts('database/crm_revista.db')
    contacts.export_contacts(file_path, file_format)