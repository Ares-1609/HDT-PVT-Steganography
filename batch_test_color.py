import os
import csv
import cv2
import numpy as np
import math
from steganography_color import embed_data_color
from utils import embedding_capacity, draw_tiles

# ---------------------------------------------------------
# CUSTOM COLOR METRICS (Bypassing utils.py Grayscale Lock)
# ---------------------------------------------------------
def mse_color(original_path, stego_path):
    """Calculates Mean Squared Error across all 3 color channels (BGR)."""
    img1 = cv2.imread(original_path).astype(np.float32)
    img2 = cv2.imread(stego_path).astype(np.float32)
    
    # np.mean averages the error across Height, Width, and Channels
    return float(np.mean((img1 - img2) ** 2))

def psnr_color(original_path, stego_path):
    """Calculates Peak Signal-to-Noise Ratio for color images."""
    error = mse_color(original_path, stego_path)
    if error == 0:
        return 100.0
    return 10 * math.log10((255 ** 2) / error)

# ---------------------------------------------------------
# BATCH TESTING LOGIC
# ---------------------------------------------------------
def run_batch_tests_color():
    output_dir = 'color-results'
    os.makedirs(output_dir, exist_ok=True)
    
    # Ensure static exists because draw_tiles temporarily saves there
    os.makedirs('static', exist_ok=True) 

    # The RGB images you prepared
    images = ['baboon_color.png', 'jet_color.png', 'peppers_color.png']
    
    # Testing massive payloads (1.5KB, 3KB, 6KB, and 10.5KB)
    payload_sizes = [1500, 3000, 6000, 10500] 
    key = "vit_secure_123"

    csv_path = os.path.join(output_dir, 'performance_table_color.csv')
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image Name', 'Payload (Bytes)', 'Capacity (bpp)', 'MSE', 'PSNR (dB)'])

        for img_name in images:
            img_path = f"datasets/{img_name}"
            
            if not os.path.exists(img_path):
                print(f"⚠️ Skipping {img_name} - not found in datasets folder.")
                continue

            print(f"\n--- Testing {img_name} ---")

            for size in payload_sizes:
                # Generate a dummy payload exactly matching the target byte size
                message = 'A' * size
                
                # 1. Embed data AND capture the generated tiles
                stego_temp_path, tiles = embed_data_color(img_path, message, key)
                
                # 2. Draw the tiles using the existing utility function
                tiled_temp_path = draw_tiles(img_path, tiles)
                
                # 3. Move both files to the new color-results folder and rename
                final_stego = f"{output_dir}/stego_{size}B_{img_name}"
                final_tiled = f"{output_dir}/tiled_{size}B_{img_name}"
                
                # Clean up old files if re-running
                if os.path.exists(final_stego):
                    os.remove(final_stego)
                if os.path.exists(final_tiled):
                    os.remove(final_tiled)
                    
                os.rename(stego_temp_path, final_stego)
                os.rename(tiled_temp_path, final_tiled)
                
                # 4. Calculate true color metrics
                current_mse = mse_color(img_path, final_stego)
                current_psnr = psnr_color(img_path, final_stego)
                cap = embedding_capacity(size * 8, img_path) 
                
                # 5. Write to CSV and console
                writer.writerow([img_name, size, cap, current_mse, current_psnr])
                print(f"Payload: {size}B | PSNR: {current_psnr:.2f} dB | MSE: {current_mse:.4f}")

    print(f"\n✅ Color batch testing complete! Check the '{output_dir}' folder for your stego images, tile maps, and CSV table.")

if __name__ == "__main__":
    run_batch_tests_color()