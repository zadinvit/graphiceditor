import numpy as np
import sys
from PIL import Image
def inverze(img):
    # práce s obrázky inverzní obraz
    imgarr = np.asarray(img)
    imgarr = 255 - imgarr
    imgarr = Image.fromarray(imgarr)
    return imgarr

def levels(img_arr):
    level = input("Pro ztmavení zadejte desetinné číslo od 0-1.0 pro zesvětlení číslo >1.0\n")
    img2 = img_arr.point(lambda p: p * float(level))
    return img2

image_name = input("Zadejte cestu k obrázku: \n")
img = Image.open(image_name)

uprava= input("1) Inverze\n2) Úrovně (zesvětlit, ztmavit) \nZadejte číslo úpravy: \n")
if int(uprava) == 1:
    fin_img = inverze(img)
elif int(uprava) == 2:
    fin_img = levels(img)

image_out=input("Uložit obrázek jako: ")

fin_img.save(image_out)
print("Obrázek byl uložen jako: " + image_out)