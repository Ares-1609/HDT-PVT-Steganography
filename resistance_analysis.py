import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from PIL import Image
import os

def plot_histogram(cover_path, stego_path, output_path, img_name):
    cover = np.array(Image.open(cover_path).convert("L")).ravel()
    stego = np.array(Image.open(stego_path).convert("L")).ravel()
    
    plt.figure(figsize=(10, 5))
    plt.hist(cover, bins=256, range=(0, 256), alpha=0.5, color='blue', label='Cover Image')
    plt.hist(stego, bins=256, range=(0, 256), alpha=0.5, color='red', label='Stego Image')
    plt.title(f'Histogram Preservation Analysis - {img_name}')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(output_path, dpi=300)
    plt.close()

def chi_square_test(stego_path):
    stego = np.array(Image.open(stego_path).convert("L")).ravel()
    freq, _ = np.histogram(stego, bins=256, range=(0, 256))
    
    expected = []
    observed = []
    
    for i in range(128):
        pair_sum = freq[2*i] + freq[2*i+1]
        expected.extend([pair_sum / 2.0, pair_sum / 2.0])
        observed.extend([freq[2*i], freq[2*i+1]])
        
    expected = np.array(expected) + 1e-7 
    observed = np.array(observed)
    
    chi2_stat = np.sum((observed - expected)**2 / expected)
    p_val = chisquare(f_obs=observed, f_exp=expected)[1]
    
    return chi2_stat, p_val

def rs_analysis(img_path):
    img = np.array(Image.open(img_path).convert("L")).astype(int)
    H, W = img.shape
    H_crop = H - (H % 2)
    W_crop = W - (W % 2)
    
    blocks = img[:H_crop, :W_crop].reshape(H_crop//2, 2, W_crop//2, 2).swapaxes(1, 2).reshape(-1, 4)
    
    def f(b):
        return np.abs(b[:,0]-b[:,1]) + np.abs(b[:,1]-b[:,3]) + np.abs(b[:,3]-b[:,2]) + np.abs(b[:,2]-b[:,0])
    
    def F1(x):
        return x ^ 1
        
    def Fm1(x):
        res = np.where(x % 2 == 0, x - 1, x + 1)
        return np.clip(res, 0, 255)
        
    b_M = blocks.copy()
    b_M[:,1] = F1(b_M[:,1])
    b_M[:,2] = F1(b_M[:,2])
    
    b_m1 = blocks.copy()
    b_m1[:,1] = Fm1(b_m1[:,1])
    b_m1[:,2] = Fm1(b_m1[:,2])
    
    f_orig = f(blocks)
    f_M = f(b_M)
    f_m1 = f(b_m1)
    
    R_m = np.mean(f_M > f_orig) * 100
    S_m = np.mean(f_M < f_orig) * 100
    R_m1 = np.mean(f_m1 > f_orig) * 100
    S_m1 = np.mean(f_m1 < f_orig) * 100
    
    return R_m, S_m, R_m1, S_m1

if __name__ == "__main__":
    images = ['lena.png', 'baboon.png', 'peppers.png', 'jet.png', 'boat.png']
    payload_to_test = 3500 # Using the largest payload for worst-case scenario testing
    
    print(f"Running Resistance Analysis on all 5 images (Payload: {payload_to_test}B)...\n")
    
    for img_name in images:
        cover_image = f'datasets/{img_name}'
        stego_image = f'results/stego_{payload_to_test}B_{img_name}'
        
        if not os.path.exists(stego_image):
            print(f"Error: Could not find {stego_image}. Skipping...")
            continue
            
        print(f"--- Analysis for {img_name} ---")
        
        # 1. Histogram
        hist_output = f'results/hist_comparison_{img_name}'
        plot_histogram(cover_image, stego_image, hist_output, img_name)
        print(f"   [+] Histogram saved to {hist_output}")
        
        # 2. Chi-Square
        chi2, p = chi_square_test(stego_image)
        print(f"   [+] Chi-Square Statistic: {chi2:.2f} | p-value: {p:.4f}")
        
        # 3. RS Analysis
        Rm, Sm, Rm1, Sm1 = rs_analysis(stego_image)
        print(f"   [+] RS Analysis:")
        print(f"       R_M:  {Rm:.2f}%  |  R_-M: {Rm1:.2f}%")
        print(f"       S_M:  {Sm:.2f}%  |  S_-M: {Sm1:.2f}%\n")