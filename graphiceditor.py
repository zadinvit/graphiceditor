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
    imgarr = np.asarray(img_arr)
    img2=np.copy(imgarr)
    imgarr.setflags(write=1) #nutno aby se dalo přepisovat hodnotu v poli, pole je jinak read only

    for i in range(3):

        if float(level) > 1:

            for j in range(0, imgarr[:, :, i].shape[0] - 1):
                for k in range(0, imgarr[:, :, i].shape[1] - 1):

                    subpixel=imgarr[:, :, i][j][k] * float(level)
                    if subpixel >= 255:
                        imgarr[:, :, i][j][k] = 255
                    else:
                        imgarr[:, :, i][j][k] = subpixel
            # img2 = img_arr.point(lambda p: p * 1.9) rychlejší zesvětlení pomocí knihovny pillow

        else:
            imgarr = imgarr[:, :, i] * float(level)



    fin_img = Image.fromarray(imgarr)
    return fin_img
def seda(img):
    imgarr = np.asarray(img)
    imgarr.setflags(write=1)
    imgarr2= np.copy(imgarr)
    for i in range(0, imgarr.shape[0] - 1):
        for j in range(0, imgarr.shape[1] - 1):
            imgarr2[i][j][0] = imgarr[i][j][0] * 0.299 + imgarr[i][j][2] * 0.114 + imgarr[i][j][1] * 0.587
            imgarr2[i][j][1] = imgarr[i][j][0] * 0.299 + imgarr[i][j][2] * 0.114 + imgarr[i][j][1] * 0.587
            imgarr2[i][j][2] = imgarr[i][j][0] * 0.299 + imgarr[i][j][2] * 0.114 + imgarr[i][j][1] * 0.587
    fin_img = Image.fromarray(imgarr2)
    return  fin_img

image_name = input("Zadejte cestu k obrázku: \n")
img = Image.open(image_name)

uprava= input("1) Inverze\n2) Úrovně (zesvětlit, ztmavit)\n3) Převést obrázek do úrovní šedi \nZadejte číslo úpravy: \n")
if int(uprava) == 1:
    fin_img = inverze(img)
elif int(uprava) == 2:
    fin_img = levels(img)
elif int(uprava) == 3:
    fin_img = seda(img)

image_out=input("Uložit obrázek jako: ")

fin_img.save(image_out)
print("Obrázek byl uložen jako: " + image_out)