import tkinter as tk
from tkinter import messagebox

def start_monitoring():
    messagebox.showinfo("DDD", "Starting Driver Distraction Detection...")

root = tk.Tk()
root.title("Driver Distraction Detection")
root.geometry("400x300")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Driver Distraction Detection",
    font=("Arial", 16, "bold")
)
title.pack(pady=20)


start_btn = tk.Button(
    root,
    text="Start Monitoring",
    font=("Arial", 12),
    width=20,
    command=start_monitoring
)
start_btn.pack(pady=10)




root.mainloop()
