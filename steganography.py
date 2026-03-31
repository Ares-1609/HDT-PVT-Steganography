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
        seed = int(hash_val, 16) % 1000000

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
# TEXTURE
####################################

def texture_score(tile):
    return float(np.var(tile.astype(np.float32)))


####################################
# ADAPTIVE THRESHOLD (MEDIAN BLOCK VARIANCE)
####################################

def compute_threshold(pixels):
    H, W = pixels.shape
    H_crop = H - (H % 3)
    W_crop = W - (W % 3)
    
    if H_crop == 0 or W_crop == 0:
        return 0.0
        
    blocks = pixels[:H_crop, :W_crop].reshape(H_crop // 3, 3, W_crop // 3, 3)
    blocks = blocks.swapaxes(1, 2).reshape(-1, 3, 3)
    
    variances = np.var(blocks, axis=(1, 2), dtype=np.float32)
    return float(np.median(variances))


####################################
# EMBEDDING
####################################

def embed_data(image_path, message, key):

    img = Image.open(image_path).convert("L")
    pixels = np.array(img, dtype=np.int32)   # use int32 to avoid uint8 overflow throughout

    logistic = LogisticMap(key)

    # --- Adaptive Threshold ---
    raw_threshold = compute_threshold(pixels)
    threshold_int = int(raw_threshold)

    # Clamp threshold to fit in 2 bytes (max 65535)
    threshold_int = min(threshold_int, 65535)

    # Store threshold in first 2 pixels (low byte, high byte)
    pixels[0][0] = threshold_int % 256
    pixels[0][1] = threshold_int // 256
    threshold = float(threshold_int)

    # --- Message ---
    message_bits = text_to_bits(message)
    length = format(len(message_bits), '032b')
    bits = length + message_bits

    bit_index = 0
    total_bits = len(bits)

    H, W = pixels.shape

    row = 0
    col = 2   # skip reserved pixels
    row_max_m = 0

    tiles = []

    while row < H and bit_index < total_bits:

        m, n = generate_tile(logistic, row, col, H, W)
        row_max_m = max(row_max_m, m)

        if m <= 0 or n <= 0:
            col += max(n, 1)
            if col >= W:
                col = 0
                row += max(row_max_m, 1)
                row_max_m = 0
            continue

        tile = pixels[row:row + m, col:col + n].copy()
        tiles.append((row, col, m, n))

        P = m * n
        pivot_index = int(logistic.next() * P) % P
        pivot_r = pivot_index // n
        pivot_c = pivot_index % n
        pivot = int(tile[pivot_r][pivot_c])

        threshold_local = texture_score(tile)
        is_textured = 1 if threshold_local >= threshold else 0
        
        pivot = (pivot & ~1) | is_textured
        tile[pivot_r][pivot_c] = pivot

        for i in range(m):
            for j in range(n):

                if i == pivot_r and j == pivot_c:
                    continue

                if bit_index >= total_bits:
                    break

                p = int(tile[i][j])
                d = abs(p - pivot)

                if not is_textured:
                    ranges = [
                        (0,  7,  1),
                        (8,  15, 2),
                        (16, 31, 2)
                    ]
                else:
                    ranges = [
                        (0,  7,  1),
                        (8,  15, 2),
                        (16, 31, 3),
                        (32, 63, 4)
                    ]

                for lower, upper, k in ranges:
                    if lower <= d <= upper:

                        secret_bits = bits[bit_index:bit_index + k]

                        if len(secret_bits) < k:
                            secret_bits = secret_bits.ljust(k, '0')

                        value = int(secret_bits, 2)
                        d_new = lower + value

                        if p >= pivot:
                            p_new = pivot + d_new
                            if p_new > 255: 
                                p_new = pivot - d_new
                        else:
                            p_new = pivot - d_new
                            if p_new < 0: 
                                p_new = pivot + d_new

                        p_new = max(0, min(255, p_new))
                        tile[i][j] = p_new
                        bit_index += k
                        break

            if bit_index >= total_bits:
                break

        pixels[row:row + m, col:col + n] = tile

        col += n
        if col >= W:
            col = 0
            row += row_max_m
            row_max_m = 0

    stego = Image.fromarray(pixels.astype(np.uint8))
    output_path = "static/stego.png"
    stego.save(output_path)

    return output_path, tiles


####################################
# EXTRACTION
####################################

def extract_data(image_path, key):

    img = Image.open(image_path).convert("L")
    pixels = np.array(img, dtype=np.int32)   # int32 to avoid uint8 overflow

    logistic = LogisticMap(key)

    # --- Retrieve Threshold ---
    threshold_int = int(pixels[0][0]) + int(pixels[0][1]) * 256
    threshold = float(threshold_int)

    H, W = pixels.shape

    row = 0
    col = 2 
    row_max_m = 0

    bits = ""
    message_length = None

    while row < H:
        m, n = generate_tile(logistic, row, col, H, W)
        row_max_m = max(row_max_m, m)

        if m <= 0 or n <= 0:
            col += max(n, 1)
            if col >= W:
                col = 0
                row += max(row_max_m, 1)
                row_max_m = 0
            continue

        tile = pixels[row:row + m, col:col + n]

        P = m * n
        pivot_index = int(logistic.next() * P) % P
        pivot_r = pivot_index // n
        pivot_c = pivot_index % n
        pivot = int(tile[pivot_r][pivot_c])

        is_textured = pivot & 1
        done = False

        for i in range(m):
            for j in range(n):

                if i == pivot_r and j == pivot_c:
                    continue

                p = int(tile[i][j])
                d = abs(p - pivot)

                if not is_textured:
                    ranges = [
                        (0,  7,  1),
                        (8,  15, 2),
                        (16, 31, 2)
                    ]
                else:
                    ranges = [
                        (0,  7,  1),
                        (8,  15, 2),
                        (16, 31, 3),
                        (32, 63, 4)
                    ]

                for lower, upper, k in ranges:
                    if lower <= d <= upper:

                        value = d - lower
                        bits += format(value, f'0{k}b')

                        if message_length is None and len(bits) >= 32:
                            message_length = int(bits[:32], 2)
                            bits = bits[32:]

                        if message_length is not None and len(bits) >= message_length:
                            message_bits = bits[:message_length]
                            return bits_to_text(message_bits)

                        break

            if done:
                break

        col += n
        if col >= W:
            col = 0
            row += row_max_m
            row_max_m = 0

    if message_length is not None and len(bits) > 0:
        message_bits = bits[:message_length] if len(bits) >= message_length else bits
        try:
            return bits_to_text(message_bits)
        except Exception:
            pass

    return ""