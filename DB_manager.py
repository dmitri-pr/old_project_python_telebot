import sqlite3


class DB_manager:

    def __init__(self):
        self.conn = sqlite3.connect('TB_.sqlite', check_same_thread=False)

    def creat_tables(self):
        cur = self.conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS Users
         (id INTEGER NOT NULL PRIMARY KEY, user_bot_id INTEGER UNIQUE, sex TEXT,
         age TEXT, town TEXT)''')

        cur.execute('''CREATE TABLE IF NOT EXISTS Users_gelo
         (id INTEGER NOT NULL PRIMARY KEY, user_bot_id INTEGER UNIQUE, latitude
                              DOUBLE PRECISION, longitude DOUBLE PRECISION )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS Users_likes (id INTEGER NOT
                                   NULL PRIMARY KEY, user_bot_id INTEGER UNIQUE,
                                           likes INTEGER, dislikes INTEGER )''')

    def check_users_ids_without_self_id(self, cid):
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM Users WHERE user_bot_id!=?', (cid,))
        rows = cur.fetchall()
        return rows

    def check_all_users_ids(self):
        cur = self.conn.cursor()
        cur.execute('SELECT user_bot_id FROM Users')
        rows = cur.fetchall()
        return rows

    def check_all_gelo_users_ids(self):
        cur = self.conn.cursor()
        cur.execute('SELECT user_bot_id FROM Users_gelo')
        rows = cur.fetchall()
        return rows

    def user_gelo_insert(self, x, y, z):
        cur = self.conn.cursor()
        cur.execute('''INSERT OR IGNORE INTO Users_gelo (user_bot_id, latitude,
                                     longitude) VALUES (?, ?, ?)''', (x, y, z))
        self.conn.commit()

    def user_gelo_update(self, x, y, z):
        cur = self.conn.cursor()
        cur.execute('''UPDATE Users_gelo SET latitude=?, longitude=?
                                             WHERE user_bot_id=?''', (x, y, z))
        self.conn.commit()

    def user_info_insert(self, x, y, z, zz):
        cur = self.conn.cursor()
        cur.execute('''INSERT OR IGNORE INTO Users (user_bot_id, sex, age, town)
                                         VALUES (?, ?, ?, ?)''', (x, y, z, zz))
        self.conn.commit()

    def user_info_update(self, x, y, z, zz):
        cur = self.conn.cursor()
        cur.execute('''UPDATE Users SET sex=?, age=?, town=?
                                        WHERE user_bot_id=?''', (x, y, z, zz))
        self.conn.commit()

    def lookup_person_info(self, x):
        cur = self.conn.cursor()
        cur.execute('SELECT sex, age, town FROM Users WHERE user_bot_id=?', (x,))
        row = cur.fetchone()
        return row

    def choose_self_town_for_filter(self, x):
        cur = self.conn.cursor()
        cur.execute('SELECT town FROM Users WHERE user_bot_id=?', (x,))
        row = cur.fetchone()
        return row

    def lookup_person_likes_info(self, x):
        cur = self.conn.cursor()
        cur.execute('''SELECT likes, dislikes FROM Users_likes
                                                   WHERE user_bot_id=?''', (x,))
        row = cur.fetchone()
        return row

    def lookup_person_gelo_info(self, x):
        cur = self.conn.cursor()
        cur.execute('''SELECT latitude, longitude FROM Users_gelo
                                                   WHERE user_bot_id=?''', (x,))
        row = cur.fetchone()
        return row

    def check_all_likes_users_ids(self):
        cur = self.conn.cursor()
        cur.execute('SELECT user_bot_id FROM Users_likes')
        rows = cur.fetchall()
        return rows

    def user_likes_insert(self, x, y, z):
        cur = self.conn.cursor()
        cur.execute('''INSERT OR IGNORE INTO Users_likes (user_bot_id,
                               likes, dislikes) VALUES (?, ?, ?)''', (x, y, z))
        self.conn.commit()

    def user_likes_update(self, x, y, z):
        cur = self.conn.cursor()
        cur.execute('''UPDATE Users_likes SET likes=?, dislikes=?
                                             WHERE user_bot_id=?''', (x, y, z))
        self.conn.commit()


DB = DB_manager()
DB.creat_tables()
