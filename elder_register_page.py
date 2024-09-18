import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from db import connect_db

class ElderRegisterPage:
    def __init__(self, parent_window):
        parent_window.withdraw()
        self.parent_window = parent_window
        self.window = tk.Toplevel()
        self.window.title("长者注册")
        self.window.geometry("1024x768")
        self.window.config(bg="lightblue")

        self.create_widgets()

    def create_widgets(self):
        font = tkFont.Font(size=14)
        frame = Frame(self.window, bg="lightblue")
        frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(frame, text="姓名:", font=font, bg="lightblue").grid(row=0, column=0, sticky=W, pady=5)
        self.entry_name = Entry(frame, font=font)
        self.entry_name.grid(row=0, column=1, pady=5)

        Label(frame, text="密码:", font=font, bg="lightblue").grid(row=1, column=0, sticky=W, pady=5)
        self.entry_password = Entry(frame, font=font, show="*")
        self.entry_password.grid(row=1, column=1, pady=5)

        button_frame = Frame(self.window, bg="lightblue")
        button_frame.place(relx=0.5, rely=0.7, anchor=CENTER)

        Button(button_frame, text="注册", font=font, command=self.register, bg="gray", fg="white", activebackground="black", activeforeground="white").grid(row=0, column=0, padx=5, pady=5)
        Button(button_frame, text="返回", font=font, command=self.back, bg="gray", fg="white", activebackground="black", activeforeground="white").grid(row=0, column=1, padx=5, pady=5)

    def register(self):
        name = self.entry_name.get()
        password = self.entry_password.get()

        if not name or not password:
            messagebox.showerror("错误", "姓名和密码不能为空")
            return

        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM elder_login WHERE name = %s", (name,))
            existing_elder = cursor.fetchone()
            if existing_elder:
                messagebox.showerror("错误", "该姓名已被注册")
            else:
                cursor.execute("INSERT INTO elder_login (name, password) VALUES (%s, %s)", (name, password))
                db.commit()
                messagebox.showinfo("成功", "注册成功")
        except Exception as e:
            db.rollback()
            messagebox.showerror("错误", str(e))
        finally:
            cursor.close()
            db.close()

    def back(self):
        self.window.destroy()
        self.parent_window.deiconify()
