import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import ttk
from db import connect_db
import datetime


class ElderPage:
    def __init__(self, parent_window, elder_name):
        parent_window.withdraw()
        self.parent_window = parent_window
        self.window = tk.Toplevel()
        self.window.title("长者页面")
        self.window.geometry("1024x768")
        self.window.config(bg="lightblue")

        self.elder_name = elder_name
        self.selected_service_id = None
        self.undo_stack = []
        self.sort_by = None
        self.sort_ascending = True

        self.create_widgets()

    def create_widgets(self):
        font = tkFont.Font(size=14)
        frame = Frame(self.window, bg="lightblue")
        frame.pack(pady=10)

        label = Label(frame, text=f"欢迎，{self.elder_name}！", font=("Verdana", 30), bg="lightblue")
        label.pack(pady=10)

        self.info_frame = Frame(frame, bg="lightblue")
        self.info_frame.pack(pady=10)

        self.service_frame = Frame(frame, bg="lightblue")
        self.service_frame.pack(pady=10)

        self.booking_frame = Frame(frame, bg="lightblue")
        self.booking_frame.pack(pady=10)

        self.display_elder_info()
        self.display_service_records()

        right_button_frame = Frame(self.service_frame, bg="lightblue")
        right_button_frame.grid(row=1, column=4, rowspan=3, padx=10, pady=10, sticky="n")

        button_width = 20
        button_height = 2

        btn_logout = Button(right_button_frame, text="返回登录界面", font=tkFont.Font(size=16), command=self.logout,
                            width=button_width, height=button_height, fg='white', bg='gray', activebackground='black',
                            activeforeground='white')
        btn_logout.grid(row=0, column=0, padx=5, pady=5)

        btn_undo = Button(right_button_frame, text="撤销", font=tkFont.Font(size=16), command=self.undo_action,
                          width=button_width, height=button_height, fg='white', bg='gray', activebackground='black',
                          activeforeground='white')
        btn_undo.grid(row=1, column=0, padx=5, pady=5)

    def display_elder_info(self):
        font_title = tkFont.Font(size=18)
        font_content = tkFont.Font(size=12)
        Label(self.info_frame, text="长者信息", font=font_title, bg="lightblue").grid(row=0, column=0, columnspan=2,
                                                                                      pady=10)

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM elder_k WHERE name = %s", (self.elder_name,))
        record = cursor.fetchone()
        db.close()

        if record:
            Label(self.info_frame, text="编号:", font=font_content, bg="lightblue").grid(row=1, column=0, sticky=W,
                                                                                         pady=5)
            Label(self.info_frame, text=record[0], font=font_content, bg="lightblue").grid(row=1, column=1, sticky=W,
                                                                                           pady=5)

            Label(self.info_frame, text="姓名:", font=font_content, bg="lightblue").grid(row=2, column=0, sticky=W,
                                                                                         pady=5)
            Label(self.info_frame, text=record[1], font=font_content, bg="lightblue").grid(row=2, column=1, sticky=W,
                                                                                           pady=5)

            Label(self.info_frame, text="性别:", font=font_content, bg="lightblue").grid(row=3, column=0, sticky=W,
                                                                                         pady=5)
            Label(self.info_frame, text=record[2], font=font_content, bg="lightblue").grid(row=3, column=1, sticky=W,
                                                                                           pady=5)

            Label(self.info_frame, text="年龄:", font=font_content, bg="lightblue").grid(row=4, column=0, sticky=W,
                                                                                         pady=5)
            Label(self.info_frame, text=record[3], font=font_content, bg="lightblue").grid(row=4, column=1, sticky=W,
                                                                                           pady=5)

            Label(self.info_frame, text="健康状况:", font=font_content, bg="lightblue").grid(row=5, column=0, sticky=W,
                                                                                             pady=5)
            Label(self.info_frame, text=record[4], font=font_content, bg="lightblue").grid(row=5, column=1, sticky=W,
                                                                                           pady=5)
        else:
            Label(self.info_frame, text="未找到长者信息", font=font_content, bg="lightblue").grid(row=1, column=0,
                                                                                                  columnspan=2, pady=10)

    def display_service_records(self):
        font = tkFont.Font(size=14)
        self.service_frame.grid_columnconfigure(0, weight=1)
        self.service_frame.grid_columnconfigure(1, weight=3)
        self.service_frame.grid_columnconfigure(2, weight=1)
        self.service_frame.grid_columnconfigure(3, weight=3)

        Label(self.service_frame, text="服务记录", font=("Verdana", 20), bg="lightblue").grid(row=0, column=0,
                                                                                              columnspan=4, pady=10,
                                                                                              sticky="ew")

        self.tree = ttk.Treeview(self.service_frame, columns=("编号", "服务名称", "服务日期", "员工名称"),
                                 show='headings', height=8)
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

        self.fetch_and_display_records()

    def fetch_and_display_records(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT sr.id, s.name, sr.service_date, COALESCE(st.name, '公共')
            FROM service_records_k sr
            JOIN services_k s ON sr.service_id = s.id
            LEFT JOIN staff_k st ON sr.staff_id = st.id
            WHERE sr.elder_id = (SELECT id FROM elder_k WHERE name = %s)
        """, (self.elder_name,))
        records = cursor.fetchall()
        db.close()

        for record in records:
            self.tree.insert("", "end", values=(record[0], record[1], record[2], record[3]))

        self.display_available_services()

    def display_available_services(self):
        font = tkFont.Font(size=14)
        Label(self.service_frame, text="预约服务", font=("Verdana", 20), bg="lightblue").grid(row=2, column=0,
                                                                                              columnspan=4, pady=10,
                                                                                              sticky="ew")

        self.service_tree = ttk.Treeview(self.service_frame, columns=("编号", "服务名称", "服务描述"), show='headings',
                                         height=8)
        self.service_tree.grid(row=3, column=0, columnspan=4, sticky="nsew")

        for col in self.service_tree["columns"]:
            self.service_tree.heading(col, text=col,
                                      command=lambda _col=col: self.treeview_sort_column(self.service_tree, _col,
                                                                                         False))

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM services_k")
        records = cursor.fetchall()
        db.close()

        for record in records:
            self.service_tree.insert("", "end", values=(record[0], record[1], record[2]))

        self.service_tree.bind("<ButtonRelease-1>", self.on_service_select)

        button_frame = Frame(self.service_frame, bg="lightblue")
        button_frame.grid(row=3, column=4, padx=10, pady=10, sticky="n")

        button_width = 15
        button_height = 2

        Button(button_frame, text="预约服务", font=font, command=self.book_service, bg="gray", fg="white",
               activebackground="black", activeforeground="white", width=button_width, height=button_height).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
        Button(button_frame, text="取消预约", font=font, command=self.cancel_service, bg="gray", fg="white",
               activebackground="black", activeforeground="white", width=button_width, height=button_height).grid(row=1,
                                                                                                                  column=0,
                                                                                                                  padx=5,
                                                                                                                  pady=5)

    def treeview_sort_column(self, tv, col, reverse):
        # 处理数值列的排序
        try:
            l = [(int(tv.set(k, col)), k) for k in tv.get_children('')]
        except ValueError:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]

        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def on_service_select(self, event):
        selected_item = self.service_tree.selection()[0]
        service_id = self.service_tree.item(selected_item)['values'][0]
        self.selected_service_id = service_id

    def book_service(self):
        if not hasattr(self, 'selected_service_id'):
            messagebox.showerror("错误", "请先选择一个服务")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM elder_k WHERE name = %s", (self.elder_name,))
        elder_id = cursor.fetchone()

        if elder_id:
            # 检查是否是公共服务
            cursor.execute("SELECT is_public FROM services_k WHERE id = %s", (self.selected_service_id,))
            is_public = cursor.fetchone()[0]

            staff_id = None
            if not is_public:
                # 查找未被预约的员工
                cursor.execute("""
                    SELECT id FROM staff_k
                    WHERE service_id = %s AND id NOT IN (
                        SELECT staff_id FROM bookings_k WHERE service_id = %s AND booking_date = CURDATE()
                    )
                """, (self.selected_service_id, self.selected_service_id))
                available_staff = cursor.fetchone()

                if available_staff:
                    staff_id = available_staff[0]
                else:
                    messagebox.showerror("错误", "该服务的所有员工都已被预约")
                    return

            cursor.execute("""
                INSERT INTO bookings_k (elder_id, service_id, booking_date, staff_id)
                VALUES (%s, %s, CURDATE(), %s)
            """, (elder_id[0], self.selected_service_id, staff_id))

            cursor.execute("""
                INSERT INTO service_records_k (elder_id, service_id, service_date, staff_id)
                VALUES (%s, %s, CURDATE(), %s)
            """, (elder_id[0], self.selected_service_id, staff_id))

            db.commit()

            # 记录操作
            self.undo_stack.append(("book", elder_id[0], self.selected_service_id, staff_id))

            messagebox.showinfo("成功", "预约成功！")
            self.display_service_records()
        else:
            messagebox.showerror("错误", "未找到长者信息")

        db.close()

    def cancel_service(self):
        selected_item = self.tree.selection()[0]
        record_id = self.tree.item(selected_item)['values'][0]

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT service_date FROM service_records_k WHERE id = %s", (record_id,))
        service_date = cursor.fetchone()[0]

        # 只允许取消未来的预约
        if service_date < datetime.date.today():
            messagebox.showerror("错误", "无法取消已过去的预约")
            return

        cursor.execute("DELETE FROM service_records_k WHERE id = %s", (record_id,))
        cursor.execute("DELETE FROM bookings_k WHERE id = %s", (record_id,))
        db.commit()
        db.close()

        messagebox.showinfo("成功", "预约已取消！")
        self.display_service_records()

    def undo_action(self):
        if not self.undo_stack:
            messagebox.showinfo("撤销", "没有可以撤销的操作")
            return

        last_action = self.undo_stack.pop()
        action, elder_id, service_id, staff_id = last_action

        if action == "book":
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM service_records_k WHERE elder_id = %s AND service_id = %s AND staff_id = %s",
                           (elder_id, service_id, staff_id))
            cursor.execute("DELETE FROM bookings_k WHERE elder_id = %s AND service_id = %s AND staff_id = %s",
                           (elder_id, service_id, staff_id))
            db.commit()
            db.close()

            messagebox.showinfo("撤销", "撤销上一次预约操作")
            self.display_service_records()

    def logout(self):
        self.window.destroy()
        self.parent_window.deiconify()
