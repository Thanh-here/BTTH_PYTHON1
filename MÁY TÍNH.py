import tkinter as tk
from tkinter import messagebox
import math  # Thêm thư viện toán học để dùng số e


# --- HÀM XỬ LÝ LOGIC ---
def click_button(value):
    current = entry.get()
    # Nếu nhấn nút ',' thì chuyển thành '.' để Python hiểu được
    if value == ',':
        value = '.'
    entry.delete(0, tk.END)
    entry.insert(0, current + value)


def add_e():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(math.e))


def calculate_percent():
    try:
        current = float(entry.get())
        result = current / 100
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        messagebox.showerror("Lỗi", "Không thể tính %")


def clear_screen():
    entry.delete(0, tk.END)


def backspace():
    current = entry.get()
    if len(current) > 0:
        entry.delete(len(current) - 1, tk.END)


def calculate():
    try:
        # Thay thế các ký hiệu hiển thị sang ký hiệu Python trước khi tính
        expression = entry.get().replace(',', '.')
        result = eval(expression)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except Exception:
        messagebox.showerror("Lỗi", "Phép tính không hợp lệ")


# --- GIAO DIỆN ---
root = tk.Tk()
root.title("Hachimi")

entry = tk.Entry(root, width=20, font=('Arial', 20), borderwidth=5, relief="flat", justify='right')
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Danh sách nút mới đã sắp xếp lại cho đẹp
buttons = [
    'C', 'DEL', '%', '/',
    '7', '8', '9', '*',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    'e', '0', ',', '=',
]

row_val = 1
col_val = 0

for button in buttons:
    # Xử lý nút e
    if button == 'e':
        cmd = add_e
    # Xử lý nút %
    elif button == '%':
        cmd = calculate_percent
    # Xử lý nút DEL
    elif button == 'DEL':
        cmd = backspace
    # Xử lý nút Clear
    elif button == 'C':
        cmd = clear_screen
    # Xử lý nút Bằng
    elif button == '=':
        cmd = calculate
    # Các nút còn lại (số, phép tính, dấu phẩy)
    else:
        cmd = lambda b=button: click_button(b)

    tk.Button(root, text=button, width=9, height=2, command=cmd).grid(row=row_val, column=col_val, padx=2, pady=2)

    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

root.mainloop()