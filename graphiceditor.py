import numpy as np
import sys
from PIL import Image
def inverze(img):
    """Tato funkce vytvoří inverzi obrazu. Vstup je pouze cesta k obrazu
    :param img:
    :return:
    """
    # práce s obrázky inverzní obraz
    imgarr = np.asarray(img)
    imgarr = 255 - imgarr
    imgarr = Image.fromarray(imgarr)
    return imgarr

def levels(img_arr):
    """
    SLouží ke zesvětlení/ztmavení obrázku. Vstup je image a poté se do proměnné level načte ze vstupu číslo, pokud je toto číslo menší jak 1 obrázek se ztmaví např. 0.5, případně 1.5 to zase obrázek zesvětlí.
    :param img_arr:
    :return:
    """
    level = input("Pro ztmavení zadejte desetinné číslo od 0-1.0 pro zesvětlení číslo >1.0\n")
    imgarr = np.asarray(img_arr)
    img2=np.copy(imgarr)
    imgarr.setflags(write = 1) #nutno aby se dalo přepisovat hodnotu v poli, pole je jinak read only

    for i in range(3):
    #forcyklus přes jednotlivé barvy
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
            imgarr[:, :, i]= imgarr[:, :, i] * float(level)


    fin_img = Image.fromarray(imgarr)
    return fin_img
def seda(img):
    """
    Vstup je obrázek, funkce převede obrázek do odstínů šedi. Uživatel zadává jen cestu k obrázku
    :param img:
    :return:
    """
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
def hrany_filter(data):
    """
    Vektorizovaný filter pro vyhledání hran. Vstupem je část obrázku.
    :param data:
    :return:
    """
    output = np.zeros(data.shape[:2])
    output = (
            -data[0:-2, 0:-2] - data[0:-2, 1:-1] - data[0:-2, 2:] -
            data[1:-1, 0:-2] + 9 * data[1:-1, 1:-1] - data[1:-1, 2:] -
            data[2:, 0:-2] - data[2:, 1:-1] - data[2:, 2:]
    )
    return output
def hrany(img):
    """
    Vstupem je obrázek (cesta).
    :param img:
    :return:
    """
    imgarr = np.asarray(img, dtype=np.float)
    X, Y, Z = imgarr.shape
    fin = np.zeros([X - 2, Y - 2, Z])

    # aplikace filtru
    for i in range(3):
        fin[:, :, i] = hrany_filter(imgarr[:, :, i])
    fin_img = np.clip(fin, 0, 255)
    fin_img = np.asarray(fin_img, dtype=np.uint8)
    img_out = Image.fromarray(fin_img)
    return img_out

bez=1
while bez:
    try:
        image_name = input("Zadejte cestu k obrázku: \n")
        img = Image.open(image_name)
        bez=0
        pass
    except IOError as ioe:
        print('\033[41m'+"Tento obrázek neexistuje!"+ '\033[0m')
        pass



uprava= input("1) Inverze\n2) Úrovně (zesvětlit, ztmavit)\n3) Převést obrázek do úrovní šedi \n4) Zvýraznění hran \nZadejte číslo úpravy: \n")
if int(uprava) == 1:
    fin_img = inverze(img)
elif int(uprava) == 2:
    fin_img = levels(img)
elif int(uprava) == 3:
    fin_img = seda(img)
elif int(uprava) == 4:
    fin_img = hrany(img)
else:
    sys.exit()

image_out=input("Uložit obrázek jako: ")

fin_img.save(image_out)
print("Obrázek byl uložen jako: " + image_out)