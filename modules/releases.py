import sqlite3

class Releases:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date_received DATE NOT NULL,
            source TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_release(self, title, content, date_received, source):
        query = """
        INSERT INTO releases (title, content, date_received, source)
        VALUES (?, ?, ?, ?)
        """
        self.conn.execute(query, (title, content, date_received, source))
        self.conn.commit()

    def get_releases(self, filter_by=None):
        query = "SELECT * FROM releases"
        if filter_by:
            query += f" WHERE {filter_by}"
        cursor = self.conn.execute(query)
        return cursor.fetchall()