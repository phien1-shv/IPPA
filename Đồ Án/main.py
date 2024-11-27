import tkinter as tk
from tkinter import ttk, messagebox
from data_processing import DataProcessor
from chart_visualization import draw_chart
import pandas as pd


file_path = 'ObesityDataSet_raw_and_data_sinthetic.csv'
data = pd.read_csv(file_path)

data_processor = DataProcessor(file_path)
columns = list(data_processor.data.columns) 

# Tạo cửa sổ Tkinter
root = tk.Tk()
root.title("QUẢN LÝ DỮ LIỆU BÉO PHÌ")
root.geometry("2000x7000")

# Tạo Treeview để hiển thị dữ liệu
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = list(data.columns)
tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=max(10, int(20 / len(columns))), anchor="center")

tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
# Giá trị lựa chọn sẵn (ví dụ cho một số cột)
options = {
    "Gender": ["Male", "Female"],
    "family_history_with_overweight": ["yes", "no"],
    "FAVC": ["yes", "no"],
    "FCVC": ["1", "2", "3"],
    "NCP": ["1", "2", "3", "4"],
    "SMOKE": ["yes", "no"],
    "CAEC": ["no", "Sometimes", "Frequently", "Always"],
    "CH2O": ["1", "2", "3"],
    "SCC": ["yes", "no"],
    "FAF": ["0", "1", "2", "3"],
    "TUE": ["0", "1", "2"],
    "CALC": ["no", "Sometimes", "Frequently", "Always"],
}

# Hàm phân loại BMI
def classify_bmi(weight, height):
    if height > 0:
        bmi = weight / (height ** 2)
        if bmi < 18.5:
            return bmi, "Underweight"
        elif 18.5 <= bmi <= 24.9:
            return bmi, "Normal"
        elif 25 <= bmi <= 29.9:
            return bmi, "Overweight"
        elif 30 <= bmi <= 34.9:
            return bmi, "Obesity I"
        elif 35 <= bmi <= 39.9:
            return bmi, "Obesity II"
        else:
            return bmi, "Obesity III"
    return None, "Invalid BMI"

# Hàm hiển thị dữ liệu trong Treeview
def display_data(df):
    for row in tree.get_children():
        tree.delete(row)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))
display_data(data_processor.data)
# Hàm lọc dữ liệu
def filter_data():
    column = filter_column.get()
    value = filter_value.get()

    if column and value:
        filtered_df = data[data[column].astype(str).str.contains(value, case=False, na=False)]
        display_data(filtered_df)
    else:
        messagebox.showwarning("Cảnh báo", "Hãy chọn cột và nhập giá trị để lọc!")
        
# Khung bộ lọc
filter_frame = ttk.LabelFrame(root, text="Lọc dữ liệu", padding=(10, 10))
filter_frame.pack(fill=tk.X, padx=10, pady=10)

ttk.Label(filter_frame, text="Cột:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
filter_column = ttk.Combobox(filter_frame, values=columns, state="readonly", width=30)
filter_column.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(filter_frame, text="Giá trị:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
filter_value = ttk.Entry(filter_frame, width=30)
filter_value.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(filter_frame, text="Lọc", command=filter_data).grid(row=0, column=4, padx=10, pady=5)
ttk.Button(filter_frame, text="Hiển thị toàn bộ", command=lambda: display_data(data)).grid(row=0, column=5, padx=10, pady=5)

# Hàm thêm dữ liệu mới
def add_data():
    new_data = []
    weight = None
    height = None

    for field, entry in zip(columns, entry_fields):
        value = entry.get()
        if value == "":
            messagebox.showwarning("Cảnh báo", f"Chưa nhập dữ liệu cho {field}!")
            return
        if field == "Weight":
            try:
                weight = float(value)
            except ValueError:
                messagebox.showerror("Lỗi", "Weight phải là số!")
                return
        elif field == "Height":
            try:
                height = float(value)
            except ValueError:
                messagebox.showerror("Lỗi", "Height phải là số!")
                return
        new_data.append(value)

    if weight is not None and height is not None:
        bmi, bmi_class = classify_bmi(weight, height)
        new_data.append(bmi_class)
    else:
        messagebox.showerror("Lỗi", "Cần có dữ liệu về Weight và Height để tính toán BMI!")
        return

    global data
    data = pd.concat([data, pd.DataFrame([new_data], columns=columns)], ignore_index=True)
    display_data(data)
    messagebox.showinfo("Thông báo", "Dữ liệu đã được thêm thành công!")

    for entry in entry_fields:
        if isinstance(entry, ttk.Combobox):
            entry.set("")
        else:
            entry.delete(0, tk.END)
            
# Khung nhập dữ liệu mới
input_frame = ttk.LabelFrame(root, text="Nhập dữ liệu mới", padding=(10, 10))
input_frame.pack(fill=tk.X, padx=10, pady=10)

entry_fields = []

columns_to_input = [col for col in columns if col != "NObeyesdad"]
half_columns = len(columns_to_input) // 2

for idx, col in enumerate(columns_to_input[:half_columns]):
    ttk.Label(input_frame, text=col).grid(row=0, column=idx, padx=5, pady=5, sticky="w")
    if col in options:
        entry = ttk.Combobox(input_frame, values=options[col], state="readonly", width=20)
    else:
        entry = ttk.Entry(input_frame, width=20)
    entry.grid(row=1, column=idx, padx=5, pady=5)
    entry_fields.append(entry)

for idx, col in enumerate(columns_to_input[half_columns:]):
    ttk.Label(input_frame, text=col).grid(row=2, column=idx, padx=5, pady=5, sticky="w")
    if col in options:
        entry = ttk.Combobox(input_frame, values=options[col], state="readonly", width=20)
    else:
        entry = ttk.Entry(input_frame, width=20)
    entry.grid(row=3, column=idx, padx=5, pady=5)
    entry_fields.append(entry)

ttk.Button(input_frame, text="Thêm dữ liệu", command=add_data).grid(row=4, column=0, columnspan=len(columns), pady=10)
# Hàm lưu dữ liệu vào tệp CSV
def save_data():
    try:
        data.to_csv(file_path, index=False)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được lưu vào tệp CSV thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu: {e}")

# Hàm xóa dữ liệu
def delete_data():
    global data
    selected_item = tree.selection()  # Lấy dòng được chọn
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Hãy chọn dòng muốn xóa!")
        return
    
    # Xóa dữ liệu từ Treeview
    for item in selected_item:
        
        values = tree.item(item, "values")
        index_to_remove = data[data.apply(tuple, axis=1) == tuple(values)].index  # Tìm index trong DataFrame
        if not index_to_remove.empty:
            data = data.drop(index_to_remove).reset_index(drop=True)  # Xóa khỏi DataFrame
        tree.delete(item)  # Xóa khỏi Treeview
    
    messagebox.showinfo("Thông báo", "Dữ liệu đã được xóa!")
    
def load_selected_data():
    """Hiển thị dữ liệu của dòng được chọn lên các ô nhập liệu."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Hãy chọn dòng muốn cập nhật!")
        return

    # Lấy giá trị của dòng được chọn
    values = tree.item(selected_item[0], "values")

    # Gán giá trị vào các ô nhập liệu
    for field, entry, value in zip(columns_to_input, entry_fields, values):
        if isinstance(entry, ttk.Combobox):
            entry.set(value)
        else:
            entry.delete(0, tk.END)
            entry.insert(0, value)

    messagebox.showinfo("Thông báo", "Dữ liệu đã được tải lên các ô nhập liệu!")

def update_data():
    """Cập nhật dòng được chọn trong DataFrame và Treeview."""
    global data
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Hãy chọn dòng muốn cập nhật!")
        return

    # Lấy giá trị từ các ô nhập liệu
    updated_data = []
    for field, entry in zip(columns_to_input, entry_fields):
        value = entry.get()
        if value == "":
            messagebox.showwarning("Cảnh báo", f"Chưa nhập dữ liệu cho {field}!")
            return
        updated_data.append(value)

    # Tính toán BMI và phân loại nếu cần
    weight = None
    height = None
    if "Weight" in columns_to_input:
        weight_idx = columns_to_input.index("Weight")
        try:
            weight = float(updated_data[weight_idx])
        except ValueError:
            messagebox.showerror("Lỗi", "Weight phải là số!")
            return

    if "Height" in columns_to_input:
        height_idx = columns_to_input.index("Height")
        try:
            height = float(updated_data[height_idx])
        except ValueError:
            messagebox.showerror("Lỗi", "Height phải là số!")
            return

    if weight is not None and height is not None:
        _, bmi_class = classify_bmi(weight, height)
        if "NObeyesdad" in columns:
            updated_data.append(bmi_class)

    # Cập nhật DataFrame
    selected_index = tree.index(selected_item[0])
    data.iloc[selected_index] = updated_data

    # Cập nhật Treeview
    tree.item(selected_item[0], values=updated_data)
    messagebox.showinfo("Thông báo", "Dữ liệu đã được cập nhật!")

    # Xóa nội dung trong các ô nhập liệu
    for entry in entry_fields:
        if isinstance(entry, ttk.Combobox):
            entry.set("")
        else:
            entry.delete(0, tk.END)


# Nút lưu, xuất và xóa file
action_frame = ttk.Frame(root)
action_frame.pack(fill=tk.X, padx=10, pady=10)

ttk.Button(action_frame, text="Tải dữ liệu đã chọn", command=load_selected_data).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(action_frame, text="Cập nhật dữ liệu", command=update_data).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(action_frame, text="Lưu dữ liệu vào CSV", command=save_data).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(action_frame, text="Xóa dữ liệu", command=delete_data).pack(side=tk.LEFT, padx=5, pady=5)
ttk.Button(action_frame, text="Hiển thị biểu đồ", command=lambda: draw_chart(file_path)).pack(side=tk.LEFT, padx=5, pady=5)

# Chạy ứng dụng Tkinter
root.mainloop()

