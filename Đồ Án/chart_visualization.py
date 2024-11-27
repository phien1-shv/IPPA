import matplotlib.pyplot as plt
import pandas as pd

def draw_chart(file_path):
    # Hàm để vẽ biểu đồ phân bố mức độ béo phì từ file CSV.
    data = pd.read_csv(file_path)

    # Đếm số lượng từng loại mức độ béo phì
    category_counts = data['NObeyesdad'].value_counts()

    # Chuẩn bị dữ liệu cho biểu đồ
    categories = category_counts.index
    counts = category_counts.values

    # Vẽ biểu đồ cột với đường lưới
    plt.figure(figsize=(12, 7))
    bar_width = 0.7  # Giảm chiều rộng của cột
    x_positions = range(len(categories))  # Vị trí các cột
    
    bars = plt.bar(x_positions, counts, color=['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'gray'], width=bar_width)
    
    plt.xticks(x_positions, categories, fontsize=8) 
    plt.xlabel('Danh mục mức độ béo phì', fontsize=10)
    plt.ylabel('Số lượng bản ghi', fontsize=10)
    plt.title('Phân bố mức độ béo phì', fontsize=12)

    # Thêm giá trị trên mỗi cột
    for bar, category in zip(bars, categories):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 2, int(yval), ha='center', fontsize=10)
        bar.set_label(category)

    # Thêm chú thích
    plt.legend(title='Danh mục', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()


