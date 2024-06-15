import tkinter as tk
from tkinter import ttk, messagebox, Entry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class GrafikPengeluaran(tk.Tk):
    def __init__(self, db_ref, email):
        super().__init__()
        self.title("Grafik Pengeluaran")
        self.geometry("600x600")
        self.configure(bg="lightgreen")
        
        self.db_ref = db_ref
        self.email = email
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Grafik Pengeluaran", font=("Arial", 18), bg="lightgreen", fg="green")
        title_label.pack(pady=20)
        
        # Date range inputs
        date_range_frame = tk.Frame(self, bg="lightgreen")
        date_range_frame.pack(pady=20)
        
        start_label = tk.Label(date_range_frame, text="Tanggal Awal (YYYY-MM-DD)", bg="lightgreen", font=("Arial", 12))
        start_label.grid(row=0, column=0, padx=10, pady=10)
        self.start_entry = tk.Entry(date_range_frame)
        self.start_entry.grid(row=0, column=1, padx=10, pady=10)
        
        end_label = tk.Label(date_range_frame, text="Tanggal Akhir (YYYY-MM-DD)", bg="lightgreen", font=("Arial", 12))
        end_label.grid(row=1, column=0, padx=10, pady=10)
        self.end_entry = tk.Entry(date_range_frame)
        self.end_entry.grid(row=1, column=1, padx=10, pady=10)
        
        generate_button = tk.Button(self, text="Generate Graph", command=self.generate_graph, bg="green", fg="white")
        generate_button.pack(pady=10)
        
        back_button = tk.Button(self, text="Back to Home", command=self.back_to_home, bg="green", fg="white")
        back_button.place(x=10, y=10)
        
        self.canvas = None  # To store matplotlib canvas
    
    def generate_graph(self):
        start_date_str = self.start_entry.get()
        end_date_str = self.end_entry.get()
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Format tanggal harus YYYY-MM-DD.")
            return
        
        if start_date > end_date:
            messagebox.showerror("Error", "Tanggal awal harus sebelum tanggal akhir.")
            return
        
        user_id = self.get_user_id_by_email(self.email)
        if user_id:
            data = self.fetch_expenses(user_id, start_date, end_date)
            if data:
                dates = [expense['tanggal'] for expense in data]
                amounts = [expense['pengeluaran'] for expense in data]
                
                # Clear previous plot if exists
                if self.canvas:
                    self.canvas.get_tk_widget().pack_forget()
                
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(dates, amounts, marker='o', linestyle='-')
                ax.set_xlabel('Tanggal')
                ax.set_ylabel('Pengeluaran')
                ax.set_title('Grafik Pengeluaran')
                ax.grid(True)
                
                self.canvas = FigureCanvasTkAgg(fig, master=self)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(pady=20)
            else:
                messagebox.showinfo("Info", "Tidak ada data pengeluaran dalam rentang tanggal yang diminta.")
        else:
            messagebox.showerror("Error", "Email tidak ditemukan dalam database.")
    
    def get_user_id_by_email(self, email):
        result = self.db_ref.order_by_child('email').equal_to(email).get()
        if result:
            return list(result.keys())[0]
        else:
            return None
    
    def fetch_expenses(self, user_id, start_date, end_date):
        expenses_data = self.db_ref.child(user_id).child('catatan_pengeluaran').get()
        if expenses_data:
            expenses = [expense for expense in expenses_data.values()
                        if start_date <= datetime.strptime(expense['tanggal'], '%Y-%m-%d') <= end_date]
            return expenses
        else:
            return None
        
    def back_to_home(self):
        self.destroy()
        from home_page import HomePage
        home_page = HomePage(self.db_ref, self.email)
        home_page.mainloop()

