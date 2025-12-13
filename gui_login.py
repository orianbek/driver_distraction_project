import tkinter as tk
from tkinter import messagebox
from ddd_core import run_ddd
import threading

USERS = {
    "admin": "1234",
    "manager": "pass"
}
def start_monitoring():
    ddd_thread = threading.Thread(target=run_ddd)
    ddd_thread.daemon = True   
    ddd_thread.start()

def attempt_login():
    username = username_entry.get()
    password = password_entry.get()

    if username in USERS and USERS[username] == password:
        messagebox.showinfo("Login Success", f"Welcome {username}")
        open_main_screen()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_screen():
    login_root.destroy()

    main_root = tk.Tk()
    main_root.title("Driver Distraction Detection")
    main_root.geometry("400x300")
    main_root.resizable(False, False)

    title = tk.Label(
        main_root,
        text="Driver Distraction Detection",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=20)

    start_btn = tk.Button(
        main_root,
        text="Start Monitoring",
        font=("Arial", 12),
        width=20,
        command=start_monitoring
    )
    start_btn.pack(pady=10)

    exit_btn = tk.Button(
        main_root,
        text="Exit",
        font=("Arial", 12),
        width=20,
        command=main_root.destroy
    )
    exit_btn.pack(pady=10)

    main_root.mainloop()


login_root = tk.Tk()
login_root.title("Login - DDD")
login_root.geometry("400x300")
login_root.resizable(False, False)

frame = tk.Frame(login_root)
frame.pack(pady=20)


tk.Label(frame, text="Username:").grid(row=0, column=0, pady=5, sticky="e")
username_entry = tk.Entry(frame)
username_entry.grid(row=0, column=1, pady=5)


tk.Label(frame, text="Password:").grid(row=1, column=0, pady=5, sticky="e")
password_entry = tk.Entry(frame, show="*")
password_entry.grid(row=1, column=1, pady=5)

copyrights_title= tk.Label(
    login_root,
    text="Program made by orianbek",
    font=("Arial", 10, "bold")
)
copyrights_title.pack(
    side=tk.BOTTOM
)

login_btn = tk.Button(
    login_root,
    text="Login",
    width=15,
    command=attempt_login
)
login_btn.pack(pady=10)

login_root.mainloop()
