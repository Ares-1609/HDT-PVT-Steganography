import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def plot_histogram_color(cover_path, stego_path, output_path, img_name):
    # Read color images and flatten all 3 channels into a 1D array
    cover = cv2.imread(cover_path).ravel()
    stego = cv2.imread(stego_path).ravel()
    
    plt.figure(figsize=(10, 5))
    # Plotting the overall intensity distribution across all color channels
    plt.hist(cover, bins=256, range=(0, 256), alpha=0.5, color='blue', label='Cover Image (RGB)')
    plt.hist(stego, bins=256, range=(0, 256), alpha=0.5, color='red', label='Stego Image (RGB)')
    
    plt.title(f'Color Histogram Preservation Analysis - {img_name}')
    plt.xlabel('Pixel Intensity (All Channels)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_pdh_color(cover_path, stego_path, output_path, img_name):
    # Load as int32 to allow for negative pixel differences across RGB channels
    cover = cv2.imread(cover_path).astype(np.int32)
    stego = cv2.imread(stego_path).astype(np.int32)
    
    # Calculate differences between adjacent horizontal pixels across all channels
    cover_diff = cover[:, 0::2, :] - cover[:, 1::2, :]
    stego_diff = stego[:, 0::2, :] - stego[:, 1::2, :]
    
    # Flatten the arrays to analyze the global difference distribution
    cover_diff = cover_diff.ravel()
    stego_diff = stego_diff.ravel()
    
    plt.figure(figsize=(10, 5))
    bins = np.arange(-40, 41)
    
    cover_hist, _ = np.histogram(cover_diff, bins=bins)
    stego_hist, _ = np.histogram(stego_diff, bins=bins)
    
    plt.plot(bins[:-1], cover_hist, color='blue', label='Cover Image (RGB)', linewidth=1.5)
    plt.plot(bins[:-1], stego_hist, color='red', linestyle='--', label='Stego Image (RGB)', linewidth=1.5)
    
    plt.title(f'Color Pixel Difference Histogram (PDH) - {img_name}')
    plt.xlabel('Pixel Difference')
    plt.ylabel('Occurrences')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    
    plt.savefig(output_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    output_dir = 'color-results'
    images = ['baboon_color.png', 'jet_color.png', 'peppers_color.png']
    payload_to_test = 10500 # The massive payload you just successfully tested
    
    print(f"Running Security Graph Generation (Payload: {payload_to_test}B)...\n")
    
    for img_name in images:
        cover_image = f'datasets/{img_name}'
        stego_image = f'{output_dir}/stego_{payload_to_test}B_{img_name}'
        
        if not os.path.exists(stego_image):
            print(f"⚠️ Skipping {img_name} - stego file not found in {output_dir}.")
            continue
            
        print(f"--- Generating graphs for {img_name} ---")
        
        # 1. Histogram
        hist_output = f'{output_dir}/hist_comparison_{img_name}'
        plot_histogram_color(cover_image, stego_image, hist_output, img_name)
        
        # 2. PDH
        pdh_output = f'{output_dir}/pdh_{img_name}'
        plot_pdh_color(cover_image, stego_image, pdh_output, img_name)
        
    print(f"\n✅ Security graphs successfully saved to '{output_dir}'.")