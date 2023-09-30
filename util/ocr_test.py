from PIL import Image
import pytesseract
import os
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = os.getenv('TessartPath')
print(pytesseract.pytesseract.tesseract_cmd)


def Ocr(img: Path, posit: dict):
    """
    輸入一張圖片與對象範圍，回傳範圍內的文字
    - x: X座標
    - y: Y座標
    - w: 寬度
    - h: 高度
    """
    x, y, w, h = posit['X'], posit['Y'], posit['w'], posit['h']

    if w < 0:
        x, w = x + w, -w
    if h < 0:
        y, h = y + h, -h

    img2 = Image.open(img)

    # Ensure cropping is within image boundaries
    x = max(0, x)
    y = max(0, y)
    w = min(img2.width - x, w)
    h = min(img2.height - y, h)

    img2 = img2.crop([x, y, x + w, y + h])
    # img2.show()

    return pytesseract.image_to_string(img2)


if __name__ == "__main__":
    src = '..\\src\\s.png'
    data = {"name": "name", "X": 8, "Y": 8, "w": 140, "h": 21}
    text = Ocr(img=src, x=data['X'], y=data['Y'], w=data['w'], h=data['h'])
    print(text)
