import sqlite3
class DBCommands:
    CREATE_TABLE = """CREATE TABLE IF NOT EXISTS users (chatid INTEGER UNIQUE, marka TEXT, model TEXT)"""
    async def create(self):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            cursor.execute(self.CREATE_TABLE)

    ADD_USER = """INSERT INTO users (chatid, marka) VALUES ($1, $2)"""
    async def add_user(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.ADD_USER
            cursor.execute(command, par)

    UPDATE_MARKA = """UPDATE users SET marka = $1 WHERE chatid = $2"""
    async def update_marka(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.UPDATE_MARKA
            cursor.execute(command, par)

    UPDATE_MODEL = """UPDATE users SET model = $1 WHERE chatid = $2"""
    async def update_model(self, par):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.UPDATE_MODEL
            cursor.execute(command, par)

    SELECT_USER = """SELECT count(*) FROM users WHERE chatid = $1"""
    async def select_user(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_USER
            return cursor.execute(command, chatid)

    SELECT_MARKA = """SELECT marka FROM users WHERE chatid = $1"""
    async def select_marka(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_MARKA
            return cursor.execute(command, chatid)

    SELECT_MODEL = """SELECT marka FROM users WHERE chatid = $1"""
    async def select_model(self, chatid):
        with sqlite3.connect('server.db') as db:
            cursor = db.cursor()
            command = self.SELECT_MODEL
            return cursor.execute(command, chatid)