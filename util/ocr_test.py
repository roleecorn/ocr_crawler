from PIL import Image
import pytesseract
def ORC(img,x,y,w,h):
    #box coor: left, top, right, bottom
    img2 = Image.open(img).crop([x,y,x+w,y+h])
    return pytesseract.image_to_string(img2)