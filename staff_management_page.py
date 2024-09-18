import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from db import connect_db


class StaffManagementPage:
    def __init__(self, parent_window):
        parent_window.withdraw()
        self.parent_window = parent_window
        self.window = tk.Toplevel()
        self.window.title("员工管理")
        self.window.geometry("1024x768")
        self.window.config(bg="lightblue")

        self.create_widgets()

    def create_widgets(self):
        font = tkFont.Font(size=14)
        Label(self.window, text="员工管理", font=("Verdana", 30), bg="lightblue").pack(pady=10)

        self.tree = ttk.Treeview(self.window, columns=("编号", "姓名", "职位", "联系方式", "服务"), show='headings',
                                 height=15)
        self.tree.pack(pady=20)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        self.load_staff_data()

        button_frame = Frame(self.window, bg="lightblue")
        button_frame.pack(pady=20)

        Button(button_frame, text="添加员工", font=font, command=self.add_staff, bg="gray", fg="white",
               activebackground="black", activeforeground="white").grid(row=0, column=0, padx=5, pady=5)
        Button(button_frame, text="编辑员工", font=font, command=self.edit_staff, bg="gray", fg="white",
               activebackground="black", activeforeground="white").grid(row=0, column=1, padx=5, pady=5)
        Button(button_frame, text="删除员工", font=font, command=self.delete_staff, bg="gray", fg="white",
               activebackground="black", activeforeground="white").grid(row=0, column=2, padx=5, pady=5)
        Button(button_frame, text="返回", font=font, command=self.back, bg="gray", fg="white", activebackground="black",
               activeforeground="white").grid(row=0, column=3, padx=5, pady=5)

    def load_staff_data(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT st.id, st.name, st.position, st.contact, s.name
            FROM staff_k st
            LEFT JOIN services_k s ON st.service_id = s.id
        """)
        records = cursor.fetchall()
        db.close()

        for record in records:
            self.tree.insert("", "end", values=(record[0], record[1], record[2], record[3], record[4]))

    def add_staff(self):
        self.staff_form("添加员工")

    def edit_staff(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请先选择一个员工")
            return

        staff_id = self.tree.item(selected_item[0])['values'][0]
        self.staff_form("编辑员工", staff_id)

    def delete_staff(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("错误", "请先选择一个员工")
            return

        staff_id = self.tree.item(selected_item[0])['values'][0]

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM staff_k WHERE id = %s", (staff_id,))
        db.commit()
        db.close()

        messagebox.showinfo("成功", "员工删除成功")
        self.tree.delete(selected_item[0])

    def staff_form(self, title, staff_id=None):
        form_window = tk.Toplevel(self.window)
        form_window.title(title)
        form_window.geometry("400x300")
        form_window.config(bg="lightblue")

        font = tkFont.Font(size=14)

        Label(form_window, text="姓名:", font=font, bg="lightblue").grid(row=0, column=0, pady=10, padx=10, sticky=W)
        entry_name = Entry(form_window, font=font)
        entry_name.grid(row=0, column=1, pady=10, padx=10)

        Label(form_window, text="职位:", font=font, bg="lightblue").grid(row=1, column=0, pady=10, padx=10, sticky=W)
        entry_position = Entry(form_window, font=font)
        entry_position.grid(row=1, column=1, pady=10, padx=10)

        Label(form_window, text="联系方式:", font=font, bg="lightblue").grid(row=2, column=0, pady=10, padx=10,
                                                                             sticky=W)
        entry_contact = Entry(form_window, font=font)
        entry_contact.grid(row=2, column=1, pady=10, padx=10)

        Label(form_window, text="服务:", font=font, bg="lightblue").grid(row=3, column=0, pady=10, padx=10, sticky=W)
        service_var = StringVar()
        services_combobox = ttk.Combobox(form_window, textvariable=service_var, font=font, state='readonly')
        services_combobox.grid(row=3, column=1, pady=10, padx=10)

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, name FROM services_k")
        services = cursor.fetchall()
        db.close()

        services_combobox['values'] = [f"{service[0]}: {service[1]}" for service in services]

        if staff_id:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT name, position, contact, service_id FROM staff_k WHERE id = %s", (staff_id,))
            staff = cursor.fetchone()
            db.close()

            entry_name.insert(0, staff[0])
            entry_position.insert(0, staff[1])
            entry_contact.insert(0, staff[2])
            service_var.set(f"{staff[3]}: {dict(services)[staff[3]]}")

        def save_staff():
            name = entry_name.get()
            position = entry_position.get()
            contact = entry_contact.get()
            service_id = int(service_var.get().split(":")[0])

            db = connect_db()
            cursor = db.cursor()

            if staff_id:
                cursor.execute(
                    "UPDATE staff_k SET name = %s, position = %s, contact = %s, service_id = %s WHERE id = %s",
                    (name, position, contact, service_id, staff_id))
            else:
                cursor.execute("INSERT INTO staff_k (name, position, contact, service_id) VALUES (%s, %s, %s, %s)",
                               (name, position, contact, service_id))

            db.commit()
            db.close()

            messagebox.showinfo("成功", f"{title}成功")
            form_window.destroy()
            self.refresh_tree()

        Button(form_window, text="保存", font=font, command=save_staff, bg="gray", fg="white", activebackground="black",
               activeforeground="white").grid(row=4, column=0, columnspan=2, pady=20)

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_staff_data()

    def back(self):
        self.window.destroy()
        self.parent_window.deiconify()
