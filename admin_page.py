import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk

class AdminPage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title("管理员页面")
        self.window.geometry("1024x768")

        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.window, width=1024, height=768)
        self.canvas.pack(fill="both", expand=True)
        self.bg_image = Image.open("C:/Users/Asada3pro/Desktop/Python/system/background.jpeg")
        self.bg_image = self.bg_image.resize((1024, 768), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        label = Label(self.window, text="养老服务管理系统", font=("Verdana", 30), bg="lightblue")
        label.place(x=362, y=50)

        btn_manage_elders = Button(self.window, text="管理老人信息", font=tkFont.Font(size=16),
                                   command=self.manage_elders,
                                   width=20, height=2, fg='white', bg='gray', activebackground='black',
                                   activeforeground='white')
        btn_manage_elders.place(x=362, y=150)

        btn_manage_records = Button(self.window, text="管理服务记录", font=tkFont.Font(size=16),
                                    command=self.manage_service_records,
                                    width=20, height=2, fg='white', bg='gray', activebackground='black',
                                    activeforeground='white')
        btn_manage_records.place(x=362, y=250)

        btn_manage_services = Button(self.window, text="管理服务", font=tkFont.Font(size=16),
                                     command=self.manage_services,
                                     width=20, height=2, fg='white', bg='gray', activebackground='black',
                                     activeforeground='white')
        btn_manage_services.place(x=362, y=350)

        btn_manage_staff = Button(self.window, text="管理员工信息", font=tkFont.Font(size=16),
                                  command=self.manage_staff,
                                  width=20, height=2, fg='white', bg='gray', activebackground='black',
                                  activeforeground='white')
        btn_manage_staff.place(x=362, y=450)

        btn_logout = Button(self.window, text="返回登录界面", font=tkFont.Font(size=16), command=self.logout,
                            width=20, height=2, fg='white', bg='gray', activebackground='black',
                            activeforeground='white')
        btn_logout.place(x=362, y=550)

    def manage_elders(self):
        from elder_management_page import ElderManagementPage
        ElderManagementPage(self.window)

    def manage_service_records(self):
        from service_records_page import ServiceRecordsPage
        ServiceRecordsPage(self.window)

    def manage_services(self):
        from service_management_page import ServiceManagementPage
        ServiceManagementPage(self.window)

    def manage_staff(self):
        from staff_management_page import StaffManagementPage
        StaffManagementPage(self.window)

    def logout(self):
        from start_page import StartPage
        StartPage(self.window)
