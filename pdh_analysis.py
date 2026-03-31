import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def plot_pdh(cover_path, stego_path, output_path, img_name):
    # Load images as standard integers to allow for negative differences
    cover = np.array(Image.open(cover_path).convert("L"), dtype=int)
    stego = np.array(Image.open(stego_path).convert("L"), dtype=int)
    
    # Calculate differences between adjacent horizontal pixels
    cover_diff = cover[:, 0::2] - cover[:, 1::2]
    stego_diff = stego[:, 0::2] - stego[:, 1::2]
    
    # Flatten the arrays
    cover_diff = cover_diff.ravel()
    stego_diff = stego_diff.ravel()
    
    # Plotting the Pixel Difference Histogram
    plt.figure(figsize=(10, 5))
    
    # We focus on the range -40 to 40, which is standard for PDH literature
    bins = np.arange(-40, 41)
    
    # Calculate frequencies
    cover_hist, _ = np.histogram(cover_diff, bins=bins)
    stego_hist, _ = np.histogram(stego_diff, bins=bins)
    
    # Plot as line graphs to easily spot "step effects"
    plt.plot(bins[:-1], cover_hist, color='blue', label='Cover Image', linewidth=1.5)
    plt.plot(bins[:-1], stego_hist, color='red', linestyle='--', label='Stego Image', linewidth=1.5)
    
    plt.title(f'Pixel Difference Histogram (PDH) Analysis - {img_name}')
    plt.xlabel('Pixel Difference')
    plt.ylabel('Occurrences')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    images = ['lena.png', 'baboon.png', 'peppers.png', 'jet.png', 'boat.png']
    payload_to_test = 3500 # Testing at maximum capacity
    
    print("Running Pixel Difference Histogram (PDH) Analysis...\n")
    
    for img_name in images:
        cover_image = f'datasets/{img_name}'
        stego_image = f'results/stego_{payload_to_test}B_{img_name}'
        
        if not os.path.exists(stego_image):
            print(f"Skipping {img_name} - stego file not found.")
            continue
            
        output_file = f'results/pdh_{img_name}'
        plot_pdh(cover_image, stego_image, output_file, img_name)
        print(f"[+] PDH graph generated for {img_name}")
        
    print("\nCheck your 'results' folder for the PDH graphs.")