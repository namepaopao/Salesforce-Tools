import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def excel_to_csv():
    """将 Excel 文件转换为 CSV 文件"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    # 让用户选择 Excel 文件
    excel_file_path = filedialog.askopenfilename(
        title="选择 Excel 文件",
        filetypes=[("Excel 文件", "*.xlsx *.xls"), ("所有文件", "*.*")]
    )

    if not excel_file_path:
        return  # 用户取消选择

    try:
        # 读取 Excel 文件
        df = pd.read_excel(excel_file_path)

        # 生成 CSV 文件名
        csv_file_path = excel_file_path.replace('.xlsx', '.csv').replace('.xls', '.csv')
        
        # 将 DataFrame 写入 CSV 文件
        df.to_csv(csv_file_path, index=False)

        messagebox.showinfo("成功", f"Excel 文件已成功转换为 CSV 文件：\n{csv_file_path}")

    except Exception as e:
        messagebox.showerror("错误", f"转换过程中出现错误：\n{e}")

if __name__ == "__main__":
    excel_to_csv()