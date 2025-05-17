import sqlite3

class dbManagement():
    def __init__(self):
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()

    def dbCreation(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        result = self.cursor.fetchone()
        if not result:
            self.cursor.executescript('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                birthday TEXT,
                favoritePokemon TEXT,
                pocketTCG_FriendID TEXT
            );
            ''')
        else:
            print('Users table already exists')      
        self.db.commit()
        
    def dropUsersTable(self):
        self.cursor.executescript('''
        DROP TABLE IF EXISTS users
        ''')       
        self.db.commit()

    def truncateAllTables(self):
        # Disable foreign key checks (temporarily) to avoid constraint errors
        self.cursor.execute("PRAGMA foreign_keys = OFF;")

        # Get names of all user-defined tables (excluding SQLite internal ones)
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = self.cursor.fetchall()

        for (table_name,) in tables:
            print(f"Truncating table: {table_name}")
            self.cursor.execute(f"DELETE FROM {table_name};")
            # Optional: Reset auto-increment counter
            self.cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")

        # Re-enable foreign key checks
        self.cursor.execute("PRAGMA foreign_keys = ON;")

        self.db.commit()
        self.db.close()
        print("All tables truncated.")




