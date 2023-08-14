import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3

class Model:
    def __init__(self, dbname = "database.db"):  # コンストラクタ
        self.dbname = dbname
        self.con = sqlite3.connect(self.dbname)
        self.cur = self.con.cursor()
        self.Data_set()
        
    def Data_set(self):
        try:
            self.cur.execute('CREATE TABLE Money (Day STRING, category STRING, amount INTEGER)')
            self.con.commit()
        except sqlite3.OperationalError:
            pass
    
    def Data_in(self, Day, category, amount):
        try:
            self.cur.execute('INSERT INTO Money VALUES(?, ?, ?)', (Day, category, amount))
            self.con.commit()
        except sqlite3.OperationalError:
            pass
    
    def get_all_data(self):
        try:
            self.cur.execute('SELECT * FROM Money')
            return self.cur.fetchall()
        except sqlite3.OperationalError:
            return []
        
    def get_all_balance(self):
        try:
            self.cur.execute('SELECT amount FROM Money')
            return self.cur.fetchall()
        except sqlite3.OperationalError:
            pass
    
    def data_remove(self, category):
        try:
            self.cur.execute('DELETE FROM Money WHERE category = ?', (category,))
            self.con.commit()
        except sqlite3.OperationalError:
            pass
        
    def __del__(self):
        self.cur.close()
        self.con.close()