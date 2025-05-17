import sqlite3

class UserFunctions():
    def __init__(self):
        self.db = sqlite3.connect('KUA.db')
        self.cursor = self.db.cursor()
        
    async def getUser(self, user_id: int):
        try:
            self.cursor.execute('''
            SELECT * FROM users WHERE user_id = ?
            ''', (user_id,))
            results = self.cursor.fetchall()
            if (results.count <= 0):
                print('No user found')
                raise ValueError 
            elif (results.count > 1):
                print('Multiple users detected. Something is wrong.')
                raise ValueError
        except Exception as e:
            print(f'getUser failed: {e}')
            
        return results.count