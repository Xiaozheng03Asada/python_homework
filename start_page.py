import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk
from admin_page import AdminPage
from elder_page import ElderPage
from elder_register_page import ElderRegisterPage
from db import connect_db  # 确保导入数据库连接


class StartPage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title('养老服务管理系统')
        self.window.geometry('1024x768')

        self.bg_image = Image.open("C:/Users/Asada3pro/Desktop/Python/system/background.jpeg")
        self.bg_image = self.bg_image.resize((1024, 768), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.window, width=1024, height=768)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        label = Label(self.window, text="养老服务管理系统", font=("Verdana", 30), bg="lightblue")
        label.place(x=362, y=150)

        admin_button = Button(self.window, text="管理员登录", font=tkFont.Font(size=16),
                              command=self.admin_login,
                              width=30, height=2, fg='white', bg='gray', activebackground='black',
                              activeforeground='white')
        admin_button.place(x=262, y=350)

        elder_button = Button(self.window, text="长者登录", font=tkFont.Font(size=16),
                              command=self.elder_login,
                              width=30, height=2, fg='white', bg='gray', activebackground='black',
                              activeforeground='white')
        elder_button.place(x=262, y=450)

        elder_register_button = Button(self.window, text="长者注册", font=tkFont.Font(size=16),
                                       command=self.elder_register,
                                       width=30, height=2, fg='white', bg='gray', activebackground='black',
                                       activeforeground='white')
        elder_register_button.place(x=262, y=550)

        self.window.mainloop()

    def admin_login(self):
        AdminLoginPage(self.window)

    def elder_login(self):
        ElderLoginPage(self.window)  # 调用长者登录页面

    def elder_register(self):
        ElderRegisterPage(self.window)


class ElderLoginPage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title("长者登录")
        self.window.geometry("400x300")

        font = tkFont.Font(size=14)
        frame = Frame(self.window)
        frame.pack(padx=20, pady=20)

        Label(frame, text="用户名", font=font).grid(row=0, column=0, pady=10)
        self.username_entry = Entry(frame, font=font)
        self.username_entry.grid(row=0, column=1, pady=10)

        Label(frame, text="密码", font=font).grid(row=1, column=0, pady=10)
        self.password_entry = Entry(frame, font=font, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        button_frame = Frame(self.window)
        button_frame.pack(pady=20)

        Button(button_frame, text="登录", font=font, command=self.login).grid(row=0, column=0, padx=10)
        Button(button_frame, text="返回", font=font, command=self.back).grid(row=0, column=1, padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM elder_login WHERE name = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        db.close()

        if result:
            ElderPage(self.window, username)  # 传递用户名作为 elder_name 参数
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    def back(self):
        StartPage(self.window)


class AdminLoginPage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title("管理员登录")
        self.window.geometry("400x300")

        font = tkFont.Font(size=14)
        frame = Frame(self.window)
        frame.pack(padx=20, pady=20)

        Label(frame, text="用户名", font=font).grid(row=0, column=0, pady=10)
        self.username_entry = Entry(frame, font=font)
        self.username_entry.grid(row=0, column=1, pady=10)

        Label(frame, text="密码", font=font).grid(row=1, column=0, pady=10)
        self.password_entry = Entry(frame, font=font, show="*")
        self.password_entry.grid(row=1, column=1, pady=10)

        button_frame = Frame(self.window)
        button_frame.pack(pady=20)

        Button(button_frame, text="登录", font=font, command=self.login).grid(row=0, column=0, padx=10)
        Button(button_frame, text="返回", font=font, command=self.back).grid(row=0, column=1, padx=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            AdminPage(self.window)
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    def back(self):
        StartPage(self.window)


if __name__ == "__main__":
    root = tk.Tk()
    app = StartPage(root)
