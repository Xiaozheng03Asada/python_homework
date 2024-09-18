import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from db import connect_db
from admin_page import AdminPage

undo_stack = []

class ElderManagementPage:
    def __init__(self, parent_window):
        parent_window.destroy()
        self.window = tk.Tk()
        self.window.title("老人信息管理")
        self.window.geometry("1024x768")

        self.create_widgets()
        self.display_elders()

    def create_widgets(self):
        font = tkFont.Font(size=14)
        frame = Frame(self.window)
        frame.grid(row=0, column=0, padx=10, pady=10)

        Label(frame, text="编号", font=font).grid(row=0, column=0, sticky=W, pady=5)
        self.entry_id = Entry(frame, font=font)
        self.entry_id.grid(row=0, column=1, pady=5)

        Label(frame, text="姓名", font=font).grid(row=1, column=0, sticky=W, pady=5)
        self.entry_name = Entry(frame, font=font)
        self.entry_name.grid(row=1, column=1, pady=5)

        Label(frame, text="性别", font=font).grid(row=2, column=0, sticky=W, pady=5)
        self.entry_gender = Entry(frame, font=font)
        self.entry_gender.grid(row=2, column=1, pady=5)

        Label(frame, text="年龄", font=font).grid(row=3, column=0, sticky=W, pady=5)
        self.entry_age = Entry(frame, font=font)
        self.entry_age.grid(row=3, column=1, pady=5)

        Label(frame, text="健康状况", font=font).grid(row=4, column=0, sticky=W, pady=5)
        self.entry_health_status = Entry(frame, font=font)
        self.entry_health_status.grid(row=4, column=1, pady=5)

        button_frame = Frame(self.window)
        button_frame.grid(row=1, column=0, padx=10, pady=10)

        Button(button_frame, text="添加老人", font=font, command=self.add_elder).grid(row=0, column=0, padx=5, pady=5)
        Button(button_frame, text="删除老人", font=font, command=self.delete_elder).grid(row=0, column=1, padx=5, pady=5)
        Button(button_frame, text="更新老人信息", font=font, command=self.update_elder).grid(row=0, column=2, padx=5, pady=5)
        Button(button_frame, text="查询老人信息", font=font, command=self.query_elder).grid(row=0, column=3, padx=5, pady=5)
        Button(button_frame, text="撤销操作", font=font, command=self.undo).grid(row=0, column=4, padx=5, pady=5)
        Button(button_frame, text="返回", font=font, command=self.back).grid(row=0, column=5, padx=5, pady=5)

        tree_frame = Frame(self.window)
        tree_frame.grid(row=2, column=0, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("编号", "姓名", "性别", "年龄", "健康状况"), show='headings')
        self.tree.pack(fill=BOTH, expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def add_elder(self):
        elder_id = self.entry_id.get()
        name = self.entry_name.get()
        gender = self.entry_gender.get()
        age = self.entry_age.get()
        health_status = self.entry_health_status.get()

        if not elder_id.isdigit():
            messagebox.showerror("错误", "编号必须是整数")
            return

        if not elder_id or not name:
            messagebox.showerror("错误", "编号和姓名不能为空")
            return

        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM elder_k WHERE id = %s", (elder_id,))
            existing_elder = cursor.fetchone()
            if existing_elder:
                messagebox.showerror("错误", "该编号已存在")
            else:
                cursor.execute("INSERT INTO elder_k (id, name, gender, age, health_status) VALUES (%s, %s, %s, %s, %s)",
                               (elder_id, name, gender, age, health_status))
                db.commit()
                messagebox.showinfo("成功", "添加成功")
                self.display_elders()
        except Exception as e:
            db.rollback()
            messagebox.showerror("错误", str(e))
        finally:
            cursor.close()
            db.close()

    def delete_elder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请先选择一个老人")
            return

        elder_id = self.tree.item(selected_item[0])['values'][0]

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM elder_k WHERE id = %s", (elder_id,))
        record = cursor.fetchone()
        undo_stack.append(("insert", record))

        cursor.execute("DELETE FROM elder_k WHERE id = %s", (elder_id,))
        db.commit()
        db.close()
        messagebox.showinfo("成功", "老人信息删除成功！")
        self.display_elders()

    def update_elder(self):
        elder_id = self.entry_id.get()
        name = self.entry_name.get()
        gender = self.entry_gender.get()
        age = self.entry_age.get()
        health_status = self.entry_health_status.get()

        if not elder_id.isdigit():
            messagebox.showerror("错误", "编号必须是整数")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM elder_k WHERE id = %s", (elder_id,))
        old_record = cursor.fetchone()
        undo_stack.append(("update", old_record))

        cursor.execute("""
            UPDATE elder_k
            SET name = %s, gender = %s, age = %s, health_status = %s
            WHERE id = %s
        """, (name, gender, age, health_status, elder_id))
        db.commit()
        db.close()
        messagebox.showinfo("成功", "老人信息更新成功！")
        self.display_elders()

    def query_elder(self):
        elder_id = self.entry_id.get()

        if not elder_id.isdigit():
            messagebox.showerror("错误", "编号必须是整数")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM elder_k WHERE id = %s", (elder_id,))
        record = cursor.fetchone()
        db.close()

        if record:
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, record[1])
            self.entry_gender.delete(0, END)
            self.entry_gender.insert(0, record[2])
            self.entry_age.delete(0, END)
            self.entry_age.insert(0, record[3])
            self.entry_health_status.delete(0, END)
            self.entry_health_status.insert(0, record[4])
        else:
            messagebox.showinfo("信息", "未找到老人信息")

    def display_elders(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM elder_k")
        records = cursor.fetchall()
        db.close()

        for record in records:
            self.tree.insert("", "end", values=record)

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item[0], "values")

        self.entry_id.delete(0, END)
        self.entry_id.insert(0, values[0])
        self.entry_name.delete(0, END)
        self.entry_name.insert(0, values[1])
        self.entry_gender.delete(0, END)
        self.entry_gender.insert(0, values[2])
        self.entry_age.delete(0, END)
        self.entry_age.insert(0, values[3])
        self.entry_health_status.delete(0, END)
        self.entry_health_status.insert(0, values[4])

    def treeview_sort_column(self, tv, col, reverse):
        # 处理数值列的排序
        try:
            l = [(int(tv.set(k, col)), k) for k in tv.get_children('')] if col == "编号" else [(tv.set(k, col), k) for k in tv.get_children('')]
        except ValueError:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]

        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def undo(self):
        if not undo_stack:
            messagebox.showinfo("信息", "没有可以撤销的操作")
            return

        last_action = undo_stack.pop()
        db = connect_db()
        cursor = db.cursor()

        if last_action[0] == "delete":
            cursor.execute("DELETE FROM elder_k WHERE id = %s", (last_action[1],))
        elif last_action[0] == "insert":
            record = last_action[1]
            cursor.execute("INSERT INTO elder_k (id, name, gender, age, health_status) VALUES (%s, %s, %s, %s, %s)",
                        (record[0], record[1], record[2], record[3], record[4]))
        elif last_action[0] == "update":
            record = last_action[1]
            cursor.execute("""
                UPDATE elder_k
                SET name = %s, gender = %s, age = %s, health_status = %s
                WHERE id = %s
            """, (record[1], record[2], record[3], record[4], record[0]))

        db.commit()
        db.close()
        self.display_elders()

    def back(self):
        AdminPage(self.window)

if __name__ == "__main__":
    root = tk.Tk()
    app = ElderManagementPage(root)
    root.mainloop()
