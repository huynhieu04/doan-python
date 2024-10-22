
import tkinter as tk
from tkinter import messagebox, Toplevel
import psycopg2
from psycopg2 import sql

class HangHoaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quản lý hàng hóa")

        # Khởi tạo kết nối cơ sở dữ liệu
        self.db_name = 'thongtin'
        self.user = 'postgres'
        self.password = '130404'
        self.host = 'localhost'
        self.port = '5432'
        self.table_name = 'hanghoa'

        self.hang_hoa = []

        # Tạo menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Menu Database App
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Database App", menu=db_menu)

        # Menu Trang Chủ
        home_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trang Chủ", menu=home_menu)
        home_menu.add_command(label="Thêm hàng hóa", command=self.open_add_item_window)
        home_menu.add_command(label="Sửa hàng hóa", command=self.open_edit_item_window)
        home_menu.add_command(label="Xóa hàng hóa", command=self.open_delete_item_window)
        home_menu.add_command(label="Tìm kiếm hàng hóa", command=self.open_search_item_window)

        # Khung kết nối cơ sở dữ liệu
        self.create_widgets()

    def create_widgets(self):
        # Khung nhập liệu
        connection_frame = tk.Frame(self.master)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_db_name = tk.Entry(connection_frame)
        self.entry_db_name.insert(0, self.db_name)
        self.entry_db_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_user = tk.Entry(connection_frame)
        self.entry_user.insert(0, self.user)
        self.entry_user.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(connection_frame, show="*")
        self.entry_password.insert(0, self.password)
        self.entry_password.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_host = tk.Entry(connection_frame)
        self.entry_host.insert(0, self.host)
        self.entry_host.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        self.entry_port = tk.Entry(connection_frame)
        self.entry_port.insert(0, self.port)
        self.entry_port.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        query_frame = tk.Frame(self.master)
        query_frame.pack(pady=10)
        tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_table_name = tk.Entry(query_frame)
        self.entry_table_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Load Data", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        self.data_display = tk.Text(self.master, height=10, width=50)
        self.data_display.pack(pady=10)

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.entry_db_name.get(),
                user=self.entry_user.get(),
                password=self.entry_password.get(),
                host=self.entry_host.get(),
                port=self.entry_port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.entry_table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
            if not rows:
                messagebox.showinfo("Info", "Không có dữ liệu trong bảng.")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def open_add_item_window(self):
        self.add_item_window = Toplevel(self.master)
        self.add_item_window.title("Thêm hàng hóa")

        tk.Label(self.add_item_window, text="Tên hàng hóa:").grid(row=0, column=0)
        self.entry_ten = tk.Entry(self.add_item_window)
        self.entry_ten.grid(row=0, column=1)

        tk.Label(self.add_item_window, text="Giá (VND):").grid(row=1, column=0)
        self.entry_gia = tk.Entry(self.add_item_window)
        self.entry_gia.grid(row=1, column=1)

        tk.Label(self.add_item_window, text="Số lượng:").grid(row=2, column=0)
        self.entry_soluong = tk.Entry(self.add_item_window)
        self.entry_soluong.grid(row=2, column=1)

        tk.Button(self.add_item_window, text="Thêm hàng hóa", command=self.them_hanghoa).grid(row=3, column=0, columnspan=2)

    def open_edit_item_window(self):
        self.edit_item_window = Toplevel(self.master)
        self.edit_item_window.title("Sửa hàng hóa")

        tk.Label(self.edit_item_window, text="ID hàng hóa:").grid(row=0, column=0)
        self.entry_id = tk.Entry(self.edit_item_window)
        self.entry_id.grid(row=0, column=1)

        tk.Label(self.edit_item_window, text="Tên hàng hóa:").grid(row=1, column=0)
        self.entry_edit_ten = tk.Entry(self.edit_item_window)
        self.entry_edit_ten.grid(row=1, column=1)

        tk.Label(self.edit_item_window, text="Giá (VND):").grid(row=2, column=0)
        self.entry_edit_gia = tk.Entry(self.edit_item_window)
        self.entry_edit_gia.grid(row=2, column=1)

        tk.Label(self.edit_item_window, text="Số lượng:").grid(row=3, column=0)
        self.entry_edit_soluong = tk.Entry(self.edit_item_window)
        self.entry_edit_soluong.grid(row=3, column=1)

        tk.Button(self.edit_item_window, text="Cập nhật hàng hóa", command=self.cap_nhat_hanghoa).grid(row=4, column=0, columnspan=2)

    def open_delete_item_window(self):
        self.delete_item_window = Toplevel(self.master)
        self.delete_item_window.title("Xóa hàng hóa")

        tk.Label(self.delete_item_window, text="ID hàng hóa:").grid(row=0, column=0)
        self.entry_delete_id = tk.Entry(self.delete_item_window)
        self.entry_delete_id.grid(row=0, column=1)

        tk.Button(self.delete_item_window, text="Xóa hàng hóa", command=self.xoa_hanghoa).grid(row=1, column=0, columnspan=2)

    def open_search_item_window(self):
        self.search_item_window = Toplevel(self.master)
        self.search_item_window.title("Tìm kiếm hàng hóa")

        tk.Label(self.search_item_window, text="Tên hàng hóa:").grid(row=0, column=0)
        self.entry_search_ten = tk.Entry(self.search_item_window)
        self.entry_search_ten.grid(row=0, column=1)

        tk.Button(self.search_item_window, text="Tìm kiếm", command=self.tim_kiem_hanghoa).grid(row=1, column=0, columnspan=2)

    def them_hanghoa(self):
        ten = self.entry_ten.get()
        gia = self.entry_gia.get()
        soluong = self.entry_soluong.get()
        if ten and gia and soluong:
            try:
                query = sql.SQL("INSERT INTO {} (ten, gia, soluong) VALUES (%s, %s, %s)").format(sql.Identifier(self.table_name))
                self.cur.execute(query, (ten, gia, soluong))
                self.conn.commit()
                messagebox.showinfo("Success", "Thêm hàng hóa thành công!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding item: {e}")
        else:
            messagebox.showwarning("Warning", "Vui lòng nhập đầy đủ thông tin!")

    def cap_nhat_hanghoa(self):
        id_hanghoa = self.entry_id.get()
        ten = self.entry_edit_ten.get()
        gia = self.entry_edit_gia.get()
        soluong = self.entry_edit_soluong.get()
        if id_hanghoa and (ten or gia or soluong):
            try:
                if ten:
                    self.cur.execute(sql.SQL("UPDATE {} SET ten = %s WHERE id = %s").format(sql.Identifier(self.table_name)), (ten, id_hanghoa))
                if gia:
                    self.cur.execute(sql.SQL("UPDATE {} SET gia = %s WHERE id = %s").format(sql.Identifier(self.table_name)), (gia, id_hanghoa))
                if soluong:
                    self.cur.execute(sql.SQL("UPDATE {} SET soluong = %s WHERE id = %s").format(sql.Identifier(self.table_name)), (soluong, id_hanghoa))
                self.conn.commit()
                messagebox.showinfo("Success", "Cập nhật hàng hóa thành công!")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating item: {e}")
        else:
            messagebox.showwarning("Warning", "Vui lòng nhập ID hàng hóa và thông tin cần cập nhật!")

    def xoa_hanghoa(self):
        id_hanghoa = self.entry_delete_id.get()
        if id_hanghoa:
            try:
                self.cur.execute(sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(self.table_name)), (id_hanghoa,))
                self.conn.commit()
                messagebox.showinfo("Success", "Xóa hàng hóa thành công!")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting item: {e}")
        else:
            messagebox.showwarning("Warning", "Vui lòng nhập ID hàng hóa!")

    def tim_kiem_hanghoa(self):
        ten = self.entry_search_ten.get()
        if ten:
            try:
                query = sql.SQL("SELECT * FROM {} WHERE ten ILIKE %s").format(sql.Identifier(self.table_name))
                self.cur.execute(query, (f'%{ten}%',))
                rows = self.cur.fetchall()
                self.data_display.delete(1.0, tk.END)
                for row in rows:
                    self.data_display.insert(tk.END, f"{row}\n")
                if not rows:
                    messagebox.showinfo("Info", "Không tìm thấy hàng hóa.")
            except Exception as e:
                messagebox.showerror("Error", f"Error searching for item: {e}")
        else:
            messagebox.showwarning("Warning", "Vui lòng nhập tên hàng hóa cần tìm!")

    def __del__(self):
        if hasattr(self, 'cur'):
            self.cur.close()
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangHoaApp(root)
    root.mainloop()
