import tkinter as tk
import threading
import sys
import ddd_core
from tkinter import ttk
from db_manager import get_all_events


BG = "#1e1e1e"
PANEL = "#2a2a2a"
TEXT = "#ffffff"
ACCENT = "#00bcd4"
DANGER = "#d32f2f"
OK = "#4caf50"


def logout(main_root, login_root):
    import ddd_core

    ddd_core.RUNNING = False
    ddd_core.clear_current_user()

    main_root.destroy()      
    login_root.deiconify()   


def open_logs_window():
    logs_root = tk.Toplevel()
    logs_root.title("Event Logs")
    logs_root.geometry("550x450")
    logs_root.configure(bg=BG)

    title = tk.Label(
        logs_root,
        text="📊 Driver Events Log",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 14, "bold")
    )
    title.pack(pady=10)

    table_frame = tk.Frame(logs_root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("timestamp", "username", "event")

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    tree.heading("timestamp", text="Time")
    tree.heading("username", text="User")
    tree.heading("event", text="Event")

    tree.column("timestamp", width=180)
    tree.column("username", width=120)
    tree.column("event", width=200)

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    events = get_all_events()
    for row in events:
        tree.insert("", "end", values=row)


def exit_app():
    ddd_core.RUNNING = False
    sys.exit(0)

def start_monitoring(status_label, start_btn, stop_btn):
    if not ddd_core.RUNNING:
        status_label.config(text="Status: Running", fg=OK)
        ddd_thread = threading.Thread(target=ddd_core.run_ddd, daemon=True)
        ddd_thread.start()

        start_btn.config(state="disabled")
        stop_btn.config(state="normal")

def stop_monitoring(status_label, start_btn, stop_btn):
    ddd_core.RUNNING = False
    status_label.config(text="Status: Stopped", fg="#ff9800")

    start_btn.config(state="normal")
    stop_btn.config(state="disabled")


def open_main_screen(username,role, root):

    main_root = tk.Toplevel(root)
    main_root.title("Driver Distraction Detection")
    main_root.geometry("550x580")
    main_root.resizable(False, False)
    main_root.configure(bg=BG)
 
    header = tk.Frame(main_root, bg=PANEL, height=60)
    header.pack(fill="x")

    title = tk.Label(
        header,
        text="🚗 Driver Distraction Detection",
        bg=PANEL,
        fg=TEXT,
        font=("Segoe UI", 15, "bold")
    )
    title.pack(pady=15)

    status_label = tk.Label(
        main_root,
        text="Status: Idle",
        bg=BG,
        fg="#ffcc00",
        font=("Segoe UI", 11, "bold")
    )
    status_label.pack(pady=15)
    controls = tk.Frame(main_root, bg=BG)
    controls.pack(pady=10)

    start_btn = tk.Button(
    controls,
    text="▶ Start Monitoring",
    bg=ACCENT,
    fg="black",
    width=24,
    height=2,
    font=("Segoe UI", 11, "bold"),
    relief="flat"
    )

    stop_btn = tk.Button(
    controls,
    text="⏹ Stop",
    bg="#ff9800",
    fg="black",
    width=24,
    height=2,
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    state="disabled"
    )
    start_btn.config(
    command=lambda: start_monitoring(status_label, start_btn, stop_btn)
    )

    stop_btn.config(
    command=lambda: stop_monitoring(status_label, start_btn, stop_btn)
    )
    start_btn.pack(pady=8)
    stop_btn.pack(pady=8)

    logout_btn = tk.Button(
        controls,
        text="🔓 Logout",
        bg="#9e9e9e",
        fg="black",
        width=24,
        height=2,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        command=lambda: logout(main_root, root)
    )
    logout_btn.pack(pady=8)

    exit_btn = tk.Button(
        controls,
        text="🚪 Exit",
        bg=DANGER,
        fg="white",
        width=24,
        height=2,
        font=("Segoe UI", 11, "bold"),
        relief="flat",
        command=lambda: exit_app()
    )
    exit_btn.pack(pady=8)


    footer = tk.Label(
        main_root,
        text=f"👤 Logged in as: {username}",
        bg=BG,
        fg="#aaaaaa",
        font=("Segoe UI", 9)
    )
    footer.pack(side="bottom", pady=10)

    if role == "admin":
        view_logs_btn = tk.Button(
            controls,
            text="📊 View Logs",
            bg="#607d8b",
            fg="white",
            width=24,
            height=2,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=lambda: open_logs_window()
        )
    view_logs_btn.pack(pady=8)

    main_root.mainloop()
