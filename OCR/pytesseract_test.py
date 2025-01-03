import os

import pytesseract
from PIL import Image

def get_tesseract_path():
    """
       获取 Tesseract OCR 的可执行文件路径，先从用户环境变量中查找，
       然后从系统环境变量中查找，最后返回 None
       """
    tesseract_path = os.environ.get('TESSERACT_CMD')
    if tesseract_path and os.path.isfile(tesseract_path):
        return tesseract_path
    
    path_var = os.environ.get('PATH')
    if path_var:
        paths = path_var.split(os.pathsep)
        for path in paths:
            tesseract_path = os.path.join(path, 'tesseract.exe')
            if os.path.isfile(tesseract_path):
                return tesseract_path
    
    return None

# 获取 Tesseract 路径
tesseract_path = get_tesseract_path()

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

    image = Image.open("../data/images/m2-eng-test.png")
    image1 = Image.open("../data/images/google-logo-test.png")
    image2 = Image.open("../data/images/img.png")

    text = pytesseract.image_to_string(image, lang='eng')
    text1 = pytesseract.image_to_string(image1, lang='chi_sim')
    text2 = pytesseract.image_to_string(image2, lang='chi_sim')

    print(text)
    print("------------------------------------------------")
    print(text1)
    print("------------------------------------------------")
    print(text2)
else:
    print("未找到 Tesseract OCR 的可执行文件路径。请确保已安装 Tesseract，并将其路径添加到环境变量 TESSERACT_CMD 或 PATH 中。")
    print("或者手动指定路径：pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'")