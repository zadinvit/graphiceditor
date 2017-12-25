import numpy as np
import sys
from PIL import Image

image_name="kvetina.jpg"
#práce s obrázky inverzní obraz
img = Image.open(image_name)
imgarr = np.asarray(img)
print(imgarr)
imgarr = 255-imgarr
j = Image.fromarray(imgarr)
j.save("kvetina"+"out.jpeg")