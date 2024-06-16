import tkinter as tk
from tkinter import messagebox

class ManajemenBudgetPage2(tk.Tk):
    def __init__(self, db_ref, email):
        super().__init__()
        self.title("Add New Budget")
        self.geometry("400x400")
        self.configure(bg="lightgreen")

        self.db_ref = db_ref
        self.email = email

        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Add New Budget", font=("Arial", 18, "bold"), bg="lightgreen", fg="green")
        label.pack(pady=20)

        budget_name_label = tk.Label(self, text="Nama Budget:", bg="lightgreen")
        budget_name_label.pack(pady=5)
        self.budget_name_entry = tk.Entry(self, width=40)
        self.budget_name_entry.pack(pady=5)

        budget_percentage_label = tk.Label(self, text="Persentase Budget:", bg="lightgreen")
        budget_percentage_label.pack(pady=5)
        self.budget_percentage_entry = tk.Entry(self, width=40)
        self.budget_percentage_entry.pack(pady=5)

        submit_button = tk.Button(self, text="Submit", command=self.submit, bg="green", fg="white")
        submit_button.pack(pady=20)

        back_button = tk.Button(self, text="Back", command=self.back_to_manajemen_keuangan, bg="green", fg="white")
        back_button.place(x=10, y=10)

    def submit(self):
        budget_name = self.budget_name_entry.get()
        budget_percentage = self.budget_percentage_entry.get()
        try:
            percentage = float(budget_percentage)
        except ValueError:
            messagebox.showerror("Error", "Persentase tidak valid.")
            return

        user_id = self.get_user_id_by_email(self.email)
        if not user_id:
            messagebox.showerror("Error", "User not found.")
            return

        user_data = self.db_ref.child(user_id).get()
        current_budgets = user_data.get('manajemen_budget', {})
        current_percentage = sum(float(b['persentase']) for b in current_budgets.values())

        if current_percentage + percentage > 100:
            messagebox.showerror("Error", f"Total persentase akan melebihi 100%: {current_percentage + percentage}%")
            return

        new_budget_key = f"budget_{len(current_budgets) + 1}"
        current_budgets[new_budget_key] = {'kategori': budget_name, 'persentase': percentage}
        
        try:
            self.db_ref.child(user_id).update({'manajemen_budget': current_budgets})
            messagebox.showinfo("Success", "Budget baru ditambahkan!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

        self.back_to_manajemen_keuangan()

    def get_user_id_by_email(self, email):
        result = self.db_ref.order_by_child('email').equal_to(email).get()
        if result:
            return list(result.keys())[0]
        else:
            return None

    def back_to_manajemen_keuangan(self):
        self.destroy()
        from manajemen_budget_page import ManajemenBudget
        manajemen_keuangan_page = ManajemenBudget(self.db_ref, self.email)
        manajemen_keuangan_page.mainloop()
