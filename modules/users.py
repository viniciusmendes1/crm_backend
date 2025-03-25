import sqlite3
import uuid

ACTIVATION_KEY = "your_activation_key_here"


def authenticate_user(username, password):
    conn = sqlite3.connect('database/crm_revista.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None


def register_user(username, password, activation_key):
    conn = sqlite3.connect('database/crm_revista.db')
    cursor = conn.cursor()

    # Verificar se a chave de ativação é válida
    cursor.execute('SELECT * FROM activation_keys WHERE key = ? AND is_used = 0', (activation_key,))
    key = cursor.fetchone()
    if not key:
        conn.close()
        return "Chave de ativação inválida ou já usada"

    cursor.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, password))
    cursor.execute('UPDATE activation_keys SET is_used = 1 WHERE key = ?', (activation_key,))
    conn.commit()
    conn.close()
    return "Usuário registrado com sucesso"


def generate_activation_key():
    conn = sqlite3.connect('database/crm_revista.db')
    cursor = conn.cursor()
    key = str(uuid.uuid4())
    cursor.execute('''
        INSERT INTO activation_keys (key)
        VALUES (?)
    ''', (key,))
    conn.commit()
    conn.close()
    return key


def get_activation_keys():
    conn = sqlite3.connect('database/crm_revista.db')
    cursor = conn.cursor()
    cursor.execute('SELECT key, is_used, created_at FROM activation_keys')
    keys = cursor.fetchall()
    conn.close()
    return keys