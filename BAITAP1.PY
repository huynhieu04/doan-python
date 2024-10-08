import tkinter as tk
from tkinter import messagebox, Toplevel

class QuanLyHangHoa:
    def __init__(self, master):
        self.master = master
        self.master.title("Quản lý hàng hóa")

        # Danh sách hàng hóa
        self.hang_hoa = []

        # Giao diện
        self.create_widgets()

    def create_widgets(self):
        # Tên hàng hóa
        tk.Label(self.master, text="Tên hàng hóa:").grid(row=0, column=0)
        self.entry_ten = tk.Entry(self.master)
        self.entry_ten.grid(row=0, column=1)

        # Giá
        tk.Label(self.master, text="Giá:").grid(row=1, column=0)
        self.entry_gia = tk.Entry(self.master)
        self.entry_gia.grid(row=1, column=1)

        # Số lượng
        tk.Label(self.master, text="Số lượng:").grid(row=2, column=0)
        self.entry_soluong = tk.Entry(self.master)
        self.entry_soluong.grid(row=2, column=1)

        # Nút thêm hàng hóa
        tk.Button(self.master, text="Thêm hàng hóa", command=self.them_hanghoa).grid(row=3, column=0, columnspan=2)

        # Menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Menu để xem danh sách hàng hóa
        menu_xem = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Thông Báo", menu=menu_xem)
        menu_xem.add_command(label="Danh sách hàng hoá đã thêm", command=self.xem_hanghoa)

        # Menu mới để mở cửa sổ danh sách hàng hóa
        menu_list = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Danh sách", menu=menu_list)
        menu_list.add_command(label="Hàng Hoá Đã Được Thêm", command=self.mo_cua_so_hanghoa)

    def them_hanghoa(self):
        ten = self.entry_ten.get()
        gia = self.entry_gia.get()
        soluong = self.entry_soluong.get()
        if ten and gia and soluong:
            try:
                gia = float(gia)
                soluong = int(soluong)
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Giá phải là số thực và số lượng phải là số nguyên!")
                return

            # Thêm hàng hóa vào danh sách
            self.hang_hoa.append({"ten": ten, "gia": gia, "soluong": soluong})
            messagebox.showinfo("Thành công", "Thêm hàng hóa thành công!")
            self.entry_ten.delete(0, tk.END)
            self.entry_gia.delete(0, tk.END)
            self.entry_soluong.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def xem_hanghoa(self):
        if not self.hang_hoa:
            messagebox.showinfo("Thông tin", "Chưa có hàng hóa nào được thêm!")
            return

        # Tạo chuỗi danh sách hàng hóa
        danh_sach_hang_hoa = ""
        for item in self.hang_hoa:
            danh_sach_hang_hoa += f"Tên: {item['ten']}, Giá: {item['gia']}, Số lượng: {item['soluong']}\n"

        # Hiển thị danh sách hàng hóa trong một hộp thoại
        messagebox.showinfo("Danh sách hàng hóa", danh_sach_hang_hoa)

    def mo_cua_so_hanghoa(self):
        # Tạo cửa sổ mới để hiển thị danh sách hàng hóa
        new_window = Toplevel(self.master)
        new_window.title("Danh sách hàng hóa")

        if not self.hang_hoa:
            tk.Label(new_window, text="Chưa có hàng hóa nào được thêm!").pack()
        else:
            row_num = 0
            # Tạo tiêu đề cột
            tk.Label(new_window, text="Tên hàng hóa").grid(row=row_num, column=0)
            tk.Label(new_window, text="Giá").grid(row=row_num, column=1)
            tk.Label(new_window, text="Số lượng").grid(row=row_num, column=2)

            # Hiển thị hàng hóa
            for item in self.hang_hoa:
                row_num += 1
                tk.Label(new_window, text=item['ten']).grid(row=row_num, column=0)
                tk.Label(new_window, text=item['gia']).grid(row=row_num, column=1)
                tk.Label(new_window, text=item['soluong']).grid(row=row_num, column=2)


# Tạo cửa sổ chính
root = tk.Tk()
app = QuanLyHangHoa(root)
#disable resizing the gui by passing in false/false
root.resizable(False,False)

# Chạy chương trình
root.mainloop()
