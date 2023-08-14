import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3
import tkinter as tk
from tkinter import messagebox

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
        


class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("家計簿")

        root.geometry("500x400")

        self.balance = 0
        self.expenses = []

        self.balance_label = tk.Label(root, text="残高")
        self.balance_label.pack()

        self.add_button = tk.Button(root, text="追加する", command=self.add_expense)
        self.add_button.pack()
        
        self.remove_button = tk.Button(root, text="削除する", command=self.remove)
        self.remove_button.pack()

        self.expense_listbox = tk.Listbox(root, width=45, height=25)
        self.expense_listbox.pack()
        self.data_manager = Model()
        self.update_expense_listbox()
        self.updata_balance()

    def remove(self):
        selected_name = self.expense_listbox.curselection()
        if not selected_name:
            messagebox.showwarning("警告", "削除するデータを選択してください。")
            return 
        selected_index = selected_name[0]
        day, category, amount = self.data_manager.get_all_data()[selected_index]
        self.data_manager.data_remove(category)
        messagebox.showinfo("削除", category + "を削除します。")
        self.update_expense_listbox()
        self.updata_balance()
        
    def add_expense(self):
        self.expense_window = tk.Toplevel(self.root)
        self.expense_window.title("追加する")

        tk.Label(self.expense_window, text="ジャンル").pack()
        self.category_label = tk.Entry(self.expense_window)
        self.category_label.pack()

        tk.Label(self.expense_window, text="金額").pack()
        self.amount_label = tk.Entry(self.expense_window)
        self.amount_label.pack()

        tk.Label(self.expense_window, text="日付").pack()
        self.day_label = tk.Entry(self.expense_window)
        self.day_label.pack()

        tk.Button(self.expense_window, text="保存", command=self.save_expense).pack()

    def save_expense(self):
        self.day = self.day_label.get()
        self.category = self.category_label.get()
        self.amount = int(self.amount_label.get())
        
        self.data_manager.Data_set()
        self.data_manager.Data_in(self.day, self.category, self.amount)
        self.expense_window.destroy()
        self.update_expense_listbox()
        self.updata_balance()
        
    def update_expense_listbox(self):
        self.expense_listbox.delete(0, tk.END)
        all_data = self.data_manager.get_all_data()
        for data in all_data:
            day, category, amount = data
            self.expense_listbox.insert(
                tk.END, f"{day}:{category}:{amount}"
            )
    def updata_balance(self):
        all_data = self.data_manager.get_all_balance()
        self.balance = 0  
        for data_tuple in all_data:
            amount = data_tuple[0]  
            self.balance += amount
        self.balance_label.config(text=f"残高: {self.balance}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()