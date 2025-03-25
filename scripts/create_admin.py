import sqlite3

def create_admin(username, password):
    conn = sqlite3.connect('database/crm_revista.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, password, is_admin)
        VALUES (?, ?, ?)
    ''', (username, password, True))
    conn.commit()
    conn.close()
    print("Administrador criado com sucesso")

if __name__ == "__main__":
    username = input("Digite o nome de usuário do administrador: ")
    password = input("Digite a senha do administrador: ")
    create_admin(username, password)