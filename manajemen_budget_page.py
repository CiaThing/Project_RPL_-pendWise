import tkinter as tk
from tkinter import messagebox

class ManajemenBudget(tk.Tk):
    def __init__(self, db_ref, email):
        super().__init__()
        self.title("Manajemen Keuangan")
        self.geometry("600x500")
        self.configure(bg="lightgreen")

        self.db_ref = db_ref
        self.email = email
        self.budgets = {}
        self.entries = []

        self.load_existing_budgets()

        self.create_widgets()
    
    def load_existing_budgets(self):
        user_id = self.get_user_id_by_email(self.email)
        if user_id:
            user_data = self.db_ref.child(user_id).get()
            self.budgets = user_data.get('manajemen_budget', {})
    
    def create_widgets(self):
        label = tk.Label(self, text="Manajemen Budget", font=("Arial", 18, "bold"), bg="lightgreen", fg="green")
        label.pack(pady=20)
        
        budget_frame = tk.Frame(self, bg="lightgreen")
        budget_frame.pack(pady=10)
        
        for i in range(3):
            budget_name_label = tk.Label(budget_frame, text=f"Nama Budget {i+1}:", bg="lightgreen")
            budget_name_label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            budget_name_entry = tk.Entry(budget_frame, width=20)
            budget_name_entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries.append(budget_name_entry)
            
            budget_percentage_label = tk.Label(budget_frame, text=f"Persentase Budget {i+1}:", bg="lightgreen")
            budget_percentage_label.grid(row=i, column=2, padx=10, pady=5, sticky="e")
            budget_percentage_entry = tk.Entry(budget_frame, width=20)
            budget_percentage_entry.grid(row=i, column=3, padx=10, pady=5)
            self.entries.append(budget_percentage_entry)

            budget_key = f"budget_{i + 1}"
            if budget_key in self.budgets:
                budget_name_entry.insert(0, self.budgets[budget_key]['kategori'])
                budget_percentage_entry.insert(0, self.budgets[budget_key]['persentase'])
                budget_name_entry.config(state='disabled')
                budget_percentage_entry.config(state='disabled')
        
        additional_expense_label = tk.Label(self, text="Budget Pengeluaran Anda:", font=("Arial", 12, "bold"), bg="lightgreen", fg="green")
        additional_expense_label.pack(pady=10)
        self.additional_expense_entry = tk.Entry(self, width=40)
        self.additional_expense_entry.pack(pady=5)
        
        submit_button = tk.Button(self, text="Submit", command=self.submit, bg="green", fg="white")
        submit_button.pack(pady=10)
        
        add_budget_button = tk.Button(self, text="Add New Budget", command=self.add_new_budget, bg="green", fg="white")
        add_budget_button.pack(pady=10)
        
        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home, bg="green", fg="white")
        back_button.place(x=10, y=10)
    
    def submit(self):
        budgets = {}
        total_percentage = 0
        for i in range(0, len(self.entries), 2):
            budget_name = self.entries[i].get()
            budget_percentage = self.entries[i+1].get()
            try:
                percentage = float(budget_percentage)
            except ValueError:
                messagebox.showerror("Error", f"Persentase untuk budget {i//2 + 1} tidak valid.")
                return
            total_percentage += percentage
            budgets[f"budget_{i//2 + 1}"] = {'kategori': budget_name, 'persentase': percentage}

        if total_percentage > 100:
            messagebox.showerror("Error", f"Total persentase melebihi 100%: {total_percentage}%")
            return

        additional_expense = self.additional_expense_entry.get()
    
        try:
            user_id = self.get_user_id_by_email(self.email)
            if user_id:
                self.db_ref.child(user_id).update({'manajemen_budget': budgets, 'budget_pengeluaran': additional_expense})
                messagebox.showinfo("Success", "Budget data submitted successfully!")
            else:
                messagebox.showerror("Error", "User not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def get_user_id_by_email(self, email):
        result = self.db_ref.order_by_child('email').equal_to(email).get()
        if result:
            return list(result.keys())[0]
        else:
            return None

    def back_to_home(self):
        self.destroy()
        from home_page import HomePage
        home_page = HomePage(self.db_ref, self.email)
        home_page.mainloop()

    def add_new_budget(self):
        self.destroy()
        from manajemen_budget_page_2 import ManajemenBudgetPage2
        add_budget_page = ManajemenBudgetPage2(self.db_ref, self.email)
        add_budget_page.mainloop()

