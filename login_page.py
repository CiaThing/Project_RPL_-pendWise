import tkinter as tk
from tkinter import messagebox
import hashlib
from firebase_admin import db
from home_page import HomePage

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("SpendWise Login Page")
        self.geometry("400x400")
        self.configure(bg="lightgreen")
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title_label = tk.Label(self, text="Login Page", font=("Arial", 18, "bold"), bg="lightgreen", fg="green")
        title_label.pack(pady=10)
        
        email_label = tk.Label(self, text="Email", font=("Arial", 12), bg="lightgreen")
        email_label.pack()
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.pack(pady=5)
        
        password_label = tk.Label(self, text="Password", font=("Arial", 12), bg="lightgreen")
        password_label.pack()
        self.password_entry = tk.Entry(self, show='*', width=30)
        self.password_entry.pack(pady=5)
        
        submit_button = tk.Button(self, text="Login", command=self.submit)
        submit_button.pack(pady=10)
        
        register_button = tk.Button(self, text="Register", command=self.go_to_register, width=20)
        register_button.pack(pady=10)
        
    def submit(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if email and password:
            try:
                result = db.reference('Users').order_by_child('email').equal_to(email).get()
                
                if not result:
                    messagebox.showerror("Error", "User with email {} does not exist.".format(email))
                    return
                
                stored_password = list(result.values())[0].get('password')
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                if hashed_password == stored_password:
                    messagebox.showinfo("Success", "Login Successful!")
                    self.redirect_to_home(email)
                else:
                    messagebox.showerror("Error", "Incorrect password.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    
    def redirect_to_home(self, email):
        self.destroy()
        home_page = HomePage(db.reference('Users'), email)
        home_page.mainloop()
    
    def go_to_register(self):
        from register_page import RegisterPage
        self.destroy()
        register_page = RegisterPage()
        register_page.mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()
