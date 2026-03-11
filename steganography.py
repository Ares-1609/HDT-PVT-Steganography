import numpy as np
from PIL import Image
import hashlib
from utils import text_to_bits, bits_to_text


####################################
# CHAOTIC LOGISTIC MAP GENERATOR
####################################

class LogisticMap:

    def __init__(self, key):

        hash_val = hashlib.sha256(key.encode()).hexdigest()
        seed = int(hash_val,16) % 1000000
        self.x = (seed % 1000) / 1000
        self.r = 3.99

    def next(self):

        self.x = self.r * self.x * (1 - self.x)
        return self.x


####################################
# TILE GENERATION
####################################

def generate_tile(logistic, row, col, H, W):

    m = int(logistic.next() * 14) + 2
    n = int(logistic.next() * 14) + 2

    if row + m > H:
        m = H - row

    if col + n > W:
        n = W - col

    return m, n

####################################
# TEXTURE MEASUREMENT
####################################

def texture_score(tile):

    return np.var(tile)


####################################
# EMBEDDING FUNCTION
####################################

def embed_data(image_path,message,key):

    img = Image.open(image_path).convert("L")
    pixels = np.array(img)

    logistic = LogisticMap(key)

    message_bits = text_to_bits(message)

    length = format(len(message_bits), '032b')

    bits = length + message_bits
    bit_index = 0

    H,W = pixels.shape

    row = 0
    col = 0

    tiles = []

    while row < H and bit_index < len(bits):

        m,n = generate_tile(logistic, row, col, H, W)

        if row + m > H:
            m = H - row

        if col + n > W:
            n = W - col

        tile = pixels[row:row+m, col:col+n]

        tiles.append((row,col,m,n))

        P = m*n

        pivot_index = int(logistic.next()*P)

        pivot_r = pivot_index // n
        pivot_c = pivot_index % n

        pivot = tile[pivot_r][pivot_c]

        texture = texture_score(tile)

        for i in range(m):
            for j in range(n):

                if i == pivot_r and j == pivot_c:
                    continue

                if bit_index >= len(bits):
                    pixels[row:row+m, col:col+n] = tile
                    stego = Image.fromarray(pixels.astype(np.uint8))
                    output_path = "static/stego.png"
                    stego.save(output_path)
                    return output_path, tiles

                p = tile[i][j]

                d = abs(int(p) - int(pivot))

                # Texture adaptive ranges
                if texture < 20:

                    ranges = [
                        (0,7,1),
                        (8,15,2),
                        (16,31,2)
                    ]

                else:

                    ranges = [
                        (0,7,1),
                        (8,15,2),
                        (16,31,3),
                        (32,63,4)
                    ]

                for lower,upper,k in ranges:

                    if d >= lower and d <= upper:

                        secret_bits = bits[bit_index:bit_index+k]

                        if len(secret_bits) < k:
                            secret_bits = secret_bits.ljust(k,'0')

                        value = int(secret_bits,2)

                        d_new = lower + value

                        if p >= pivot:
                            p_new = pivot + d_new
                        else:
                            p_new = pivot - d_new

                        p_new = max(0,min(255,p_new))

                        tile[i][j] = p_new

                        bit_index += k
                        break

        pixels[row:row+m, col:col+n] = tile

        col += n

        if col >= W:

            col = 0
            row += m

    stego = Image.fromarray(pixels.astype(np.uint8))

    output_path = "static/stego.png"
    stego.save(output_path)

    return output_path, tiles


####################################
# EXTRACTION FUNCTION
####################################

def extract_data(image_path,key):

    img = Image.open(image_path).convert("L")
    pixels = np.array(img)

    logistic = LogisticMap(key)

    H,W = pixels.shape

    row = 0
    col = 0

    bits = ""
    message_length = None

    while row < H:

        m,n = generate_tile(logistic, row, col, H, W)

        if row + m > H:
            m = H - row

        if col + n > W:
            n = W - col

        tile = pixels[row:row+m, col:col+n]

        P = m*n

        pivot_rand = logistic.next()
        pivot_index = int(pivot_rand * P) % P   

        pivot_r = pivot_index // n
        pivot_c = pivot_index % n

        pivot = tile[pivot_r][pivot_c]

        texture = texture_score(tile)

        for i in range(m):
            for j in range(n):

                if i == pivot_r and j == pivot_c:
                    continue

                p = tile[i][j]

                d = abs(int(p) - int(pivot))

                if texture < 20:

                    ranges = [
                        (0,7,1),
                        (8,15,2),
                        (16,31,2)
                    ]

                else:

                    ranges = [
                        (0,7,1),
                        (8,15,2),
                        (16,31,3),
                        (32,63,4)
                    ]

                for lower,upper,k in ranges:

                    if d >= lower and d <= upper:

                        value = d - lower

                        bits += format(value,f'0{k}b')

                        # Read message length
                        if message_length is None and len(bits) >= 32:

                            length_bits = bits[:32]
                            message_length = int(length_bits,2)

                            bits = bits[32:]

                        # Extract message
                        if message_length is not None and len(bits) >= message_length:

                            message_bits = bits[:message_length]

                            return bits_to_text(message_bits)

        col += n

        if col >= W:

            col = 0
            row += m

    return ""