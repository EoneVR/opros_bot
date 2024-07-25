import sqlite3
import pandas


class Database:
    def __init__(self):
        self.database = sqlite3.connect('anketa.db', check_same_thread=False)
        self.create_users_table()

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def create_users_table(self):
        sql = '''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            full_name TEXT,
            gender TEXT,
            age INTEGER,
            phone TEXT,
            language TEXT,
            occupation TEXT,
            time DATETIME 
            )
            '''
        self.manager(sql, commit=True)

    def get_user_by_chat_id(self, chat_id):
        sql = '''
        SELECT * FROM users WHERE chat_id = ?
        '''
        return self.manager(sql, chat_id, fetchone=True)

    def first_register_user(self, chat_id):
        sql = '''
        INSERT INTO users(chat_id) VALUES (?)
        '''
        self.manager(sql, chat_id, commit=True)

    def set_user_language(self, chat_id, lang):
        user = self.get_user_by_chat_id(chat_id)
        if user:
            sql = '''
            UPDATE users SET language = ? WHERE chat_id = ?
            '''
            self.manager(sql, lang, chat_id, commit=True)
        else:
            sql = '''
            INSERT INTO users (chat_id, language) VALUES (?,?)
            '''
            self.manager(sql, chat_id, lang, commit=True)

    def get_user_language(self, chat_id):
        sql = '''
        SELECT language FROM users WHERE chat_id = ?
        '''
        result = self.manager(sql, chat_id, fetchone=True)
        if result:
            return result[0]
        return None

    def update_data(self, chat_id, full_name, gender, age, phone, occupation, time):
        sql = '''
        UPDATE users
        SET full_name = ?,
        gender = ?,
        age = ?,
        phone = ?,
        occupation = ?,
        time = ?
        WHERE chat_id = ?
        '''
        self.manager(sql, full_name, gender, age, phone, occupation, time, chat_id, commit=True)

    def save_data_for_excel(self):
        sql = '''SELECT * FROM users'''
        pf = pandas.read_sql_query(sql, self.database)
        pf.to_excel('users.xlsx', index=False, engine='openpyxl')
