import numpy as np
import sys
from PIL import Image
def is_number(s):
    """
    Kontroluje jestli je string číslo
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
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
    bez = 1
    while bez:
        level = input("Pro ztmavení zadejte desetinné číslo od 0-1.0 pro zesvětlení číslo >1.0\n")
        if is_number(level):
            if float(level) >= 0:
                bez = 0
            else:
                print('\033[41m' + "Číslo nesmí být záporné!" + '\033[0m')
        else:
            print('\033[41m' + "Nezadali jste číslo" + '\033[0m')


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
def rotate_coords(x, y, theta, ox, oy):
    """
    Otočí pole x a y podle úhlu theta okolo bodu ox, oy(nastaveno na střed obrázku)
    :param x:
    :param y:
    :param theta: úhel otočení
    :param ox: souřadnice x středu (bodu otočení)
    :param oy: souřadnice y středu (bodu otočení)
    :return:
    """


    s, c = np.sin(theta), np.cos(theta)

    x, y = np.asarray(x) - ox, np.asarray(y) - oy
    return x * c - y * s + ox, x * s + y * c + oy

def rotate_image(src, theta, ox, oy, fill=255):
    """
    Otočí obrázek podle úhlu theta a podle souřadni ox, oy - v tomto případě střed obrázku
    :param src: zdrojový obrázek
    :param theta: úhel otočení
    :param ox: střed obrázku
    :param oy: střed obrázku
    :param fill:
    :return:
    """
    #musím otočit úhel aby se rotovalo správně
    theta = -theta

    sh, sw = src.shape

    cx, cy = rotate_coords([0, sw, sw, 0], [0, 0, sh, sh], theta, ox, oy)

    dw, dh = (int(np.ceil(c.max() - c.min())) for c in (cx, cy))

    dx, dy = np.meshgrid(np.arange(dw), np.arange(dh))

    sx, sy = rotate_coords(dx + cx.min(), dy + cy.min(), -theta, ox, oy)

    sx, sy = sx.round().astype(int), sy.round().astype(int)

    mask = (0 <= sx) & (sx < sw) & (0 <= sy) & (sy < sh)

    dest = np.empty(shape=(dh, dw), dtype=src.dtype)

    dest[dy[mask], dx[mask]] = src[sy[mask], sx[mask]]

    dest[dy[~mask], dx[~mask]] = fill

    return dest
def rotate(img):
    """
    Přijme obrázek, načte úhel(angle) a ten obrázek otočí podle zadaného úhlu.
    :param img:
    :return:
    """
    imgarr = np.asarray(img)
    r, g, b = np.rollaxis(imgarr, axis=-1)
    bez=1
    while bez:
        angle = input("Zadejte úhel, o který chcete obrázek otočit: \n")
        if is_number(angle):
            bez=0
        else:
            print('\033[41m'+"Nezadali jste číslo"+ '\033[0m')

    r2 = rotate_image(r, int(angle) * np.pi / 180, int(imgarr.shape[0] // 2), int(imgarr.shape[1] // 2))
    g2 = rotate_image(g, int(angle) * np.pi / 180, int(imgarr.shape[0] // 2), int(imgarr.shape[1] // 2))
    b2 = rotate_image(b, int(angle) * np.pi / 180, int(imgarr.shape[0] // 2), int(imgarr.shape[1] // 2))
    img2 = np.dstack((r2, g2, b2))
    fin_img = Image.fromarray(img2)
    return fin_img
def zrcadleni(img):
    """
    Převrátí obrázek zrcadlově, buďto vertikální po zadání 0, nebo horizontálně po zadání 1.
    :param img: vstupní obrázek
    :return:
    """
    imgarr = np.asarray(img)
    bez =1
    while bez:
        volba = input("Pro horizontální převrácení zadejte 1, pro vertikální 0: \n")
        if is_number(volba):
            if int(volba) == 1 or int(volba) == 0:
                bez = 0
            else:
                print('\033[41m' + "Zadejte prosím 0 nebo 1." + '\033[0m')
        else:
            print('\033[41m' + "Nezadali jste číslo" + '\033[0m')
    img2 = np.flip(imgarr,int(volba))
    fin_img = Image.fromarray(img2)
    return fin_img
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



uprava= input("1) Inverze\n2) Úrovně (zesvětlit, ztmavit)\n3) Převést obrázek do úrovní šedi \n4) Zvýraznění hran \n5) Rotace obrázku\n6) Zrcadlové převrácení\nZadejte číslo úpravy: \n")
if int(uprava) == 1:
    fin_img = inverze(img)
elif int(uprava) == 2:
    fin_img = levels(img)
elif int(uprava) == 3:
    fin_img = seda(img)
elif int(uprava) == 4:
    fin_img = hrany(img)
elif int(uprava) == 5:
    fin_img = rotate(img)
elif int(uprava) == 6:
    fin_img = zrcadleni(img)
else:
    sys.exit()

image_out=input("Uložit obrázek jako: ")

fin_img.save(image_out)
print("Obrázek byl uložen jako: " + image_out)