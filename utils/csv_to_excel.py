import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import openpyxl
from openpyxl.styles import Font

def csv_to_excel():
    """将 CSV 文件转换为 Excel 文件，并将所有字体设置为微软雅黑"""
    root = tk.Tk()
    root.withdraw()

    csv_file_path = filedialog.askopenfilename(
        title="选择 CSV 文件",
        filetypes=[("CSV 文件", "*.csv"), ("所有文件", "*.*")]
    )

    if not csv_file_path:
        return

    try:
        df = pd.read_csv(csv_file_path)
        excel_file_path = csv_file_path.replace(".csv", ".xlsx")

        # 将 DataFrame 写入 Excel 文件
        df.to_excel(excel_file_path, index=False)

        # 使用 openpyxl 设置字体
        workbook = openpyxl.load_workbook(excel_file_path)
        font = Font(name="微软雅黑")

        for sheet in workbook: # 遍历所有工作表
            sheet.delete_cols(1) # 删除第一列
            for row in sheet:
                for cell in row:
                    cell.font = font

        workbook.save(excel_file_path)

        messagebox.showinfo("成功", f"CSV 文件已成功转换为 Excel 文件：\n{excel_file_path}")

    except Exception as e:
        messagebox.showerror("错误", f"转换过程中出现错误：\n{e}")

if __name__ == "__main__":
    csv_to_excel()