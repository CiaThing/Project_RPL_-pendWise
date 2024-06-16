import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class PencatatanPengeluaranPage2(tk.Tk):
    def __init__(self, db_ref, email, selected_budget=None):
        super().__init__()

        self.title("Pencatatan Pengeluaran - Page 2")
        self.geometry("600x600")
        self.configure(bg="lightgreen")
        
        self.db_ref = db_ref
        self.email = email
        self.selected_budget = selected_budget
        self.budgets = []
        self.budget_persen = {}
        self.budget_pengeluaran = 0
        
        self.load_budgets()
        self.create_widgets()

    def load_budgets(self):
        user_id = self.get_user_id_by_email(self.email)
        if user_id:
            user_data = self.db_ref.child(user_id).get()
            self.budgets = [budget['kategori'] for budget in user_data.get('manajemen_budget', {}).values()]
            self.budget_persen = {budget['kategori']: float(budget['persentase']) for budget in user_data.get('manajemen_budget', {}).values()}
            self.budget_pengeluaran = float(user_data.get('budget_pengeluaran', 0))

    def get_user_id_by_email(self, email):
        result = self.db_ref.order_by_child('email').equal_to(email).get()
        if result:
            return list(result.keys())[0]
        else:
            return None
    
    def create_widgets(self):
        title_label = tk.Label(self, text="Pencatatan Pengeluaran", font=("Arial", 24, "bold"), bg="lightgreen", fg="green")
        title_label.pack(pady=20)

        budget_label = tk.Label(self, text="Pilih Kategori Budget", bg="lightgreen", font=("Arial", 14))
        budget_label.pack(pady=10)

        self.budget_var = tk.StringVar()
        self.budget_dropdown = ttk.Combobox(self, textvariable=self.budget_var, state='readonly', values=self.budgets)
        self.budget_dropdown.pack(pady=10)
        self.budget_dropdown.bind("<<ComboboxSelected>>", self.enable_inputs)

        amount_label = tk.Label(self, text="Jumlah Pengeluaran", bg="lightgreen", font=("Arial", 14))
        amount_label.pack(pady=10)
        self.amount_entry = tk.Entry(self, state='disabled')
        self.amount_entry.pack(pady=10)

        date_label = tk.Label(self, text="Tanggal Pengeluaran (YYYY-MM-DD)", bg="lightgreen", font=("Arial", 14))
        date_label.pack(pady=10)
        self.date_entry = tk.Entry(self, state='disabled')
        self.date_entry.pack(pady=10)

        note_label = tk.Label(self, text="Catatan Pengeluaran", bg="lightgreen", font=("Arial", 14))
        note_label.pack(pady=10)
        self.note_text = tk.Text(self, height=5, width=50, state='disabled')
        self.note_text.pack(pady=10)
        
        self.note_text.bind("<KeyRelease>", self.limit_text_length)

        save_expense_button = tk.Button(self, text="Save Expense", command=self.save_expense, bg="green", fg="white", state='disabled')
        save_expense_button.pack(pady=10)

        back_button = tk.Button(self, text="Back", command=self.back_to_previous, bg="green", fg="white")
        back_button.place(x=10, y=10)

        self.save_expense_button = save_expense_button  

    def enable_inputs(self, event):
        self.amount_entry.config(state='normal')
        self.date_entry.config(state='normal')
        self.note_text.config(state='normal')
        self.save_expense_button.config(state='normal')

    def limit_text_length(self, event):
        if len(self.note_text.get("1.0", "end-1c")) > 200:
            self.note_text.delete("1.0", "end-1c")
            self.note_text.insert("1.0", self.note_text.get("1.0", "end-1c")[:200])

    def save_expense(self):
        selected_budget = self.budget_var.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        note = self.note_text.get("1.0", "end-1c").strip()
        
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Jumlah pengeluaran harus berupa angka.")
            return

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD.")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Jumlah pengeluaran harus lebih dari 0.")
            return
        
        if not note:
            messagebox.showerror("Error", "Catatan pengeluaran tidak boleh kosong.")
            return

        user_id = self.get_user_id_by_email(self.email)
        if user_id:
            
            if selected_budget not in self.budget_persen:
                messagebox.showerror("Error", f"Budget '{selected_budget}' tidak ditemukan.")
                return
            
            budget_limit = self.budget_pengeluaran * (self.budget_persen[selected_budget] / 100)
            current_expenses_data = self.db_ref.child(user_id).child('catatan_pengeluaran').get()
            
            if current_expenses_data is None:
                current_expenses = []
            else:
                current_expenses = [exp['pengeluaran'] for exp in current_expenses_data.values() if exp.get('kategori') == selected_budget]
            
            current_expenses_sum = sum(current_expenses)
            
            if current_expenses_sum + amount > budget_limit:
                messagebox.showerror("Error", "Pengeluaran sudah melebihi batas budget.")
                return

            new_expense_ref = self.db_ref.child(user_id).child('catatan_pengeluaran').push()
            new_expense_ref.set({
                'tanggal': date,
                'catatan': note,
                'pengeluaran': amount,
                'kategori': selected_budget
            })
            messagebox.showinfo("Success", "Pengeluaran berhasil disimpan.")
            self.back_to_previous()

        
    def back_to_previous(self):
        self.destroy()
        from pencatatan_pengeluaran_page import PencatatanPengeluaran
        app = PencatatanPengeluaran(self.db_ref, self.email)
        app.mainloop()


