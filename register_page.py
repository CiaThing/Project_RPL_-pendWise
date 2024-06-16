import tkinter as tk
from tkinter import messagebox
import hashlib
from firebase_admin import auth, db


class RegisterPage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("SpendWise Register Page")
        self.geometry("400x400")
        self.configure(bg="lightgreen")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="$Pendwise", font=("Arial", 24, "bold"), bg="lightgreen", fg="green")
        title_label.pack(pady=10)
        
        register_label = tk.Label(self, text="Register Page", font=("Arial", 18, "bold"), bg="lightgreen", fg="green")
        register_label.pack(pady=10)
        
        email_label = tk.Label(self, text="Email", font=("Arial", 12), bg="lightgreen")
        email_label.pack()
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack(pady=5)
        
        username_label = tk.Label(self, text="Username", font=("Arial", 12), bg="lightgreen")
        username_label.pack()
        self.username_entry = tk.Entry(self, width=30)
        self.username_entry.pack(pady=5)
        
        password_label = tk.Label(self, text="Password", font=("Arial", 12), bg="lightgreen")
        password_label.pack()
        self.password_entry = tk.Entry(self, show='*', width=30)
        self.password_entry.pack(pady=5)
        
        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.pack(pady=10)
        
        login_button = tk.Button(self, text="Login page", command=self.go_to_login)
        login_button.pack(pady=10)

        
    def submit(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if email and username and password:
            try:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                user = auth.create_user(
                    email=email,
                    password=password
                )
                
                ref = db.reference('Users')
                ref.child(user.uid).set({
                    'email': email,
                    'username': username,
                    'password': hashed_password  # password disimpan setelah hashing
                })
                
                messagebox.showinfo("Success", "Registration Successful!")
                self.clear_fields()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    
    def clear_fields(self):
        self.email_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def go_to_login(self):
        from login_page import LoginPage
        self.destroy()
        login_page = LoginPage()
        login_page.mainloop()

if __name__ == "__main__":
    app = RegisterPage()
    app.mainloop()
