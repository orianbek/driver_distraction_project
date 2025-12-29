import tkinter as tk
from tkinter import messagebox
from db_manager import check_login
from ddd_core import set_current_user

BG = "#1e1e1e"
PANEL = "#2a2a2a"
TEXT = "#ffffff"
ACCENT = "#00bcd4"

login_root = None



def start_login():
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        role = check_login(username,password)

        if role :
            messagebox.showinfo("Login Success", f"Welcome {username}")
            set_current_user(username)
            login_root.withdraw()

            from gui_main import open_main_screen
            open_main_screen(username,role, login_root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


    global login_root
    if login_root is None:
        login_root = tk.Tk()
        login_root.title("Login - DDD")
        login_root.geometry("420x320")
        login_root.resizable(False, False)
        login_root.configure(bg=BG)

        header = tk.Frame(login_root, bg=PANEL, height=60)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="🔐 Driver Distraction Detection",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        )
        title.pack(pady=15)

        content = tk.Frame(login_root, bg=BG)
        content.pack(pady=25)

        tk.Label(content, text="👤 Username", bg=BG, fg=TEXT).pack(anchor="w")
        username_entry = tk.Entry(content, width=25)
        username_entry.pack(pady=5)

        tk.Label(content, text="🔑 Password", bg=BG, fg=TEXT).pack(anchor="w")
        password_entry = tk.Entry(content, show="*", width=25)
        password_entry.pack(pady=5)

        login_btn = tk.Button(
            login_root,
            text="Login ▶",
            bg=ACCENT,
            fg="black",
            width=20,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=attempt_login
        )
        login_btn.pack(pady=15)

        footer = tk.Label(
            login_root,
            text="program made by orianbek",
            bg=BG,
            fg="#888888",
            font=("Segoe UI", 9)
        )
        footer.pack(side="bottom", pady=8)

        login_root.mainloop()


if __name__ == "__main__":
    start_login()
