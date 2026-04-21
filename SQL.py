import sqlite3
import tkinter as tk
from tkinter import messagebox

# ================= DATABASE =================
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    major TEXT,
    gpa REAL
)
""")
conn.commit()


# ================= FUNCTIONS =================
def add_student():
    name = entry_name.get()
    major = entry_major.get()
    gpa = entry_gpa.get()

    if name == "" or major == "" or gpa == "":
        messagebox.showwarning("Lỗi", "Nhập đầy đủ thông tin")
        return

    try:
        cursor.execute("INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)",
                       (name, major, float(gpa)))
        conn.commit()
        messagebox.showinfo("OK", "Đã thêm sinh viên")
        show_all()
    except ValueError:
        messagebox.showerror("Lỗi", "GPA phải là số (ví dụ: 3.5)")


def show_all():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        # Định dạng: ID | Tên {Ngành} GPA
        # Mình giữ ID ở đầu để máy hiểu cần Update dòng nào
        display_text = f"{row[0]} | {row[1]} {{{row[2]}}} {row[3]}"
        listbox.insert(tk.END, display_text)


def show_gpa_3():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students WHERE gpa > 3.0")
    for row in cursor.fetchall():
        display_text = f"{row[0]} | {row[1]} {{{row[2]}}} {row[3]}"
        listbox.insert(tk.END, display_text)


def update_gpa():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Lỗi", "Vui lòng chọn 1 sinh viên trong danh sách")
        return

    # Lấy ID từ chuỗi hiển thị (phần trước dấu '|')
    content = listbox.get(selected[0])
    student_id = content.split(" | ")[0]

    new_gpa = entry_gpa.get()
    try:
        cursor.execute("UPDATE students SET gpa=? WHERE id=?",
                       (float(new_gpa), student_id))
        conn.commit()
        messagebox.showinfo("OK", f"Đã cập nhật GPA cho SV ID {student_id}")
        show_all()
    except ValueError:
        messagebox.showerror("Lỗi", "Nhập GPA mới vào ô GPA")


def delete_low_gpa():
    cursor.execute("DELETE FROM students WHERE gpa < 2.0")
    conn.commit()
    messagebox.showinfo("OK", "Đã xóa sinh viên GPA < 2.0")
    show_all()


# ================= GUI =================
root = tk.Tk()
root.title("Quản lý Hachimi")

tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Major").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="GPA").grid(row=2, column=0, padx=10, pady=5)

entry_name = tk.Entry(root)
entry_major = tk.Entry(root)
entry_gpa = tk.Entry(root)

entry_name.grid(row=0, column=1, padx=10, pady=5)
entry_major.grid(row=1, column=1, padx=10, pady=5)
entry_gpa.grid(row=2, column=1, padx=10, pady=5)

tk.Button(root, text="Thêm SV", command=add_student, width=15).grid(row=3, column=0, pady=5)
tk.Button(root, text="Hiển thị tất cả", command=show_all, width=15).grid(row=3, column=1, pady=5)
tk.Button(root, text="GPA > 3.0", command=show_gpa_3, width=15).grid(row=4, column=0, pady=5)
tk.Button(root, text="Cập nhật GPA", command=update_gpa, width=15).grid(row=4, column=1, pady=5)
tk.Button(root, text="Xóa GPA < 2.0", command=delete_low_gpa, width=15).grid(row=5, column=0, pady=5, columnspan=2)

listbox = tk.Listbox(root, width=60)
listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Tự động hiển thị dữ liệu khi mở app
show_all()

root.mainloop()
conn.close()