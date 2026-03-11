import numpy as np
from PIL import Image, ImageDraw
import math


################################
# TEXT CONVERSION
################################

def text_to_bits(text):
    return ''.join(format(ord(c),'08b') for c in text)


def bits_to_text(bits):

    chars=[]

    for i in range(0,len(bits),8):

        byte = bits[i:i+8]
        chars.append(chr(int(byte,2)))

    return ''.join(chars)


################################
# IMAGE QUALITY METRICS
################################

def mse(original,stego):

    img1 = np.array(Image.open(original).convert("L"))
    img2 = np.array(Image.open(stego).convert("L"))

    return np.mean((img1-img2)**2)


def psnr(original,stego):

    error = mse(original,stego)

    if error == 0:
        return 100

    return 10 * math.log10((255**2)/error)


################################
# CAPACITY CALCULATION
################################

def embedding_capacity(bits,image_path):

    img = Image.open(image_path)
    w,h = img.size

    pixels = w*h

    return bits/pixels


################################
# TILE VISUALIZATION
################################

def draw_tiles(image_path,tiles):

    img = Image.open(image_path).convert("RGB")

    draw = ImageDraw.Draw(img)

    for tile in tiles:

        r,c,m,n = tile

        draw.rectangle(
            [(c,r),(c+n,r+m)],
            outline="red",
            width=1
        )

    output = "static/tile_map.png"

    img.save(output)

    return output