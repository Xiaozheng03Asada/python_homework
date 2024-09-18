import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
from db import connect_db
from admin_page import AdminPage

class ServiceManagementPage:
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.parent_window.withdraw()
        self.window = tk.Toplevel()
        self.window.title("服务管理")
        self.window.geometry("1024x768")

        self.create_widgets()
        self.display_services()

    def create_widgets(self):
        font = tkFont.Font(size=14)
        frame = Frame(self.window)
        frame.grid(row=0, column=0, padx=10, pady=10)

        Label(frame, text="编号", font=font).grid(row=0, column=0, sticky=W, pady=5)
        self.entry_id = Entry(frame, font=font)
        self.entry_id.grid(row=0, column=1, pady=5)

        Label(frame, text="服务名称", font=font).grid(row=1, column=0, sticky=W, pady=5)
        self.entry_name = Entry(frame, font=font)
        self.entry_name.grid(row=1, column=1, pady=5)

        Label(frame, text="描述", font=font).grid(row=2, column=0, sticky=W, pady=5)
        self.entry_description = Entry(frame, font=font)
        self.entry_description.grid(row=2, column=1, pady=5)

        button_frame = Frame(self.window)
        button_frame.grid(row=1, column=0, padx=10, pady=10)

        Button(button_frame, text="添加服务", font=font, command=self.add_service).grid(row=0, column=0, padx=5, pady=5)
        Button(button_frame, text="删除服务", font=font, command=self.delete_service).grid(row=0, column=1, padx=5, pady=5)
        Button(button_frame, text="更新服务信息", font=font, command=self.update_service).grid(row=0, column=2, padx=5, pady=5)
        Button(button_frame, text="查询服务信息", font=font, command=self.query_service).grid(row=0, column=3, padx=5, pady=5)
        Button(button_frame, text="返回", font=font, command=self.back).grid(row=0, column=4, padx=5, pady=5)

        tree_frame = Frame(self.window)
        tree_frame.grid(row=2, column=0, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("编号", "服务名称", "描述"), show='headings')
        self.tree.pack(fill=BOTH, expand=True)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def add_service(self):
        service_id = self.entry_id.get()
        name = self.entry_name.get()
        description = self.entry_description.get()

        if not service_id.isdigit():
            messagebox.showerror("错误", "编号必须是整数")
            return

        if not service_id or not name:
            messagebox.showerror("错误", "编号和服务名称不能为空")
            return

        db = connect_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM services_k WHERE id = %s", (service_id,))
            existing_service = cursor.fetchone()
            if existing_service:
                messagebox.showerror("错误", "该编号已存在")
            else:
                cursor.execute("INSERT INTO services_k (id, service_name, description) VALUES (%s, %s, %s)",
                               (service_id, name, description))
                db.commit()
                messagebox.showinfo("成功", "添加成功")
                self.display_services()
        except Exception as e:
            db.rollback()
            messagebox.showerror("错误", str(e))
        finally:
            cursor.close()
            db.close()

    def delete_service(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请先选择一个服务")
            return

        service_id = self.tree.item(selected_item[0])['values'][0]

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM services_k WHERE id = %s", (service_id,))
        db.commit()
        db.close()
        messagebox.showinfo("成功", "服务信息删除成功！")
        self.display_services()

    def update_service(self):
        service_id = self.entry_id.get()
        name = self.entry_name.get()
        description = self.entry_description.get()

        if not service_id.isdigit():
            messagebox.showerror("错误", "编号必须是整数")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE services_k SET service_name = %s, description = %s WHERE id = %s",
                       (name, description, service_id))
        db.commit()
        db.close()
        messagebox.showinfo("成功", "服务信息更新成功！")
        self.display_services()

    def query_service(self):
        service_id = self.entry_id.get()

        if not service_id.isdigit():
            messagebox.showerror("错误", "编号必须是整数")
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM services_k WHERE id = %s", (service_id,))
        record = cursor.fetchone()
        db.close()

        if record:
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, record[1])
            self.entry_description.delete(0, END)
            self.entry_description.insert(0, record[2])
        else:
            messagebox.showinfo("信息", "未找到服务信息")

    def display_services(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM services_k")
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
        self.entry_description.delete(0, END)
        self.entry_description.insert(0, values[2])

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

    def back(self):
        self.window.destroy()
        self.parent_window.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServiceManagementPage(root)
    root.mainloop()
