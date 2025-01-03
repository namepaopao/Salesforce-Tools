import fitz  # PyMuPDF
import json
import argparse
import requests
import io
from PIL import Image
import pytesseract
import os

def scan_pdf(pdf_path_or_url, enable_ocr=False):
    """
    扫描 PDF 文档并提取文本内容。

    Args:
        pdf_path_or_url: PDF 文件的本地路径或 URL。
        enable_ocr: 是否启用 OCR 功能 (默认 False)。

    Returns:
        一个字典，包含 PDF 的页数和每页的文本内容。
    """
    try:
        if pdf_path_or_url.startswith("http"):
            # 通过 URL 下载 PDF
            response = requests.get(pdf_path_or_url, stream=True)
            response.raise_for_status()  # 检查请求是否成功
            doc = fitz.open(stream=response.content, filetype="pdf")
        else:
            # 打开本地 PDF 文件
            doc = fitz.open(pdf_path_or_url)

        results = {"page_count": doc.page_count, "pages": []}
        for page in doc:
            if enable_ocr:
                # 使用 OCR 提取文本
                image_list = page.get_images(full=True)
                text = ""
                for img in image_list:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_data = base_image["image"]
                    try:
                        pil_image = Image.open(io.BytesIO(image_data))
                        text += pytesseract.image_to_string(pil_image) + "\n"
                    except Exception as e:
                        print(f"Error during OCR: {e}")
                        text += "\n" # OCR 失败时添加换行符
            else:
                # 直接提取文本
                text = page.get_text()

            results["pages"].append({"page_number": page.number + 1, "text": text})
        doc.close()

        return results
    except requests.exceptions.RequestException as e:
        return {"error": f"Error downloading PDF: {e}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scan a PDF file and extract text content.")
    parser.add_argument("pdf_source", help="Path to the PDF file or a URL to the PDF file.")
    parser.add_argument("--ocr", action="store_true", help="Enable OCR for scanned PDFs.")
    args = parser.parse_args()

    result = scan_pdf(args.pdf_source, enable_ocr=args.ocr)
    print(json.dumps(result, indent=4))