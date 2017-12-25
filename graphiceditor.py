import numpy as np
import sys
from PIL import Image
def inverze(image_name):
    # práce s obrázky inverzní obraz
    img = Image.open(image_name)
    imgarr = np.asarray(img)
    imgarr = 255 - imgarr
    j = Image.fromarray(imgarr)
    image_out=input("Uložit obrázek jako: ")
    j.save(image_out)
    print("Obrázek byl uložen jako:" + image_out)
image_name= input("Zadejte cestu k obrázku: \n")
inverze(image_name)

