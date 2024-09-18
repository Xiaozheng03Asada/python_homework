import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import ttk
from db import connect_db


class ServiceRecordsPage:
    def __init__(self, parent_window):
        parent_window.withdraw()
        self.parent_window = parent_window
        self.window = tk.Toplevel()
        self.window.title("服务记录管理")
        self.window.geometry("1024x768")
        self.window.config(bg="lightblue")

        self.selected_record_id = None
        self.undo_stack = []
        self.sort_by = None
        self.sort_ascending = True

        self.create_widgets()
        self.fetch_and_display_records()

    def create_widgets(self):
        font = tkFont.Font(size=14)
        frame = Frame(self.window, bg="lightblue")
        frame.pack(pady=10)

        label = Label(frame, text="服务记录管理", font=("Verdana", 30), bg="lightblue")
        label.pack(pady=10)

        self.info_frame = Frame(frame, bg="lightblue")
        self.info_frame.pack(pady=10)

        self.record_frame = Frame(frame, bg="lightblue")
        self.record_frame.pack(pady=10)

        self.action_frame = Frame(frame, bg="lightblue")
        self.action_frame.pack(pady=10)

        self.create_info_form()
        self.create_record_table()
        self.create_action_buttons()

    def create_info_form(self):
        font_content = tkFont.Font(size=12)
        Label(self.info_frame, text="编号", font=font_content, bg="lightblue").grid(row=0, column=0, sticky=W, pady=5)
        self.id_entry = Entry(self.info_frame, font=font_content)
        self.id_entry.grid(row=0, column=1, pady=5)

        Label(self.info_frame, text="老人编号", font=font_content, bg="lightblue").grid(row=1, column=0, sticky=W,
                                                                                        pady=5)
        self.elder_id_entry = Entry(self.info_frame, font=font_content)
        self.elder_id_entry.grid(row=1, column=1, pady=5)

        Label(self.info_frame, text="服务类型", font=font_content, bg="lightblue").grid(row=2, column=0, sticky=W,
                                                                                        pady=5)
        self.service_id_entry = Entry(self.info_frame, font=font_content)
        self.service_id_entry.grid(row=2, column=1, pady=5)

        Label(self.info_frame, text="服务日期", font=font_content, bg="lightblue").grid(row=3, column=0, sticky=W,
                                                                                        pady=5)
        self.service_date_entry = Entry(self.info_frame, font=font_content)
        self.service_date_entry.grid(row=3, column=1, pady=5)

    def create_record_table(self):
        font = tkFont.Font(size=14)
        self.record_frame.grid_columnconfigure(0, weight=1)
        self.record_frame.grid_columnconfigure(1, weight=3)
        self.record_frame.grid_columnconfigure(2, weight=1)
        self.record_frame.grid_columnconfigure(3, weight=3)

        Label(self.record_frame, text="服务记录", font=("Verdana", 20), bg="lightblue").grid(row=0, column=0,
                                                                                             columnspan=4, pady=10,
                                                                                             sticky="ew")

        self.tree = ttk.Treeview(self.record_frame, columns=("编号", "老人编号", "服务类型", "服务日期"),
                                 show='headings', height=8)
        self.tree.grid(row=1, column=0, columnspan=4, sticky="nsew")

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

        self.tree.bind("<ButtonRelease-1>", self.on_record_select)

    def create_action_buttons(self):
        font = tkFont.Font(size=14)

        # 第一行按钮的框架
        button_frame1 = Frame(self.action_frame, bg="lightblue")
        button_frame1.pack(pady=10)

        # 第二行按钮的框架
        button_frame2 = Frame(self.action_frame, bg="lightblue")
        button_frame2.pack(pady=10)

        button_width = 20
        button_height = 2

        # 第一行按钮
        Button(button_frame1, text="添加服务记录", font=font, command=self.add_service_record, bg="gray", fg="white",
               activebackground="black", activeforeground="white", width=button_width, height=button_height).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
        Button(button_frame1, text="删除服务记录", font=font, command=self.delete_service_record, bg="gray", fg="white",
               activebackground="black", activeforeground="white", width=button_width, height=button_height).grid(row=0,
                                                                                                                  column=1,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
        Button(button_frame1, text="更新服务记录", font=font, command=self.update_service_record, bg="gray", fg="white",
               activebackground="black", activeforeground="white", width=button_width, height=button_height).grid(row=0,
                                                                                                                  column=2,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
        Button(button_frame1, text="查询服务记录", font=font, command=self.fetch_and_display_records, bg="gray",
               fg="white", activebackground="black", activeforeground="white", width=button_width,
               height=button_height).grid(row=0, column=3, padx=5, pady=5)

        # 第二行按钮
        Button(button_frame2, text="撤销操作", font=font, command=self.undo_action, bg="gray", fg="white",
               activebackground="black", activeforeground="white", width=button_width, height=button_height).grid(row=0,
                                                                                                                  column=0,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
        Button(button_frame2, text="返回", font=font, command=self.logout, bg="gray", fg="white",
               activebackground="black", activeforeground="white", width=button_width, height=button_height).grid(row=0,
                                                                                                                  column=1,
                                                                                                                  padx=5,
                                                                                                                  pady=5)

    def fetch_and_display_records(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT id, elder_id, service_id, service_date
            FROM service_records_k
        """)
        records = cursor.fetchall()
        db.close()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for record in records:
            self.tree.insert("", "end", values=(record[0], record[1], record[2], record[3]))

    def on_record_select(self, event):
        selected_item = self.tree.selection()[0]
        record = self.tree.item(selected_item)['values']

        self.selected_record_id = record[0]
        self.id_entry.delete(0, END)
        self.id_entry.insert(0, record[0])

        self.elder_id_entry.delete(0, END)
        self.elder_id_entry.insert(0, record[1])

        self.service_id_entry.delete(0, END)
        self.service_id_entry.insert(0, record[2])

        self.service_date_entry.delete(0, END)
        self.service_date_entry.insert(0, record[3])

    def add_service_record(self):
        elder_id = self.elder_id_entry.get()
        service_id = self.service_id_entry.get()
        service_date = self.service_date_entry.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO service_records_k (elder_id, service_id, service_date)
            VALUES (%s, %s, %s)
        """, (elder_id, service_id, service_date))
        db.commit()
        db.close()

        messagebox.showinfo("成功", "服务记录已添加！")
        self.fetch_and_display_records()

    def delete_service_record(self):
        if not self.selected_record_id:
            messagebox.showerror("错误", "请先选择一个服务记录")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM service_records_k WHERE id = %s", (self.selected_record_id,))
        db.commit()
        db.close()

        messagebox.showinfo("成功", "服务记录已删除！")
        self.fetch_and_display_records()

    def update_service_record(self):
        if not self.selected_record_id:
            messagebox.showerror("错误", "请先选择一个服务记录")
            return

        elder_id = self.elder_id_entry.get()
        service_id = self.service_id_entry.get()
        service_date = self.service_date_entry.get()

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE service_records_k
            SET elder_id = %s, service_id = %s, service_date = %s
            WHERE id = %s
        """, (elder_id, service_id, service_date, self.selected_record_id))
        db.commit()
        db.close()

        messagebox.showinfo("成功", "服务记录已更新！")
        self.fetch_and_display_records()

    def undo_action(self):
        if not self.undo_stack:
            messagebox.showinfo("撤销", "没有可以撤销的操作")
            return

        last_action = self.undo_stack.pop()
        action, record_id, elder_id, service_id, service_date = last_action

        if action == "add":
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM service_records_k WHERE id = %s", (record_id,))
            db.commit()
            db.close()

        elif action == "delete":
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO service_records_k (id, elder_id, service_id, service_date)
                VALUES (%s, %s, %s, %s)
            """, (record_id, elder_id, service_id, service_date))
            db.commit()
            db.close()

        messagebox.showinfo("撤销", "撤销上一次操作")
        self.fetch_and_display_records()

    def logout(self):
        self.window.destroy()
        self.parent_window.deiconify()

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


if __name__ == "__main__":
    root = tk.Tk()
    app = ServiceRecordsPage(root)
    root.mainloop()
