import tkinter as tk
from register_page import RegisterPage

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("spendwise-8106d-firebase-adminsdk-gikah-b09d804b61.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spendwise-8106d-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

if __name__ == "__main__":
    app = RegisterPage()
    app.mainloop()
