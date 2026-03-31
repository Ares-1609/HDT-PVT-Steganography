import os
import csv
import shutil
from steganography import embed_data
from utils import psnr, mse, embedding_capacity, draw_tiles

def run_batch_tests():
    # Ensure our output directories exist
    os.makedirs('results', exist_ok=True)
    os.makedirs('static', exist_ok=True) 

    # The 5 test images downloaded in Step 1
    images = ['baboon.png', 'boat.png', 'jet.png', 'lena.png', 'peppers.png'] 
    # Testing 500B, 1KB, 2KB, and 3.5KB payloads
    payload_sizes = [500, 1000, 2000, 3500] # In bytes
    key = "123"

    # Open a CSV file to generate the Performance Analysis table
    with open('results/performance_table.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Image Name', 'Payload (Bytes)', 'Capacity (bpp)', 'MSE', 'PSNR (dB)'])

        for img_name in images:
            img_path = f"datasets/{img_name}"
            
            if not os.path.exists(img_path):
                print(f"Skipping {img_name}, please make sure it is in the datasets folder.")
                continue

            print(f"\n--- Testing {img_name} ---")

            for size in payload_sizes:
                # 1 character = 1 byte. We generate an exact dummy payload.
                message = 'A' * size
                
                # 1. Embed data (saves to static/stego.png)
                stego_path, tiles = embed_data(img_path, message, key)
                
                # 2. Generate tiled visualization (saves to static/tile_map.png)
                tiled_path = draw_tiles(img_path, tiles)
                
                # 3. Rename and move files to the results folder so they aren't overwritten
                final_stego = f"results/stego_{size}B_{img_name}"
                final_tiled = f"results/tiled_{size}B_{img_name}"
                
                shutil.move(stego_path, final_stego)
                shutil.move(tiled_path, final_tiled)
                
                # 4. Calculate performance metrics
                current_mse = mse(img_path, final_stego)
                current_psnr = psnr(img_path, final_stego)
                cap = embedding_capacity(size * 8, img_path)
                
                # 5. Record results in the table
                writer.writerow([img_name, size, cap, current_mse, current_psnr])
                print(f"Payload: {size}B | PSNR: {current_psnr:.2f} dB | MSE: {current_mse:.4f}")

    print("\nBatch testing complete! Check the 'results' folder for your images and CSV table.")

if __name__ == "__main__":
    run_batch_tests()