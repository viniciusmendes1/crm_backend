import sqlite3
import pandas as pd


def generate_report():
    conn = sqlite3.connect('database/crm_revista.db')
    cursor = conn.cursor()

    # Verificar se a coluna 'created_at' existe na tabela 'contacts'
    cursor.execute("PRAGMA table_info(contacts)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'created_at' not in columns:
        # Adicionar a coluna 'created_at' se não existir
        cursor.execute("ALTER TABLE contacts ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        conn.commit()

    # Gerar o relatório com base nos dados da tabela 'contacts'
    cursor.execute('''
        SELECT id, name, email, phone, created_at
        FROM contacts
    ''')
    contacts = cursor.fetchall()

    # Criar um DataFrame com os dados dos contatos
    df = pd.DataFrame(contacts, columns=["ID", "Nome", "Email", "Telefone", "Data de Criação"])

    # Salvar o relatório em um arquivo Excel
    df.to_excel('relatorio_contatos.xlsx', index=False)

    conn.close()