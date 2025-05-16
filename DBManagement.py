import sqlite3

class DBManagement():
    def __init__(self):
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()

    def dbCreation(self):
        self.cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            birthday TEXT,
            favoritePokemon TEXT,
            pocketTCG_FriendID TEXT
        );
        ''')       
        self.db.commit()




