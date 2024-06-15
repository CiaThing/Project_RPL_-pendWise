import tkinter as tk
from tkinter import messagebox  # Import messagebox directly from tkinter
from PIL import Image, ImageTk

class HomePage(tk.Tk):
    def __init__(self, db_ref, email):
        super().__init__()
        
        self.title("$Pendwise")
        self.geometry("600x400")
        self.configure(bg="lightgreen")
        
        self.db_ref = db_ref
        self.email = email
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="$Pendwise", font=("Arial", 24, "bold"), bg="lightgreen", fg="green")
        title_label.pack(pady=20)
        
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self, bg="lightgreen")
        button_frame.pack(pady=20)
        
        # Load images from assets folder
        self.pencatatan_image = ImageTk.PhotoImage(Image.open("asset\\pencatatan.png").resize((150, 150)))
        self.manajemen_image = ImageTk.PhotoImage(Image.open("asset\\manajemen.png").resize((150, 150)))
        self.grafik_image = ImageTk.PhotoImage(Image.open("asset\\grafik.png").resize((150, 150)))
        
        # Create buttons
        pencatatan_button = tk.Button(button_frame, image=self.pencatatan_image, command=self.open_pencatatan)
        pencatatan_button.grid(row=0, column=0, padx=20)
        
        manajemen_button = tk.Button(button_frame, image=self.manajemen_image, command=self.open_manajemen)
        manajemen_button.grid(row=0, column=1, padx=20)
        
        grafik_button = tk.Button(button_frame, image=self.grafik_image, command=self.open_grafik)
        grafik_button.grid(row=0, column=2, padx=20)
        
        # Logout button
        logout_button = tk.Button(self, text="Logout", command=self.logout, bg="red", fg="white")
        logout_button.place(relx=0.98, rely=0.98, anchor='se')

        
    def open_pencatatan(self):
        from pencatatan_keuangan_page import PencatatanPengeluaran
        self.destroy()
        pencatatan_keuangan_page = PencatatanPengeluaran(self.db_ref, self.email)
        pencatatan_keuangan_page.mainloop()
        
    def open_manajemen(self):
        from manajemen_keuangan_page import ManajemenBudget
        self.destroy()
        manajemen_keuangan_page = ManajemenBudget(self.db_ref, self.email)
        manajemen_keuangan_page.mainloop()
        
    def open_grafik(self):
        from grafik_pengeluaran_page import GrafikPengeluaran
        self.destroy()
        grafik_pengeluaran_page = GrafikPengeluaran(self.db_ref, self.email)
        grafik_pengeluaran_page.mainloop()
        
    def logout(self):
        # Implement logout functionality here
        # For example, you can destroy the current window and open a login window
        messagebox.showinfo("Logout", "Anda berhasil logout.")
        self.destroy()
        # Example: Open login page
        from login_page import LoginPage
        login_page = LoginPage()
        login_page.mainloop()

