import tkinter as tk
from tkinter import ttk, messagebox

class PencatatanPengeluaran(tk.Tk):
    def __init__(self, db_ref, email):
        super().__init__()
        
        self.title("Pencatatan Pengeluaran")
        self.geometry("600x600")
        self.configure(bg="lightgreen")
        
        self.db_ref = db_ref
        self.email = email
        self.budgets = []
        self.expenses = []

        self.load_budgets()
        self.create_widgets()
    
    def load_budgets(self):
        user_id = self.get_user_id_by_email(self.email)
        if user_id:
            user_data = self.db_ref.child(user_id).get()
            self.budgets = [budget['kategori'] for budget in user_data.get('manajemen_budget', {}).values()]
    
    def get_user_id_by_email(self, email):
        result = self.db_ref.order_by_child('email').equal_to(email).get()
        if result:
            return list(result.keys())[0]
        else:
            return None
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Pencatatan Pengeluaran", font=("Arial", 24, "bold"), bg="lightgreen", fg="green")
        title_label.pack(pady=20)
        
        budget_label = tk.Label(self, text="Pilih Kategori Budget", bg="lightgreen", font=("Arial", 14))
        budget_label.pack(pady=10)
        
        self.budget_var = tk.StringVar()
        self.budget_dropdown = ttk.Combobox(self, textvariable=self.budget_var, state='readonly', values=self.budgets)
        self.budget_dropdown.pack(pady=10)
        self.budget_dropdown.bind("<<ComboboxSelected>>", self.load_expenses)

        self.no_expense_label = tk.Label(self, text="Tidak ada pengeluaran untuk budget ini", bg="lightgreen", font=("Arial", 12), fg="red")
        self.no_expense_label.pack(pady=10)
        self.no_expense_label.pack_forget()

        self.table_frame = tk.Frame(self, bg="lightgreen")
        self.table_frame.pack(pady=20)
        self.table_frame.pack_forget()  

        self.tree = ttk.Treeview(self.table_frame, columns=("No.", "Date", "Expense", "Note"), show="headings")
        self.tree.heading("No.", text="No.")
        self.tree.heading("Date", text="Tanggal")
        self.tree.heading("Expense", text="Pengeluaran")
        self.tree.heading("Note", text="Catatan")
        self.tree.pack()

        add_expense_button = tk.Button(self, text="Add Expense", command=self.add_expense, bg="green", fg="white")
        add_expense_button.pack(pady=10)
        
        back_button = tk.Button(self, text="Back", command=self.back_to_home, bg="green", fg="white")
        back_button.place(x=10, y=10)
    
    def load_expenses(self, event):
        selected_budget = self.budget_var.get()
        user_id = self.get_user_id_by_email(self.email)
        if user_id:
            expenses_data = self.db_ref.child(user_id).child('catatan_pengeluaran').get()
            self.expenses = [exp for exp in expenses_data.values() if exp['kategori'] == selected_budget]
            self.update_table()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if self.expenses:
            self.no_expense_label.pack_forget()
            self.table_frame.pack(pady=20)
            for idx, expense in enumerate(self.expenses, start=1):
                self.tree.insert("", "end", values=(idx, expense["tanggal"], expense["pengeluaran"], expense["catatan"]))
        else:
            self.table_frame.pack_forget()  
            self.no_expense_label.pack(pady=10)

    def add_expense(self):
        from pencatatan_pengeluaran_page_2 import PencatatanPengeluaranPage2
        self.destroy()
        add_expense_page = PencatatanPengeluaranPage2(self.db_ref, self.email, self.budget_var.get())
        add_expense_page.mainloop()

    def back_to_home(self):
        self.destroy()
        from home_page import HomePage
        home_page = HomePage(self.db_ref, self.email)
        home_page.mainloop()

