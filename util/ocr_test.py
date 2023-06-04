from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'D:\\program\\Tesseract-OCR\\tesseract.exe'


def Ocr(img,x,y,w,h):
    #box coor: left, top, right, bottom
    img2 = Image.open(img)
    img2=img2.crop([x,y,x+w,y+h])
    img2.show()
    return pytesseract.image_to_string(img2)


if __name__ == "__main__":
    src = '..\\src\\s.png'
    data = {"name": "name", "X": 8, "Y": 8,"w": 140, "h": 21}
    text = Ocr(img=src, x=data['X'], y=data['Y'], w=data['w'], h=data['h'])
    print(text)
